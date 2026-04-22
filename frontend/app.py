import streamlit as st
import requests

API_URL = "http://localhost:8000"

# ------------------ PAGE CONFIG ------------------
st.set_page_config(layout="wide", page_title="RepoSearch: RAG-based Assistant to Query GitHub Repositories", page_icon=":octopus:")

# ------------------ CUSTOM CSS ------------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1220;
    color: white;
    font-family: "Times New Roman", serif;
}

section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.block-container {
    padding-top: 2rem;
}

/* Card styling */
.card {
    background-color: #111827;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
}

/* Inputs */
input, textarea {
    background-color: #1f2937 !important;
    color: white !important;
    border-radius: 6px !important;
}

/* Buttons */
.stButton button {
    background-color: #e11d48;
    color: white;
    border-radius: 6px;
    border: none;
}

/* Section titles */
.section-title {
    font-size: 22px;
    margin-bottom: 10px;
}
            
header[data-testid="stHeader"] {
    background: transparent;
    box-shadow: none;
}
}
            
</style>
""", unsafe_allow_html=True)

# ------------------ SIDEBAR ------------------
st.sidebar.title("Menu")

menu = st.sidebar.selectbox(
    "Navigate",
    ["Query Repo", "Evaluation"]
)

repo_url = st.sidebar.text_input("GitHub Repo URL")

if st.sidebar.button("Ingest"):
    with st.sidebar:
        with st.spinner("Processing..."):
            try:
                r = requests.post(
                    f"{API_URL}/ingest",
                    json={"repo_url": repo_url}
                )
                if r.status_code == 200:
                    st.success("Ingested successfully")
                else:
                    st.error("Failed")
            except Exception as e:
                st.error(str(e))

# ------------------ HOME ------------------
if menu == "Home":
    st.title("RepoSearch: RAG-based Assistant to Query GitHub Repositories")

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("### Overview")
    st.write("""
    - Ingest GitHub repositories  
    - Ask questions using RAG  
    - Evaluate responses with metrics  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ QUERY ------------------
if menu == "Query Repo":

    st.title("Query Repository")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    query = st.text_input("Question")

    if st.button("Submit Query"):
        with st.spinner("Running..."):
            try:
                r = requests.get(
                    f"{API_URL}/query",
                    params={"repo_url": repo_url, "q": query}
                )

                if r.status_code == 200:
                    data = r.json()

                    st.markdown("### Answer")
                    st.write(data.get("answer"))

                    if "sources" in data:
                        st.markdown("### Sources")
                        for s in data["sources"]:
                            st.code(s)

                else:
                    st.error("Query failed")

            except Exception as e:
                st.error(str(e))

    st.markdown('</div>', unsafe_allow_html=True)

# ------------------ EVALUATION ------------------
elif menu == "Evaluation":

    st.title("Evaluation")

    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.button("Run Evaluation"):
        with st.spinner("Evaluating..."):
            try:
                r = requests.get(f"{API_URL}/eval")

                if r.status_code == 200:
                    res = r.json()

                    # If using average_scores format
                    avg = res.get("average_scores", res)

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric("Faithfulness", round(avg.get("faithfulness", 0), 2))
                        st.metric("Answer Relevancy", round(avg.get("answer_relevancy", 0), 2))

                    with col2:
                        st.metric("Context Precision", round(avg.get("context_precision", 0), 2))
                        st.metric("Context Recall", round(avg.get("context_recall", 0), 2))

                else:
                    st.error("Eval failed")

            except Exception as e:
                st.error(str(e))

    st.markdown('</div>', unsafe_allow_html=True)