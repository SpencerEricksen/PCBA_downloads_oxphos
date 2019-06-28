#!/home/ssericksen/anaconda2/bin/python2.7

import pandas as pd
import numpy as np
import sys

# pcba-aid1055297.csv
input_aid = sys.argv[1]

aid_number = str( input_aid.split('-')[-1].split('.')[0][3:] )

df = pd.read_csv( input_aid, low_memory=False )
df = df[ pd.to_numeric( df['PUBCHEM_SID'], errors='coerce' ).notnull() ]
df3 = df[['PUBCHEM_SID', 'PUBCHEM_ACTIVITY_OUTCOME', 'PUBCHEM_ACTIVITY_SCORE' ] ]
df3.loc[ :, 'PUBCHEM_SID' ] = df3['PUBCHEM_SID'].astype(int)
#df3['PUBCHEM_ACTIVITY_SCORE'] = df3['PUBCHEM_ACTIVITY_SCORE'].astype(int)
#df3['PUBCHEM_SID'] = df3['PUBCHEM_SID'].astype(int)
df3.set_index( 'PUBCHEM_SID', inplace=True)
df3.drop_duplicates(keep='first')

df3.to_csv('pcba-aid'+aid_number+'_activities_sid.csv', index_label='PUBCHEM_SID')

'''
# if we want to keep ACTIVITY_OUTCOME and ACTIVITY_SCORE:
df = pd.read_csv('./AIDs/pcba-aid1465.csv', low_memory=False)
df = df[ pd.to_numeric( df['PUBCHEM_SID'], errors='coerce' ).notnull() ]
df3 = df[['PUBCHEM_SID', 'PUBCHEM_ACTIVITY_OUTCOME', 'PUBCHEM_ACTIVITY_SCORE' ] ]
df3['PUBCHEM_ACTIVITY_SCORE'] = df3['PUBCHEM_ACTIVITY_SCORE'].astype(int)
df3.sort_values( by='PUBCHEM_ACTIVITY_SCORE', ascending=False )
'''
