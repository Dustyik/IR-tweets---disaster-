from gensim.models import Word2Vec

MIN_COUNT = 5 #min count of words when training model, default is 5
SIZE = 50 #dimensions of embedding, default 100
WORKERS = 3 #number of partitions during training, default workers is 3
WINDOW = 3 #max window size of words around it, default 5 
SG = 0 #training algo, either CBOW (0) or SKIPGRAM (1), default CBOW

class Word2Vec:
    def __init__(self, pandasdf):
        self.corpus = self.process_corpus(pandasdf)
        self.model = self.create_model(self.corpus)
        print (self.corpus)
        
    def process_corpus(self, pandasdf):
        list_of_list = [row.split(',') for row in pandasdf.clean_text]
        return list_of_list
        #return pandasdf.clean_text.tolist()
        
    def create_model(self, corpus):
        return Word2Vec(sentences = corpus, min_count = MIN_COUNT,size = SIZE,workers = WORKERS, window = WINDOW, sg = SG)
    