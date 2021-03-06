
import sys
import requests

def get_reqid(aid):
    '''first get a reqid for the request'''
    # <ListKey>3978115397428862005</ListKey>
    url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/'+aid+'/sids/XML?list_return=listkey'
    print(url)
    r = requests.get(url)
    listkey = r.content.split()[8].split('>')[1].split('<')[0]
    try:
        mol_total = int( r.content.split()[9].split('>')[1].split('<')[0] )
    except:
        print('failed to obtain mol_total, using mol_total=10')
        mol_total = 10000
    return listkey, mol_total

def get_aids_data(aid, listkey, aid_data_file, mol_total):
    '''using listkey, go ahead an download your records in 10000 sid chunks'''
    for i in range(0, int(mol_total), 10000):
        url = 'https://pubchem.ncbi.nlm.nih.gov/rest/pug/assay/aid/'+aid+'/CSV?sid=listkey&listkey='+listkey+'&listkey_start='+str(i)+'&listkey_count=10000'
        r = requests.get(url)
        aid_data_file.write(r.content)
    aid_data_file.close()


aid_data_input_file = sys.argv[1]

with open(aid_data_input_file, 'r') as fh:
    data = fh.readlines()
for line in data:
    print('*'*30)
    aid = line.split()[0]
    print(aid)
    listkey, mol_total = get_reqid( aid )
    print(listkey)
    #mol_total = line.split()[-1].strip()
    print(mol_total)
    csv_data_file = './pcba-aid'+str(aid)+'.csv'
    print(csv_data_file)
    datafile = open( csv_data_file, 'w' )
    get_aids_data(aid, listkey, datafile, mol_total)

