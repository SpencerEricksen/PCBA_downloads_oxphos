
import sys
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors

try:
    incsv = sys.argv[1]
    outcsv = sys.argv[2]
except:
    print('usage: python ./source/rdkit_add_chemical_features.py  inputcsv   outputcsv')
    exit

# functions for fingerprint generation
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

# function for adding PAINS flags
def pains_flags_from_mol( mol ):
    try:
        mol = Chem.MolFromSmiles( smi )
        for k,v in dic.items():
            subs = Chem.MolFromSmarts( k )
            if subs != None:
                if mol.HasSubstructMatch( subs ):
                    mol.SetProp(v,k)
        props = [ prop for prop in mol.GetPropNames() ]
        if len(props) == 0:
            props = False
    except:
        props = False
        pass
    return props

# function to generate rdkit descriptors
def get_desc_list( mol ):
    '''return list of RDKit mol descriptors from rdkit mol object'''
    desc_list = []
    try:
        for tup in Descriptors.descList:
            desc_list.append(tup[1](mol))
    except:
        pass
    return desc_list



# get mol objects from clean smiles 
df = pd.read_csv(incsv, low_memory=False, sep="|")
df['rdkit_mol']  = df['smiles'].apply( lambda x: get_mol_from_smiles(x) if x is not None else None )


# add fingerprints
df['morgan_r3'] = df['rdkit_mol'].apply( lambda m: get_morgan_r3(m) if m is not None else None )
df['morgan_bitstring'] = df['morgan_r3'].apply( lambda fp: make_bitstring( fp ) if fp is not None else None )
df.drop( columns=['morgan_r3'], inplace=True )


# get the pains definitions, load into dict
inf = open("./source/pains.txt", "r")
sub_strct = [ line.rstrip().split(" ") for line in inf ]
smarts = [ line[0] for line in sub_strct]
desc = [ line[1] for line in sub_strct]
dic = dict(zip(smarts, desc))
# add pains flags
df['pains'] = df['rdkit_mol'].apply( lambda m: pains_flags_from_mol(m) if m is not None else None )


# add rdkit mol descriptors
df['descriptors'] = df['rdkit_mol'].apply( lambda m: get_desc_list(m) if m is not None else None )


# remove mol objects
df.drop( columns=['rdkit_mol'], inplace=True )

# dump dataframe with all chemical features (fingerprints, descriptors, pains)
df.to_csv(outcsv, sep="|", index=False)


