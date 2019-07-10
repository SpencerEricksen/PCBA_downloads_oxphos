#!/home/ssericksen/anaconda2/bin/python

import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem


def get_mol_from_smiles(m):
    try:
        return Chem.MolFromSmiles(m)
    except:
        return None

def get_morgan_r3(m):
    try:
        return AllChem.GetMorganFingerprintAsBitVect( m, 3, nBits=2048 )
    except:
        return None

def make_bitstring(fp):
    try:
        return "".join( [ str(i) for i in fp ] )
    except:
        return None

df = pd.read_csv('all_oxphos_aids_cids.csv')

df['rdkit_mol']  = df['smiles'].apply( lambda x: get_mol_from_smiles(x) if x is not None else None )

df['morgan_r3'] = df['rdkit_mol'].apply( lambda m: get_morgan_r3(m) if m is not None else None )

df['morgan_bitstring'] = df['morgan_r3'].apply( lambda fp: make_bitstring( fp ) if fp is not None else None )

# now dump to CSV only relevant columns (remove 'rdkit_mol' and 'morgan_r3')
df.drop( columns=['rdkit_mol','morgan_r3'], inplace=True )
df.to_csv('all_oxphos_aids_cids_fps.csv')
