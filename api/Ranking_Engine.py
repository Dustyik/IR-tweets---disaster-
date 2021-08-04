import numpy as np

K = 30
RANKING_MODEL = "ndcg"

def get_rank(ranking_model, data):
    if(ranking_model == RANKING_MODEL):
        rel_score = data.relevance_score.tolist()
        return ndcg_at_k(rel_score)

def dcg_at_k(r, k, method=0):
    r = np.asfarray(r)[:k]
    if r.size:
        if method == 0:
            return r[0] + np.sum(r[1:] / np.log2(np.arange(2, r.size + 1)))
        elif method == 1:
            return np.sum(r / np.log2(np.arange(2, r.size + 2)))
        else:
            raise ValueError('method must be 0 or 1.')
    return 0.


def ndcg_at_k(r, k = K, method=0):
    '''
    r - relevance scores in rank order, k: number of results to consider, method considers when log is applied
    '''
    dcg_max = dcg_at_k(sorted(r, reverse=True), k, method)
    if not dcg_max:
        return 0.
    return dcg_at_k(r, k, method) / dcg_max
