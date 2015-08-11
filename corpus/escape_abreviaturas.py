import codecs
import sys
import re
import abreviaturas

sys.stdin = codecs.getreader('utf8')(sys.stdin)
sys.stdout = codecs.getwriter('utf8')(sys.stdout)


def capitalize(ss):
    return ".".join(map(lambda s: s[0].upper() + s[1:], ss.split(".")))

dict_reemp = {}
for abreviatura in abreviaturas.abreviaturas:
    dict_reemp[capitalize(abreviatura + ".")] = \
        dict_reemp[abreviatura + "."] = abreviatura.replace(" ", "")

regex_siglas = re.compile(r"([A-Z]\.)+")
regex_enum = re.compile(r"([0-9]+\.)")
regex_abreviaturas = re.compile(r"(^| )(%s)" % "|".join(map(re.escape, dict_reemp.keys())))

for index, line in enumerate(sys.stdin.readlines()):
    print regex_enum.sub(
        lambda mo: "",
        regex_siglas.sub(
            lambda mo: mo.string[mo.start():mo.end()].replace(".", " ")[:-1],
            regex_abreviaturas.sub(
                lambda mo: " " + dict_reemp[mo.string[mo.start():mo.end()].lstrip()],
                line[:-1]
                )
            )
        )
    if index % 1000 == 0:
        sys.stdout.flush()

print >>sys.stderr, "abreviaturas, siglas, and enums escaped"
