#!/home/ssericksen/anaconda2/bin/python2.7

# script to read-in SID list and write out cgi XML files
# for molecule downloads from pubchem using PUG REST

# usage:  script.py   pcba-aid411_activities.csv

import pandas as pd
import sys

def dump_cgi_xml( outfile, sid_list, AID, AID_chunk ):
    '''write out a cgi xml file for fetching'''
    outfile.write(
    '<?xml version="1.0"?>\n'
    '<!DOCTYPE PCT-Data PUBLIC "-//NCBI//NCBI PCTools/EN" "http://pubchem.ncbi.nlm.nih.gov/pug/pug.dtd">\n'
    "<PCT-Data>\n"
    "  <PCT-Data_input>\n"
    "    <PCT-InputData>\n"
    "      <PCT-InputData_download>\n"
    "        <PCT-Download>\n"
    "          <PCT-Download_uids>\n"
    "            <PCT-QueryUids>\n"
    "              <PCT-QueryUids_ids>\n"
    "                <PCT-ID-List>\n"
    "                  <PCT-ID-List_db>pcsubstance</PCT-ID-List_db>\n"
    "                  <PCT-ID-List_uids>\n"
    )

    for sid in sid_list:
        if sid != '0':
            print >> outfile, "                    <PCT-ID-List_uids_E>"+sid+"</PCT-ID-List_uids_E>"

    outfile.write(
    "                  </PCT-ID-List_uids>\n"
    "                </PCT-ID-List>\n"
    "              </PCT-QueryUids_ids>\n"
    "            </PCT-QueryUids>\n"
    "          </PCT-Download_uids>\n"
    '          <PCT-Download_format value="smiles"/>\n'
    '          <PCT-Download_compression value="gzip"/>\n'
    '          <PCT-Download_use-3d value="false"/>\n'
    "        </PCT-Download>\n"
    "      </PCT-InputData_download>\n"
    "    </PCT-InputData>\n"
    "  </PCT-Data_input>\n"
    "</PCT-Data>\n"
    )
    outfile.close()

AID_SID_list = sys.argv[1]
AID = AID_SID_list.split('-')[1].split('.')[0]

df = pd.read_csv( AID_SID_list, index_col='PUBCHEM_SID' )
sids = [ str(sid) for sid in df.index.to_list() ]

count = 0
chunk = 0
tmp_sid_list = []
for sid in sids:
    tmp_sid_list.append(sid)
    if count < 249999:
        count += 1    
    else:
        out_xml_file = open('pc_fetch_'+AID+'_'+str(chunk)+'.cgi', 'w')
        dump_cgi_xml( out_xml_file, tmp_sid_list, AID, chunk )
        count = 0
        chunk += 1
        tmp_sid_list = []

out_xml_file = open('pc_fetch_'+AID+'_'+str(chunk)+'.cgi', 'w')
dump_cgi_xml( out_xml_file, tmp_sid_list, AID, chunk )

