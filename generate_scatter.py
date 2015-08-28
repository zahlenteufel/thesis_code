# execute comparison.py.. put the results in a js file data.js

from predictor import get_text_targets
import os

text, targets = get_text_targets(1, 7)

with open("data.js", "w") as data:
    print >>data, "var dict = [%s];" % ",\n".join("\"'%s', %s, %s\"" % (word.replace("'", ""), [c.replace("'", "") for c in context], [p.replace("'", "") for p in preds]) for word, context, preds, _ in targets)

os.system("""
echo "var data = [" >> data.js
python comparison.py -text_numbers 1 -orders 7 -categories content -dump "[LX,LY,dict[I]]," >> data.js
echo "[]];\ndata.pop();\n" >> data.js
""")
