from predict_this.text.prediction_text import PredictionText
from predict_this.text.word import Word
from predict_this.text.word import to_ascii
from predict_this.category.analyze_syntax import analyze
from itertools import izip
import io
import sys


def get_raw_prediction_text(index):
	prediction_text = PredictionText(index)
	raw_text = ""
	for line in prediction_text.lines():
		raw_text += " ".join(map(Word.original_word, line[1:])) + "\n"
	return raw_text


def get_text_analysis(index):
	print "analyzing text %d with freeling.. (this may take a while, please wait)" % index
	for analyzed_line in analyze(get_raw_prediction_text(index).replace("%", "")):
		yield analyzed_line


analyzed_words = [word_analysis for i in (1, 2, 3, 4, 5, 7, 8) for line in get_text_analysis(i) for word_analysis in line]
# # create a new csv, with category replaced with this..

def write_row(file, fields, separator=","):
	file.write(separator.join(fields) + "\n")

with io.open("predict_this/text/texts1234578.csv", "r", encoding="utf-8") as csvfile:
	with io.open("predict_this/text/texts1234578_2.csv", "w", encoding="utf-8") as new_csvfile:
		header = csvfile.next()[:-1].split(",")
		tag_index = header.index("tag")
		lemma_index = header.index("lemma")
		write_row(new_csvfile, header)
		i = 1
		for line, analyzed in izip(csvfile, analyzed_words):
			row = line[:-1].split(",")
			if row[0].replace("%", "") != analyzed[0]:
				print "line %d. %s != %s" % (i, row[0], analyzed[0])
				sys.exit(1)
			row[tag_index] = analyzed[2].split("+")[0]
			row[lemma_index] = to_ascii(analyzed[1].split("+")[0])
			write_row(new_csvfile, row)
			i += 1
