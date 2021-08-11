from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from tfidfImplementation import *
from utils import QueryParsers


#First segment involves retrieving K documents with tf-idf
#Second segment involves reranking them with a BERT encoder
K = 100

#BERT_MODEL = 'bert-base-nli-mean-tokens'
BERT_MODEL = "paraphrase-multilingual-mpnet-base-v2"

class BERTmodel:
    def __init__(self, tweets_data):
        self.tweets_data = tweets_data
        self.cosineSimilarity = CosineSimilarity(tweets_data)
        self.BERT_model = SentenceTransformer(BERT_MODEL)
    
    def tfidf_retrieve_K_tweets(self, article_id, article_title):
        topKResults = self.cosineSimilarity.query(query_id=article_id, query_text=article_title)[:K]
        return topKResults
        
    def return_BERT_query(self, article_id, article_title):
        topKResults = self.tfidf_retrieve_K_tweets(article_id, article_title)
        queryStemmed = " ".join(QueryParsers(article_title).query)
        query_vector_embedding = self.BERT_model.encode(queryStemmed)
        topKResults['vector_embedding'] = topKResults.apply(lambda row: self.BERT_model.encode(row.clean_text), axis = 1)
        topKResults["BERT_similarity"] = topKResults.apply(lambda row: cosine_similarity(np.array(query_vector_embedding).reshape(1, -1), np.array(row.vector_embedding).reshape(1, -1)).item(), axis = 1)
        topKResults.sort_values(by='BERT_similarity',ascending=False,inplace=True)
        return topKResults
