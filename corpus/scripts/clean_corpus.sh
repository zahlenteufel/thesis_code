#!/usr/bin/env bash

set -e

echo "joining texts"
find libros_txt -type f -print0 -name "*" | sort -z | xargs -0 cat -- > tmp/corpus_1.txt

echo "cleaning some characters"
sed -e "s/ – //g" tmp/corpus_1.txt |
	sed -e "s/ ρ //g" |
	sed -e "s/γη/\n/g" |
	sed -e "s/ \/ /\n/g" |
	python clean_characters.py > tmp/corpus_2.txt

echo "fix abreviaturas, siglas, enums"
python escape_abreviaturas.py < tmp/corpus_2.txt > tmp/corpus_3.txt

echo "fix broken words"
python fix_broken_words.py < tmp/corpus_3.txt > tmp/corpus_4.txt

echo "delete links, emails, blank lines.."
sed -E "/(www|http|@|©|®)/d" tmp/corpus_4.txt | # delete lines with links, emails, copyroghts
	sed -e "s/^\s*//" |                         # delete trailing spaces
	sed -e "s/\s*$//" |                         # delete leading spaces
	sed -e "/^[0-9]+$/d" |                      # delete only number line
	sed -E "s/\s+/ /g" |                        # collapse multiple spaces
	sed -e "/^$/d" |                            # delete empty lines
	sed -e "s/“/«/g" |                          # unify characters for easier processing later
	sed -e "s/”/»/g" |
	sed -E "s/\"([^\"]*)\"/«\1»/g" > tmp/corpus_5.txt 

echo "handle parenthesis brackets"
python handle_parenthesis_brackets.py < tmp/corpus_5.txt > tmp/corpus_6.txt

echo "break lines, delete lines with weird characters"
sed -e "s/[¡\!¿\?\.,:;—]/\n/g" < tmp/corpus_6.txt |
	sed -e "/[^A-Za-záéíóúÁÉÍÓÚñÑüÜ0-9 ]/d" |
	sed -e "s/^\s*//" |                         # delete trailing spaces
	sed -e "s/\s*$//" |                         # delete leading spaces
	sed -e "/^[0-9]+$/d" |                      # delete only number line
	sed -E "s/\s+/ /g" |                        # collapse multiple spaces
	sed -e "/^$/d" > tmp/corpus_cleaned.txt     # delete empty lines
