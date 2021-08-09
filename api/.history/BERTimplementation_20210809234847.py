from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
from tfidfImplementation import *

#First segment involves retrieving K documents with tf-idf
#Second segment involves reranking them with a BERT encoder
K = 200

class BERTmoddel:
    def __init__(self, tweets_data):
        self.tweets_data = tweets_data
        self.cosineSimilarity = CosineSimilarity(tweets_data, return_size=K)
        self.BERT_model = SentenceTransformer('bert-base-nli-mean-tokens')
    
    def tfidf_retrieve_K_tweets(self, article_id, article_title):
        topKResults = self.cosineSimilarity.query(query_id=article_id, query_text=article_title)
        

    def return_BERT_query(self, article_id, article_title):
        sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
        topKResults = self.tfidf_retrieve_K_tweets(article_id, article_title)
        #document_embeddings = self.BERT_model.encode(topKResults['clean_text'])
        query_vector_embedding = self.BERT_model.encode(article_title)
        topKResults['embedding'] = topKResults.apply(lambda row: self.BERT_model.encode(row.clean_text), axis = 1)
        topKResults["BERT_similarity"] = topKResults.apply(lambda row: cosine_similarity(np.array(query_vector_embedding).reshape(1, -1), np.array(row.embedding).reshape(1, -1)).item())
        tweets_data.sort_values(by='similarity',ascending=False,inplace=True)
        print (pairwise_similarities)

    #most_similar(0,pairwise_similarities,'Cosine Similarity')
    #most_similar(0,pairwise_differences,'Euclidean Distance')

'''
def most_similar(doc_id,similarity_matrix,matrix):
    print (f'Document: {documents_df.iloc[doc_id]["documents"]}')
    print ('\n')
    print ('Similar Documents:')
    if matrix=='Cosine Similarity':
        similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
    elif matrix=='Euclidean Distance':
        similar_ix=np.argsort(similarity_matrix[doc_id])
    for ix in similar_ix:
        if ix==doc_id:
            continue
        print('\n')
        print (f'Document: {documents_df.iloc[ix]["documents"]}')
        print (f'{matrix} : {similarity_matrix[doc_id][ix]}')
'''