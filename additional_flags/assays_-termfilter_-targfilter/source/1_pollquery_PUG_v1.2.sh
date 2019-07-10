#!/bin/bash
#
#################
#
# To check status of job on PUBCHEM with PUG
#
# usage: ./1_pollquery_PUG.sh  pc_fetch_aid833_2.cgi
#
##################

query_file=$1

aid=`echo ${query_file} | cut -f3 -d"_" | cut -c4-`
aid_chunk=`echo ${query_file} | cut -f4 -d"_" | cut -f1 -d"."`

url="https://pubchem.ncbi.nlm.nih.gov/pug/pug.cgi"

#reqid="2164301182858591537"
reqid=`cat submitquery_${aid}_${aid_chunk}_log.html | grep "Waiting_reqid" | cut -d">" -f2 | cut -d"<" -f1`
cat poll.cgi | sed "s/REQID_NUM/${reqid}/g" > poll_${reqid}_${aid}_${aid_chunk}.cgi

xml=poll_${reqid}_${aid}_${aid_chunk}.cgi

# curl -X POST -d @filename http://hostname/resource
curl -X POST -d @$xml $url > pollquery_${aid}_${aid_chunk}_log.html 2>&1 &

# now clean up after poll request
#rm $xml


