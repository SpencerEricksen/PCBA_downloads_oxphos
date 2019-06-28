#!/bin/bash
#
#################
#
# To check status of job on PUBCHEM with PUG
#
# usage:   ./2_downloadresults_PUG_v1.1.sh   fetch_file.cgi
#
##################

query_file=$1

aid=`echo ${query_file} | cut -f3 -d"_" | cut -c4-`
aid_chunk=`echo ${query_file} | cut -f4 -d"_" | cut -f1 -d"."`

remotefilepath=`grep fetch pollquery_${aid}_${aid_chunk}_log.html | cut -d">" -f2 | cut -d"<" -f1`

wget $remotefilepath > download_queryresults_${aid}_${aid_chunk}.log 2>&1 &

# just the filename from the pathname
# fn="${remotelink##*/}"

# remove filename from pathname
# remotedir="${remotelink%/*}"

#### or use curl
#curl --url $remotelink > download.log 2>&1 &

# if we had a file containing a list of filenames to download:
#wget --base=$remotedir --input-file=$fn &"

