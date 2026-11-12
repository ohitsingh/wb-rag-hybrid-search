from rag import vector_search
from bm25 import keyword_search
from reranker import rerank
from langsmith import traceable


@traceable(name="hybrid_search")
def hybrid_search(query):

    vector_docs = vector_search(query, k=10)

    keyword_docs = keyword_search(query, k=10)

    merged = {}

    for doc in vector_docs + keyword_docs:
        merged[doc.page_content] = doc

    candidates = list(merged.values())

    return rerank(query, candidates, top_k=5)
