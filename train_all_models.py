#!/usr/bin/env python

from datetime import datetime
import glob
import predict_this.text.text as Text
import predict_this.flm.flm_specification as FlmSpec

text = Text.Text.from_flat_file("prueba.txt")

log_file = open("training.log", "a")


def log(s):
    print >>log_file, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), ":", s
    log_file.flush()


for flm_model_filename in glob.glob("flm_models/*.flm"):
    log("started training " + flm_model_filename)

    flm_spec = FlmSpec.FLM_Specification().initialize_with_model_file(flm_model_filename)

    # os.system("fngram-count -factor-file %s -no-virtual-end-sentence -lm -write-counts -text %s" % (
    #     flm_model_filename,
    #     factored_corpus_file
    #     ))
    log("done training " + flm_model_filename)

# # ft = FactoredText.FactoredText(flm, text)

# prediction_text = PT.PredictionText(1)

# text = Text.Text.from_flat_file("prueba.txt")

# for line in text.lines():
#     for word in line:
#         print flm_spec.convert_to_flm_format(word)



# predictor = FLMP.FLMPredictor(flm_spec, 3, "bigramWG.flm", "count_file")
# predictor.predict(prediction_text)




# corpus = Text("half_corpus.txt")
# prediction_texts = map(PredictionText, [1, 2, 3, 4, 5, 7, 8])

# ngram_model = models.ngram.train(corpus, 7)  # or load from disk

# flm_specs = [load from disk (models/*Pflm)]

# predictions = []

# for order in [2, 3, 4, 5, 6, 7]:
#   ngram_predictor = ngram_model.predictor(order)
#   predictions.add(("ngram_%d" % order, ngram_predictor.batch_predict(prediction_texts))

# del ngram_predictor
# del ngram_model # release memory

# for flm_spec in flm_spec_list():
#   flm_model = flm.train(flm_spec, corpus)
#   predictions.add((flm_spec.name(), flm_predictor.batch_predict(prediction_texts)))

# # save predictions in a file

# dump_predictions:

# compare correlations, try to find (fit) best mixture...
