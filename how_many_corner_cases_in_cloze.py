from predict_this.text.prediction_texts import PredictionTexts

target_words = list(PredictionTexts([1, 2, 3, 4, 5, 7, 8]).target_words())

not_guessed = sum(1 for target_word in target_words if target_word.was_not_guessed())

everyone_guessed = sum(1 for target_word in target_words if target_word.everyone_guessed())

total = float(len(target_words))
print "total:", total
print "not guessed: %d (%.2f%%)" % (not_guessed, 100 * not_guessed / total)
print "everyone guessed: %d (%.2f%%)" % (everyone_guessed, 100 * everyone_guessed / total)
