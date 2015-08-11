#!/usr/bin/env bash

log_file=log_train_all_models.log

for flm_model in flm_models/*flm; do
	echo "$(date): training $flm" >> $log_file
	fngram-count -factor-file $flm_model -no-virtual-end-sentence -lm -write-counts -text factored_corpus.txt
done
echo "$(date): done" >> $log_file

# corpus = Text("half_corpus.txt")
# prediction_texts = map(PredictionText, [1, 2, 3, 4, 5, 7, 8])

# ngram_model = models.ngram.train(corpus, 7)  # or load from disk

# flm_specs = [load from disk (models/*Pflm)]

# predictions = []

# for order in [2, 3, 4, 5, 6, 7]:
# 	ngram_predictor = ngram_model.predictor(order)
# 	predictions.add(("ngram_%d" % order, ngram_predictor.batch_predict(prediction_texts))

# del ngram_predictor
# del ngram_model # release memory

# for flm_spec in flm_spec_list():
# 	flm_model = flm.train(flm_spec, corpus)
# 	predictions.add((flm_spec.name(), flm_predictor.batch_predict(prediction_texts)))

# # save predictions in a file

# dump_predictions:

# compare correlations, try to find (fit) best mixture...
