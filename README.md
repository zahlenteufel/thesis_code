# thesis code

Word prediction in large texts using python and srilm.

# Structure

- **predict_this/**: library
  - **category/**:
  	- **analyze_syntax.py**: Analyze syntax using FreeLing.
  	- **categories_es.py**: Categories Taxonomy for Spanish.
  	- **category.py**: Categories Parsing.
  - **predictor/**:
    - **predictor.py**: Base class for all predictors.
    - **flm_predictor.py**: Predictor for FLMs.
    - **human_predictor.py**: Predictor based on human responses to cloze experiments.
    - **ngram_predictor.py**: Predictor based on n-grams.
    - **unigram_cache_predictor.py**: Predictor based on recent history (cache model).
  - **flm/**:
    - **backoff_graph.py**: FLM Backoff-Graph parsing and visualization.
  	- **flm_specification.py**: FLM Specification parsing.
  - **text/**:
  	- **text.py**: 
  	- **prediction_text.py**: Prediction text used for evaluation.
  	- **prediction_texts.py**: Prediction texts.
  	- **word.py**: Word base class.
  	- **target_word.py**: Derived class for target words.
  	- **texts1234578.csv**: Dataset of prediction texts.

- **corpus/**: scrips for generating the training corpus.

# Dependencies

- FreeLing.
- SRILM.
- python libraries: *more_itertools*, *unidecode*, *peekable*.

# Usage

## Corpus creation

There is a *Makefile* for creating the corpus from the collection of books. It will use the file in *tmp/1_joined_texts.txt* to crete the final file *corpus_cleaned_normalized.txt*.

Example of making a corpus file from the texts in snpanish_books:
```bash
cd corpus
find spanish_books/ -type f -print0 -name "*.txt" | sort -z | xargs -0 cat -- > tmp/1_joined_texts.txt
make
```

If you need to tag it (for example when working with FLMs) you can do it by running *TAG_CORPUS.sh* (?).

## Training

To train a model, once you have a clean, normalized corpus (a unique file, say *corpus_cleaned_normalized.txt*), then you can run:

```bash
ngram-count -text corpus_cleaned_normalized.txt -order 4 -unk -no-eos -lm 4-gram.lm.gz
```

This will create the model *4gram.lm.gz*.

## Calculate correlation of probabilities with Human


## Entropy

## Factored Language Models

> TODO