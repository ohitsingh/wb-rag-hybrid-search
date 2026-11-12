import pickle
import re

from rank_bm25 import BM25Okapi

# Load indexed documents
with open("documents.pkl", "rb") as f:
    documents = pickle.load(f)

# Better tokenization
tokenized_docs = []

for doc in documents:

    tokens = re.findall(r"\w+", doc.page_content.lower())

    tokenized_docs.append(tokens)

# Build BM25 index
bm25 = BM25Okapi(tokenized_docs)


def keyword_search(query, k=5):

    query_tokens = re.findall(r"\w+", query.lower())

    scores = bm25.get_scores(query_tokens)

    ranked_docs = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)

    # Return only relevant documents
    results = []

    for score, doc in ranked_docs:

        if score > 0:
            results.append(doc)

        if len(results) >= k:
            break

    return results


# import pickle
# from rank_bm25 import BM25Okapi

# with open("documents.pkl", "rb") as f:
#     documents = pickle.load(f)

# tokenized_docs = [doc.page_content.lower().split() for doc in documents]

# bm25 = BM25Okapi(tokenized_docs)


# def keyword_search(query, k=5):
#     scores = bm25.get_scores(query.lower().split())

#     ranked_docs = sorted(zip(scores, documents), key=lambda x: x[0], reverse=True)

#     return [doc for _, doc in ranked_docs[:k]]
