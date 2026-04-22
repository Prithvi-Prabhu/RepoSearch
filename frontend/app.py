import streamlit as st
import requests

# ---------------- PAGE CONFIG ---------------- #
st.set_page_config(
    page_title="Repo RAG Assistant",
    layout="wide",
    page_icon="🤖"
)

# ---------------- CUSTOM CSS ---------------- #
st.markdown("""
<style>
/* Global font + spacing */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Chat bubbles */
.chat-user {
    background-color: #1f2937;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 8px;
}

.chat-assistant {
    background-color: #111827;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 12px;
}

/* Sidebar styling */
section[data-testid="stSidebar"] {
    background-color: #0f172a;
}

/* Buttons */
button {
    border-radius: 8px !important;
}

/* Metric cards */
[data-testid="metric-container"] {
    background-color: #111827;
    padding: 10px;
    border-radius: 10px;
}

/* Hide Streamlit footer */
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ---------------- #
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- SIDEBAR ---------------- #
with st.sidebar:
    st.title("📥 Repo Ingestion")

    repo = st.text_input("GitHub Repo URL")

    if st.button("Ingest Repo"):
        if not repo:
            st.warning("Enter a repo URL")
        else:
            with st.spinner("Indexing repository..."):
                try:
                    r = requests.post(
                        "http://localhost:8000/ingest",
                        json={"repo_url": repo}
                    )
                    if r.ok:
                        st.success("✅ Repo indexed successfully!")
                    else:
                        st.error(r.text)
                except:
                    st.error("Backend not running!")

    st.divider()

    st.markdown("### ⚙️ Settings")
    st.caption("Local embeddings + FAISS")

# ---------------- MAIN LAYOUT ---------------- #
col1, col2 = st.columns([3, 1])

# ---------------- CHAT PANEL ---------------- #
with col1:
    st.title("💬 Repo RAG Assistant")
    st.caption("Ask questions about any GitHub repository")

    # Chat input
    query = st.chat_input("Ask something about the repo...")

    if query:
        st.session_state.history.append(("user", query))

        with st.spinner("Thinking..."):
            try:
                r = requests.get(
                    "http://localhost:8000/query",
                    params={"repo_url": repo, "q": query}
                )

                if r.ok:
                    res = r.json()
                    answer = res["answer"]
                    sources = res.get("sources", [])

                    st.session_state.history.append(("assistant", answer, sources))
                else:
                    st.session_state.history.append(
                        ("assistant", f"Error: {r.text}", [])
                    )

            except:
                st.session_state.history.append(
                    ("assistant", "Backend not running!", [])
                )

    # Display chat history
    for item in st.session_state.history:
        if item[0] == "user":
            with st.chat_message("user"):
                st.markdown(item[1])
        else:
            with st.chat_message("assistant"):
                st.markdown(item[1])

                # Sources (expandable)
                if len(item) > 2 and item[2]:
                    with st.expander("📄 Sources"):
                        for s in item[2]:
                            st.write(s)

# ---------------- METRICS PANEL ---------------- #
with col2:
    st.title("📊 Evaluation")

    if st.button("Run Evaluation"):
        with st.spinner("Running evaluation..."):
            try:
                r = requests.get("http://localhost:8000/eval")

                if r.ok:
                    res = r.json()

                    st.metric("Faithfulness", res.get("faithfulness", "N/A"))
                    st.metric("Answer Relevance", res.get("answer_relevance", "N/A"))
                    st.metric("Context Recall", res.get("context_recall", "N/A"))

                else:
                    st.error("Eval failed")

            except:
                st.error("Backend not running")

    st.divider()

    st.markdown("### 🧠 System Info")
    st.caption("""
    - FAISS Vector DB  
    - Local Embeddings  
    - Groq LLM  
    - LangSmith Logging  
    """)
