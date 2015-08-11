#!/usr/bin/env python
import sys
import os
import tempfile
import predict_this.flm.flm_specification as FlmSpec

input_model = sys.argv[1] if len(sys.argv) > 1 else "flm_models/trigramWGN.flm"
output_image = sys.argv[2] if len(sys.argv) > 2 else "out.png"

flm_spec = FlmSpec.FLM_Specification(input_model)

with tempfile.NamedTemporaryFile() as dot:
    print >>dot, flm_spec.visualize()
    dot.flush()

    command = "dot %s -Tpng" % dot.name
    if output_image != "-":
        command += " > %s " % output_image
    os.system(command)
