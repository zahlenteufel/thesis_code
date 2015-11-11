#!/usr/bin/env bash

# Experiment:
# Train ngram and a flm with different corpus sizes and compare.

#izes="10000 100000 500000 1000000 2000000 4000000 8000000 15000000";
MAX=1000000
MIN=50000
sizes="$MIN 75000 100000 250000 500000 $MAX" # 500000 1000000 2000000"
logfile="experiment_ngram_vs_flm.log";
flm_model="4gramWC";
fngram_count_command="fngram-count -factor-file flm_models/$flm_model.flm -no-virtual-begin-sentence -nonull -no-virtual-end-sentence -unk -lm -write-counts -no-add-end-sentence-token";
four_gram_lm_file="4gram_experiment_size.lm.gz";
ngram_count_command="ngram-count -order 4 -unk -no-eos -lm $four_gram_lm_file";

set -e

echo "$(date): begin experiment ngram vs $flm_model" | tee -a $logfile;
echo "sizes: $sizes" | tee -a $logfile;
echo "fngram_count_command: '$fngram_count_command'" | tee -a $logfile;
echo "ngram_count_command: '$ngram_count_command'" | tee -a $logfile;

shuf -n $MAX corpus/factored_corpus_WGNCPL.txt > tmp_shuf_corpus_factored;
sed -E 's/([^ :]*):([^ ])*/\1/g' < tmp_shuf_corpus_factored > tmp_shuf_corpus;
head -n $MIN tmp_shuf_corpus | tr " " "\n" | sort -u > vocab_shuf_min;

for size in $sizes; do
	# tmp_corpus=corpus/tmp_shuf_$size;
	# tmp_factored_corpus=${tmp_corpus}_factored;
	# head -n $size tmp_shuf_corpus > $tmp_factored_corpus;

	rm -f flm_models/$flm_model.count.gz flm_models/$flm_model.lm.gz;
	rm -f $four_gram_lm_file;

	echo "$(date): train flm" | tee -a $logfile;
	head -n $size tmp_shuf_corpus_factored | $fngram_count_command -text -;

	echo "$(date): train ngram" | tee -a $logfile;
	head -n $size tmp_shuf_corpus | $ngram_count_command -text -;

	echo "perplexities:"

	echo -n "$size " >> SALIDA

	python predictor_tables.py -ngram_lm $four_gram_lm_file -only_targets_in vocab_shuf_min -ngram_predictor_orders 3 4 -flm_model_filenames flm_models/$flm_model.flm > pruned_predictions_$size.csv
	python analyze_perplexities.py < pruned_predictions_$size.csv --terminal --no_header |
	tee -a SALIDA;

done

rm -f flm_models/$flm_model.count.gz flm_models/$flm_model.lm.gz;
rm -f $four_gram_lm_file;
rm -f tmp_shuf_corpus tmp_shuf_corpus_factored vocab_shuf_min;

echo "$(date): done" | tee -a $logfile;
