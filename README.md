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

There is a *Makefile* for creating the corpus from the collection of books. It will use the files in *corpus/spanish_books/* to create the final files *corpus_cleaned.txt* and *corpus_cleaned_normalized.txt* and *vocabulary.txt*. The first one is used for the tagging process and the second one for the predictions using n-grams, the third file is the vocabulary of *corpus_cleaned_normalized.txt* and it's used for the entropy calculations.

For creating the corpus:
```bash
cd corpus
make
```

For creating the tagged corpus execute this Makefile with the target *tagged_corpus*: 
```bash
make tagged_corpus
```

## Training

To train the n-grams models from the corpus (*corpus/corpus_cleaned_normalized.txt*) execute

```bash
python train_ngrams.py
```

This will generate the files *models/1-gram.lm.gz* through *models/4-gram.lm.gz*.

## Calculating predictions

Once you have the models trained you can execute *predictor_tables.py*. For example if we want the predicitons of the 2-gram and 3-gram for the texts 1, 2 and 3, and store it in a file named TABLE then you can execute:

```bash
python predictor_tables.py -ngram_predictor_orders 2 3 text_numbers 1 2 3 > TABLE
```

This will store it in a csv file, which you can use it to plot the correlations with the predictions of the humans (cloze):

```bash
python analyze_table.py < TABLE
```

Many of these scripts have a flag for a description of the parameters using the flag *-h*.

## Entropy

Yo can use the *predictor_tables.py* script with the flag *-entropy* and it will output the entropy instead of the probabilities (Now this works only for HumanPredictor, because for n-grams it takes too long).

For calculating the entropy of n-grams (without or without cache):

- First you have to obtain the conditional probability distribution at the targets of a text (e.g. text number 1):

```bash
python print_distributions -text_number 1 -ngram_predictor_order 4 -output_filename DIST_4gram_text1
```

- Then you can use the ** script for calculating the entropy at each target:

```bash
python calculate_entropy_from_conditional_distributions -filename DIST_4gram_text1
```

This will output for each target the target word, the entropy, the entropy using only the top 10 predicitions and then the top 10 predictions.

- If you want to calculate the entropy interpolating with you can do it with the appropiate flags:

```bash
python calculate_entropy_from_conditional_distributions -filename DIST_4gram_text1 -calculate_with_cache -cache_text_number 1 -cache_lambda 0.22
```

## Factored Language Models

### Training

After you have a tagged corpus (*corpus/factored_corpus_WGNCPL.txt*), you can train all the models in *flm_models* executing:

```bash
python train_all_flm_models.py
```

And this will generate a script called *train_all_models.sh*, which you can edit at your convenience and then execute it:

```bash
./train_all_flm_models.sh
```

### Calculating predictions

If you want to calculate the predictions using the model in *flm_models/bigramWN.flm* for the texts 1, 2 and 3, and store it in a file named TABLE then you can execute:

```bash
python predictor_tables.py -flm_model_filenames flm_models/bigramWN.flm text_numbers 1 2 3 > TABLE
```

An this will generate the predictions as in the n-gram models case.
