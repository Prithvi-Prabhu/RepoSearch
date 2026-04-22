from app.retrieval.retriever import retrieve
from app.chains.rag_chain import run
from app.utils.helpers import get_repo_id

from app.evaluation.metrics import (
    faithfulness_score,
    answer_relevancy,
    context_precision,
    context_recall,
)


def _extract_score(result: dict) -> float:
    """Pull numeric score from a metric result dict."""
    return result.get("score", 0.0) if isinstance(result, dict) else float(result)


def _extract_reason(result: dict) -> str:
    return result.get("reason", "") if isinstance(result, dict) else ""


# ─── Evaluate single sample ───────────────────────────────────────────────────

def evaluate_sample(sample: dict) -> dict:
    repo_id = get_repo_id(sample["repo_url"])

    docs = retrieve(repo_id, sample["question"])
    answer, _ = run(repo_id, sample["question"])

    context = "\n\n".join(doc.page_content for doc in docs) if docs else ""

    if not answer:
        print("Warning: empty answer for:", sample["question"])

    faith = faithfulness_score(sample["question"], context, answer)
    rel   = answer_relevancy(sample["question"], answer)
    prec  = context_precision(sample["question"], context)
    rec   = context_recall(sample["expected_answer"], context)

    result = {
        "question":          sample["question"],
        "answer":            answer,
        "faithfulness":      _extract_score(faith),
        "answer_relevancy":  _extract_score(rel),
        "context_precision": _extract_score(prec),
        "context_recall":    _extract_score(rec),
        "reasons": {
            "faithfulness":      _extract_reason(faith),
            "answer_relevancy":  _extract_reason(rel),
            "context_precision": _extract_reason(prec),
            "context_recall":    _extract_reason(rec),
        },
        # keyword check: simple binary pass/fail
        "keyword_match": _keyword_check(answer, sample.get("keywords", [])),
    }

    print("Eval result:", {k: v for k, v in result.items() if k != "answer"})
    return result


def _keyword_check(answer: str, keywords: list[str]) -> dict:
    """
    Checks whether expected keywords appear in the answer.
    Returns per-keyword hits and an overall hit-rate.
    """
    if not keywords:
        return {"hit_rate": None, "hits": {}}

    answer_lower = answer.lower()
    hits = {kw: kw.lower() in answer_lower for kw in keywords}
    hit_rate = sum(hits.values()) / len(hits)
    return {"hit_rate": round(hit_rate, 2), "hits": hits}


# ─── Run full evaluation ──────────────────────────────────────────────────────

def run_evaluation(dataset: list[dict]) -> list[dict]:
    results = []

    for sample in dataset:
        try:
            results.append(evaluate_sample(sample))
        except Exception as e:
            print("Error evaluating sample:", e)
            results.append({
                "question":          sample["question"],
                "answer":            "",
                "faithfulness":      0.0,
                "answer_relevancy":  0.0,
                "context_precision": 0.0,
                "context_recall":    0.0,
                "reasons":           {},
                "keyword_match":     {"hit_rate": 0.0, "hits": {}},
            })

    return results