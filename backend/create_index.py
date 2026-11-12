import os
import pickle

from api_loader import load_worldbank_api

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# API_URLS = [
#     "https://api.worldbank.org/v2/country/IND/indicator/SP.POP.TOTL?format=json",
#     "https://api.worldbank.org/v2/country/IND/indicator/NY.GDP.MKTP.CD?format=json",
#     "https://api.worldbank.org/v2/country/BRA/indicator/SP.POP.TOTL?format=json",
#     "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json",
# ]

API_URLS = [
    "https://api.worldbank.org/v2/country/IND/indicator/SP.POP.TOTL?format=json",
    "https://api.worldbank.org/v2/country/IND/indicator/NY.GDP.MKTP.CD?format=json",
    "https://api.worldbank.org/v2/country/BRA/indicator/SP.POP.TOTL?format=json",
    "https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json",
]

PDF_FOLDER = "../data"


def load_pdfs():

    pdf_docs = []

    for file in os.listdir(PDF_FOLDER):

        if file.endswith(".pdf"):

            pdf_path = os.path.join(PDF_FOLDER, file)

            print(f"Loading PDF: {file}")

            loader = PyPDFLoader(pdf_path)

            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = file

                # Page-level citation support
                doc.metadata["page"] = doc.metadata.get("page", 0) + 1

            pdf_docs.extend(docs)

    return pdf_docs


def build_index():

    all_docs = []

    print("\nLoading World Bank APIs...")

    for url in API_URLS:

        docs = load_worldbank_api(url)

        all_docs.extend(docs)

    print(f"API Documents: {len(all_docs)}")

    print("\nLoading PDFs...")

    pdf_docs = load_pdfs()

    print(f"PDF Pages Loaded: {len(pdf_docs)}")

    all_docs.extend(pdf_docs)

    print(f"\nTotal Documents: {len(all_docs)}")

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    chunks = splitter.split_documents(all_docs)

    print(f"Total Chunks: {len(chunks)}")

    # -------------------------
    # Save chunks for BM25
    # -------------------------

    with open("documents.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("✅ Documents saved for BM25")

    # -------------------------
    # Create FAISS Vector Index
    # -------------------------

    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    print("Creating FAISS Index...")

    vector_store = FAISS.from_documents(chunks, embeddings)

    vector_store.save_local("faiss_index")

    print("✅ FAISS Index created successfully")
    print("✅ Indexing completed")


if __name__ == "__main__":
    build_index()
