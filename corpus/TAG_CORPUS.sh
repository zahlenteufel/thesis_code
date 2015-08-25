#!/usr/bin/env bash

# set -e (doesn't work with the loop in the bottom :/)

[ ! -d chunks ] && mkdir chunks
[ ! -d tagged_chunks ] && mkdir tagged_chunks

split --number=l/10000 -d tmp/corpus_cleaned.txt chunks/

analyze_es="analyze -f /usr/local/share/freeling/config/es.cfg"

N=7
(
for i in {0..9999}
do
	((x=x%N)); ((x++==0)) && wait;
	ind=`printf %04d $(echo $i | sed 's/[^0-9]*//g')`
	echo "$(date): tagging $ind"
	$analyze_es --nortk --nortkcon --nodate --noloc --flush < chunks/$ind > tagged_chunks/$ind &
done
)
echo converting to ascii

cd ..
python convert_to_ascii

echo terminado $(date)
