
import sys
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

try:
    incsv = sys.argv[1]
    outcsv = sys.argv[2]
except:
    print('usage: ./rdkit_add_fingerprints  inputcsv   outputcsv')
    exit


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


#df = pd.read_csv('all_oxphos_aids_cids.csv')
df = pd.read_csv(incsv)

df['rdkit_mol']  = df['smiles'].apply( lambda x: get_mol_from_smiles(x) if x is not None else None )

df['morgan_r3'] = df['rdkit_mol'].apply( lambda m: get_morgan_r3(m) if m is not None else None )

df['morgan_bitstring'] = df['morgan_r3'].apply( lambda fp: make_bitstring( fp ) if fp is not None else None )

# now dump to CSV only relevant columns (remove 'rdkit_mol' and 'morgan_r3')
df.drop( columns=['rdkit_mol','morgan_r3'], inplace=True )
#df.to_csv('all_oxphos_aids_cids_fps.csv')
df.to_csv( outcsv, index=False )

#!/home/ssericksen/anaconda2/envs/py36_chem/bin/python3.6

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import sys
from rdkit import Chem

def pains_flags_from_smi( smi ):
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


# load CSV file into dataframe
incsv = sys.argv[1]
outcsv = sys.argv[2]

df = pd.read_csv( incsv, sep="|" )

# get the pains definitions, load into dict
inf = open("pains.txt", "r")
sub_strct = [ line.rstrip().split(" ") for line in inf ]

smarts = [ line[0] for line in sub_strct]
desc = [ line[1] for line in sub_strct]
dic = dict(zip(smarts, desc))

# add pains flags
df['pains'] = df['smiles'].apply( pains_flags_from_smi )

df.to_csv( outcsv, sep="|", index=False )


import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors



def get_desc_list( can ):
    '''return list of RDKit mol descriptors from a canonical smiles'''
    desc_list = []
    try:
        m = Chem.MolFromSmiles(can)
        for tup in Descriptors.descList:
            desc_list.append(tup[1](m))
    except:
        pass
    return desc_list


# load data frame
df = pd.read_csv('ultimate_oxphos_pcassay_dataset_npscores_ETC.csv', sep="|")


# add a column containing a list of numerical mol descriptors from RDKit
df['descriptors'] = np.nan
df['descriptors'] = df['smiles'].apply( lambda x: get_desc_list(x) )

# dump dataframe with descriptors
df.to_csv('ultimate_oxphos_pcassay_dataset_npscores_ETC_desc.csv', sep="|", index=False)


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

# load CSV as dataframe
df = pd.read_csv('ultimate_oxphos_pcassay_dataset_npscores_ETC_desc.csv', sep="|")
df.drop( columns='Unnamed: 0', inplace=True )

with open('rdkit_desc_list2.txt', 'r') as fh:
    data = fh.readlines()
desc_keys = []
for l in data:
    desc_keys.append( l.strip() )

# convert descriptor string to list
#df['descriptors'] = df['descriptors'].apply( lambda x: convert_str_to_list(x) )
df['descriptors'] = df['descriptors'].apply( convert_str_to_list )

# apply filter
df2 = df.loc[ ( df['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active') &
              ( df['ETC_linked_AID'] == True) &
              ( df['descriptors'].str[5] > 200.0 ) &
              ( df['descriptors'].str[113] < 5.8 ) &
              ( df['descriptors'].str[73] < 150 ) &
              ( df['descriptors'].str[96] > 20 ) &
              ( df['descriptors'].str[98] > 0 ) &
              ( df['descriptors'].str[112] > 0 )
            ]

# dump to new CSV
df2.to_csv( 'ultimate_oxphos_pcassay_dataset_npscores_ETC_descfilt_actives.csv', sep="|", index=False )


# filter dataframe based on individual descriptors

# desc_keys[5] = 'MolWt'
# desc_keys[113] = 'MolLogP'
# desc_keys[73] = 'TPSA'
# desc_keys[96] = 'HeavyAtomCount'
# desc_keys[98] = 'NOCount' # number of Ns or Os
# desc_keys[112] = 'RingCount' # number of rings

'''
actives and ETC_linked_AID                              1998
active, ETC_linked_AID, MolWT > 180, MolLogP < 5.6      1433
active, ETC_linked_AID, MolWT > 200, MolLogP < 5.0      1187

len( df.loc[ ( df['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active') &
             ( df['ETC_linked_AID'] == True) &
             ( df['descriptors'].str[5] > 200.0 ) &
             ( df['descriptors'].str[113] < 5.0 )
           ]['PUBCHEM_CID'].unique())

# if you want descriptor dictionary:

# get the numerical values:
desc_values = df['descriptors'].iloc[10]

# zip values to keys to build dictionary
desc_dict = dict( zip( desc_keys, desc_values ) )
'''
#
# calculation of natural product-likeness as described in:
#
# Natural Product-likeness Score and Its Application for Prioritization of Compound Libraries
# Peter Ertl, Silvio Roggo, and Ansgar Schuffenhauer
# Journal of Chemical Information and Modeling, 48, 68-74 (2008)
# http://pubs.acs.org/doi/abs/10.1021/ci700286x
#
# for the training of this model only openly available data have been used
# ~50,000 natural products collected from various open databases
# ~1 million drug-like molecules from ZINC as a "non-NP background"
#
# peter ertl, august 2015
#


from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
import numpy as np
import sys, math, gzip, pickle
import os.path
from collections import namedtuple


def readNPModel(filename=os.path.join(os.path.dirname(__file__), 'publicnp.model.gz')):
  """Reads and returns the scoring model,
  which has to be passed to the scoring functions."""
  print("reading NP model ...", file=sys.stderr)
  fscore = pickle.load(gzip.open(filename))
  print("model in", file=sys.stderr)
  return fscore


def scoreMolWConfidence(mol, fscore):
  """Next to the NP Likeness Score, this function outputs a confidence value
  between 0..1 that descibes how many fragments of the tested molecule
  were found in the model data set (1: all fragments were found).
  Returns namedtuple NPLikeness(nplikeness, confidence)"""

  if mol is None:
    raise ValueError('invalid molecule')
  fp = rdMolDescriptors.GetMorganFingerprint(mol, 2)
  bits = fp.GetNonzeroElements()

  # calculating the score
  score = 0.0
  bits_found = 0
  for bit in bits:
    if bit in fscore:
      bits_found += 1
      score += fscore[bit]

  try:
      score /= float(mol.GetNumAtoms())
      confidence = float(bits_found / len(bits))
  except:
      #score = 0.000
      #confidence = 0.000
      score = np.nan
      confidence = np.nan

  # preventing score explosion for exotic molecules
  if score > 4:
    score = 4. + math.log10(score - 4. + 1.)
  elif score < -4:
    score = -4. - math.log10(-4. - score + 1.)
  NPLikeness = namedtuple("NPLikeness", "nplikeness,confidence")
  return NPLikeness(score, confidence)


def scoreMol(mol, fscore):
  """Calculates the Natural Product Likeness of a molecule.
  Returns the score as float in the range -5..5."""
  return scoreMolWConfidence(mol, fscore).nplikeness


def processMols(fscore, suppl):
  print("calculating ...", file=sys.stderr)
  print('smiles,PUBCHEM_CID,npscore')
  count = {}
  n = 0
  for i, m in enumerate(suppl):
    if m is None:
      continue

    n += 1
    score = "%.3f" % scoreMol(m, fscore)

    smiles = Chem.MolToSmiles(m, True)
    name = m.GetProp('_Name')
    #print(smiles + "\t" + name + "\t" + score)
    print(smiles+','+name+','+score)
  print("finished, " + str(n) + " molecules processed", file=sys.stderr)


if __name__ == '__main__':

  fscore = readNPModel()  # fills fscore

  suppl = Chem.SmilesMolSupplier(sys.argv[1], smilesColumn=0, nameColumn=1, titleLine=False)
  processMols(fscore, suppl)

#
# Copyright (c) 2015, Novartis Institutes for BioMedical Research Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#     * Neither the name of Novartis Institutes for BioMedical Research Inc.
#       nor the names of its contributors may be used to endorse or promote
#       products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
