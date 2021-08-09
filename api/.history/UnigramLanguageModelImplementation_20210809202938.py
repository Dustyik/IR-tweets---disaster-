import math
from IPython.display import display
import sys
from BM25implementation import QueryParsers


ALPHA = 0.75
NORMALIZE_PROBABILITY = True

class UnigramLanguageModel:
    def __init__(self, tweets_data): #tweets is a pandas dataframe
        self.tweets_data = tweets_data
        self.wordsCollectionFrequencyDictionary = self.create_words_frequency_dict(tweets_data)

    def create_words_frequency_dict(self, tweets_data, collection = True):
        word_frequency_dictionary = {}
        
        if collection:
            tweets = tweets_data.clean_text.tolist()
        
            for sentence in tweets:
                sentence_list = list(sentence.split(" "))
                for word in sentence_list:
                    if word in word_frequency_dictionary:
                        word_frequency_dictionary[word] += 1
                    else:
                        word_frequency_dictionary[word] = 1
        else:
            for word in tweets_data:
                if word in word_frequency_dictionary:
                    word_frequency_dictionary[word] += 1
                else:
                    word_frequency_dictionary[word] = 1
        return word_frequency_dictionary
    
    def calculate_total_no_of_words(self, wordsCollectionFrequencyDictionary):
        values = wordsCollectionFrequencyDictionary.values()
        total = sum(values)
        return total
    
    def calculate_unigram_probability(self, word: str, wordCollectionFrequencyDictionary):
        totalNumberOfWords = self.calculate_total_no_of_words(wordCollectionFrequencyDictionary)
        try:
            value = wordCollectionFrequencyDictionary[word]/totalNumberOfWords
        except KeyError as ke:
            value = 1/totalNumberOfWords #add one smoothing for documents
            
        #print (word, value)
        return value
    
    def calculate_interpolated_sentence_probability(self, querySentenceList:list, document, alpha=ALPHA, normalize_probability=NORMALIZE_PROBABILITY):
        total_score = 1
        documentListOfStrings = list(document.split(" "))
        documentWordFrequencyDictionary = self.create_words_frequency_dict(documentListOfStrings, collection = False)
        for word in querySentenceList:
            score_of_word = alpha*(self.calculate_unigram_probability(word, documentWordFrequencyDictionary)) + (1 - alpha)*(self.calculate_unigram_probability(word, self.wordsCollectionFrequencyDictionary))
            total_score *= score_of_word
        if normalize_probability == True:
            return total_score
        else:
            return (math.log(total_score)/math.log(2))
        
    def getQueryLikelihoodModelScore(self, querySentence:list):
        querySentenceList = QueryParsers(querySentence).query
        self.tweets_data["QueryLikelihoodModelScore"] = self.tweets_data.apply(lambda row: self.calculate_interpolated_sentence_probability(querySentenceList, row.clean_text), axis = 1)
        self.tweets_data.sort_values(by='QueryLikelihoodModelScore',ascending=False,inplace=True)
        return self.tweets_data

