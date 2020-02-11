
# Pipeline for compiling PubChem BioAssay data for all compounds with deposited testing outcomes against a given target system.

Here, we applied this pipeline to acquire compound testing data from PubChem from assays related to the OXPHOS pathway. This includes a wide variety of assays involving different biochemical targets, whole cells, etc.  

The pipeline begings with a search based on key word terms in the 'Assay Description' to identify assays potentially related to our target with potentially relevant data. Here is the site for structuring and submitting your query:
https://www.ncbi.nlm.nih.gov/pcassay/advanced


The following query was performed on May 22, 2019 at 13:51

>("electron transport chain"[Assay Description] OR "mitochondrial complex"[Assay Description] OR "mitochondrial respiratory chain"[Assay Description] OR "mitochondrial membrane potential"[Assay Description])

A list of 4645 AIDs is returned that can be downloaed ('pcassay_result.txt'). Four assays were ultimately removed from this set as they did not involve or report compounds (CIDs). This reduces the assay set to 4641 AIDs.
    
###############

    2019-06-28
    total substance records: 361124
    unique CIDs:		308531
    unique AIDs:		4641
    unique murcko:	108785 
    unique gen murcko:	47200

###############

# Preparing python environment
The following procedure was executed on Ubuntu 18.04.4 LTS using shell commands/scripts and python scripts. The python scripts were developed and tested in a conda environment running python 3.6.7 (conda version 4.7.11).

# Procedure for downloading cpd data for a set of assays (AIDs) in PubChem

get access to scripts in ./source
```
export PATH="${PWD}/source:"$PATH
```

download pcassay_result.txt from query and use to make a simple assay list:

```
grep AID: pcassay_result.txt | awk '{print $2}' > assay_list.list
```

download AID data tables for each AID (output files go to 'AIDs' folder

```
mkdir AIDs
python ./source/get_bioassay_data_v1.4.py assay_list.list > get_bioassay_data.log 2>&1 &
```

prepare CID CSVs (including columns PUBCHEM_ACTIVITY_OUTCOMES and PUBCHEM_ACTIVITY_SCORE), move these to CID_lists folder

```
for aid in AIDs/pcba-aid*.csv; do python ./source/dump_assay_cid_activity_csv_v1.1.py ${aid}; done
```

prepare .xml query files for PUG REST. These are built from CID lists for each AID. These will be used to fetch smiles for all CIDs tested in each assay.

```
for c in CID_lists/pcba-aid*_activities.csv; do python ./source/0A_write_cgi_v1.4.py $c; echo $c; done
``` 

Use .xml query files to fetch via [Power User Gateway (PUG) SOAP](https://pubchemdocs.ncbi.nlm.nih.gov/power-user-gateway$_3-1) the smiles for all tested cpds from each AID. I run the following wrapper in the ./fetch_CGIs directory. The individual requests have time delays to respect PubChem bandwidth so it may take some time for large number of assays. Note a few assays failed because they did not contain any CIDs (RNA samples in some cases). However, for about ~300of the assays, the CID SMILES fetch failed for other reasons. These I obtained by running a second wrapper_fetch loop on just the subset of ~300 missing assay SMILES downloads.

```
for f in pc_fetch_aid1[1234]*; do ./wrapper_fetch_v1.2.sh $f; done
```

Merge downloaded smiles and downloaded assay outcomes (activities) into individal files for each AID, canonicalize, de-salt smiles, also extact SMILES strings for the Bemis-Murcko scaffolds and generic Murcko scaffolds (all carbon). Must create 'merged' directory to store the individual merged assay/cpd dataframes (CSVs).

```
mkdir merged
for a in `cat assay_list.list`; do echo $a; python ./source/rdkit_merge_assaydata_cids_cln_smiles.py $a; done
```

Concatenate all of these merged assay outcomes/smiles tables, remove all but top header line.

```
cat aid_*.csv > all_oxphos_aids_cids.csv
sed -i '2,${/PUBCHEM_CID/d;}' all_oxphos_aids_cids.csv
```


# Obtain assay descriptions/metadata 

Download assay description data from PubChem. Extract relevant fields from assay data files (.xml). Merge the relevant assay description fields into dataframe, with rows for each AID.
```
mkdir assay_descriptions
./source/curl_xml_download_wrapper.sh assay_list.list
```
Had to determine what is the full set of assay attributes in these xml files. 
```
for f in `cat assay_list.list`; do python ./source/parse_pcba_AIDs_desc_xml_v1.4.py $f; done |  awk -F":" '{print $1}' | sort | uniq > unique_attributes.list
```
Looking over the list of unique attributes and the individual xml files, I found a small subset of desired attributes and edited parse script to just dump those.
```
for f in `cat assay_list.list`; do python ./source/parse_pcba_AIDs_desc_xml_v1.4.py $f; done > all_assays_desc.csv
```
Then I removed all but the top header line.
```
sed -i '2,${/^AID/d;}' all_assays_desc.csv
```
NOTE: i used '|' as delimiter to avoid issues with commas appearing in abstracts (false delimiters). I think this was the
issue. By using alternative delimiter we should be able to read correctly into spreadsheet


Merge assay description data with compound records. Assay info includes target info (cells, protein target, CHEMBL targetID), assay info, DOIs/PMIDs for associated papers, abstracts, etc.
```
python ./source/merge_assaydesc_v1.1.py
```

Flag cpd records based on matches with assay description terms. Will remove these.
```
python ./source/add_column_ETC-linked_matched_name_terms.py
```

Flag cpd records based on matches to expert-confirmed relevant PMIDs (PubMed IDs to papers linked to AIDs)
```
python ./source/add_column_ETC-linked_PMID.py
```

# Add molecule features

Features include:
- chemical fingerprint bitstrings (RDKit Morgan fingerprints of radius=3 length=2048), 
- rdkit descriptors, 
- PAINS 

The functions I have for these feature generators require building mol object from smiles. To reduce number of cpds to process, could deduplicate to get set of smiles/cids first. This set can then be re-integrated into original input CSV with key on cids.
```
python ./source/rdkit_add_chemical_features.py   active_oxphos_aids_cids_assaydesc_ETC_pmids.csv   active_oxphos_aids_cids_assaydesc_ETC_pmids_feats.csv
```

Add natural product likeness score as an additional feature
```
python ./source/npscorer_v1.2.py active_oxphos_aids_cids_assaydesc_ETC_pmids_feats.csv active_oxphos_aids_cids_assaydesc_ETC_pmids_feats_nps.csv
```

Isolate only the actives ('PUBCHEM_ACTIVITY_OUTCOME'==TRUE) and de-duplicate CIDs by priority on "ETC_linked_PMID"==TRUE and "PUBCHEM_ACTIVITY_SCORE". Then filter based on MolWt (\>200), MolLopP (\<5.8), TPSA (\<150), HeavyAtomCount (\>20), NOCount (>0), and RingCount (>0)

```
python ./source/final_filter.py 
```


Cluster full molecule set based on fingerprints, store clusterIDs
```
```









#########
NOTES:
> was missing smiles for AID 1465 (by far the largest data set with >200k cpds). I ran the pc_fetch wrapper from command line in steps and waited for request to finish. used a sleep of 40 seconds before starting download and perhaps that isn't long enough. Probably better to grep some flag out of the poll query to test condition for wget to rpoceed with download. I poll this query and waited until it was finished before downloading.

> Also missing smiles for AIDs:

-    504801 --> RNAi (494 SIDs)
-    651810 --> siRNA (18,119 SIDs)
-    651811 --> siRNA (64,752 SIDs)

> but these are not small molecules (no CIDs) so we'll skip these


##########################################
# extras

get list of ASSAY AIDs to download

```
grep pcba-aid* get_bioassay_oxphos_all_assays.log > x
grep pcba-aid* get_bioassay_oxphos_all_assays_contd.log > y
cat x y > z
cat z | cut -f2 -d"-" | cut -f1 -d"." | cut -c4- > zz
```

had to finish merging dataframes when terminal connection was disrupted, need list of unfinshed assays

```
with open('z', 'r') as fh:
    data = fh.readlines()
newdata = [ i.strip() for i in data ]
with open('zz', 'w') as dump:
    for i in newdata:
        print >> dump, i
```

remove any garbage lines from previous get_bioassay_data versions

```
for f in pcba-aid*.csv; do sed -i -e '/^Code:/d' -e '/^Message:/d' -e '/^Status:/d' $f; echo $f; done
```





