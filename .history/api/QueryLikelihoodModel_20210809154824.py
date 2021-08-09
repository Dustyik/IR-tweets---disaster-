import re
import math
import numpy as np

UNK = None
SENTENCE_START = "<s>"
SENTENCE_END = "</s>"

ALPHA = 0.75
NORMALIZE_PROBABILITY = True

class UnigramLanguageModel:
    def __init__(self, sentences: list, mode="collection", smoothing=False):

        '''
            sentences: sentences of the dataset
            mode: whether this language model is for the whole corpus/collection or just a single document
            smoothing: add-one smoothing
        '''
        self.sentences = sentences
        self.mode = mode

        #for add one smoothing
        self.smoothing = smoothing

        
    def calculate_unigram_probability(self, word: str):
        '''
            calculate unigram probability of a word
        '''
        total_number_of_words = 0
        frequency_of_word = 0
        for sentence in self.sentences:
            for word_in_sentence in sentence:
                if word_in_sentence != SENTENCE_START and SENTENCE_END:
                    if word_in_sentence == word:
                        frequency_of_word += 1
                    total_number_of_words += 1
        
        if (self.smoothing and frequency_of_word == 0):
            frequency_of_word = 1

        return (frequency_of_word/total_number_of_words)
    
def calculate_interpolated_sentence_probability(sentence:list, doc:UnigramLanguageModel, collection: UnigramLanguageModel, alpha=ALPHA, normalize_probability=NORMALIZE_PROBABILITY):
    '''
        calculate interpolated sentence/query probability using both sentence and collection unigram models.
        sentence: input sentence/query
        doc: unigram language model a doc. HINT: this can be an instance of the UnigramLanguageModel class
        collection: unigram language model a collection. HINT: this can be an instance of the UnigramLanguageModel class
        alpha: the hyperparameter to combine the two probability scores coming from the document and collection language models.
        normalize_probability: If true then log of probability is not computed. Otherwise take log2 of the probability score.
    '''
    total_score = 1
    for word in sentence:
        if word != SENTENCE_START and word != SENTENCE_END:
            score_of_word = alpha*(doc.calculate_unigram_probability(word)) + (1 - alpha)*(collection.calculate_unigram_probability(word))
            total_score *= score_of_word

    if normalize_probability == True:
        return total_score
    else:
        return (math.log(total_score)/math.log(2))

