import pandas as pd
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from IPython.display import display


file_path = r"D:\Desktop\IR_term_8\IR-tweets---disaster-\dataset_scrapped.csv"
col = ["id", "title"]
csv = pd.read_csv(file_path) 
data = pd.DataFrame(csv)

porter = PorterStemmer()

def tokenize_stem_lower(text):	
	    tokens = word_tokenize(text)
	    tokens = list(filter(lambda x: x.isalpha(), tokens))
	    tokens = [porter.stem(x.lower()) for x in tokens]
	    return ' '.join(tokens)

def get_clean_data(df):
    df['clean_text'] = df.apply(lambda x: tokenize_stem_lower(x.title), axis=1)
    return df 

data.title = data.title.astype(str)
df = get_clean_data(data)
df.to_csv('article_titles_stemmed.csv', index=False)
display(data.head())