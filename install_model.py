import sys
import os
import os.path
from itertools import ifilter


def install_model(name, model_filename, destination_folder="flm_models/"):
    target_factor_file_filename = destination_folder + name + ".flm"
    with open(model_filename) as original_flm_spec_file:
        flm_spec = ifilter(meaningful_line, original_flm_spec_file)
        with open(target_factor_file_filename, "w") as new_flm_spec:
            num = int(flm_spec.next())
            assert num == 1
            print >>new_flm_spec, num
            header = flm_spec.next().split()
            if header[0].endswith(":"):
                header = [header[0][:-1], ":"] + header[1:]
            num_backoff_lines = header[-1]
            header[-2] = destination_folder + name + ".lm.gz"
            header[-3] = destination_folder + name + ".counts.gz"
            print >>new_flm_spec, " ".join(header)
            for i in xrange(num_backoff_lines):
                print >>new_flm_spec, flm_spec.next()
            if any(flm_spec):
                print "WARNING: lines after the declared backoff lines amount"
    model_filename_base = model_filename.rsplit('.', 1)[0]
    if os.path.isfile(model_filename_base + ".count.gz") and os.path.isfile(model_filename_base + ".lm.gz"):
        os.system("ln -v " + model_filename_base + ".count.gz " + destination_folder + name + ".count.gz")
        os.system("ln -v " + model_filename_base + ".lm.gz " + destination_folder + name + ".lm.gz")


def meaningful_line(it):
    for line in it:
        if line != "\n" and not line.startswith("##"):
            yield line[:-1]


if __name__ == "__main__":
    install_model(sys.argv[1], sys.argv[2])
