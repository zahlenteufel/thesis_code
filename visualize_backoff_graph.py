#!/usr/bin/env python
import sys
import os
import tempfile
import predict_this.flm.flm_specification as FlmSpec

input_model = sys.argv[1] if len(sys.argv) > 1 else "flm_models/trigramWGN.flm"

flm_spec = FlmSpec.FLM_Specification(input_model)

with tempfile.NamedTemporaryFile() as neato:
    print >>neato, flm_spec.visualize()
    neato.flush()
    os.system("neato -n %s -Tpng > out.png_1" % neato.name)

with tempfile.NamedTemporaryFile() as dot:
    print >>dot, flm_spec.backoff_graph.visualize()
    dot.flush()
    os.system("dot %s -Tpng > out.png_2" % dot.name)

os.system("convert +append out.png_1 out.png_2 out.png")
os.system("feh out.png")
os.unlink("out.png_1")
os.unlink("out.png_2")
os.unlink("out.png")
