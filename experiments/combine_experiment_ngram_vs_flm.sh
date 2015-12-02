#!/usr/bin/env bash

sizes="2000 5000 10000 20000 30000 40000 50000 75000 100000 250000 500000 1000000"

result="predicciones_ngram_y_flms.csv";
> $result

# #texto,#palabra,palabra,cloze_predictor,unigram_cache_predictor,3gram,4gram,flm_models/4gramWC.flm

for size in $sizes; do
	# agarrar las predictions_$size.csv, afanarle las columnas que quiero y concatenarlas, usando el 
	# correcto header y armar un 
	prediction_file="predictions_$size.csv";
	title=`head -n 1 $prediction_file | cut -d "," -f 8`;
	filename=${title#*/};
	name=${filename%.flm}_$size;
	echo $name > _tmp;
	tail -n +2 $prediction_file | cut -d "," -f 8 >> _tmp;
	paste -d "," $result _tmp > _tmp2
	cp _tmp2 $result
done

cut -d "," -f 1 --complement < _tmp2 > $result

rm -f _tmp _tmp2

echo "Done. result in $result"
