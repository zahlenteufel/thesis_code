ccyellow=$(shell echo "\033[0;33m")
ccred=$(shell echo "\033[0;31m")
ccend=$(shell echo "\033[0m")
log=@echo "$(ccyellow)$(shell date): $(1)$(ccend)"
# error=rm -f $@
# ; @echo "$(ccred)$(shell date): ERROR! $(ccend)")


.DELETE_ON_ERROR: tmp/1_joined_texts.txt tmp/2_cleaned_characters.txt tmp/3_abreviaturas_fixed.txt tmp/4_fixed_broken_words.txt tmp/5_removed_emails_and_blanks.txt tmp/6_removed_parenthesis.txt corpus_cleaned.txt corpus_cleaned_normalized.txt tmp/factored_corpus_WGNCP.txt factored_corpus_WGNCPL.txt vocabulary.txt

.PHONY: clean all tagged_corpus

all: corpus_cleaned_normalized.txt vocabulary.txt

tagged_corpus: factored_corpus_WGNCPL.txt

clean:
	rm -f tmp/2_cleaned_characters.txt
	rm -f tmp/3_abreviaturas_fixed.txt
	rm -f tmp/4_fixed_broken_words.txt
	rm -f tmp/5_removed_emails_and_blanks.txt
	rm -f tmp/6_removed_parenthesis.txt


tmp/1_joined_texts.txt:
	$(call log, joining texts)
	mkdir -p tmp
	find spanish_books -type f -print0 -name "*" | \
		sort -z | \
		xargs -0 cat -- > \
		$@

tmp/2_cleaned_characters.txt: tmp/1_joined_texts.txt
	$(call log, cleaning characters)
	scripts/clean_characters.sh $< $@

tmp/3_abreviaturas_fixed.txt: tmp/2_cleaned_characters.txt
	$(call log, fix abreviaturas siglas enums)
	python scripts/escape_abreviaturas.py < $< > $@

tmp/4_fixed_broken_words.txt: tmp/3_abreviaturas_fixed.txt
	$(call log, fix broken words)
	python scripts/fix_broken_words.py < $< > $@

tmp/5_removed_emails_and_blanks.txt: tmp/4_fixed_broken_words.txt
	$(call log, delete links emails blank_lines..)
	scripts/delete_links_emails.sh $< $@

tmp/6_removed_parenthesis.txt: tmp/5_removed_emails_and_blanks.txt
	$(call log, handle parenthesis brackets)
	python scripts/handle_parenthesis_brackets.py < $< > $@

corpus_cleaned.txt: tmp/6_removed_parenthesis.txt
	$(call log, delete lines with weird characters)
	scripts/delete_lines_with_weird_characters.sh $< $@

corpus_cleaned_normalized.txt: corpus_cleaned.txt
	$(call log, normalize corpus)
	python scripts/normalize_corpus.py

vocabulary.txt: corpus_cleaned_normalized.txt
	$(call log, vocabulary)
	tr " " "\n" < corpus_cleaned_normalized.txt | sed '/^\s*$$/d' | sort -u > vocabulary.txt

tmp/factored_corpus_WGNCP.txt: corpus_cleaned.txt
	$(call log, tag corpus)
	scripts/tag_corpus.sh

factored_corpus_WGNCPL.txt: tmp/factored_corpus_WGNCP.txt
	$(call log, merge lemma factor)
	python scripts/factors_zip_lemmas.py
