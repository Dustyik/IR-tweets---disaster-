from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics.pairwise import euclidean_distances

sbert_model = SentenceTransformer('bert-base-nli-mean-tokens')

