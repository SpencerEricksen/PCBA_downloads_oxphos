#!/home/ssericksen/anaconda2/bin/python

from sklearn.cluster import AgglomerativeClustering
from sklearn.neighbors import DistanceMetric
from itertools import combinations


def clst_medoids( num_clusters, fps_file ):
    '''given num_clusters and a CSV of chemical fingerprints (binary strings), return
       a cluster medoid list of cpd molids

       note: agglomerative hierarchical clustering is applied with average linkage
             and a distance matrix is computed using Jaccard distances between fingerprints'''

    # read in CSV fingerprints to dataframe
    df = pd.read_csv( fps_file, index_col='PUBCHEM_CID' )

    # uniquify cpd set (multiple occurrences of CIDs)
    df.drop_duplicates( subset='PUBCHEM_CID', keep='first', inplace=True)

    df.index = df.index.map(str)
    # split up bitstrings into integer bit vectors
    df['features'] = df['morgan_bitstring'].apply( lambda x: np.array(list(map(int,list(x)))))

    tup = tuple( df['features'].values )
    # make feature matrix (rows:examples, columns:features)
    X = np.vstack( tup )

    # get mol identifiers "molids"
    molids = tuple(df.index)
    n_cpds = len(molids)

    # get the Jaccard distance matrix
    dist = DistanceMetric.get_metric('jaccard')
    dist_mat = dist.pairwise(X)

    # run Agglomerative Clustering with Average linkage using precomputed dist matrix
    model = AgglomerativeClustering(linkage='average', affinity='precomputed', connectivity=None, n_clusters=num_clusters)
    model = model.fit(dist_mat)
    # note, sklearn will not allow k-means with precomputed dist--it uses Euclidean distances between points
    # not sure how this compares to Jaccard distances for our Morgan radius=3 features (2048 element bit vectors)

    # get medoids (most central structure in each cluster)
    dist_dict = {}
    cids = list(set(model.labels_))

    for cid in cids:
        member_cpds = np.where( model.labels_ == cid )[0]
        cid_dist_matrix = np.zeros( (n_cpds, n_cpds) )
        for pair in combinations( member_cpds, 2 ):
            cid_dist_matrix[ pair[0], pair[1] ] = dist_mat[ pair[0], pair[1] ]

        # get dist sums
        cid_dist_sums = ( cid_dist_matrix.sum( axis=0 ) + cid_dist_matrix.sum( axis=1 ) ) / float(len(member_cpds))
        for cpd, dist_sum in zip( member_cpds, cid_dist_sums[member_cpds] ):
            # store clustering info for each frame
            if cid not in dist_dict:
                dist_dict[cid] = [ (cpd, dist_sum) ]
            else:
                dist_dict[cid].append( (cpd, dist_sum) )

        dist_dict[cid] = sorted( dist_dict[cid], key=lambda x:x[1] )

    # find representative frame for each cid
    rep_frames = [ dist_dict[cid][0][0] for cid in dist_dict ]

    medoid_list = []
    for cid in dist_dict:
        medoid_list.append( molids[dist_dict[cid][0][0]] )
    return medoid_list


