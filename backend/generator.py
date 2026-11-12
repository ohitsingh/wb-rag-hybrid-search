import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langsmith import traceable

# --------------------------------
# Load Environment Variables
# --------------------------------

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=ENV_PATH)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY missing")

# --------------------------------
# OpenAI Model
# --------------------------------

llm = ChatOpenAI(
    model="gpt-4.1-mini",
    temperature=0,
    timeout=60,
    max_retries=2,
)

# --------------------------------
# Generate Answer
# --------------------------------


@traceable(name="generate_answer")
def generate_answer(question, docs, history=None):

    context = "\n\n".join([doc.page_content for doc in docs])

    chat_history = ""

    if history:
        for msg in history[-10:]:

            chat_history += f"{msg['role'].upper()}: " f"{msg['content']}\n"

    prompt = f"""
You are a World Bank Knowledge Assistant.

Rules:

1. Use conversation history only for understanding follow-up questions.
2. Answer ONLY using the provided context.
3. Do not use external knowledge.
4. If answer is not available in context reply exactly:
I could not find this information.
5. Keep answers concise and factual.

Conversation History:

{chat_history}

Context:

{context}

Question:

{question}

Answer:
"""

    response = llm.invoke(prompt)

    return response.content


# import os
# from pathlib import Path

# from dotenv import load_dotenv
# from langchain_openai import ChatOpenAI
# from langsmith import traceable

# # --------------------------------
# # 1. Load Environment Variables
# # --------------------------------

# ENV_PATH = Path(__file__).resolve().parent.parent / ".env"

# load_dotenv(dotenv_path=ENV_PATH)

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# # Validate API key
# if not OPENAI_API_KEY:
#     raise ValueError("OPENAI_API_KEY is missing in .env file")


# # --------------------------------
# # 2. Initialize OpenAI Model
# # --------------------------------

# llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0, timeout=60, max_retries=2)


# # --------------------------------
# # 3. Generate RAG Answer
# # --------------------------------


# @traceable(name="generate_answer")
# def generate_answer(question, docs):

#     context = "\n\n".join([doc.page_content for doc in docs])

#     prompt = f"""
# You are a World Bank Knowledge Assistant.

# Rules:

# 1. Answer ONLY from provided context.
# 2. Do not use external knowledge.
# 3. If answer is not available, respond exactly:
#    I could not find this information.
# 4. Provide concise factual answers.

# Context:
# {context}

# Question:
# {question}
# """

#     print("Sending request to OpenAI...", flush=True)

#     response = llm.invoke(prompt)

#     print("OpenAI response received successfully!", flush=True)

#     return response.content
