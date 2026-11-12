# reranker.py

from sentence_transformers import CrossEncoder

reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")


def rerank(query, docs, top_k=5):

    pairs = [(query, doc.page_content) for doc in docs]

    scores = reranker.predict(pairs)

    ranked_docs = sorted(zip(scores, docs), key=lambda x: x[0], reverse=True)

    return [doc for _, doc in ranked_docs[:top_k]]
