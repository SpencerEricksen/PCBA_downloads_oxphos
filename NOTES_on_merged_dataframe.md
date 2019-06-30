Scripts and Procedure for downloading cpd data for various assay IDs (AIDs) from PubChem

2019-06-28


###############################
####### all cpds in set #######

# total substance records: 361124
#
# number of unique:
# 	CIDs:		308531
#	AIDs:		4641
#	murcko:		108785 
#	gen murcko:	47200
 
df['murcko'].value_counts()
c1ccccc1                                                        16370
c1ccncc1                                                         1531
O=C(Nc1ccccc1)c1ccccc1                                           1423
c1ccc2[nH]ccc2c1                                                  971
O=S(=O)(Nc1ccccc1)c1ccccc1                                        924
...

df['gen_murcko'].value_counts()
C1CCCCC1                                               20737
C1CCC2CCCC2C1                                           4916
C1CCC(C2CCCC2)CC1                                       4877
C1CCCC1                                                 3985
C1CCC(CC2CCCCC2)CC1                                     3753
CC(CC1CCCCC1)C1CCCCC1                                   3729
...

df['PUBCHEM_CID'].value_counts()
3385         131
53248678     128
73349392      83
127052794     78
46231422      73
134148659     71
134152499     71
134135855     70
3686          70
127042467     63
56835077      63
5351344       62
118715557     58
44592813      58
127038448     56
49864230      56
49864238      56
6442493       55
71451715      54
127052377     54
71455260      54
127052378     54
15923208      53
49864232      51
71699613      50
6758          50
36314         49
118735019     49
118737016     48
71680605      47
            ...

df['AID'].value_counts()
1465       215289
540299     102628
720635       8110
720634       8110
720637       8110
651754       1335
651755       1335
1259412       117
576507         94
663105         70
734049         51
1284106        51
1244542        46
1244541        46
1244540        46
1244543        46
1202124        40
1202122        40
1202125        40
1202126        40
1202123        40
1202121        40
1185724        38
1185723        38
1185725        38
1336751        37
1336750        37
1170948        37
1336749        37
1336748        37
...



#########################################
# ACTIVE UCC+ CPDS ONLY
df2 = df.loc[ (df['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active') & (df['match'] == True )  ]

# total substance records: 2230
#
# number of unique:
#       CIDs:           636
#       AIDs:           546
#       murcko:         265
#       gen murcko:     237


df2['AID'].value_counts()
720635     107
720637      74
1465        62
1284106     37
1300838     25
1300839     24
1300840     24
144480      23
1308546     23
608127      23
1308542     23
1308544     23
1308541     23
1308543     23
1308545     23
144499      23
1300841     22
491598      22
491597      22
1242126     21
1242127     20
1242129     20
1161321     19
1242128     19
1161324     19
720634      19
1300842     19
769610      18
769612      18
769611      18
          ...

 df2['PUBCHEM_CID'].value_counts()
44592813     38
49777789     34
53248678     34
46830377     30
25211156     29
6442493      23
56945282     20
56945405     20
44452656     20
127052794    20
134130677    17
11542064     16
10259181     16
5326018      15
73352016     14
73353478     14
71653325     14
71653474     14
71653473     14
5281526      14
54753797     14
71699540     14
71699538     14
46898059     14
71699613     14
73352015     14
73352017     14
73352019     14
73356538     14
3686         13
             ..

df2['gen_murcko'].value_counts()
CC(CCCC1CCCCC1)C1CC(C2CCCCC2)CC1C1CCCCC1                                       126
CC(CCC1CCC2CCCCC21)C1CCCCC1                                                    101
CC1CC2C(CCC3(C(C)CC4CCCCC4)CCCCC23)C2CCC3CCCCC3C12                              90
CC1C(CC2CCCCC2)CC(C(C)C(C)C2CC(CC3CCCCC3)C(C)C(CC3CCCCC3)C2)CC1CC1CCCCC1        80
CC(CC(C)C1CC(CC2CCCCC2)C(C)C(CC2CCCCC2)C1)C1CC(CC2CCCCC2)C(C)C(CC2CCCCC2)C1     79
C1CCC(CCC2CCC(C3CCCCC3)C2)CC1                                                   73
CC1CCC2(CC1)CC(C)C(C1CCCCC1)C2C1CCCCC1                                          68
CC(CC1CC(C)C2CCC3CCCCC3C2C1C)C1CCCCC1                                           64
CC1CC2C3CCCCC3CCC2C2CCC3CCCCC3C12                                               61
CC(CCC1CCCCC1)C1CCC(CCC2CCCCC2)CC1                                              61
CC(CCC1CCCCC1)C1CCCC(C(C)CCC2CCCCC2)C1C1CCCCC1                                  59
CC1CCCC1CCCCCCCCCCCCCC1CCC(C2CCCC2)C1                                           45
CC1CC2CCCCC2CC1CC1CCC(CCC2CCC(C3CCCCC3)C2)CC1                                   43
CC(CCC1CCCCC1)C1CC2CCCCC2C2CCCCC12                                              42
CC1CCC2CCC3CCCCC3C2C1                                                           38
CC(CC1CC(C)C2CC(CC(C)C3CCCCC3)C3CCCCC3C2C1C)C1CCCCC1                            36
CC1CCCCC1                                                                       36
CC1C(C)C(CC2CCCCC2)C2CCCCC12                                                    35
CC1CCC(C)CC1                                                                    35
CC(CCCCC1CCCC1)CC1CC2CCCC3CCCC(CCCC(C)CC(C2)C1)C3                               32
CC1CCC2C(CCC3C4CCCC4CCC23)C1                                                    29
CC1CCC(C)C2CC3C(CC12)C(C)C1CCC2CCCC3C21                                         27
CC(CCC1CCC2CCCCC21)C1CCCC2CCCCC21                                               25
CC1CC(CC2CCCCC2)C(C)C2CCCCC12                                                   24
CC1CC(C)C(C)C1                                                                  23
CC1CCC2CCC3CCCCC3C2C1C                                                          21
CC(CCCCCCCC1CCCC1C)CCCCCC1CCC(C2CCCC2)C1                                        20
CC1CC2CCCCC3CC3CCC2C1C                                                          20
CC1CC2CCCCC2C1CC1CCCC(CCC2CCC(CC3CCCCC3)C2)C1                                   19
CC(CCC1CCC(CC2C(C)CC3CCCCC32)CC1)C1CCCCC1                                       18
...

df2['murcko'].value_counts()
O=C(C=CNc1ccccc1)c1cn(-c2ccccc2)nc1-c1ccccc1                                         126
O=C(C=Cc1c[nH]c2ccccc12)c1ccccc1                                                     101
O=C1C=C2C(CCC3(C(=O)Nc4ccccc4)CCCCC23)C2CCC3CCCCC3C12                                 90
O=C1C(=Cc2ccccc2)CN(C(=O)C(=O)N2CC(=Cc3ccccc3)C(=O)C(=Cc3ccccc3)C2)CC1=Cc1ccccc1      80
O=C1C(=Cc2ccccc2)CN(C(=O)CC(=O)N2CC(=Cc3ccccc3)C(=O)C(=Cc3ccccc3)C2)CC1=Cc1ccccc1     79
c1ccc(OCc2cn(-c3ccccc3)nn2)cc1                                                        69
O=C1C=C(OC(=O)c2ccccc2)C(=O)C2=C1CCC1CCCCC21                                          64
O=C1C=C2C3CCCCC3CCC2C2CCC3CCCCC3C12                                                   61
O=C(C=Cc1ccccc1)c1ccc(C=Cc2ccccc2)cc1                                                 61
O=C(C=Cc1ccccc1)c1cccc(C(=O)C=Cc2ccccc2)c1-c1ccccc1                                   59
O=C1OCC=C1CCCCCCCCCCCCCC1CCC(C2CCCO2)O1                                               45
O=C(C=Cc1ccccc1)c1cc2c(c3c1OCCC3)OCCC2                                                42
O=C1CC2CCCCC2CC1=Cc1ccc(OCc2cn(-c3ccccc3)nn2)cc1                                      40
O=C1C=CC2=CCC3CCCCC3C2=C1                                                             38
O=C1C=C(OC(=O)c2ccccc2)C(=O)C2=C1CC(OC(=O)c1ccccc1)C1CCCCC21                          36
O=C1C=CC2(C=C1)OC(=O)C(c1ccccc1)=C2c1ccccc1                                           36
O=C1C(=O)N(Cc2ccccc2)c2ccccc21                                                        35
O=C1C=CC(=O)C=C1                                                                      35
C=C1C=CCCO1                                                                           34
O=C(C=CCCc1cocn1)OC1CC2CCCC3CCCC(CCOC(=O)CC(C1)O2)O3                                  32
O=C1C=CC2(C=C1)NC(=O)C(c1ccccc1)=C2c1ccccc1                                           32
O=C1C=CC(=O)c2cc3c(cc21)C(=O)c1occ2c1C3CCC2                                           27
O=C(C=Cc1c[nH]c2ccccc12)c1cccc2c1OCC=C2                                               25
C=C1CC(=C)C(=O)O1                                                                     23
O=C1C=CC2C(=C1)CCC1C3CCCC3CCC21                                                       23
O=C1C=C(Nc2ccccc2)C(=O)c2ccccc21                                                      23
O=C1C=CC2=C(C1=O)C1CCCCC1CC2                                                          21
C=C1C(=O)OC2C=CCCC3OC3CCC12                                                           20
O=C1Nc2ccccc2C1=Cc1cccc(OCc2cn(Cc3ccccc3)nn2)c1                                       19
O=C1Nc2ccc(C(c3ccccc3)c3ccccc3)cc2C1=Cc1cccc(OCc2cn(Cc3ccccc3)nn2)c1                  17
...


###################################################
# ACTIVE CPDS (UCC+ and UCC-)
df2 = df.loc[ (df['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active')  ]

# total substance records: 10187
#
# number of unique:
#       CIDs:           3818
#       AIDs:           1613
#       murcko:         1536
#       gen murcko:     1095

df['PUBCHEM_CID'].value_counts()
3385         90
72197691     39
72197692     39
44592813     38
49777789     34
53248678     34
31703        32
46830377     30
25211156     29
5351344      29
6758         28
71680187     25
127052378    24
127052377    23
6442493      23
72197868     23
10448831     22
118737016    22
118726131    22
188448       22
36314        20
127052794    20
44452656     20
56945282     20
56945405     20
118737006    20
118737020    20
71462730     19
127039865    19
72735425     19
             ..

df2['AID'].value_counts()
720635     1300
720637      904
540299      436
720634      260
1465        158
651754      125
651755      112
1259412     100
576507       88
663105       60
1244542      46
1244541      45
1244540      45
1284106      38


##########################################

# UCC+ only (active, inactive, inconclusive, unknown)
df2 = df.loc[ (df['match'] == True)  ]

# total substance records: 30946
#
# number of unique:
#       CIDs:           24385
#       AIDs:           1490
#       murcko:         8835
#       gen murcko:     5142

df2['murcko'].value_counts()
c1ccccc1                                                                             1034
O=C1C(=Cc2ccccc2)CN(C(=O)C(=O)N2CC(=Cc3ccccc3)C(=O)C(=Cc3ccccc3)C2)CC1=Cc1ccccc1      226
O=C1C=CC(=O)C=C1                                                                      220
O=C1NC=CC(c2ccccc2)N1                                                                 198
O=C(C=Cc1c[nH]c2ccccc12)c1ccccc1                                                      198
O=C(C=Cc1ccccc1)c1cc2c(c3c1OCCC3)OCCC2                                                198
O=C1C(=Cc2ccccc2)CN(C(=O)CC(=O)N2CC(=Cc3ccccc3)C(=O)C(=Cc3ccccc3)C2)CC1=Cc1ccccc1     184
O=C1C=C2CCC3C4CCCC4CCC3C2CC1                                                          183
O=C(C=Cc1ccccc1)Nc1ccccc1                                                             182
O=C1C=CC2C(=C1)CCC1C3CCCC3CCC21                                                       180
O=C(C=CNc1ccccc1)c1cn(-c2ccccc2)nc1-c1ccccc1                                          174
C1=CC(c2ccccc2)C=CN1                                                                  141
O=C1C=C2C(CCC3(C(=O)Nc4ccccc4)CCCCC23)C2CCC3CCCCC3C12                                 138
C=C1C=CCCO1                                                                           128
O=C1C=C2C3CCCCC3CCC2C2CCC3CCCCC3C12                                                   123
O=C(C=Cc1ccccc1)c1ccccc1                                                              121
c1ccc(OCc2cn(-c3ccccc3)nn2)cc1                                                        112
O=C1C=CCCC1                                                                           106
O=C1C=CC(=O)c2ccccc21                                                                 101
O=C(C=Cc1ccccc1)c1ccc(C=Cc2ccccc2)cc1                                                 100
O=C1OCC=C1CCCCCCCCCCCCCC1CCC(C2CCCO2)O1                                                94
O=C1C=C(OC(=O)c2ccccc2)C(=O)C2=C1CCC1CCCCC21                                           90
O=C1NC(c2ccccc2)C(=Cc2ccccc2)C1=O                                                      86
c1ccsc1                                                                                85
O=C1Nc2ccccc2C1=Cc1cccc(OCc2cn(Cc3ccccc3)nn2)c1                                        84
O=C(C=Cc1ccccc1)c1cccc(C(=O)C=Cc2ccccc2)c1-c1ccccc1                                    84
O=C(C=CNc1ccccc1)c1ccccc1                                                              84
O=C(NC=Cc1ccccc1)c1ccccc1                                                              76
O=C1C=CC2(C=C1)OC(=O)C(c1ccccc1)=C2c1ccccc1                                            74
O=C1CC2CCC3C4CCC5CCCCC5C4=CCC3C2CC1=Cc1ccccc1                                          65
                                                                                     ...


######################################################
# UCC- (active, inactive, inconclusive, unknown)
 df2 = df.loc[ (df['match'] == False)  ]

# number of records: 330172
# number of unique CIDs: 284144
# number of unique AIDs: 3536
# number of murcko: 100488
# number generic murcko: 43924


