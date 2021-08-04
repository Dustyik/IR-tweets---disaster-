 from sklearn.metrics import ndcg_score

def calculate_ndcg(true_relevance, scores, k=10):
    return ndcg_score(true_relevance, scores, k=k)