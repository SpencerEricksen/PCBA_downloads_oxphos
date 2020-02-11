
import pandas as pd
import numpy as np

# load the original dataframe of all cpd records in OXPHOS-related assays
df1 = pd.read_csv('all_oxphos_aids_cids_assaydesc_ETC.csv', sep="|", low_memory=False )

# get list of PMIDs that Liping confirmed to be associated with complexes I-IV
df2 = pd.read_excel( './source/ETC_inhibitor.xlsx')

pmid_list = []
temp = df2['PMID'].dropna()
temp_arr = temp.unique()
for i in temp_arr:
    if type(i) == int:
        pmid_list.append( i )
    else:
        try:
            j_list = [int(x) for x in i.split(',')]
            for j in j_list:
                pmid_list.append( j )
        except:
            print('problem with {}'.format(i) )

# uniquify pmid_list
new_pmid_list = list(set(pmid_list))

# list PMIDs as strings (pmid column in original dataframe contains strings)
new_pmid_list = [ str(i) for i in new_pmid_list ]

# make column to indicate whether record is associated with an ETC-linked PMID
df1['ETC_linked_PMID'] = False
df1['ETC_linked_PMID'].loc[ df1['pmid'].isin( new_pmid_list ) ] = True

# dump with new column indicating ETC_linked_PMID
df1.to_csv('all_oxphos_aids_cids_assaydesc_ETC_pmids.csv', sep="|", index=False )


# extras...

# cpd records in original dataframe
# len(df1) = 361124 (cpd records)

# number of cpd records with ETC_linked_PMIDs
#df1['ETC_linked_PMID'].sum()
# 2263 

# number of cpd records with that are active and with ETC_linked_PMIDs
#df1.loc[ (df1['ETC_linked_PMID'] == True) & (df1['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active' ) ]['PUBCHEM_CID']
# 894  

# list of unique compounds (CIDs) that are active and with ETC_linked_PMIDs, and their number of occurrences
#df1.loc[ (df1['ETC_linked_PMID'] == True) & (df1['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active' ) ]['PUBCHEM_CID'].value_counts()
# 316 (number of unique cpds--PUBCHEM_CIDs)



