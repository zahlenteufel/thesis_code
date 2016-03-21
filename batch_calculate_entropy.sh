#!/usr/bin/env bash

set -e

> _batch

for i in {1,2,3,4,5,7,8}; do
	echo "python calculate_entropy_with_cache.py -text_numbers $i -cache_lambda 0.22" >> _batch;
done

parallel < _batch
rm -f _batch

Y="entropy_prob4_prunned_dist"

salida="$EXPERIMENTS_DATA_PATH/$Y.csv"

echo "$Y" |
	cat - $EXPERIMENTS_DATA_PATH/entropy_with_cache_* |
	paste -d "," "$EXPERIMENTS_DATA_PATH/analisis_4gram.csv" - > $salida
