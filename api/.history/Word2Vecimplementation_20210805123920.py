class Word2Vec:
    def __init__(self, pandasdf):
        self.corpus = self.process_corpus(pandasdf)
        print (self.corpus)
        
    def process_corpus(self, pandasdf):
        sent = [row.split(',') for row in pandasdf.clean_text]
        print (sent)
        #return pandasdf.clean_text.tolist()