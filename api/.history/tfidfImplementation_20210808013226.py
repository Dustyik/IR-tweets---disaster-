import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

class CosineSimilarity:
    def __init__(self, titles, tweets, type='tfidf', return_size = 30):
        self.titles = titles  #contains titles data
        self.tweets = tweets #contains tweets data
        self.vectorizer = self.change_matrix_type(type)
        self.return_size = return_size

    def get_result(self):
        cos_sim = cosine_similarity(self.matrix, self.matrix)
        top_ind = np.flip(np.argsort(cos_sim[0]))[:self.return_size]
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

    def query(self, query_id, query_text):
        self.query_id = query_id
        term_doc = self.vectorizer.fit_transform([query_text]+list(self.tweets.clean_text)) #returns document term matrix
        ind = ["query"] + list(self.tweets.tweet)
        self.matrix = pd.DataFrame(term_doc.toarray(), columns=self.vectorizer.get_feature_names(), index=ind) #indexes are the tweets, columns is the entire vocab
        self.get_result(self.return_size)
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
    def __init__(self, titles, tweets, type='tfidf', return_size = 30):
        self.titles = titles  #contains titles data
        self.tweets = tweets #contains tweets data
        self.vectorizer = self.change_matrix_type(type)

    def get_result(self):
        euclidean = euclidean_distances(self.matrix.values[1:], [self.matrix.values[0]])
        top_ind = np.argsort(euclidean.T[0])[:self.return_size]
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

