from nltk.stem import PorterStemmer 
import re

class QueryParsers:
    
	def __init__(self, query):
		self.query= self.get_queries(query)

	def get_queries(self, query):
		q = query.lower()
		#subsitute all non-word characters with whitespace
		pattern = re.compile('\W+')
		q = pattern.sub(' ', q)
		# split text into words (tokenized list for a document)
		q = q.split()
		# stemming words
		stemmer = PorterStemmer()
		q = [stemmer.stem(w) for w in q ]
		return q #returns a list of stemmed words