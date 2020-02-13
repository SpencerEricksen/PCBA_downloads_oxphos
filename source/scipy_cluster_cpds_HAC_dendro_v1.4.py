#!/home/ssericksen/anaconda2/envs/py36_chem/bin/python3.6

import sys
import time as time

import numpy as np
import pandas as pd
from itertools import combinations
#from sklearn.neighbors import DistanceMetric
#from sklearn.cluster import AgglomerativeClustering
#from sklearn.decomposition import PCA
import matplotlib
from matplotlib import pyplot as plt

from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from scipy.spatial.distance import pdist, squareform



# load fps data file
try:
    dist_thresh = float( sys.argv[1] )
    incsv = sys.argv[2]
    outcsv = sys.argv[3]
except:
    print("")
    print("./script  dist_thresh   incsv   outcsv ")
    print("             (float)                   ")
    print("")
    exit

# build dataframe -- "ultimate_oxphos_pcassay_dataset_npscores_cplxI-IV.csv" = 361124 cpd records
df1 = pd.read_csv( incsv, sep="|" )

# get active cpds that are associated with ETC-linked PMIDs  # gets down to 894 records
#df1 = df0.loc[ (df0['ETC_linked_AID'] == True) & (df0['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active' ) ]
df2 = df1[ ['PUBCHEM_CID', 'morgan_bitstring'] ]
df2.dropna( inplace=True )  
# just keep one occurrence of each cpd--df3 is down to 316 unique compounds
df3 = df2.drop_duplicates( subset=['PUBCHEM_CID'], keep='first' )

# get molid list
molid_list = list(df3['PUBCHEM_CID'])

# split fp bitstrings into vectors (lists)
df3['fp_lst'] = df3['morgan_bitstring'].apply( lambda x: list(x) )

# generate array of fingerprints
X = list(df3['fp_lst'])
X_arr = np.array( X, dtype=int)
# np.shape(X_arr) = (316, 2048)

st = time.time()
# compute Jaccard condensed dist matrix with scipy function pdist
# returns a condensed distance matrix--aflat array of upper triangle 
# of full dist matrix chokes on np.nans or missing values
cond_dist_mat = pdist( X_arr, metric='jaccard')
dist_mat = squareform( cond_dist_mat )   # will need this later to get medoids

# use distance matrix to cluster (compute linkage matrix) for plotting dendrogram
Z = linkage( cond_dist_mat, method='average', optimal_ordering=True)
#Z = hierarchy.linkage( X_arr, metric='jaccard', method='average')
elapsed_time = time.time() - st
print( "distance matrix, linkage matrix -- Elapsed time: %.2fs" % elapsed_time )

from scipy.cluster.hierarchy import fcluster
#knowing dist_thresh
clusters = fcluster(Z, dist_thresh, criterion='distance')
#clusters = fcluster(Z, k, criterion='maxclust')

# get set of cluster IDs
labels = np.unique(clusters).tolist()

# get cluster rep (most central structure)
# get clusterIDs for each instance:
n_mols = np.shape(X_arr)[0]

# how many clusters?
#num_clusters = len(labels)

# get the relative distances among members within each clusters to find medoid (rep)
dist_dict = {}
for cid in labels:
    member_mols = np.where( clusters == cid )[0]
    cid_dist_matrix = np.zeros( (n_mols, n_mols) )
    for pair in combinations( member_mols, 2 ):
        cid_dist_matrix[ pair[0], pair[1] ] = dist_mat[ pair[0], pair[1] ]
    # get dist sums
    cid_dist_sums = ( cid_dist_matrix.sum( axis=0 ) + cid_dist_matrix.sum( axis=1 ) ) / float(len(member_mols))
    for mol, dist_sum in zip( member_mols, cid_dist_sums[member_mols] ):
        # store clustering info for each mol
        if cid not in dist_dict:
            dist_dict[cid] = [ (mol, dist_sum) ]
        else:
            dist_dict[cid].append( (mol, dist_sum) )
        #print(" cid, frame, dist_sum")
    dist_dict[cid] = sorted( dist_dict[cid], key=lambda x:x[1] )

# find representative cpd for each cid
rep_mols = [ dist_dict[cid][0][0] for cid in dist_dict ]

print("cluster_idx,cluster_mol_rep,cluster_pop")
for cid in dist_dict:
    print( '{:d},{:d},{:d}'.format( cid, molid_list[ dist_dict[cid][0][0] ], len(dist_dict[cid]) ) )

# indicate in original dataframe which PUBCHEM_CIDs are cluster medoids
rep_mols_pccids = [ molid_list[i] for i in rep_mols ]
df3['medoid'] = 0
df3.loc[ df3['PUBCHEM_CID'].isin( rep_mols_pccids ), 'medoid' ] = 1

# put cluster IDs into new dataframe, merge new dataframe with input dataframe and dump
print("dumping new dataframe with cluster ids")
d = { 'PUBCHEM_CID': list(molid_list), 'cluster_id':list(clusters), 'medoid':df3['medoid'].tolist() } 
df4 = pd.DataFrame.from_dict( d )
df5 = df4.merge( df1, how='right', on='PUBCHEM_CID')
#df5.drop( columns=['Unnamed: 0'], inplace=True )

df5.to_csv( outcsv, sep="|", index=False )
print("done writing new dataframe")
print("")

############### draw dendrogram ###################

matplotlib.rcParams['lines.linewidth'] = 0.25

# run dendrogram to get leaf components
R = dendrogram( Z, truncate_mode='lastp', p=len( labels ), no_plot=True )
temp = { R["leaves"][i]: labels[i] for i in range( len(R["leaves"] ) ) }
#temp = {R["leaves"][ii]:(labels[ii], R["ivl"][ii]) for ii in range(len(R["leaves"]))}
def llf(xx):
    leaf = xx
    c = temp[xx]    # get cluster number for given leaf
    pccid = df3.loc[ (clusters == c) & (df3['medoid'] == 1), 'PUBCHEM_CID' ].iloc[0]
    pop = len( clusters[ clusters == c ] )
    return "{} {} ({})".format( str(c), str(pccid), str(pop) )

# plot dendrogram using scipy dendrogram plotting function
plt.figure()
plt.title('Hierarchical Clustering Dendrogram')
plt.xlabel('sample index')
plt.ylabel('distance')

dendrogram(
        Z,
        truncate_mode='lastp',          # show only the last p merged clusters
        p=len( labels ),                # show only the last p merged clusters
        #show_leaf_counts=False,        # otherwise numbers in brackets are counts
        leaf_label_func=llf,             # call up labels for each leaf
        leaf_rotation=90.,      # rotates the x axis labels
        leaf_font_size=1.,      # font size for the x axis labels
        show_contracted=True,   # to get a dist impression in truncated branch
        #color_threshold=0.85,    # color branches below this threshold
)

# draw horizontal cutoff line at max_d
#plt.axhline(y=dist_thresh, c='r')
#plt.axhline(y=0.85, c='r')
plt.ylim((0.775,0.985))
#plt.ylim(bottom=0.8)
#plot_dendrogram(model, labels=model.labels_)   ### note: could also label with medoid PUBCHEM_CID (rep_mols_pccids) as determined below
plt.savefig( 'dendro_HAC_'+str(dist_thresh)+'_ETC.png', dpi=600, figsize=(30,8) )

