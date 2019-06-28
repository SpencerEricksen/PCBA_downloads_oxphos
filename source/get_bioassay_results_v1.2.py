#!/home/ssericksen/anaconda2/bin/python2.7

##!/usr/bin/python

# script to download PCBA assay results (CSV) file
# I think there is a 500,000 molecule limit?

import sys
import requests


try:
    aid = sys.argv[1]
except:
    print " "
    print "usage:  ./get_bioassay_results_v1.2.py  588342"
    print " "
    exit

''''
import requests
aid = '833'
url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/'+aid+'sids/XML?list_return=listkey'
r = requests.get( url )
listkey = r.content.split()[8]


import subprocess
output = subprocess.check_output("curl https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/883/sids/XML?list_return=listkey", shell=True)
'''
def get_reqid(aid):
    '''first get a reqid for the request'''
    # <ListKey>3978115397428862005</ListKey>
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/'+aid+'/sids/XML?list_return=listkey'
    print url
    r = requests.get(url)
    listkey = r.content.split()[8].split('>')[1].split('<')[0]
    return listkey

def get_aids_data(aid, listkey, aid_data_file, mol_total):
    '''using listkey, go ahead an download your records in 10000 sid chunks'''
    for i in range(0, int(mol_total), 10000):
        url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/'+aid+'/CSV?sid=listkey&listkey='+listkey+'&listkey_start='+str(i)+'&listkey_count=10000'
        r = requests.get(url)
        aid_data_file.write(r.content)
        #aid_data_file.close()

'''
aid_data_input_file = sys.argv[1]

with open(aid_data_input_file, 'r') as fh:
    data = fh.readlines()
for line in data[1:]:
'''

aid = sys.argv[1]
mol_total = 500000 
#mol_total = line.split()[-1].strip()
#    aid = line.split()[0]
print aid
listkey = get_reqid( aid )
print listkey
#mol_total = line.split()[-1].strip()
print mol_total
csv_data_file = 'pcba-aid'+str(aid)+'.csv'
print csv_data_file
datafile = open( csv_data_file, 'w' )
get_aids_data(aid, listkey, datafile, mol_total)

