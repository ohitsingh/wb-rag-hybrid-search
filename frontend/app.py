import streamlit as st
import requests
import uuid

# ---------------------------------------------------
# API CONFIG
# ---------------------------------------------------

API_URL = "http://127.0.0.1:8000/ask"
SESSION_API = "http://127.0.0.1:8000/session"

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="WB Chatbot",
    page_icon="🌍",
    layout="wide",
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown(
    """
<style>

.main {
    padding-top: 1rem;
}

.stButton button {
    width: 100%;
    border-radius: 10px;
    background-color: #0070C0;
    color: white;
    font-weight: 600;
    border: none;
}

.stButton button:hover {
    background-color: #005999;
}

.metric-card {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #e3e3e3;
    text-align: center;
}

.answer-card {
    background-color: #f8fbff;
    padding: 20px;
    border-left: 6px solid #0070C0;
    border-radius: 12px;
    margin-bottom: 20px;
}

.source-card {
    background-color: #ffffff;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #dcdcdc;
    margin-top: 10px;
}

</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# SESSION INIT
# ---------------------------------------------------

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# ---------------------------------------------------
# HERO HEADER
# ---------------------------------------------------

st.markdown(
    """
<div style="
padding:25px;
border-radius:15px;
background:linear-gradient(90deg,#0070C0,#00A3E0);
color:white;
text-align:center;
margin-bottom:25px;
">

<h1>🌍 WB Chatbot</h1>

<p style="font-size:18px;">
World Bank Knowledge Assistant powered by RAG
</p>

</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.header("⚙ Settings")

    st.caption(f"Session: {st.session_state.session_id[:8]}")

    if st.button("🆕 New Chat"):

        try:
            requests.delete(
                f"{SESSION_API}/{st.session_state.session_id}",
                timeout=10,
            )
        except:
            pass

        st.session_state.session_id = str(uuid.uuid4())
        st.rerun()

    retrieval_method = st.selectbox("Retrieval Method", ["hybrid", "vector", "bm25"])

    st.info("""
✅ World Bank APIs

✅ PDF Documents

✅ Vector Search

✅ BM25 Search

✅ Hybrid Search

✅ Reranking

✅ Citations

✅ Session Memory

✅ Logging & Monitoring
""")

# ---------------------------------------------------
# QUESTION INPUT
# ---------------------------------------------------

question = st.text_area(
    "Ask a Question",
    placeholder="How has India's population changed over the last 10 years?",
    height=120,
)

# ---------------------------------------------------
# SEARCH
# ---------------------------------------------------

if st.button("🔍 Search"):

    if not question.strip():
        st.warning("Please enter a question.")
        st.stop()

    try:

        with st.spinner("Searching World Bank Knowledge Base..."):

            response = requests.post(
                API_URL,
                json={
                    "session_id": st.session_state.session_id,
                    "question": question,
                    "method": retrieval_method,
                },
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

        answer = data.get(
            "answer",
            "No answer returned",
        )

        # ---------------------------------------------------
        # SUCCESS MESSAGE
        # ---------------------------------------------------

        if answer.strip().lower() == "i could not find this information.":

            st.warning("⚠ No Relevant Context Found")

        else:

            st.success("✅ Answer Generated Successfully")

        # ---------------------------------------------------
        # ANSWER CARD
        # ---------------------------------------------------

        st.markdown("## 🤖 WB Assistant")

        st.markdown(
            f"""
            <div class="answer-card">
            {answer}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ---------------------------------------------------
        # METRICS
        # ---------------------------------------------------

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("⚡ Retrieval Time", f"{data.get('retrieval_time',0)} sec")

        with col2:
            st.metric("🧠 Generation Time", f"{data.get('generation_time',0)} sec")

        with col3:
            st.metric("⏱ Total Time", f"{data.get('execution_time',0)} sec")

        # ---------------------------------------------------
        # CITATIONS
        # ---------------------------------------------------

        answer_found = data.get("answer_found", True)

        citations = data.get("citations", [])

        if answer_found and citations:

            st.markdown("---")
            st.markdown("## 📚 References Used")

            unique_sources = set()

            html = """
            <div class="source-card">
            """

            for citation in citations:

                source = citation.get("source", "Unknown")

                page = citation.get("page")

                year = citation.get("year")

                key = f"{source}-{page}-{year}"

                if key in unique_sources:
                    continue

                unique_sources.add(key)

                html += f"""
                <div style="
                margin-bottom:12px;
                padding-bottom:12px;
                border-bottom:1px solid #eee;
                ">
                📄 <b>{source}</b>
                """

                if page:
                    html += f" | Page {page}"

                if year:
                    html += f" | Year {year}"

                html += "</div>"

            html += "</div>"

            st.markdown(
                html,
                unsafe_allow_html=True,
            )

    except Exception as e:

        st.error(f"Error contacting backend: {str(e)}")

# import streamlit as st
# import requests
# import uuid

# API_URL = "http://127.0.0.1:8000/ask"
# SESSION_API = "http://127.0.0.1:8000/session"

# # ---------------------------------------------------
# # Page Config
# # ---------------------------------------------------

# st.set_page_config(
#     page_title="Enterprise Knowledge Assistant",
#     page_icon="📚",
#     layout="wide",
# )

# # ---------------------------------------------------
# # Session Initialization
# # ---------------------------------------------------

# if "session_id" not in st.session_state:
#     st.session_state.session_id = str(uuid.uuid4())

# # ---------------------------------------------------
# # Title
# # ---------------------------------------------------

# st.title("📚 Enterprise Knowledge Assistant")
# st.caption("World Bank Documents + API powered RAG System")

# # ---------------------------------------------------
# # Sidebar
# # ---------------------------------------------------

# with st.sidebar:

#     st.header("Settings")

#     st.caption(f"Session: {st.session_state.session_id[:8]}")

#     # New Chat
#     if st.button("🆕 New Chat"):

#         try:
#             requests.delete(
#                 f"{SESSION_API}/{st.session_state.session_id}",
#                 timeout=10,
#             )
#         except Exception:
#             pass

#         st.session_state.session_id = str(uuid.uuid4())

#         st.rerun()

#     retrieval_method = st.selectbox("Retrieval Method", ["hybrid", "vector", "bm25"])

#     st.info("""
#         Features

#         ✅ World Bank APIs

#         ✅ PDF Documents

#         ✅ Vector Search

#         ✅ BM25 Search

#         ✅ Hybrid Search

#         ✅ Reranking

#         ✅ Citations

#         ✅ Session Memory

#         ✅ Logging & Monitoring
#         """)

# # ---------------------------------------------------
# # Question Input
# # ---------------------------------------------------

# question = st.text_area(
#     "Ask a Question",
#     placeholder="How has India's population changed over the last 10 years?",
#     height=100,
# )

# # ---------------------------------------------------
# # Search Button
# # ---------------------------------------------------

# if st.button("🔍 Search", use_container_width=True):

#     if not question.strip():

#         st.warning("Please enter a question.")
#         st.stop()

#     try:

#         with st.spinner("Searching knowledge base..."):

#             response = requests.post(
#                 API_URL,
#                 json={
#                     "session_id": st.session_state.session_id,
#                     "question": question,
#                     "method": retrieval_method,
#                 },
#                 timeout=120,
#             )

#             response.raise_for_status()

#             data = response.json()

#         answer = data.get("answer", "No answer returned")

#         # -----------------------------------------
#         # Success / No Context Found
#         # -----------------------------------------

#         if answer.strip().lower() == ("i could not find this information."):

#             st.warning("⚠️ No Relevant Context Found")

#         else:

#             st.success("✅ Answer Generated Successfully")

#         # -----------------------------------------
#         # Answer
#         # -----------------------------------------

#         st.subheader("📌 Answer")
#         st.markdown(answer)

#         # -----------------------------------------
#         # Metrics
#         # -----------------------------------------

#         col1, col2, col3 = st.columns(3)

#         col1.metric(
#             "Retrieval Time",
#             f"{data.get('retrieval_time', 0)} sec",
#         )

#         col2.metric(
#             "Generation Time",
#             f"{data.get('generation_time', 0)} sec",
#         )

#         col3.metric(
#             "Total Time",
#             f"{data.get('execution_time', 0)} sec",
#         )

#         # -----------------------------------------
#         # Citations
#         # -----------------------------------------

#         answer_found = data.get(
#             "answer_found",
#             True,
#         )

#         citations = data.get(
#             "citations",
#             [],
#         )

#         if answer_found and citations:

#             st.subheader("📚 Sources & Citations")

#             with st.expander(
#                 "View Supporting Sources",
#                 expanded=True,
#             ):

#                 for i, citation in enumerate(
#                     citations,
#                     start=1,
#                 ):

#                     st.markdown(f"### Source {i}")

#                     source = citation.get(
#                         "source",
#                         "Unknown",
#                     )

#                     page = citation.get("page")
#                     year = citation.get("year")

#                     st.write(f"📄 Source: {source}")

#                     if page:
#                         st.write(f"📑 Page: {page}")

#                     if year:
#                         st.write(f"📅 Year: {year}")

#                     st.divider()

#     except Exception as e:

#         st.error(f"Error contacting backend: {str(e)}")
