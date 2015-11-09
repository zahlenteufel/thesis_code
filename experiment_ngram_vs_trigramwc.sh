#!/usr/bin/env bash

# Experiment:
# Train ngram and trigramWC flm with different corpus sizes and compare.

#izes="10000 100000 500000 1000000 2000000 4000000 8000000 15000000";
sizes="10000"
logfile="experiment_ngram_vs_trigramwc.log";
fngram_count_command="fngram-count -factor-file flm_models/trigramWC.flm -no-virtual-begin-sentence -nonull -no-virtual-end-sentence -unk -lm -write-counts -no-add-end-sentence-token";
four_gram_lm_file="4gram_experiment_size.lm.gz";
ngram_count_command="ngram-count -order 4 -unk -no-eos -lm $four_gram_lm_file";

echo "$(date): begin experiment ngram vs trigramwc" | tee -a $logfile;
echo "$(date): sizes: $sizes" | tee -a $logfile;
echo "$(date): fngram_count_command: '$fngram_count_command'" | tee -a $logfile;
echo "$(date): ngram_count_command: '$ngram_count_command'" | tee -a $logfile;

for size in $sizes; do
	echo "$(date): creating sample corpus of size $size" | tee -a $logfile;
	tmp_corpus=corpus/tmp_shuf_$size;
	tmp_factored_corpus=${tmp_corpus}_factored;
	shuf -n $size corpus/factored_corpus_WGNCPL.txt > $tmp_factored_corpus;

	echo "$(date): train flm" | tee -a $logfile;
	$fngram_count_command -text $tmp_factored_corpus;

	echo "$(date): extract words only" | tee -a $logfile;

	sed -E 's/([^ :]*):([^ ])*/\1/g' < $tmp_factored_corpus > $tmp_corpus;

	# rm -f $tmp_factored_corpus;

	echo "$(date): train ngram" | tee -a $logfile;

	$ngram_count_command -text $tmp_corpus;

	echo "perplexities:"

	python predictor_tables.py -ngram_lm $four_gram_lm_file -ngram_predictor_orders 4 -flm_model_filenames flm_models/trigramWC.flm |
	python analyze_perplexities.py --terminal |
	tee -a $logfile;

done

# rm -f flm_models/trigramWC.count.gz flm_models/trigramWC.lm.gz;
# rm -f $four_gram_lm_file;

echo "$(date): done" | tee -a $logfile;
