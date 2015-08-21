import sys

assert len(sys.argv) == 3, "parameter count"

with open(sys.argv[1], "r") as input_file:
    with open(sys.argv[2], "w") as output_file:
        for line in input_file:
            print >>output_file, " ".join(field.split(":", 1)[0] for field in line[:-1].split())
