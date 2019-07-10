#!/home/ssericksen/anaconda2/bin/python2.7

import pandas as pd
import numpy as np
import sys

# pcba-aid1055297.csv
input_aid = sys.argv[1]

aid_number = str( input_aid.split('-')[-1].split('.')[0][3:] )

df = pd.read_csv( input_aid, low_memory=False )
df = df[ pd.to_numeric( df['PUBCHEM_CID'], errors='coerce' ).notnull() ]
df3 = df[['PUBCHEM_CID', 'PUBCHEM_ACTIVITY_OUTCOME', 'PUBCHEM_ACTIVITY_SCORE' ] ]
df3.loc[ :, 'PUBCHEM_CID' ] = df3['PUBCHEM_CID'].astype(int)
#df3['PUBCHEM_ACTIVITY_SCORE'] = df3['PUBCHEM_ACTIVITY_SCORE'].astype(int)
#df3['PUBCHEM_CID'] = df3['PUBCHEM_CID'].astype(int)
df3.set_index( 'PUBCHEM_CID', inplace=True)
df3.drop_duplicates(keep='first')

df3.to_csv('pcba-aid'+aid_number+'_activities.csv', index_label='PUBCHEM_CID')

'''
# if we want to keep ACTIVITY_OUTCOME and ACTIVITY_SCORE:
df = pd.read_csv('./AIDs/pcba-aid1465.csv', low_memory=False)
df = df[ pd.to_numeric( df['PUBCHEM_CID'], errors='coerce' ).notnull() ]
df3 = df[['PUBCHEM_CID', 'PUBCHEM_ACTIVITY_OUTCOME', 'PUBCHEM_ACTIVITY_SCORE' ] ]
df3['PUBCHEM_ACTIVITY_SCORE'] = df3['PUBCHEM_ACTIVITY_SCORE'].astype(int)
df3.sort_values( by='PUBCHEM_ACTIVITY_SCORE', ascending=False )
'''
