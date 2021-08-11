from gensim.models import Word2Vec
import tempfile
import numpy as np

MIN_COUNT = 5 #min count of words when training model, default is 5
SIZE = 50 #dimensions of embedding, default 100
WORKERS = 3 #number of partitions during training, default workers is 3, used for training parallelization 
WINDOW = 3 #max window size of words around it, default 5 
SG = 0 #training algo, either CBOW (0) or SKIPGRAM (1), default CBOW
VECTOR_SIZE = 100 #dimensional space that Word2Vec maps the words onto, default 100
EPOCHS = 1

GENSIM_MODEL_FILEPATH = ""

class Word2VecModel:
    def __init__(self, pandasdf):
        self.corpus = self.process_corpus(pandasdf)
        self.model = self.create_model(self.corpus)
        
    def process_corpus(self, pandasdf):
        list_of_list = [row.split(',') for row in pandasdf.clean_text]
        return list_of_list
        #return pandasdf.clean_text.tolist()
        
    def create_model(self, corpus):
        return Word2Vec(sentences = corpus, 
                        min_count = MIN_COUNT,
                        workers = WORKERS, 
                        window = WINDOW, 
                        sg = SG,
                        vector_size = VECTOR_SIZE)
    
    def store_model(self):
        with tempfile.NamedTemporaryFile(prefix='IR-gensim-model', delete=False) as tmp:
            temporary_filepath = tmp.name
            print ("Saving Model Temporary Filepath", temporary_filepath)
            self.save(temporary_filepath)
            
    def load_model(self):
        loaded_model = Word2Vec.load(GENSIM_MODEL_FILEPATH)
        return loaded_model
    
    def train_model(self):
        self.model.train()
        
    def document_embedding_w2v(self, doc_tokens):
        embeddings = []
        if len(doc_tokens) < 1:
            return np.zeros(VECTOR_SIZE)
        else:
            for tok in doc_tokens:
                if tok in self.model.wv.vocab:
                    embeddings.append(self.model.wv.word_vec(tok))
                else:
                    embeddings.append(np.random.rand(300))
            # mean the vectors of individual words to get the vector of the document
            return np.mean(embeddings, axis=0)
        
    
    def return_most_significant_tweets(query, n):
        
        return 
        
    
        
    