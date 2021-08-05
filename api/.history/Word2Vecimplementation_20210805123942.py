class Word2Vec:
    def __init__(self, pandasdf):
        self.corpus = self.process_corpus(pandasdf)
        print (self.corpus)
        
    def process_corpus(self, pandasdf):
        list_of_list = [row.split(',') for row in pandasdf.clean_text]
        return list_of_list
        #return pandasdf.clean_text.tolist()