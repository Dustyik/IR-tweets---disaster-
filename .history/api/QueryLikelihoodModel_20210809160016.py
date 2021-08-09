import math

ALPHA = 0.75
NORMALIZE_PROBABILITY = True

class UnigramLanguageModel:
    def __init__(self, sentences: list, tweets, smoothing=False):

        '''
            sentences: sentences of the dataset
            mode: whether this language model is for the whole corpus/collection or just a single document
            smoothing: add-one smoothing
        '''
        self.sentences = sentences
        self.wordsFrequencyDictionary = self.create_words_frequency_dict(tweets)
        self.totalNumberOfWords = self.calculate_total_no_of_words(self.wordsFrequencyDictionary)
        self.smoothing = smoothing

    def create_words_frequency_dict(self, tweets):
        word_frequency_dictionary = {}
        for sentence in tweets:
            for word in sentence:
                if word_frequency_dictionary.has_key(word):
                    word_frequency_dictionary[word] += 1
                else:
                    word_frequency_dictionary[word] = 1
        return word_frequency_dictionary
    
    def calculate_total_no_of_words(self, wordsFrequencyDictionary):
        values = wordsFrequencyDictionary.values()
        total = sum(values)
        return values
    
    def calculate_unigram_probability(self, word: str):
        value = self.wordsFrequencyDictionary[word]/self.totalNumberOfWords
        return value
    
    def calculate_interpolated_sentence_probability(self, querySentence:list, alpha=ALPHA, normalize_probability=NORMALIZE_PROBABILITY):
        total_score = 1
        for word in querySentence:
            score_of_word = alpha*(self.calculate_unigram_probability(word)) + (1 - alpha)*(collection.calculate_unigram_probability(word))
            total_score *= score_of_word

        if normalize_probability == True:
            return total_score
        else:
            return (math.log(total_score)/math.log(2))

