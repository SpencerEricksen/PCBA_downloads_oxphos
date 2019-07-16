# download XML files that include rich information for each AID
 ./curl_xml_download_wrapper.sh assay_list.list &


# what are the different attributes in the xml files that get dumped when I do extraction
for f in `cat assay_list.list`; do ./parse_pcba_AIDs_desc_xml_v1.3.py $f; done | awk -F":" '{print $1}' | sort | uniq > unique_attributes.list 

# I narrowed down from unique_attributes to the desired attributes and edited parse script to just dump those.

for f in `cat assay_list.list`; do ./parse_pcba_AIDs_desc_xml_v1.3.py $f; done > all_assays_desc.csv

# remove all but first header line
sed -i '2,${/^AID/d;}' all_assays_desc.csv

NOTE: i used '|' as delimiter to avoid issues with commas appearing in abstracts (false delimiters). I think this was the issue. By using alternative delimiter we should be able to read correctly into spreadsheet

