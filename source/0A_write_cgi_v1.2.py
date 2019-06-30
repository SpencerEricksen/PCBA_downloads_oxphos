#!/home/ssericksen/anaconda2/bin/python2.7

# script to read-in CID list and write out cgi XML files
# for molecule downloads from pubchem using PUG REST

# usage:  script.py   pcba-aid411.cid

import sys

def dump_cgi_xml( outfile, cid_list, AID, AID_chunk ):
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
    "                  <PCT-ID-List_db>pccompound</PCT-ID-List_db>\n"
    "                  <PCT-ID-List_uids>\n"
    )

    for cid in cid_list:
        if cid != '0':
            print >> outfile, "                    <PCT-ID-List_uids_E>"+cid+"</PCT-ID-List_uids_E>"

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

AID_CID_list = sys.argv[1]
AID = AID_CID_list.split('-')[1].split('.')[0]

with open( AID_CID_list, 'r' ) as fh:
    data = fh.readlines()

count = 0
chunk = 0
tmp_cid_list = []
for line in data:
    cid = line.split()[0].strip()
    tmp_cid_list.append(cid)
    if count < 249999:
        count += 1    
    else:
        out_xml_file = open('pc_fetch_'+AID+'_'+str(chunk)+'.cgi', 'w')
        dump_cgi_xml( out_xml_file, tmp_cid_list, AID, chunk )
        count = 0
        chunk += 1
        tmp_cid_list = []

out_xml_file = open('pc_fetch_'+AID+'_'+str(chunk)+'.cgi', 'w')
dump_cgi_xml( out_xml_file, tmp_cid_list, AID, chunk )
