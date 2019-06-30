
# use advanced query to find PubChem BioAssays (AIDs) with potentially relevant data
https://www.ncbi.nlm.nih.gov/pcassay/advanced

# the following query returns 4645 assays--performed on May 22, 2019 at 13:51
("electron transport chain"[Assay Description] OR "mitochondrial complex"[Assay Description] OR "mitochondrial respiratory chain"[Assay Description] OR "mitochondrial membrane potential"[Assay Description])


# 2019-06-28
#
# total substance records: 361124
#
# number of unique:
# 	CIDs:		308531
#	AIDs:		4641
#	murcko:		108785 
#	gen murcko:	47200


#############################
Scripts and Procedure for downloading cpd data for various assay IDs (AIDs) from PubChem
#############################

# download AID data tables for each AID (output files go to 'AIDs' folder
nohup ./get_bioassay_data_v1.3.py assay_list.list > get_bioassay_oxphos_all_assays.log 2>&1 &

# prepare CID CSVs (including columns PUBCHEM_ACTIVITY_OUTCOMES and PUBCHEM_ACTIVITY_SCORE)
#for aid in AIDs/pcba-aid*.csv; do ./dump_assay_cid_activity_csv.py ${aid}; done

# prepare simple CID lists for each assay in AIDs folder, move thiese to CID_lists folder
for a in AIDs/pcba-aid*.csv; do ./dump_cid_list_v1.1.py  ${a}; done

# prepare .xml query files for PUG REST. These are built from CID lists for each AID.
# These will be used to fetch smiles for all CIDs tested in each assay.
for c in CID_lists/pcba-aid*_activities.csv; do ./0A_write_cgi_v1.3.py $c; echo $c; done

# Use .xml query files to fetch via PUG REST the smiles for all tested cpds from each AID
for f in pc_fetch_aid1[1234]*; do ./wrapper_fetch_v1.2.sh $f; done

# merge downloaded smiles and downloaded assay outcomes into individal files for each AID
# add substructure 'match' result and smiles for Bemis-Murcko scaffolds and generic Murcko scaffolds (all carbon)
for a in `cat assay_list.list`; do echo ${a}; ./rdkit_substructure_matcher_v1.6.py ${a}; done

# merge all of these merged assay outcomes/smiles tables:
cat aid_*.csv > all_oxphos_aids_cids.csv
sed -i '2,${/PUBCHEM_CID/d;}' all_oxphos_aids_cids.csv

# process all_oxphos_aids_cids.csv to add fingerprints (RDKit Morgan fingerprints of radius=3 and 2048 bits)
./rdkit_add_fingerprints.py





##########################################
# extras

# get list of ASSAY AIDs to download
grep pcba-aid* get_bioassay_oxphos_all_assays.log > x
grep pcba-aid* get_bioassay_oxphos_all_assays_contd.log > y
cat x y > z
cat z | cut -f2 -d"-" | cut -f1 -d"." | cut -c4- > zz

# had to finish merging dataframes when terminal connection was disrupted, need list of unfinshed assays
with open('z', 'r') as fh:
    data = fh.readlines()
newdata = [ i.strip() for i in data ]
with open('zz', 'w') as dump:
    for i in newdata:
        print >> dump, i

# remove any garbage lines from previous get_bioassay_data versions
for f in pcba-aid*.csv; do sed -i -e '/^Code:/d' -e '/^Message:/d' -e '/^Status:/d' $f; echo $f; done





