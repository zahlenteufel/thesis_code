# import predict_this.text.text as Text
from predict_this.flm.flm_specification import FLM_Specification
from predict_this.text.prediction_texts import PredictionTexts

# factorize the tagged prediction_text for using in GA-FLM


def dump_factorized_prediction_text(flm_spec, prediction_texts):
    for tagged_line in prediction_texts.lines():
        print " ".join(map(flm_spec.convert_to_flm_format, tagged_line))


flm_spec = FLM_Specification("flm_models/WGNCPL.flm.dummy")
dump_factorized_prediction_text(flm_spec, PredictionTexts([1, 2, 3, 4, 5, 7, 8]))
