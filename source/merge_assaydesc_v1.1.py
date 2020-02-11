import pandas as pd
import numpy as np

df1 = pd.read_csv('all_oxphos_aids_cids.csv')
df2 = pd.read_csv('./assay_descriptions/all_assays_desc.csv', sep="|")
df3 = df2.merge( df1, how='right', on='AID')
df3.to_csv('all_oxphos_aids_cids_assaydesc.csv', sep="|", index=False )

