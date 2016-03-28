#!/usr/bin/env bash

# set -e (doesn't work with the loop in the bottom :/)

[ ! -d tmp/chunks ] && mkdir tmp/chunks
[ ! -d tmp/tagged_chunks ] && mkdir tmp/tagged_chunks

split --number=l/10000 -d corpus_cleaned.txt tmp/chunks/

analyze_es="analyze -f /usr/local/share/freeling/config/es.cfg"

N=7
(
for i in {0..9999}
do
	((x=x%N)); ((x++==0)) && wait;
	ind=`printf %04d $(echo $i | sed 's/[^0-9]*//g')`
	echo "$(date): tagging $ind"
	$analyze_es --nortk --nortkcon --nonumb --nocoref --noorto --nodate --nophon --noner --noloc --flush < tmp/chunks/$ind > tmp/tagged_chunks/$ind &
done
)

echo $(date): finished tagging

echo $(date): converting to ascii

python scripts/convert_to_ascii.py

echo $(date): concatenating files

find tmp/tagged_chunks/ -type f -print0 -name "*.ascii" | sort -z | xargs -0 cat -- > tmp/factored_corpus_WGNCP.txt

echo $(date): finished 
