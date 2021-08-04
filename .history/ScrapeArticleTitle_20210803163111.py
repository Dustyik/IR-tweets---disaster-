import pandas as pd
import json
import ast
import os
from nltk.tokenize import word_tokenize
from IPython.display import display

def get_article_titles_from_json():
    filename = r"D:\Desktop\IR_term_8\sample-1M.jsonl" #file is too huge
    with open(filename) as json_file:      
        data = json_file.readlines()
        data = list(map(json.loads, data)) 

    df = pd.DataFrame(data)
    for col in df.columns:
        print (col)

    labels_to_drop = ["content", "media-type", "source", "published"]
    df = df.drop(labels_to_drop, axis = 1)

    count = len(df)

    out_header = ["title"]

    for idx, e in df.iterrows():
        print("Row ",idx," out of ",count)
        entry = e.values.tolist()
        print (entry)
        #for src in src_lst:
        #    print (src)

        #output.to_csv(output_path, sep='\t', header=is_first, index=False, mode='a')
        #is_first = False

    df.to_csv('article_titles.csv', index=False)
    #print (path)


#Tokenising Funtions
def tokenize_stem_lower(text):	
	    tokens = word_tokenize(text)
	    tokens = list(filter(lambda x: x.isalpha(), tokens))
	    tokens = [porter.stem(x.lower()) for x in tokens]
	    return ' '.join(tokens)

def get_clean_data(df):
    df['clean_text'] = df.apply(lambda x: tokenize_stem_lower(x.tweet), axis=1)
    return df 
