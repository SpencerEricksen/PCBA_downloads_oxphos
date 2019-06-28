#!/home/ssericksen/anaconda2/bin/python2.7

import pandas as pd
import numpy as np
import sys
from rdkit import Chem
from rdkit.Chem import PandasTools

aid = str( sys.argv[1] )

# substructure to search
#frag = Chem.MolFromSmarts('C(=O)C=CC')
#frag = Chem.MolFromSmarts('C(=O)')
#frag = Chem.MolFromSmarts('C(=O)C')
#frag = Chem.MolFromSmarts('C(=O)C=[C,N]')
frag = Chem.MolFromSmarts('C(=O)C=C')

# get smiles
df_smi = pd.read_csv( './fetch_CGIs/pcba-aid'+aid+'_0.smi', index_col=0, header=None, sep='\t', names=['smiles'] )
df_smi.index.name = 'PUBCHEM_CID'
df_smi = df_smi.reset_index().drop_duplicates(subset='PUBCHEM_CID', keep='first').set_index('PUBCHEM_CID')
# probably easier:
#df_smi = df_smi.groupby(level=0).first()
df_smi.index = df_smi.index.map(str)

# get activities
df_act = pd.read_csv('./CID_lists/pcba-aid'+aid+'_activities.csv')
df_act.set_index('PUBCHEM_CID', inplace=True)
df_act = df_act.reset_index().drop_duplicates(subset='PUBCHEM_CID', keep='first').set_index('PUBCHEM_CID')
#df_act = df_act.groupby(level=0).first()
df_act.index = df_act.index.map(str)

# merge smiles and activities into a single dataframe
df = pd.concat( [df_act, df_smi], axis=1 )

# set AID column
df['AID'] = aid

# make column to store mol objects
PandasTools.AddMoleculeColumnToFrame( df, 'smiles', 'rdkit_mol', includeFingerprints=False )
#df['rdkit_mol'] = df['smiles'].apply( lambda x: Chem.MolFromSmiles(x) if x is not None else None )

# need to remove salts/frags...
from rdkit.Chem import SaltRemover
_saltRemover = SaltRemover.SaltRemover()
df['rdkit_mol'] = df['rdkit_mol'].apply( lambda x: _saltRemover.StripMol(x) if x is not None else None)
# this bombs on missing mols: 
#PandasTools.RemoveSaltsFromFrame( df, molCol='rdkit_mol')

df['smiles'] = np.nan
df['match'] = np.nan
df['murcko'] = np.nan
df['gen_murcko'] = np.nan

# replace smiles with clean smiles
df['smiles'] = df[[ df['rdkit_mol'].notnull() ].apply(  lambda x: Chem.MolToSmiles(x) )
#df['smiles'] = df['rdkit_mol'].apply( lambda x: Chem.MolToSmiles(x) if x is not None else None )

# boolean for detection of substructure
#df['match'] = df[ df['rdkit_mol'] >= frag ]
df['match'] = df['rdkit_mol'].apply( lambda x: x.HasSubstructMatch(frag) if x is not None else None )

# add Murcko scaffold column
#df['murcko'] = df['rdkit_mol'].apply( lambda x: Chem.Scaffolds.MurckoScaffold.MurckoScaffoldSmiles(x) if x is not None else None )
df['murcko'] = df['smiles'].apply( lambda smi: Chem.Scaffolds.MurckoScaffold.MurckoScaffoldSmilesFromSmiles(smi) if smi is not None else None )
df['rdkit_mol_gen_murcko'] = df['rdkit_mol'].apply( lambda x: Chem.Scaffolds.MurckoScaffold.MakeScaffoldGeneric(x) if x is not None else None )
df['gen_murcko'] = df['rdkit_mol_gen_murcko'].apply( lambda x: Chem.MolToSmiles(x) if x is not None else None )
#df['gen_murcko'] = df['rdkit_mol'].apply( lambda x: Chem.MolToSmiles( Chem.Scaffolds.MuckoScaffold.MakeScaffoldGeneric(x) if x is not None else None )

# dump to CSV
# drop the mol objects columns if dumping to CSV
df.drop( columns=['rdkit_mol','rdkit_mol_gen_murcko'], inplace=True )
#df = df.replace(to_replace='None', value=np.nan).dropna( subset=['rdkit_mol'] )
#df.dropna( subset=['rdkit_mol'], inplace=True )
df.to_csv( 'aid_'+aid+'.csv', index_label='PUBCHEM_CID' )

# dump to spreadsheet (with images):
#df = df.reset_index()
#PandasTools.SaveXlsxFromFrame( df, 'aid_'+aid+'.xlsx', molCol='rdkit_mol', size=(200,200) )

