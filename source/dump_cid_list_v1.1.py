#!/home/ssericksen/anaconda2/bin/python2.7

import pandas as pd
import numpy as np
import sys

# pcba-aid1055297.csv
input_aid = sys.argv[1]

aid_number = str( input_aid.split('-')[-1].split('.')[0][3:] )

df = pd.read_csv( input_aid )
df = df[ pd.to_numeric( df['PUBCHEM_CID'], errors='coerce' ).notnull() ]
cid_list = df['PUBCHEM_CID'].dropna().astype(int).to_list()

#print("AID:{},NUMCPDS:{},CIDS:{}".format( aid_number, len(cid_list), "_".join( [ str(i) for i in cid_list ] ) ) )

with open( "pcba-aid"+aid_number+".cid", 'w' ) as fh:
    for cid in cid_list:
        print >> fh, cid

'''
# if we want to keep ACTIVITY_OUTCOME and ACTIVITY_SCORE:
df = pd.read_csv('./AIDs/pcba-aid1465.csv', low_memory=False)
df = df[ pd.to_numeric( df['PUBCHEM_CID'], errors='coerce' ).notnull() ]
df3 = df[['PUBCHEM_CID', 'PUBCHEM_ACTIVITY_OUTCOME', 'PUBCHEM_ACTIVITY_SCORE' ] ]
df3['PUBCHEM_ACTIVITY_SCORE'] = df3['PUBCHEM_ACTIVITY_SCORE'].astype(int)
df3.sort_values( by='PUBCHEM_ACTIVITY_SCORE', ascending=False )
'''
