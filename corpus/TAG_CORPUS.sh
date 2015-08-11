#!/usr/bin/env bash

# set -e

[ ! -d pedazos_corpus ] && mkdir pedazos_corpus
[ ! -d resultados ] && mkdir resultados

split --number=l/10000 -d corpus_cleaned.txt pedazos_corpus/

analyze_es="analyze -f /usr/local/share/freeling/config/es.cfg"

N=7
(
for i in {0..9999}
do
	((x=x%N)); ((x++==0)) && wait;
	ind=`printf %04d $(echo $i | sed 's/[^0-9]*//g')`
	echo $ind $(date)
	$analyze_es --nortk --nortkcon --flush < pedazos_corpus/$ind > resultados/analisis_$ind.txt &
done
)
echo terminado $(date)
