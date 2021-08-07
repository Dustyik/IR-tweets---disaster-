from Word2Vecimplementation import Word2VecModel
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
from BM25implementation import *
from IPython.display import display

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

	return rankedDocs

def checkIfArticleIdMatchesQueryId(pandasRow, articleId):
    if pandasRow.article_id != articleId:
        row.relevance_score = 0
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

class CosineSimilarity:
	def __init__(self, titles, tweets, type='tfidf'):
		self.titles = titles  #contains titles data
		self.tweets = tweets #contains tweets data
		self.vectorizer = self.change_matrix_type(type)

	def get_result(self, return_size = RETURN_SIZE):
		cos_sim = cosine_similarity(self.matrix, self.matrix)
		top_ind = np.flip(np.argsort(cos_sim[0]))[:return_size]
		top_id = [list(self.matrix.index)[i] for i in top_ind]
		self.result = []
		for i in top_id:
			filt = self.tweets[self.tweets.tweet==i]
			for ind, r in filt.iterrows():
				rel = r['relevance_score']
				text = r['tweet']
				id = r["tweet_id"]
				related = r['article_id']
				if related != self.query_id:
					rel = 0
				self.result.append({'tweet_id':id, 'tweet': text, 'article_id':related, "relevance_score": rel})

	def query(self, query_id, query_text, return_size=RETURN_SIZE):
		self.query_id = query_id
		term_doc = self.vectorizer.fit_transform([query_text]+list(self.tweets.clean_text)) #returns document term matrix
		ind = ["query"] + list(self.tweets.tweet)
		self.matrix = pd.DataFrame(term_doc.toarray(), columns=self.vectorizer.get_feature_names(), index=ind) #indexes are the tweets, columns is the entire vocab
		self.get_result(return_size)
		return pd.DataFrame(self.result)

	def change_matrix_type(self, type):
		if type == 'tfidf':
			return TfidfVectorizer() 
		elif type == 'dt':
			return CountVectorizer() #transforms the entire word matrix into a set of vectors
		else:
			print('Type is invalid')

	def get_matrix(self):
		return self.matrix

class EuclideanDistance:
	def __init__(self, titles, tweets, type='tfidf'):
		self.titles = titles  #contains titles data
		self.tweets = tweets #contains tweets data
		self.vectorizer = self.change_matrix_type(type)

	def get_result(self, return_size = RETURN_SIZE):
		euclidean = euclidean_distances(self.matrix.values[1:], [self.matrix.values[0]])
		top_ind = np.argsort(euclidean.T[0])[:return_size]
		top_id = [list(self.matrix.index)[i] for i in top_ind]
		self.result = []
		for i in top_id:
			filt = self.tweets[self.tweets.tweet==i]
			for ind, r in filt.iterrows():
				rel = r['relevance_score']
				text = r['tweet']
				id = r["tweet_id"]
				related = r['article_id']
				if related != self.query_id:
					rel = 0
				self.result.append({'tweet_id':id, 'tweet': text, 'article_id':related, "relevance_score": rel})

	def query(self, query_id, query_text, return_size=RETURN_SIZE):
		self.query_id = query_id
		term_doc = self.vectorizer.fit_transform([query_text]+list(self.tweets.clean_text))
		ind = ['query'] + list(self.tweets.tweet)
		self.matrix = pd.DataFrame(term_doc.toarray(), columns=self.vectorizer.get_feature_names(), index=ind)
		self.get_result(return_size)
		return pd.DataFrame(self.result)

	def change_matrix_type(self, type):
		if type == 'tfidf':
			return TfidfVectorizer() 
		elif type == 'dt':
			return CountVectorizer()
		else:
			print('Type is invalid')

	def get_matrix(self):
		return self.matrix


#dataProcessor = DataProcessor()
test_title_1 = "Company Update (NYSE:MET): MetLife Increases Share Repurchase Authorization to $1 Billion"
test_title_2 = "Perkins Eastman Celebrates Groundbreaking of Clark-Lindsey's Small Homes for Dementia Care"
#display(dataProcessor.BM25query("123", test_title_1))

#dataProcessor = DataProcessor()
#returnTweetsBasedOnSearchModel(dataProcessor, "testId", test_title_1, "Word2Vec w Cosine Similarity")
