#!/home/ssericksen/anaconda2/bin/python2.7

import pandas as pd
import numpy as np
import sys

# pcba-aid1055297.csv
input_aid = sys.argv[1]

aid_number = str( input_aid.split('-')[-1].split('.')[0][3:] )

df = pd.read_csv( input_aid )
cid_list = df['PUBCHEM_CID'].dropna().astype(int).to_list()
#print("AID:{},NUMCPDS:{},CIDS:{}".format( aid_number, len(cid_list), "_".join( [ str(i) for i in cid_list ] ) ) )

with open( "pcba-aid"+aid_number+".cid", 'w' ) as fh:
    for cid in cid_list:
        print >> fh, cid


