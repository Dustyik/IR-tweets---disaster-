import pandas as pd
import json
import ast
import os
from nltk.tokenize import word_tokenize

'''
filename = r"D:\Desktop\IR_term_8\sample-1M.jsonl"
output_path = r"D:\Desktop\IR_term_8"

with open(filename) as json_file:      
    data = json_file.readlines()
    # this line below may take at least 8-10 minutes of processing for 4-5 million rows. It converts all strings in list to actual json objects. 
    data = list(map(json.loads, data)) 

df = pd.DataFrame(data)
for col in df.columns:
    print (col)

labels_to_drop = ["content", "media-type", "source", "published"]
df = df.drop(labels_to_drop, axis = 1)

'''
def tokenize_stem_lower(self, text):	
    tokens = word_tokenize(text)
    tokens = list(filter(lambda x: x.isalpha(), tokens))
    tokens = [self.porter.stem(x.lower()) for x in tokens]
    return ' '.join(tokens)

df.head()


count = len(df)

out_header = ["title"]
'''
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
'''