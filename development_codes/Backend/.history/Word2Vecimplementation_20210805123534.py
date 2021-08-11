class Word2Vec:
    def __init__(self, pandasdf):
        self.corpus = self.process_corpus(pandasdf)
        print (self.corpus)
        
    def process_corpus(self, pandasdf):
        return pandasdf.clean_text.to_list()