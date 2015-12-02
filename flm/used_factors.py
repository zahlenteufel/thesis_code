import predict_this.flm.flm_specification as FlmSpec
import sys

filename = sys.argv[1]
flm_spec = FlmSpec.FLM_Specification(filename)

print " ".join(sorted(["W"] + list(flm_spec.factors())))
