import time
import logging

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from hybrid import hybrid_search
from bm25 import keyword_search
from rag import vector_search
from generator import generate_answer
from memory import conversation_memory, MAX_HISTORY
from langsmith import traceable

# ---------------------------------------------
# Logging Configuration
# ---------------------------------------------

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)

# ---------------------------------------------
# FastAPI App
# ---------------------------------------------

app = FastAPI(
    title="Enterprise Knowledge Assistant",
    description="World Bank RAG System",
    version="1.0.0",
)

# ---------------------------------------------
# Request Model
# ---------------------------------------------


class QueryRequest(BaseModel):
    session_id: str
    question: str = Field(..., min_length=1)
    method: str = "hybrid"


# ---------------------------------------------
# Health Check
# ---------------------------------------------


@app.get("/")
def home():
    return {
        "status": "running",
        "retrieval_methods": ["vector", "bm25", "hybrid"],
    }


# ---------------------------------------------
# Delete Session
# ---------------------------------------------


@app.delete("/session/{session_id}")
def clear_session(session_id: str):

    if session_id in conversation_memory:
        del conversation_memory[session_id]

    logger.info("Session cleared: %s", session_id)

    return {
        "message": "Session cleared",
        "session_id": session_id,
    }


# ---------------------------------------------
# Ask Endpoint
# ---------------------------------------------


@traceable(name="ask_endpoint")
@app.post("/ask")
def ask(request: QueryRequest):

    start_time = time.time()

    try:

        question = request.question.strip()
        session_id = request.session_id
        # question_lower = question.lower()

        # -----------------------------------------
        # Create Session
        # -----------------------------------------

        if session_id not in conversation_memory:
            conversation_memory[session_id] = []

        # Store User Message

        conversation_memory[session_id].append(
            {
                "role": "user",
                "content": question,
            }
        )

        logger.info("=" * 60)
        logger.info("Session: %s", session_id)
        logger.info("Question: %s", question)
        logger.info("Method: %s", request.method)

        # -----------------------------------------
        # Retrieval
        # -----------------------------------------

        retrieval_start = time.time()

        if request.method == "vector":

            docs = vector_search(
                question,
                k=5,
            )

        elif request.method == "bm25":

            docs = keyword_search(
                question,
                k=5,
            )

        else:

            docs = hybrid_search(question)

        retrieval_time = time.time() - retrieval_start

        logger.info(
            "Retrieved %s documents in %.2f sec",
            len(docs),
            retrieval_time,
        )

        retrieved_sources = []

        for doc in docs:

            retrieved_sources.append(
                {
                    "source": doc.metadata.get("source"),
                    "page": doc.metadata.get("page"),
                    "year": doc.metadata.get("year"),
                }
            )

        logger.info(
            "Retrieved Documents: %s",
            retrieved_sources,
        )

        # -----------------------------------------
        # No Documents Found
        # -----------------------------------------

        if not docs:

            answer = "I could not find this information."

            conversation_memory[session_id].append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

            conversation_memory[session_id] = conversation_memory[session_id][
                -MAX_HISTORY:
            ]

            return {
                "session_id": session_id,
                "question": question,
                "answer": answer,
                "answer_found": False,
                "citations": [],
                "execution_time": round(
                    time.time() - start_time,
                    2,
                ),
            }

        # -----------------------------------------
        # Generation
        # -----------------------------------------

        generation_start = time.time()

        history = conversation_memory[session_id]

        logger.info(
            "Session %s contains %s messages",
            session_id,
            len(history),
        )

        answer = generate_answer(
            question=question,
            docs=docs,
            history=history,
        )

        generation_time = time.time() - generation_start

        # -----------------------------------------
        # Store Assistant Response
        # -----------------------------------------

        conversation_memory[session_id].append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        # Keep Only Last N Messages

        conversation_memory[session_id] = conversation_memory[session_id][-MAX_HISTORY:]

        logger.info(
            "Generation completed in %.2f sec",
            generation_time,
        )

        # -----------------------------------------
        # Citations
        # -----------------------------------------

        citations = []

        seen = set()

        for doc in docs:

            source = doc.metadata.get(
                "source",
                "Unknown",
            )

            page = doc.metadata.get("page")
            year = doc.metadata.get("year")

            key = (
                source,
                page,
                year,
            )

            if key not in seen:

                citations.append(
                    {
                        "source": source,
                        "page": page,
                        "year": year,
                    }
                )

                seen.add(key)

        # -----------------------------------------
        # Answer Found Flag
        # -----------------------------------------

        answer_text = str(answer)

        answer_found = (
            answer_text.strip().lower() != "i could not find this information."
        )

        # Hide citations when answer not found

        if not answer_found:
            citations = []

        total_time = time.time() - start_time

        logger.info(
            "Total execution time %.2f sec",
            total_time,
        )

        logger.info(
            "Answer Length: %s chars",
            len(answer),
        )

        # -----------------------------------------
        # Response
        # -----------------------------------------

        return {
            "session_id": session_id,
            "question": question,
            "method": request.method,
            "answer": answer,
            "answer_found": answer_found,
            "citations": citations,
            "retrieval_time": round(
                retrieval_time,
                2,
            ),
            "generation_time": round(
                generation_time,
                2,
            ),
            "execution_time": round(
                total_time,
                2,
            ),
        }

    except Exception as e:

        logger.exception("Pipeline Error")

        raise HTTPException(
            status_code=500,
            detail=str(e),
        )


# import time
# import logging

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field

# from hybrid import hybrid_search
# from bm25 import keyword_search
# from rag import vector_search
# from generator import generate_answer
# from memory import conversation_memory, MAX_HISTORY
# from langsmith import traceable

# # ---------------------------------------------
# # Logging Configuration
# # ---------------------------------------------

# logging.basicConfig(
#     filename="app.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# logger = logging.getLogger(__name__)

# # ---------------------------------------------
# # FastAPI App
# # ---------------------------------------------

# app = FastAPI(
#     title="Enterprise Knowledge Assistant",
#     description="World Bank RAG System",
#     version="1.0.0",
# )

# # ---------------------------------------------
# # Request Model
# # ---------------------------------------------


# class QueryRequest(BaseModel):
#     session_id: str
#     question: str = Field(..., min_length=1)
#     method: str = "hybrid"
#     # question: str = Field(..., min_length=1)
#     # method: str = "hybrid"


# # ---------------------------------------------
# # Health Check
# # ---------------------------------------------


# @app.get("/")
# def home():
#     return {"status": "running", "retrieval_methods": ["vector", "bm25", "hybrid"]}


# # ---------------------------------------------
# # Delete Session
# # ---------------------------------------------
# @app.delete("/session/{session_id}")
# def clear_session(session_id: str):

#     if session_id in conversation_memory:
#         del conversation_memory[session_id]

#     return {"message": "Session cleared"}


# # ---------------------------------------------
# # Ask Endpoint
# # ---------------------------------------------


# @traceable(name="ask_endpoint")
# @app.post("/ask")
# def ask(request: QueryRequest):

#     start_time = time.time()

#     try:

#         # question = request.question.strip()

#         question = request.question.strip()

#         session_id = request.session_id

#         if session_id not in conversation_memory:
#             conversation_memory[session_id] = []

#         conversation_memory[session_id].append(
#             {
#                 "role": "user",
#                 "content": question,
#             }
#         )

#         logger.info("=" * 60)
#         logger.info("Question: %s", question)
#         logger.info("Method: %s", request.method)

#         # -------------------------
#         # Retrieval
#         # -------------------------

#         retrieval_start = time.time()

#         if request.method == "vector":

#             docs = vector_search(question, k=5)

#         elif request.method == "bm25":

#             docs = keyword_search(question, k=5)

#         else:

#             docs = hybrid_search(question)

#         retrieval_time = time.time() - retrieval_start

#         logger.info("Retrieved %s documents in %.2f sec", len(docs), retrieval_time)

#         retrieved_sources = []

#         for doc in docs:

#             retrieved_sources.append(
#                 {
#                     "source": doc.metadata.get("source"),
#                     "page": doc.metadata.get("page"),
#                     "year": doc.metadata.get("year"),
#                 }
#             )

#         logger.info(f"Retrieved Documents: {retrieved_sources}")

#         if not docs:

#             answer = "I could not find this information."

#             conversation_memory[session_id].append(
#                 {
#                     "role": "assistant",
#                     "content": answer,
#                 }
#             )

#             return {
#                 "question": question,
#                 "answer": answer,
#                 "citations": [],
#                 "execution_time": round(time.time() - start_time, 2),
#             }

#         # -------------------------
#         # Generation
#         # -------------------------

#         # generation_start = time.time()

#         # # answer = generate_answer(question, docs)

#         # history = conversation_memory[session_id]

#         # answer = generate_answer(
#         #     question=question,
#         #     docs=docs,
#         #     history=history,
#         # )

#         # generation_time = time.time() - generation_start

#         generation_start = time.time()

#         history = conversation_memory[session_id]

#         answer = generate_answer(
#             question=question,
#             docs=docs,
#             history=history,
#         )

#         generation_time = time.time() - generation_start

#         conversation_memory[session_id].append(
#             {
#                 "role": "assistant",
#                 "content": answer,
#             }
#         )

#         conversation_memory[session_id] = conversation_memory[session_id][-MAX_HISTORY:]

#         logger.info("Generation completed in %.2f sec", generation_time)

#         # -------------------------
#         # Citations
#         # -------------------------

#         citations = []

#         seen = set()

#         for doc in docs:

#             source = doc.metadata.get("source", "Unknown")

#             page = doc.metadata.get("page")

#             year = doc.metadata.get("year")

#             key = (source, page, year)

#             if key not in seen:

#                 citations.append(
#                     {
#                         "source": source,
#                         "page": page,
#                         "year": year,
#                     }
#                 )

#                 seen.add(key)

#         total_time = time.time() - start_time

#         logger.info("Total execution time %.2f sec", total_time)

#         logger.info("Answer Length: %s chars", len(answer))

#         return {
#             "session_id": session_id,
#             "question": question,
#             "method": request.method,
#             "answer": answer,
#             "citations": citations,
#             "retrieval_time": round(retrieval_time, 2),
#             "generation_time": round(generation_time, 2),
#             "execution_time": round(total_time, 2),
#         }

#     except Exception as e:

#         logger.exception("Pipeline Error")

#         raise HTTPException(status_code=500, detail=str(e))


# import time
# import logging

# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel, Field

# from hybrid import hybrid_search
# from bm25 import keyword_search
# from rag import vector_search
# from generator import generate_answer
# from langsmith import traceable

# # ---------------------------------------------
# # Logging Configuration
# # ---------------------------------------------

# logging.basicConfig(
#     filename="app.log",
#     level=logging.INFO,
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

# logger = logging.getLogger(__name__)

# # ---------------------------------------------
# # FastAPI App
# # ---------------------------------------------

# app = FastAPI(
#     title="Enterprise Knowledge Assistant",
#     description="World Bank RAG System",
#     version="1.0.0",
# )

# # ---------------------------------------------
# # Request Model
# # ---------------------------------------------


# class QueryRequest(BaseModel):
#     question: str = Field(..., min_length=1)
#     method: str = "hybrid"


# # ---------------------------------------------
# # Health Check
# # ---------------------------------------------


# @app.get("/")
# def home():
#     return {"status": "running", "retrieval_methods": ["vector", "bm25", "hybrid"]}


# # ---------------------------------------------
# # Ask Endpoint
# # ---------------------------------------------


# @traceable(name="ask_endpoint")
# @app.post("/ask")
# def ask(request: QueryRequest):

#     start_time = time.time()

#     try:

#         question = request.question.strip()

#         logger.info("=" * 60)
#         logger.info("Question: %s", question)
#         logger.info("Method: %s", request.method)

#         # -------------------------
#         # Retrieval
#         # -------------------------

#         retrieval_start = time.time()

#         if request.method == "vector":

#             docs = vector_search(question, k=5)

#         elif request.method == "bm25":

#             docs = keyword_search(question, k=5)

#         else:

#             docs = hybrid_search(question)

#         retrieval_time = time.time() - retrieval_start

#         logger.info("Retrieved %s documents in %.2f sec", len(docs), retrieval_time)

#         if not docs:

#             return {
#                 "question": question,
#                 "answer": "I could not find this information.",
#                 "citations": [],
#                 "execution_time": round(time.time() - start_time, 2),
#             }

#         # -------------------------
#         # Generation
#         # -------------------------

#         generation_start = time.time()

#         answer = generate_answer(question, docs)

#         generation_time = time.time() - generation_start

#         logger.info("Generation completed in %.2f sec", generation_time)

#         # -------------------------
#         # Citations
#         # -------------------------

#         citations = []

#         seen = set()

#         for doc in docs:

#             source = doc.metadata.get("source", "Unknown")

#             page = doc.metadata.get("page")

#             year = doc.metadata.get("year")

#             key = (source, page, year)

#             if key not in seen:

#                 citations.append(
#                     {
#                         "source": source,
#                         "page": page,
#                         "year": year,
#                     }
#                 )

#                 seen.add(key)

#         total_time = time.time() - start_time

#         logger.info("Total execution time %.2f sec", total_time)

#         logger.info("Answer Length: %s chars", len(answer))

#         return {
#             "question": question,
#             "method": request.method,
#             "answer": answer,
#             "citations": citations,
#             "retrieval_time": round(retrieval_time, 2),
#             "generation_time": round(generation_time, 2),
#             "execution_time": round(total_time, 2),
#         }

#     except Exception as e:

#         logger.exception("Pipeline Error")

#         raise HTTPException(status_code=500, detail=str(e))


# from fastapi import FastAPI
# from pydantic import BaseModel

# from hybrid import hybrid_search
# from generator import generate_answer

# app = FastAPI()


# class QueryRequest(BaseModel):
#     question: str


# @app.get("/")
# def home():
#     return {"status": "running"}


# @app.post("/ask")
# def ask(request: QueryRequest):

#     # Retrieve documents using Hybrid + Reranker
#     docs = hybrid_search(request.question)

#     # Generate grounded answer
#     answer = generate_answer(request.question, docs)

#     # Build citations
#     citations = []

#     for doc in docs:

#         citations.append(
#             {
#                 "source": doc.metadata.get("source", "Unknown"),
#                 "page": doc.metadata.get("page", None),
#                 "year": doc.metadata.get("year", None),
#             }
#         )

#     return {"question": request.question, "answer": answer, "citations": citations}
