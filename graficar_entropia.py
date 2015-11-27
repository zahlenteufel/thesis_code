import matplotlib.pyplot as plt
from scipy.special import logit
import argparse
import sys


def transpose(table):
    return map(list, zip(*table))


def get_lines(file):
    return map(lambda l: l[:-1].split(","), file)


def parse_csv(file):
    lines = get_lines(file)
    header, rows = lines[0], lines[1:]
    rows = map(lambda row: map(float, row), rows)
    return dict(zip(header, transpose(rows)))


def plot_cols(d, name1, name2, logit_scale=False, output_file=None):
    x = d[name1]
    y = d[name2]
    plt.xlabel(name1 + ("(logit)" if logit_scale else ""))
    plt.ylabel(name2 + ("(logit)" if logit_scale else ""))
    plot(x, y, logit_scale, output_file)


def plot(x, y, logit_scale=False, output_file=None):
    if logit_scale:
        x = logit(x)
        y = logit(y)
    plt.scatter(x, y, alpha=0.05)
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()
        plt.close()


def interpolate(alpha, xs, ys):
    return [x * alpha + y * (1 - alpha) for x, y in zip(xs, ys)]


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Graficar scatter plots con las columnas de un csv")
    parser.add_argument("-x")
    parser.add_argument("-y")
    parser.add_argument("-o", help="output plot file")
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    d = parse_csv(sys.stdin)
    # d["prob4gram+cache"] = interpolate(arguments.cache_lambda, d["prob_cache"], d["prob_4gram"])
    if arguments.x not in d:
        print "error, '%s' not in columns" % arguments.x
        print "columns available:"
        print "  - " + '\n  - '.join(d.keys())
        sys.exit(1)
    if arguments.y not in d:
        print "error, '%s' not in columns  " % arguments.y
        print "columns available:"
        print "  - " + '\n  - '.join(d.keys())
        sys.exit(1)
    plot_cols(d, arguments.x, arguments.y, output_file=arguments.o)
