from Word2Vecimplementation import Word2VecModel
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from BM25implementation import *
from IPython.display import display
from tfidfImplementation import *

RETURN_SIZE = 30

'''
Functions to write:
1. tf-idf with cosine sim/Euclidean distance
- represent terms in each document with its tf-idf weights, 
2. VSM with cosine sim/Euclidean distance
3. BIM
4. BM25
5. BERT

'''

titles_file_path = r"D:\Desktop\IR_term_8\IR-tweets---disaster-\article_titles.csv"
tweets_file_path = r"D:\Desktop\IR_term_8\IR-tweets---disaster-\tweets_data_stemmed.csv"

SEARCH_MODELS = {
	"tfcs": "Tf-idf w Cosine Sim", 
	"tfed": "Tf-idf w Euclidean Dist",
	"BM25": "Okapi-BM25",
	"W2Vcs": "Word2Vec w Cosine Similarity",
	"W2Ved": "Word2Vec w Euclidean Distance"
	}

tweet_col_names = ["article_id","tweet_id", "relevance", "tweet", "clean_text"]

def returnTweetsBasedOnSearchModel(dataProcessor, articleId, articleTitle, searchModel):
	#accepts a search model, article title, and article id, returns n most relevant results	
	if searchModel == SEARCH_MODELS["tfcs"]:
		return dataProcessor.cosineSimilarity.query(articleId, articleTitle)
	if searchModel == SEARCH_MODELS["tfed"]:
		return dataProcessor.euclideanDistance.query(articleId, articleTitle)
	if searchModel == SEARCH_MODELS["BM25"]:
		rankedDocs = dataProcessor.BM25query(articleId, articleTitle)
	if searchModel == SEARCH_MODELS["W2Vcs"]:
		rankedDocs =  dataProcessor.Word2Vecquery(articleId, articleTitle, SEARCH_MODELS["W2Vcs"])
	if searchModel == SEARCH_MODELS["W2Ved"]:
		rankedDocs = dataProcessor.Word2Vecquery(articleId, articleTitle, SEARCH_MODELS["W2Ved"])

	rankedDocs = rankedDocs.apply(lambda row:checkIfArticleIdMatchesQueryId(row, articleId), axis=1)
	return rankedDocs

def checkIfArticleIdMatchesQueryId(pandasRow, articleId):
	if pandasRow.article_id != articleId:
		pandasRow.relevance_score = 0
	return pandasRow

class DataProcessor:
	def __init__(self):
		self.titles_data = pd.read_csv(titles_file_path) 
		self.tweets_data = pd.read_csv(tweets_file_path) 
		self.titles_data = self.titles_data.dropna()
		self.tweets_data = self.tweets_data.dropna()
		self.cosineSimilarity = CosineSimilarity(self.titles_data, self.tweets_data)
		self.euclideanDistance = EuclideanDistance(self.titles_data, self.tweets_data)	
		self.word2VecModel = Word2VecModel(self.tweets_data)
		print ("Data Processor up and ready...")

	def Word2Vecquery(self, articleId, articleTitle, type = SEARCH_MODELS["W2Vcs"]):	
		rankedDocs = self.word2VecModel.return_most_significant_tweets(articleTitle, type = type)
		return rankedDocs[:RETURN_SIZE]

	def BM25query(self, articleId, articleTitle):
		tweet_col_names = ["related_article","tweet_id", "relevance", "text", "clean_text"]
		query_list = QueryParsers(articleTitle).query
		bM25Class = BM25Class(self.tweets_data, query_list)
		rankedDocs = bM25Class.rankedDocs[:RETURN_SIZE]
		return_dataFrame = pd.DataFrame()
		for dataPoint in rankedDocs:
			tweetId = dataPoint[0]
			for index, row in self.tweets_data.iterrows():
				if (row.tweet_id == tweetId):
					return_dataFrame = return_dataFrame.append(row)
					continue
		#return_dataFrame = return_dataFrame.drop(["clean_text"], axis = 1)
		return_dataFrame = return_dataFrame.reset_index()
		return return_dataFrame


#dataProcessor = DataProcessor()
test_title_1 = "Company Update (NYSE:MET): MetLife Increases Share Repurchase Authorization to $1 Billion" 
test_title_1_id = "8b31120e-d654-45b4-a5df-8fef674339d8"
test_title_2 = "Perkins Eastman Celebrates Groundbreaking of Clark-Lindsey's Small Homes for Dementia Care"
test_title_2_id = "32023021-1141-4832-9939-c8442d505b34"
#display(dataProcessor.BM25query("123", test_title_1))

dataProcessor = DataProcessor()
ret = returnTweetsBasedOnSearchModel(dataProcessor, test_title_1_id, test_title_1, "Word2Vec w Cosine Similarity")
