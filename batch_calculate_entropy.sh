#!/usr/bin/env bash

set -e

for PRUNE in {10,100,1000,10000,100000}; do

	echo "Calculating with PRUNE=$PRUNE"

	> _batch

	PRUNE=10000

	for i in {1,2,3,4,5,7,8}; do
		echo "python calculate_entropy_with_cache.py -text_numbers $i -prune $PRUNE -cache_lambda 0" >> _batch;
	done

	parallel < _batch
	rm -f _batch

	X="prob4_$PRUNE"
	Y="entropy_prob4_$PRUNE"

	salida="analisis_4gram_prunned_$PRUNE.csv"

	echo "$X,$Y" |
		cat - entropy_with_cache_* |
		paste -d "," analisis_4gram.csv - > $salida

	python graficar_entropia.py < $salida -x $X -y prob_cloze -o "plot1_$PRUNE.png";
	python graficar_entropia.py < $salida -x $Y -y entropia_cloze -o "plot2_$PRUNE.png";
	python graficar_entropia.py < $salida -x $X -y $Y -o "plot3_$PRUNE.png";

done
