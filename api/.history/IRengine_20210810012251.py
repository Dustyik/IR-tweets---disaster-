from word2Vecimplementation import *
from BM25implementation import *
from tfidfImplementation import *
from queryLikelihoodModelImplementation import *
from BERTimplementation import *
from utils import QueryParsers
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
	"W2Ved": "Word2Vec w Euclidean Distance",
	"QLM": "Query Likelihood Model",
	"BERT": "BERT w tfidf",
	}

class DataProcessor:
	def __init__(self):
		self.titles_data = pd.read_csv(titles_file_path) 
		self.tweets_data = pd.read_csv(tweets_file_path) 
		self.titles_data = self.titles_data.dropna()
		self.tweets_data = self.tweets_data.dropna()[:30]
		self.cosineSimilarity = CosineSimilarity(self.tweets_data, return_size = RETURN_SIZE)
		self.euclideanDistance = EuclideanDistance(self.tweets_data, return_size = RETURN_SIZE)	
		self.word2VecModel = Word2VecModel(self.tweets_data)
		self.queryLikelihoodModel = QueryLikelihoodModel(self.tweets_data)
		#self.BERTmodel = BERTmodel(self.tweets_data)
		print ("Data Processor up and ready...")

	def returnTweetsBasedOnSearchModel(self, articleId, articleTitle, searchModel):
		#accepts a search model, article title, and article id, returns n most relevant results	
		if searchModel == SEARCH_MODELS["tfcs"]:
			rankedDocs = self.cosineSimilarity.query(articleId, articleTitle)
		if searchModel == SEARCH_MODELS["tfed"]:
			rankedDocs = self.euclideanDistance.query(articleId, articleTitle)
		if searchModel == SEARCH_MODELS["BM25"]:
			rankedDocs = self.BM25query(articleId, articleTitle)
		if searchModel == SEARCH_MODELS["W2Vcs"]:
			rankedDocs =  self.Word2Vecquery(articleId, articleTitle, SEARCH_MODELS["W2Vcs"])
		if searchModel == SEARCH_MODELS["W2Ved"]:
			rankedDocs = self.Word2Vecquery(articleId, articleTitle, SEARCH_MODELS["W2Ved"])
		if searchModel == SEARCH_MODELS["QLM"]:
			rankedDocs = self.queryLikelihoodModelQuery(articleId, articleTitle)
		if searchModel == SEARCH_MODELS["BERT"]:
			rankedDocs = self.BERTquery(articleId, articleTitle)

		rankedDocs = rankedDocs.reset_index(drop = True)
		rankedDocs = rankedDocs.apply(lambda row: self.checkIfArticleIdMatchesQueryId(row, articleId), axis=1)
		#print (rankedDocs.relevance_score)
		display(rankedDocs)
		return rankedDocs

	def checkIfArticleIdMatchesQueryId(self, pandasRow, articleId):
		print (articleId, pandasRow.articleId)
		if pandasRow.article_id != articleId:
			pandasRow.relevance_score = 0
		return pandasRow

	def BERTquery(self, articleId, articleTitle):
		rankedDocs = self.BERTmodel.return_BERT_query(articleId, articleTitle)
		return rankedDocs

	def queryLikelihoodModelQuery(self, articleId, articleTitle):
		rankedDocs = self.queryLikelihoodModel.getQueryLikelihoodModelScore(articleTitle)
		return rankedDocs[:RETURN_SIZE]

	def Word2Vecquery(self, articleId, articleTitle, type = SEARCH_MODELS["W2Vcs"]):	
		rankedDocs = self.word2VecModel.return_most_significant_tweets(articleTitle, type = type)
		return rankedDocs[:RETURN_SIZE]

	def BM25query(self, articleId, articleTitle):
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
		return return_dataFrame

#dataProcessor = DataProcessor()
test_title_1 = "Company Update (NYSE:MET): MetLife Increases Share Repurchase Authorization to $1 Billion" 
test_title_1_id = "8b31120e-d654-45b4-a5df-8fef674339d8"
test_title_2 = "Perkins Eastman Celebrates Groundbreaking of Clark-Lindsey's Small Homes for Dementia Care"
test_title_2_id = "32023021-1141-4832-9939-c8442d505b34"
#display(dataProcessor.BM25query("123", test_title_1))

#dataProcessor = DataProcessor()
#display(dataProcessor.BERTquery(test_title_1_id, test_title_1))
#dataProcessor.returnTweetsBasedOnSearchModel(test_title_1_id, test_title_1, "Query Likelihood Model")