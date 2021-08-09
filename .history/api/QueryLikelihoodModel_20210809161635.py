import math
from IPython.display import display


ALPHA = 0.75
NORMALIZE_PROBABILITY = True

class UnigramLanguageModel:
    def __init__(self, tweets_data, smoothing=False): #tweets is a pandas dataframe
        self.tweets_data = tweets_data
        self.wordsCollectionFrequencyDictionary = self.create_words_frequency_dict(tweets_data)

    def create_words_frequency_dict(self, tweets_data, collection = True):
        tweets = tweets_data.clean_text.tolist()
        word_frequency_dictionary = {}
        
        if (collection):
            for sentence in tweets:
                for word in sentence:
                    if word_frequency_dictionary.has_key(word):
                        word_frequency_dictionary[word] += 1
                    else:
                        word_frequency_dictionary[word] = 1
        else:
            for word in tweets:
                if word_frequency_dictionary.has_key(word):
                    word_frequency_dictionary[word] += 1
                else:
                    word_frequency_dictionary[word] = 1
            
        return word_frequency_dictionary
    
    def calculate_total_no_of_words(self, wordsCollectionFrequencyDictionary):
        values = wordsCollectionFrequencyDictionary.values()
        total = sum(values)
        return values
    
    def calculate_unigram_probability(self, word: str, wordCollectionFrequencyDictionary):
        totalNumberOfWords = self.calculate_total_no_of_words(wordCollectionFrequencyDictionary)
        value = wordCollectionFrequencyDictionary[word]/totalNumberOfWords
        return value
    
    def calculate_interpolated_sentence_probability(self, querySentence:list, document, alpha=ALPHA, normalize_probability=NORMALIZE_PROBABILITY):
        total_score = 1
        for word in querySentence:
            score_of_word = alpha*(self.calculate_unigram_probability(word)) + (1 - alpha)*(self.calculate_unigram_probability(word, self.wordsCollectionFrequencyDictionary))
            total_score *= score_of_word

        if normalize_probability == True:
            return total_score
        else:
            return (math.log(total_score)/math.log(2))
        
    def getQueryLikelihoodModelScore(self, querySentence:list):
        self.tweets_data["QueryLikelihoodModelScore"] = self.tweets_data.apply(lambda row: self.calculate_interpolated_sentence_probability(querySentence, row.clean_text))
        disp
        
        return 

