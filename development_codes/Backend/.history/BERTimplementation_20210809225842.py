from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances


def create_BERT_embeddings(tweets_data):
    sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')
    document_embeddings = sbert_model.encode(tweets_data['clean_text'])


    pairwise_similarities=cosine_similarity(document_embeddings)
    pairwise_differences=euclidean_distances(document_embeddings)

    most_similar(0,pairwise_similarities,'Cosine Similarity')
    most_similar(0,pairwise_differences,'Euclidean Distance')

