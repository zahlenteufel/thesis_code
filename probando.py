# import predict_this as pd
# import predict_this.text.text as Text
import predict_this.flm.flm_specification as FlmSpec
# import predict_this.text.factored_text as FactoredText
# import predict_this.predictor.flm_predictor as FLMP
# import predict_this.text.prediction_text as PT
# text = Text.Text.from_flat_file("prueba.txt")
flm_spec = FlmSpec.FLM_Specification().initialize_with_model_file("flm_models/trigramWGN.flm")

print flm_spec.visualize()
# # ft = FactoredText.FactoredText(flm, text)

# prediction_text = PT.PredictionText(1)

# text = Text.Text.from_flat_file("prueba.txt")

# for line in text.lines():
#     for word in line:
#         print flm_spec.convert_to_flm_format(word)



# predictor = FLMP.FLMPredictor(flm_spec, 3, "bigramWG.flm", "count_file")
# predictor.predict(prediction_text)
