
import sys
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import PandasTools

try:
    inputdata = sys.argv[1]
except:
    print('')
    print("provide dataframe with 'cluster_id' column to plot molecule clusters")
    print('')
    exit()

df1 = pd.read_csv( inputdata, sep="|" )
df2 = df1[['PUBCHEM_CID', 'cluster_id', 'smiles', 'medoid' ] ]
df3 = df2.drop_duplicates( subset=['PUBCHEM_CID'], keep='first' )

PandasTools.AddMoleculeColumnToFrame( df3, 'smiles', 'rdkit_mol', includeFingerprints=False )

for cid in df3['cluster_id'].unique():
    # for each cluster,
    # get molecule structures--medoid and non-medoids, put medoid first in order
    ms_medoid = df3.loc[ (df3['cluster_id'] == cid) & (df3['medoid'] == 1), 'rdkit_mol' ].to_list()
    ms        = df3.loc[ (df3['cluster_id'] == cid) & (df3['medoid'] == 0), 'rdkit_mol' ].to_list()
    ms = ms_medoid + ms
    # get molecule identifiers
    m_names_medoid = df3.loc[ (df3['cluster_id'] == cid) & (df3['medoid'] == 1), 'PUBCHEM_CID' ].to_list()
    m_names        = df3.loc[ (df3['cluster_id'] == cid) & (df3['medoid'] == 0), 'PUBCHEM_CID' ].to_list()
    m_names = m_names_medoid + m_names
    cluster_pop = len(ms)
    print( "cid:{} cluster_pop:{} len(ms):{} len(m_names):{}".format( cid, cluster_pop, len(ms), len(m_names) ) )
    if cluster_pop > 25:
        # obtain random draw of 24 members from cluster, add medoid first in order (25 cpds drawn)
        rnd_idx = np.random.choice( cluster_pop - 1, 24, replace=False) + 1
        rnd_idx = [0] + list(rnd_idx)
        try:
            ms = [ ms[i] for i in rnd_idx ]
            m_names = [ m_names[i] for i in rnd_idx ]
        except:
            print( "indices:{}".format( ",".join( [str(i) for i in rnd_idx] ) ) )
            pass
    try:
        img = Draw.MolsToGridImage( ms, molsPerRow=5, subImgSize=(400,400), legends=[ str(x) for x in m_names ]  )
        #img.save( "cluster_index"+str(cid).zfill(3)+"_pop"+str(cluster_pop).zfill(3)+".png")
        img.save( "./cluster_actives/cluster_pop"+str(cluster_pop).zfill(3)+"_index"+str(cid).zfill(3)+".png")
    except:
        m_smiles = df3.loc[ df3['cluster_id'] == cid, 'smiles' ].to_list()
        m_names =  df3.loc[ df3['cluster_id'] == cid, 'PUBCHEM_CID' ].to_list()
        m_names_smiles = zip( m_names, m_smiles )
        print( "cluster_id:{} bombed".format( cid ) )
        for x in m_names_smiles:
            print( "\t{}:{}".format( str(x[0]), str(x[1]) ) )
        print('')
        pass

    

