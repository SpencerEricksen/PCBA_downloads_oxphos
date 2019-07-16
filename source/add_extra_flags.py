
import pandas as pd
import numpy as np

df = pd.read_csv('../all_oxphos_aids_cids_fps.csv')

df = df.drop( columns=['Unnamed: 0'] )


# add flag for whether AID has biochemical target (True)

df['biochemical_target'] = False

with open( '../../additional_flags/assays_-termfilter_+targfilter/assay_list_221.txt', 'r' ) as fh:
    data = fh.readlines()

biochem_aid_list = [ int(x.strip()) for x in data ]

for i in biochem_aid_list:
    df.loc[ df['AID'] == i, 'biochemical_target' ] = True



# add flag for whether assay (AID) passes additional term filter

df['pass_term_filter'] == False

with open( '../../additional_flags/assays_+termfilter_-targfilter/assay_list_4346.txt', 'r' ) as fh:
    data = fh.readlines()

termfilter_aid_list = [ int(x.strip()) for x in data ]

for i in termfilter_aid_list:
    df.loc[ df['AID'] == i, 'pass_term_filter' ] = True


# dump to new CSV
df.to_csv('../all_oxphos_aids_cids_fps_terms_bctarg.csv')


