# TODO: do a Makefile of this :P

find libros_txt -type f -print0 -name "*" | sort -z | xargs -0 cat -- > tmp_corpus.txt

# put each sentence in a separate line (be careful with abreviaturas)



# do a version in ascii
# --> corpus_ascii.txt