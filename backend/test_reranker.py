# test_reranker.py

from hybrid import hybrid_search

docs = hybrid_search("India GDP 2023")

for doc in docs:
    print("-" * 50)
    print(doc.page_content[:300])
