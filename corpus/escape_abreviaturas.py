import re
import abreviaturas
import io
import sys

stdin = io.open(sys.stdin.fileno(), "r", encoding="utf-8")
stdout = io.open(sys.stdout.fileno(), "w", encoding="utf-8")


def capitalize(ss):
    return ".".join(map(lambda s: s[0].upper() + s[1:] if s else "", ss.split(".")))


# TODO: lidiar con 4to.. 5to..

dict_reemp = {}
for abreviatura in abreviaturas.abreviaturas:
    dict_reemp[capitalize(abreviatura.replace(" ", ".") + ".")] = \
        dict_reemp[abreviatura + "."] = abreviatura

regex_siglas = re.compile(r"([A-Z]\.)+")
regex_enum = re.compile(r"([0-9]+\.)")
regex_abreviaturas = re.compile(r"(^| )(%s)" % "|".join(map(re.escape, dict_reemp.keys())))

for index, line in enumerate(stdin):
    stdout.write(regex_enum.sub(
        lambda mo: "",
        regex_siglas.sub(
            lambda mo: mo.string[mo.start():mo.end()].replace(".", " ")[:-1],
            regex_abreviaturas.sub(
                lambda mo: " " + dict_reemp[mo.string[mo.start():mo.end()].lstrip()],
                line[:-1]
                )
            )
        ) + "\n"
    )
    if index % 1000 == 0:
        stdout.flush()
