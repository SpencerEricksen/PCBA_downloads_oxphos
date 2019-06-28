#!/bin/bash

templist=$1

cp $templist tmp

for aid in `cat zz`; do
    cat tmp | grep -v ^${aid}$ > tmp2
    mv tmp2 tmp
done

