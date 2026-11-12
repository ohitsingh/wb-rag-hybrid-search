# 🌍 Enterprise Knowledge Assistant
### World Bank Knowledge Assistant powered by Retrieval-Augmented Generation (RAG)

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-REST_API-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Frontend-Streamlit-red.svg)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/Framework-LangChain-green.svg)](https://www.langchain.com/)
[![FAISS](https://img.shields.io/badge/Vector_DB-FAISS-orange.svg)](https://github.com/facebookresearch/faiss)
[![LLM](https://img.shields.io/badge/LLM-GPT--4.1--mini-black.svg)](https://platform.openai.com/)

An AI-powered Enterprise Knowledge Assistant that retrieves information from World Bank documents and public World Bank APIs using Retrieval-Augmented Generation (RAG).

The application combines semantic vector search, BM25 keyword retrieval, hybrid search, and cross-encoder reranking to provide context-grounded answers with document and page-level citations.

It also supports conversational sessions, multiple retrieval strategies, REST API integration, and application logging.

---

# 📌 1. Problem Statement

Organizations maintain large volumes of information across documents, reports, research publications, and external APIs.

Traditional keyword-based search systems often struggle to understand semantic relationships between user questions and document content.

This project addresses that challenge by developing an Enterprise Knowledge Assistant that:

- Collects publicly available World Bank information.
- Ingests PDF documents and World Bank API responses.
- Processes and indexes the collected information.
- Retrieves relevant information using multiple retrieval approaches.
- Generates answers using an LLM and retrieved context.
- Provides source and page-level citations.
- Supports questions requiring information from multiple documents.
- Avoids fabricating answers when supporting information is unavailable.
- Exposes the functionality through REST APIs.
- Provides a Streamlit-based interactive interface.
- Logs retrieval performance, execution latency, and failures.

---

# 🎯 2. Key Features

| Feature | Implementation |
|---|---|
| Document ingestion | PyPDFLoader |
| External data ingestion | World Bank REST API |
| Document chunking | RecursiveCharacterTextSplitter |
| Embeddings | BAAI/bge-small-en-v1.5 |
| Vector database | FAISS |
| Keyword retrieval | BM25 |
| Semantic retrieval | FAISS similarity search |
| Hybrid retrieval | Vector + BM25 |
| Reranking | CrossEncoder |
| LLM | OpenAI GPT-4.1-mini |
| RAG framework | LangChain |
| Conversational memory | Session-based in-memory history |
| Backend | FastAPI |
| Frontend | Streamlit |
| Observability | Python logging and LangSmith tracing |

### Retrieval strategies

The application supports three retrieval methods:

1. Vector Search
2. BM25 Keyword Search
3. Hybrid Search with Cross-Encoder Reranking

Users can select the retrieval strategy directly from the Streamlit interface.

---

# 🏗️ 3. System Architecture

The solution follows a modular Retrieval-Augmented Generation architecture.

## High-Level Architecture

```text
                  USER
                    |
                    |
             Streamlit Frontend
                    |
                    |
                FastAPI
                    |
                    |
              /ask Endpoint
                    |
                    |
             Query Processing
                    |
          +---------+----------+
          |                    |
          |                    |
     Vector Search         BM25 Search
       (FAISS)              (BM25)
          |                    |
          |                    |
          +---------+----------+
                    |
                    |
              Hybrid Search
                    |
                    |
              Candidate Merge
                    |
                    |
             Cross-Encoder
                Reranker
                    |
                    |
             Top-K Documents
                    |
                    |
              Context Builder
                    |
                    |
             Prompt Engineering
                    |
                    |
             OpenAI GPT-4.1-mini
                    |
                    |
              Answer Generation
                    |
                    |
             Citation Extraction
                    |
                    |
              JSON Response
                    |
                    |
              Streamlit UI
```

## Document Ingestion Architecture

```text
             DATA SOURCES
                   |
          +--------+---------+
          |                  |
          |                  |
      PDF Documents      World Bank APIs
          |                  |
          |                  |
      PyPDFLoader        API Loader
          |                  |
          |                  |
          +--------+---------+
                   |
                   |
             Document Objects
                   |
                   |
             Text Chunking
                   |
                   |
          RecursiveCharacter
              Text Splitter
                   |
                   |
          +--------+---------+
          |                  |
          |                  |
      Embeddings         Pickle Storage
          |                  |
          |                  |
       HuggingFace           BM25
          |                  |
          |                  |
          FAISS Index       Keyword Index
```

---

# 📂 4. Project Structure

```text
wb-rag-hybrid-search/
│
├── backend/
│   │
│   ├── api_loader.py
│   ├── bm25.py
│   ├── create_index.py
│   ├── create_tables.py
│   ├── generator.py
│   ├── hybrid.py
│   ├── main.py
│   ├── memory.py
│   ├── rag.py
│   ├── reranker.py
│   │
│   ├── test_hybrid.py
│   ├── test_langsmith.py
│   ├── test_rag.py
│   ├── test_reranker.py
│   ├── testbm23.py
│   │
│   ├── faiss_index/          # Generated during indexing
│   └── documents.pkl         # Generated BM25 document store
│
├── frontend/
│   └── app.py
│
├── data/
│   └── Place PDF documents here
│
├── .env                      # API credentials (not committed)
├── .gitignore
├── .python-version
├── main.py
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

**Note:** The FAISS index and `documents.pkl` are generated artifacts and are excluded from Git. The PDF files are also excluded. Generate the indexes locally before starting the backend.

---

# ⚙️ 5. Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Programming Language | Python 3.12+ | Application development |
| LLM | OpenAI GPT-4.1-mini | Answer generation |
| Embedding Model | BAAI/bge-small-en-v1.5 | Semantic embeddings |
| Vector Database | FAISS | Similarity search |
| Keyword Search | BM25Okapi | Lexical retrieval |
| Reranking | CrossEncoder | Improve relevance |
| RAG Framework | LangChain | Document processing and LLM integration |
| Backend | FastAPI | REST API |
| Frontend | Streamlit | User interface |
| PDF Processing | PyPDFLoader | PDF ingestion |
| Chunking | RecursiveCharacterTextSplitter | Text splitting |
| Monitoring | LangSmith | LLM tracing |
| Logging | Python Logging | Application logs |
| API Integration | Requests | World Bank API integration |

---

# 📥 6. Data Ingestion

The application collects information from two primary sources.

## 6.1 PDF Document Ingestion

The application uses PyPDFLoader to extract text from PDF documents.

PDF files are placed inside the `data/` directory.

Example:

```text
data/
│
├── India_development_update.pdf
└── Poverty and Shared Prosperity 2020.pdf
```

The ingestion process:

1. Reads PDF files.
2. Extracts page-level text.
3. Preserves source document metadata.
4. Captures page numbers.
5. Converts pages into LangChain Document objects.

Example metadata:

```json
{
  "source": "India_development_update.pdf",
  "page": 12
}
```

Page metadata enables document-level and page-level citations.

## 6.2 World Bank API Integration

The application integrates with the public World Bank REST API.

API endpoints currently configured:

**India Population**

```text
https://api.worldbank.org/v2/country/IND/indicator/SP.POP.TOTL?format=json
```

**India GDP**

```text
https://api.worldbank.org/v2/country/IND/indicator/NY.GDP.MKTP.CD?format=json
```

**Brazil Population**

```text
https://api.worldbank.org/v2/country/BRA/indicator/SP.POP.TOTL?format=json
```

**USA GDP**

```text
https://api.worldbank.org/v2/country/USA/indicator/NY.GDP.MKTP.CD?format=json
```

Official API documentation:

https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information

The API loader converts the World Bank API response into LangChain Document objects.

Example:

```text
India Population for year 2023 was <value>.
```

Metadata includes:

- Country
- Indicator
- Year
- Source API URL

This allows the application to retrieve structured economic and demographic information using natural-language questions.

---

# ✂️ 7. Document Chunking and Indexing

After ingestion, the application combines PDF pages and API records into a common document collection.

The RecursiveCharacterTextSplitter is used for chunking.

Current configuration:

```python
RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
```

### Why chunking?

Large documents cannot efficiently be passed directly to an LLM.

Chunking helps:

- Improve retrieval precision.
- Reduce unnecessary context.
- Preserve relevant information.
- Support document-level retrieval.
- Control LLM context size.

### Embedding generation

The application uses:

```python
HuggingFaceEmbeddings(
    model_name="BAAI/bge-small-en-v1.5"
)
```

Each document chunk is converted into a numerical vector representation.

### FAISS indexing

The generated embeddings are stored in a local FAISS index.

```python
FAISS.from_documents(
    chunks,
    embeddings
)
```

The index is persisted locally for subsequent retrieval.

The same document chunks are serialized into `documents.pkl` to support BM25 retrieval.

---

# 🔍 8. Retrieval Strategies

The application implements multiple retrieval strategies to compare their effectiveness.

## 8.1 Vector Search (Semantic Search)

Vector search retrieves documents based on semantic similarity.

Implementation:

```python
def vector_search(query, k=5):
    return vector_store.similarity_search(
        query,
        k=k
    )
```

Process:

1. Convert the user query into an embedding.
2. Search the FAISS vector index.
3. Calculate vector similarity.
4. Retrieve the top-K semantically relevant documents.

**Advantages:**

- Understands semantic meaning.
- Handles natural-language questions.
- Retrieves conceptually related information.
- Less dependent on exact keyword matching.

**Limitations:**

- May miss exact identifiers or specific terminology.
- Similarity does not always guarantee factual relevance.

## 8.2 BM25 Keyword Search

BM25 is a probabilistic lexical retrieval algorithm.

Implementation uses:

```python
from rank_bm25 import BM25Okapi
```

Process:

1. Tokenize document chunks.
2. Build the BM25 index.
3. Tokenize the user query.
4. Calculate BM25 relevance scores.
5. Return the highest-scoring documents.

**Advantages:**

- Effective for exact keywords.
- Useful for names, terminology, and identifiers.
- Does not require embeddings.

**Limitations:**

- Limited understanding of semantic relationships.
- Can miss relevant documents with different wording.

## 8.3 Hybrid Search

Hybrid search combines semantic and keyword retrieval.

The implementation retrieves:

- Top 10 documents from vector search.
- Top 10 documents from BM25.

The retrieved candidates are merged and deduplicated.

The merged candidates are passed to a CrossEncoder reranker.

```python
def hybrid_search(query):

    vector_docs = vector_search(
        query,
        k=10
    )

    keyword_docs = keyword_search(
        query,
        k=10
    )

    merged = {}

    for doc in vector_docs + keyword_docs:
        merged[doc.page_content] = doc

    candidates = list(merged.values())

    return rerank(
        query,
        candidates,
        top_k=5
    )
```

## 8.4 Cross-Encoder Reranking

The application uses:

```text
cross-encoder/ms-marco-MiniLM-L-6-v2
```

Unlike bi-encoder retrieval, a cross-encoder evaluates the query and candidate document together.

It assigns relevance scores to candidate pairs.

The documents are sorted based on their reranking scores.

The top five documents are passed to the generation pipeline.

### Retrieval comparison

| Retrieval Method | Approach | Main Strength | Limitation |
|---|---|---|---|
| Vector Search | Semantic similarity | Understands meaning | Can miss exact terms |
| BM25 | Keyword matching | Exact terminology | Limited semantic understanding |
| Hybrid Search | Vector + BM25 + reranking | Combines semantic and lexical retrieval | Additional computation and latency |

The Streamlit interface allows users to select and compare these retrieval methods.

---

# 🤖 9. Retrieval-Augmented Generation (RAG)

The application follows a context-grounded generation approach.

### Workflow

1. User submits a question.
2. The selected retrieval strategy retrieves relevant documents.
3. The top retrieved documents are combined into context.
4. Conversation history is included for follow-up questions.
5. The prompt is passed to GPT-4.1-mini.
6. The LLM generates an answer using the retrieved context.
7. The API returns the answer and citations.

### LLM Configuration

```python
ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    timeout=60,
    max_retries=2
)
```

### Grounded generation instructions

The generation prompt instructs the LLM to:

- Answer only using the provided context.
- Avoid using external knowledge.
- Use conversation history only for understanding follow-up questions.
- Avoid fabricating information.
- Return a predefined response when the answer is unavailable.

When supporting information is unavailable, the expected response is:

```text
I could not find this information.
```

This approach reduces unsupported answers by constraining generation to retrieved context.

---

# 📚 10. Multi-Document Question Answering

The application can retrieve multiple relevant document chunks for a single question.

The retrieved documents are combined into a common context before being passed to the LLM.

Example question:

```text
Compare India's economic growth and population trends
using the available World Bank information.
```

The system can retrieve relevant information from:

- India GDP API records.
- India population API records.
- India development reports.

The LLM receives the combined context and generates an answer based on the available evidence.

This enables multi-document question answering instead of relying on a single retrieved document.

The quality of the comparison depends on the retrieved evidence and the coverage of the indexed sources.

---

# 📌 11. Document-Level and Page-Level Citations

Source attribution is important for enterprise knowledge systems.

The application preserves document metadata during ingestion and retrieval.

For PDF documents:

```json
{
  "source": "India_development_update.pdf",
  "page": 12
}
```

For World Bank API documents:

```json
{
  "source": "World Bank API URL",
  "country": "India",
  "indicator": "Population, total",
  "year": "2023"
}
```

The FastAPI response includes unique source citations.

Example:

```json
{
  "citations": [
    {
      "source": "India_development_update.pdf",
      "page": 12,
      "year": null
    },
    {
      "source": "World Bank API URL",
      "page": null,
      "year": "2023"
    }
  ]
}
```

The Streamlit frontend displays the document name, page number, and year where available.

**Note:** These are retrieved-source citations. The current implementation does not validate that every individual generated claim is independently supported by its cited passage.

---

# 🌐 12. REST API Documentation

The backend is implemented using FastAPI.

## Base URL

```text
http://127.0.0.1:8000
```

## 12.1 Health Check

**Endpoint**

```http
GET /
```

Example response:

```json
{
  "status": "running",
  "retrieval_methods": [
    "vector",
    "bm25",
    "hybrid"
  ]
}
```

## 12.2 Ask a Question

**Endpoint**

```http
POST /ask
```

Request:

```json
{
  "session_id": "session-001",
  "question": "What is India's population trend?",
  "method": "hybrid"
}
```

Supported retrieval methods:

| Method | Description |
|---|---|
| vector | Semantic vector search |
| bm25 | Keyword-based search |
| hybrid | Combined retrieval with reranking |

Example response:

```json
{
  "session_id": "session-001",
  "question": "What is India's population trend?",
  "method": "hybrid",
  "answer": "Answer generated from the retrieved World Bank context.",
  "answer_found": true,
  "citations": [
    {
      "source": "India_development_update.pdf",
      "page": 12,
      "year": null
    }
  ],
  "retrieval_time": 0.35,
  "generation_time": 2.45,
  "execution_time": 2.82
}
```

The example values above illustrate the response structure; they are not measured benchmark results.

## 12.3 Clear Conversation Session

**Endpoint**

```http
DELETE /session/{session_id}
```

Example:

```http
DELETE /session/session-001
```

Example response:

```json
{
  "message": "Session cleared",
  "session_id": "session-001"
}
```

## 12.4 Interactive API Documentation

FastAPI automatically exposes Swagger documentation.

```text
http://127.0.0.1:8000/docs
```

Alternative:

```text
http://127.0.0.1:8000/redoc
```

---

# 🖥️ 13. Streamlit Frontend

The application provides an interactive Streamlit interface.

Features:

- Natural-language question input.
- Retrieval strategy selection.
- Conversational session management.
- Answer display.
- Document and page-level citations.
- Retrieval latency display.
- Generation latency display.
- Total execution time display.
- New chat functionality.

The user can switch between:

- Hybrid Search
- Vector Search
- BM25 Search

This allows retrieval strategies to be compared using the same question.

---

# 🚀 14. Installation and Execution

Follow the steps below to run the application locally.

## Prerequisites

Install:

- Python 3.12 or later.
- Git.
- OpenAI API key.
- Internet connectivity for World Bank API access and model downloads.

Repository:

```bash
git clone https://github.com/ohitsingh/wb-rag-hybrid-search.git
```

Navigate to the project:

```bash
cd wb-rag-hybrid-search
```

## Step 1: Create Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Activate again:

```powershell
.venv\Scripts\Activate.ps1
```

## Step 2: Install Dependencies

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install requirements:

```powershell
pip install -r requirements.txt
```

Alternatively, if using the existing uv configuration:

```powershell
pip install uv
uv sync
```

## Step 3: Configure Environment Variables

Create a `.env` file in the project root.

```env
OPENAI_API_KEY=your_openai_api_key

# Optional LangSmith configuration
LANGSMITH_TRACING=false
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_PROJECT=world-bank-knowledge-assistant

# Optional database configuration
DATABASE_URL=your_postgresql_connection_string
```

Replace the placeholder values with your actual credentials.

Do not commit `.env` to GitHub.

The current application requires `OPENAI_API_KEY` for LLM generation.

LangSmith and PostgreSQL are optional for the basic RAG execution path.

## Step 4: Add PDF Documents

Place your PDF files inside the root-level `data/` directory.

Example:

```text
data/
│
├── India_development_update.pdf
└── Poverty and Shared Prosperity 2020.pdf
```

You can also run the application with World Bank API data alone by leaving the directory empty.

## Step 5: Build the Knowledge Base

Navigate to the backend:

```powershell
cd backend
```

Execute:

```powershell
python create_index.py
```

This script performs the following operations:

1. Downloads World Bank API data.
2. Loads PDF documents from the root-level data directory.
3. Extracts text from PDFs.
4. Splits documents into chunks.
5. Generates embeddings.
6. Creates the FAISS vector index.
7. Saves document chunks into `documents.pkl`.

Expected generated artifacts:

```text
backend/
│
├── faiss_index/
│
└── documents.pkl
```

The embedding model and reranker models may download automatically the first time they are initialized.

**Important:** Index creation requires internet access. Rebuild the index whenever the underlying documents or API dataset changes.

## Step 6: Start the FastAPI Backend

Remain inside the `backend/` directory.

Execute:

```powershell
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

Backend URL:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Keep this terminal running.

## Step 7: Start the Streamlit Frontend

Open another VS Code terminal.

Navigate to the project root:

```powershell
cd D:\wb-rag-hybrid-search
```

Activate the virtual environment:

```powershell
.venv\Scripts\Activate.ps1
```

Start Streamlit:

```powershell
streamlit run frontend/app.py
```

The frontend should open at:

```text
http://localhost:8501
```

You can now start asking questions.

---

# 🧪 15. Evaluation and Retrieval Comparison

The application supports three retrieval configurations.

The purpose of the evaluation is to understand how retrieval strategy affects answer quality, relevance, and latency.

## Retrieval Evaluation

| Evaluation Dimension | Vector Search | BM25 | Hybrid + Reranking |
|---|---|---|---|
| Semantic matching | Supported | Limited | Supported |
| Exact keyword matching | Supported through embeddings | Strong | Strong |
| Multiple retrieval signals | No | No | Yes |
| Reranking | No | No | Yes |
| Retrieval latency | To be measured | To be measured | To be measured |
| Context relevance | To be measured | To be measured | To be measured |
| Answer correctness | To be measured | To be measured | To be measured |

### Evaluation Metrics

The following metrics should be used to evaluate retrieval and generation quality.

**1. Precision@K**

Measures how many retrieved documents are relevant.

```text
Precision@K =
Relevant Retrieved Documents / K
```

**2. Recall@K**

Measures how many relevant documents were successfully retrieved.

```text
Recall@K =
Relevant Retrieved Documents / Total Relevant Documents
```

**3. Mean Reciprocal Rank (MRR)**

Measures the position of the first relevant result.

**4. Context Precision**

Measures whether relevant information appears near the top of the retrieved context.

**5. Context Recall**

Measures whether the retrieved context contains the information required to answer the question.

**6. Answer Relevance**

Measures how well the generated answer addresses the user's question.

**7. Faithfulness**

Measures whether the answer is supported by the retrieved context.

**8. Latency**

Measures retrieval, generation, and total execution time.

### Evaluation Dataset

A reproducible evaluation dataset should contain:

- Questions answerable from one document.
- Questions requiring multiple documents.
- Exact keyword questions.
- Semantic questions.
- Questions involving API data.
- Questions with unavailable answers.
- Questions containing ambiguous terminology.

### Evaluation Results

No independently measured benchmark results are currently included in this repository.

The evaluation table should be populated after running the same test questions against all three retrieval methods.

| Metric | Vector | BM25 | Hybrid + Reranking |
|---|---:|---:|---:|
| Precision@5 | TBD | TBD | TBD |
| Recall@5 | TBD | TBD | TBD |
| MRR | TBD | TBD | TBD |
| Context Precision | TBD | TBD | TBD |
| Context Recall | TBD | TBD | TBD |
| Answer Faithfulness | TBD | TBD | TBD |
| Average Retrieval Latency | TBD | TBD | TBD |
| Average End-to-End Latency | TBD | TBD | TBD |

**Expected hypothesis:** Hybrid retrieval with reranking should improve relevance by combining semantic and lexical signals. Actual effectiveness must be established through measured evaluation rather than assumed.

---

# 📊 16. Logging and Monitoring

The backend implements Python logging.

Log file:

```text
backend/app.log
```

The application records:

- User questions.
- Session identifiers.
- Selected retrieval method.
- Number of retrieved documents.
- Retrieved source metadata.
- Retrieval execution time.
- Generation execution time.
- Total execution time.
- Answer length.
- Pipeline failures.

### LangSmith Integration

The application uses LangSmith's `@traceable` decorator on selected pipeline functions.

This provides tracing for:

- Ask endpoint execution.
- Hybrid retrieval.
- Answer generation.

LangSmith can be enabled through environment configuration.

**Current implementation note:** The FastAPI response exposes retrieval, generation, and total latency. Direct token-count and cost accounting are not currently implemented in the API response. Production deployment should add explicit provider usage tracking and cost monitoring.

---

# 🔐 17. Production Security Considerations

The current repository is a local demonstration implementation.

For enterprise production deployment, the following controls should be implemented.

## 17.1 Authentication

Use an identity provider such as:

- OAuth 2.0
- OpenID Connect
- Microsoft Entra ID
- Enterprise SSO

The backend should validate access tokens and identify users before processing requests.

## 17.2 Document-Level Authorization

Documents should contain authorization metadata.

Example:

```json
{
  "document_id": "DOC-001",
  "department": "Finance",
  "allowed_roles": [
    "Finance",
    "Admin"
  ]
}
```

Before retrieval results are returned to the LLM, enforce user-specific access policies.

Unauthorized document chunks must never enter the LLM context.

Authorization should be enforced during retrieval, not merely at the frontend.

## 17.3 Prompt Injection Protection

Documents and user queries may contain malicious instructions.

Production controls should include:

- Treat retrieved content as untrusted data.
- Separate system instructions from retrieved context.
- Never allow document text to override system instructions.
- Validate tool calls and external actions.
- Apply input and output guardrails.
- Monitor suspicious prompt patterns.
- Restrict tool permissions using least privilege.

## 17.4 Confidential Information Protection

Sensitive information must be protected through:

- Encryption in transit using HTTPS/TLS.
- Encryption at rest.
- Secret management using a secure vault.
- PII detection and masking.
- Access-controlled logging.
- Data retention policies.
- Audit trails.
- Secure API credential management.

API keys should never be stored directly in source code or committed to Git.

## 17.5 Production Observability

Recommended monitoring:

- Retrieval latency.
- LLM latency.
- Token consumption.
- API cost.
- Retrieval quality.
- Answer faithfulness.
- Error rates.
- Request volume.
- Failed authentication attempts.

These production controls are design recommendations and are not all implemented in the current repository.

---

# ⚠️ 18. Current Limitations

The current implementation is designed as a working RAG assignment/demo, not a fully hardened enterprise deployment.

Known limitations include:

1. FAISS and BM25 indexes are generated locally and must be rebuilt after cloning.
2. Conversation memory is stored in application memory and is not persistent across restarts.
3. The current API does not implement user authentication.
4. Document-level authorization is not implemented.
5. Direct LLM token and cost accounting is not implemented.
6. Retrieval evaluation metrics require a labeled evaluation dataset and benchmark execution.
7. Prompt injection defenses need additional production hardening.
8. Source citations identify retrieved documents and pages but do not perform claim-level citation verification.
9. The current World Bank API endpoints are statically configured.
10. The current logging implementation should be hardened before processing confidential enterprise data.

---

# 🔮 19. Future Enhancements

Potential improvements include:

- Add PostgreSQL-backed persistent conversation history.
- Add user authentication using OAuth 2.0.
- Implement document-level authorization.
- Introduce metadata-filtered vector retrieval.
- Add Reciprocal Rank Fusion (RRF).
- Implement query rewriting and multi-query retrieval.
- Add automated retrieval evaluation using RAGAS.
- Introduce claim-level citation verification.
- Add token usage and LLM cost tracking.
- Implement structured observability dashboards.
- Add Docker-based deployment.
- Introduce CI/CD using GitHub Actions.
- Implement production-grade prompt injection protection.
- Add configurable World Bank API ingestion.

---

# 🎬 20. Working Demo

The application can be demonstrated using the following workflow.

1. Start the FastAPI backend.
2. Start the Streamlit frontend.
3. Select a retrieval strategy.
4. Submit a natural-language question.
5. Review the generated answer.
6. Inspect the source document and page citations.
7. Compare results using Vector, BM25, and Hybrid Search.
8. Review retrieval and generation latency.

### Example Questions

**Question 1: Population**

```text
How has India's population changed over the available years?
```

**Question 2: Economic indicators**

```text
What is India's GDP according to the available World Bank data?
```

**Question 3: Multi-document reasoning**

```text
Compare India's population trend with its economic development.
```

**Question 4: Document-based question**

```text
What are the major development challenges discussed in the India Development Update?
```

**Question 5: Unavailable information**

```text
What is India's exact GDP forecast for the year 2040 in the indexed documents?
```

The system should return:

```text
I could not find this information.
```

when the required information is not supported by the retrieved context.

---

# 📚 21. References

- GitHub Repository: https://github.com/ohitsingh/wb-rag-hybrid-search
- World Bank Open Data: https://data.worldbank.org/
- World Bank API Documentation: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information
- LangChain: https://www.langchain.com/
- FastAPI: https://fastapi.tiangolo.com/
- Streamlit: https://streamlit.io/
- FAISS: https://github.com/facebookresearch/faiss
- Hugging Face: https://huggingface.co/
- OpenAI API: https://platform.openai.com/docs/
- LangSmith: https://docs.langchain.com/langsmith/home

---

# 👨‍💻 22. Author

**Developed by:** Mohit Singh

**Project:** wb-bot

**Repository:** https://github.com/ohitsingh/wb-rag-hybrid-search

---

⭐ If you find this project useful, consider giving the repository a star.
