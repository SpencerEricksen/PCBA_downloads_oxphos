#!/bin/bash

##########################
#
# usage: ./0_submitquery_PUG_v4.1.sh   pc_fetch.cgi.xml
#
# where the 1st argument is the .xml file obtained from
# the https://pubchem.ncbi.nlm.nih.gov/pc_fetch/pc_fetch.cgi
# where I submitted a list of CIDs to put into my query for
# downloading (3D coordinates in .sdf format)
#
###########################

#url="https://pubchem.ncbi.nlm.nih.gov/pc_fetch/pc_fetch.cgi"
url="https://pubchem.ncbi.nlm.nih.gov/pug/pug.cgi"

xml_file=$1
#xml="pc_fetch_aid686979_0.cgi"
aid=`echo ${xml_file} | cut -f3 -d"_" | cut -c4-`
aid_chunk=`echo ${xml_file} | cut -f4 -d"_" | cut -f1 -d"."`

# curl -X POST -d @filename http://hostname/resource
curl -X POST -d @${xml_file} $url > submitquery_${aid}_${aid_chunk}_log.html 2>&1 &

echo "Query XML: "${xml_file} >> submitquery_${aid}_${aid_chunk}_log.html

