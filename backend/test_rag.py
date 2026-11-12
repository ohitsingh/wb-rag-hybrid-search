from rag import search

query = input("Question: ")

docs = search(query)

for i, doc in enumerate(docs, 1):

    print("\n")
    print("=" * 80)

    print(f"Result {i}")

    print(doc.page_content[:1000])

    print("\nMetadata:")

    print(doc.metadata)
