import streamlit as st
import requests
import time

API_URL = "http://localhost:8000"

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="RepoSearch",
    page_icon="🐙",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Roboto:wght@400;500;700;900&display=swap');

:root {
    --bg:       #0c0a0a;
    --surface:  #161010;
    --surface2: #1e1515;
    --border:   #2e1f1f;
    --accent:   #800020;
    --accent-l: #a0002a;
    --accent-d: #5c0016;
    --accent2:  #c0392b;
    --danger:   #e74c3c;
    --text:     #f0e8e8;
    --muted:    #7a6060;
    --success:  #27ae60;
}

html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* Hide streamlit chrome individually — never hide header wholesale */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent !important; }

/* Force sidebar always open */
section[data-testid="stSidebar"] {
    transform: none !important;
    visibility: visible !important;
    display: block !important;
    background: var(--surface) !important;
    border-right: 2px solid var(--accent-d) !important;
    min-width: 260px !important;
    width: 260px !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

/* Hide only the collapse arrow, not the whole header */
button[data-testid="collapsedControl"] { display: none !important; }
section[data-testid="stSidebar"] > div:first-child > button { display: none !important; }

.block-container { padding: 2rem 2rem 4rem; }

/* Logo */
.logo {
    font-size: 24px;
    font-weight: 900;
    letter-spacing: -0.5px;
    color: var(--text);
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 24px;
}
.logo span { color: var(--accent2); }

/* Section labels in sidebar */
.sidebar-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin: 16px 0 6px;
}

/* Cards — heavier borders, more padding */
.card {
    background: var(--surface);
    border: 2px solid var(--border);
    border-radius: 10px;
    padding: 22px 26px;
    margin-bottom: 18px;
}
.card-accent {
    border-left: 4px solid var(--accent) !important;
}

/* Metric tiles — stronger visual weight */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 14px;
    margin: 18px 0;
}
.metric-tile {
    background: var(--surface2);
    border: 2px solid var(--border);
    border-radius: 10px;
    padding: 20px 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.metric-tile::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
}
.metric-tile .val {
    font-size: 36px;
    font-weight: 900;
    font-family: 'JetBrains Mono', monospace;
    line-height: 1;
}
.metric-tile .lbl {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 8px;
}
.good { color: var(--success); }
.ok   { color: #e67e22; }
.bad  { color: var(--danger); }

/* Score bars — taller, heavier */
.score-bar-wrap { margin: 10px 0; }
.score-bar-label {
    display: flex;
    justify-content: space-between;
    font-size: 12px;
    font-weight: 700;
    color: var(--muted);
    margin-bottom: 5px;
}
.score-bar-bg {
    background: var(--border);
    border-radius: 3px;
    height: 8px;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 3px;
    transition: width 0.6s ease;
}

/* Keyword badges */
.kw-hit  { background:#0d3b26; color:#6ee7b7; padding:3px 10px; border-radius:4px; font-size:12px; font-weight:700; margin:2px; display:inline-block; border:1px solid #1a6645; }
.kw-miss { background:#3b0d0d; color:#fca5a5; padding:3px 10px; border-radius:4px; font-size:12px; font-weight:700; margin:2px; display:inline-block; border:1px solid #6b1a1a; }

/* Source pills — maroon tones */
.source-pill {
    background: #2a0a10;
    border: 1px solid var(--accent-d);
    border-radius: 6px;
    padding: 4px 12px;
    font-size: 12px;
    font-weight: 500;
    font-family: 'JetBrains Mono', monospace;
    color: #e08090;
    margin: 3px 2px;
    display: inline-block;
    word-break: break-all;
}

/* Buttons — solid maroon, heavy */
.stButton button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Roboto', sans-serif !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
    padding: 0.55rem 1.4rem !important;
    transition: background 0.15s;
    box-shadow: 0 2px 8px rgba(128,0,32,0.4) !important;
}
.stButton button:hover {
    background: var(--accent-l) !important;
}
.stButton button:active {
    background: var(--accent-d) !important;
}

/* Inputs */
.stTextInput input {
    background: var(--surface2) !important;
    color: var(--text) !important;
    border: 2px solid var(--border) !important;
    border-radius: 6px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 13px !important;
}
.stTextInput input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(128,0,32,0.2) !important;
}
.stSelectbox > div > div {
    background: var(--surface2) !important;
    border: 2px solid var(--border) !important;
    border-radius: 6px !important;
    color: var(--text) !important;
    font-weight: 500 !important;
}

/* Headings */
h1, h2, h3 {
    font-family: 'Roboto', sans-serif !important;
    font-weight: 900 !important;
    letter-spacing: -0.3px;
}

/* Answer block */
.answer-block {
    background: var(--surface2);
    border: 2px solid var(--border);
    border-left: 4px solid var(--accent);
    border-radius: 8px;
    padding: 20px;
    font-size: 14px;
    font-weight: 400;
    line-height: 1.75;
    white-space: pre-wrap;
    margin-top: 12px;
}

/* Divider */
hr { border-color: var(--border) !important; border-width: 1px !important; }

/* Expander */
[data-testid="stExpander"] {
    border: 2px solid var(--border) !important;
    border-radius: 8px !important;
    background: var(--surface) !important;
}
[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    font-size: 14px !important;
}
</style>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def score_class(v: float) -> str:
    if v >= 0.75: return "good"
    if v >= 0.45: return "ok"
    return "bad"

def bar_color(v: float) -> str:
    if v >= 0.75: return "#10b981"
    if v >= 0.45: return "#f59e0b"
    return "#f43f5e"

def score_bar(label: str, value: float):
    pct = int(value * 100)
    color = bar_color(value)
    st.markdown(f"""
    <div class="score-bar-wrap">
      <div class="score-bar-label"><span>{label}</span><span>{pct}%</span></div>
      <div class="score-bar-bg">
        <div class="score-bar-fill" style="width:{pct}%; background:{color};"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def metric_tile(label: str, value: float):
    cls = score_class(value)
    pct = f"{int(value * 100)}%"
    return f"""
    <div class="metric-tile">
      <div class="val {cls}">{pct}</div>
      <div class="lbl">{label}</div>
    </div>"""

def call_api(method: str, path: str, **kwargs):
    try:
        fn = requests.get if method == "GET" else requests.post
        r = fn(f"{API_URL}{path}", timeout=60, **kwargs)
        if r.status_code == 429:
            return None, "Rate limit hit — please wait a moment and try again."
        if r.status_code != 200:
            return None, f"API error {r.status_code}: {r.text[:200]}"
        return r.json(), None
    except requests.exceptions.ConnectionError:
        return None, "Cannot connect to the API. Is the backend running?"
    except Exception as e:
        return None, str(e)


# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown('<div class="logo"> Repo<span style="color:#c0392b;">Search</span></div>', unsafe_allow_html=True)

    menu = st.selectbox("Navigate", ["Query Repo", "Evaluation"], label_visibility="collapsed")

    st.markdown("---")
    st.markdown("**GitHub Repo URL**")
    repo_url = st.text_input(
        "repo_url",
        placeholder="https://github.com/owner/repo",
        label_visibility="collapsed"
    )

    ingest_btn = st.button("⬆ Ingest Repo", use_container_width=True)
    if ingest_btn:
        if not repo_url:
            st.error("Enter a repo URL first.")
        else:
            with st.spinner("Cloning and indexing…"):
                data, err = call_api("POST", "/ingest", json={"repo_url": repo_url})
            if err:
                st.error(err)
            elif data.get("status") == "already indexed":
                st.info("Already indexed ✓")
            else:
                files = data.get("files", "?")
                st.success(f"Indexed {files} files ✓")

    st.markdown("---")
    st.caption("Powered by Groq · FAISS · LangChain")


# ── Query page ────────────────────────────────────────────────────────────────

if menu == "Query Repo":
    st.markdown("## Ask a question about a repository")

    st.markdown('<div class="card card-accent">', unsafe_allow_html=True)

    query_text = st.text_input(
        "Your question",
        placeholder="e.g. How does authentication work in this codebase?",
    )

    submit = st.button("Submit →")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        if not repo_url:
            st.warning("Set a GitHub repo URL in the sidebar first.")
        elif not query_text:
            st.warning("Enter a question.")
        else:
            with st.spinner("Searching and generating answer…"):
                t0 = time.time()
                data, err = call_api(
                    "GET", "/query",
                    params={"repo_url": repo_url, "q": query_text}
                )
                elapsed = round(time.time() - t0, 1)

            if err:
                st.error(err)
            else:
                answer = data.get("answer", "")
                sources = data.get("sources", [])

                st.markdown(f"**Answer** <span style='color:var(--muted);font-size:12px;margin-left:8px;'>{elapsed}s</span>", unsafe_allow_html=True)
                st.markdown(f'<div class="answer-block">{answer}</div>', unsafe_allow_html=True)

                if sources:
                    st.markdown("**Sources retrieved**")
                    seen = set()
                    pills = ""
                    for s in sources:
                        f = s.get("file", "")
                        if f and f not in seen:
                            seen.add(f)
                            short = f.split("/tmp/")[-1] if "/tmp/" in f else f
                            pills += f'<span class="source-pill">{short}</span>'
                    if pills:
                        st.markdown(pills, unsafe_allow_html=True)


# ── Evaluation page ───────────────────────────────────────────────────────────

elif menu == "Evaluation":
    st.markdown("## RAG Evaluation Dashboard")
    st.markdown("Runs your evaluation dataset through the full retrieval + generation pipeline and scores each metric using an LLM judge.")

    run_btn = st.button("▶ Run Evaluation")

    if run_btn:
        with st.spinner("Evaluating all samples — this may take a minute…"):
            data, err = call_api("GET", "/eval")

        if err:
            st.error(err)
        else:
            avg = data.get("average_scores", {})
            results = data.get("results", [])
            kw_summary = data.get("keyword_summary", [])
            n = data.get("num_samples", len(results))

            # ── Overall score banner ──────────────────────────────────────────
            overall = avg.get("overall", 0)
            overall_cls = score_class(overall)
            st.markdown(f"""
            <div class="card" style="text-align:center; margin-bottom: 24px;">
              <div style="font-size:13px; letter-spacing:2px; text-transform:uppercase; color:var(--muted); margin-bottom:6px;">Overall Score</div>
              <div style="font-size:56px; font-weight:800; font-family:'JetBrains Mono',monospace;" class="{overall_cls}">{int(overall*100)}%</div>
              <div style="font-size:13px; color:var(--muted); margin-top:6px;">{n} sample{"s" if n!=1 else ""} evaluated</div>
            </div>
            """, unsafe_allow_html=True)

            # ── 4 metric tiles ────────────────────────────────────────────────
            tiles_html = '<div class="metric-grid">'
            for key, label in [
                ("faithfulness",      "Faithfulness"),
                ("answer_relevancy",  "Answer Relevancy"),
                ("context_precision", "Context Precision"),
                ("context_recall",    "Context Recall"),
            ]:
                tiles_html += metric_tile(label, avg.get(key, 0))
            tiles_html += "</div>"
            st.markdown(tiles_html, unsafe_allow_html=True)

            # ── Score bars ────────────────────────────────────────────────────
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown("**Metric breakdown**")
            for key, label in [
                ("faithfulness",      "Faithfulness — answer grounded in context"),
                ("answer_relevancy",  "Answer Relevancy — question answered directly"),
                ("context_precision", "Context Precision — retrieved docs are on-topic"),
                ("context_recall",    "Context Recall — context covers expected answer"),
            ]:
                score_bar(label, avg.get(key, 0))
            st.markdown("</div>", unsafe_allow_html=True)

            # ── Keyword hit rate ──────────────────────────────────────────────
            if kw_summary and any(k.get("hit_rate") is not None for k in kw_summary):
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.markdown("**Keyword hit rate** — do answers contain expected terms?")
                for item in kw_summary:
                    rate = item.get("hit_rate")
                    if rate is None:
                        continue
                    q = item["question"]
                    hits = item.get("hits", {})
                    st.markdown(f"**{q}** — {int(rate*100)}% keywords matched")
                    badges = ""
                    for kw, hit in hits.items():
                        cls = "kw-hit" if hit else "kw-miss"
                        icon = "✓" if hit else "✗"
                        badges += f'<span class="{cls}">{icon} {kw}</span>'
                    st.markdown(badges, unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Per-question detail ───────────────────────────────────────────
            st.markdown("### Per-question results")
            for i, r in enumerate(results, 1):
                with st.expander(f"Q{i}: {r['question']}"):
                    # Mini score bars
                    for key, label in [
                        ("faithfulness",      "Faithfulness"),
                        ("answer_relevancy",  "Relevancy"),
                        ("context_precision", "Precision"),
                        ("context_recall",    "Recall"),
                    ]:
                        score_bar(label, r.get(key, 0))

                    # LLM reasons
                    reasons = r.get("reasons", {})
                    if any(reasons.values()):
                        st.markdown("**LLM judge reasoning**")
                        for key, label in [
                            ("faithfulness",      "Faithfulness"),
                            ("answer_relevancy",  "Relevancy"),
                            ("context_precision", "Precision"),
                            ("context_recall",    "Recall"),
                        ]:
                            reason = reasons.get(key, "")
                            if reason:
                                st.caption(f"**{label}:** {reason}")

                    # Generated answer
                    ans = r.get("answer", "")
                    if ans:
                        st.markdown("**Generated answer**")
                        st.markdown(f'<div class="answer-block" style="font-size:13px;">{ans}</div>', unsafe_allow_html=True)