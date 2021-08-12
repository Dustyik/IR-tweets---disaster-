from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

def return_BERT_query(tweets_data, article_title):
    print ("In BERT function")
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    document_embeddings = sbert_model.encode(tweets_data['clean_text'])
    query_embedding = sbert_model(article_title)
    tweets_data['embeddings'] = tweets_data.apply(lambda row: sbert_model.encode(row.clean_text), axis = 1)
    tweets_data["BERT_similarity"] = tweets_data.apply(lambda row: cosine_similarity(np.array(query_vector_embedding).reshape(1, -1),np.array(x).reshape(1, -1)).item())
    
    print (pairwise_similarities)

    #most_similar(0,pairwise_similarities,'Cosine Similarity')
    #most_similar(0,pairwise_differences,'Euclidean Distance')

'''
def most_similar(doc_id,similarity_matrix,matrix):
    print (f'Document: {documents_df.iloc[doc_id]["documents"]}')
    print ('\n')
    print ('Similar Documents:')
    if matrix=='Cosine Similarity':
        similar_ix=np.argsort(similarity_matrix[doc_id])[::-1]
    elif matrix=='Euclidean Distance':
        similar_ix=np.argsort(similarity_matrix[doc_id])
    for ix in similar_ix:
        if ix==doc_id:
            continue
        print('\n')
        print (f'Document: {documents_df.iloc[ix]["documents"]}')
        print (f'{matrix} : {similarity_matrix[doc_id][ix]}')
'''