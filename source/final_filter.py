import pandas as pd
import numpy as np
from ast import literal_eval

def convert_str_to_list( input_str ):
    '''pandas stores descriptor list as a literal string, use
       literal_eval to get list object back for parsing, etc.'''
    try:
        l = literal_eval( input_str )
    except:
        l = np.nan
        pass
    return l

df1 = pd.read_csv('all_oxphos_aids_cids_assaydesc_ETC_pmids_feats.csv', sep="|", low_memory=False )

df1['descriptors'] = df1['descriptors'].apply( convert_str_to_list )
df2 = df1.loc[ ( df1['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active') &
              ( df1['ETC_linked_AID'] == True) &
              ( df1['descriptors'].str[5] > 200.0 ) &
              ( df1['descriptors'].str[113] < 5.8 ) &
              ( df1['descriptors'].str[73] < 150 ) &
              ( df1['descriptors'].str[96] > 20 ) &
              ( df1['descriptors'].str[98] > 0 ) &
              ( df1['descriptors'].str[112] > 0 )
            ]

# filter dataframe based on individual descriptors

#with open('rdkit_desc_list2.txt', 'r') as fh:
#    data = fh.readlines()
#desc_keys = []
#for l in data:
#    desc_keys.append( l.strip() )

# desc_keys[5] = 'MolWt'
# desc_keys[113] = 'MolLogP'
# desc_keys[73] = 'TPSA'
# desc_keys[96] = 'HeavyAtomCount'
# desc_keys[98] = 'NOCount' # number of Ns or Os
# desc_keys[112] = 'RingCount' # number of rings

# prioritize redundant cpd list first by assays with ETC-linked PMID=True and then PUBCHEM_ACTIVITY_SCORE
df3 = df2.sort_values( by=['ETC_linked_PMID','PUBCHEM_ACTIVITY_SCORE'], ascending=False ).drop_duplicates( subset='PUBCHEM_CID', keep='first')

# write CSV for set of active CIDs
df3.to_csv('active_oxphos_aids_cids_assaydesc_ETC_pmids_feats.csv', sep="|", index=False)

