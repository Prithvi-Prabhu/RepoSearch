from fastapi import APIRouter
from app.evaluation.evaluator import run_evaluation
from app.evaluation.dataset import EVAL_DATA

router = APIRouter()

METRIC_KEYS = ["faithfulness", "answer_relevancy", "context_precision", "context_recall"]


@router.get("/eval")
def evaluate():
    results = run_evaluation(EVAL_DATA)

    if not results:
        return {"error": "No evaluation results"}

    avg_scores = {
        key: round(sum(r[key] for r in results) / len(results), 4)
        for key in METRIC_KEYS
    }

    # Overall score: equal-weight average of all four metrics
    avg_scores["overall"] = round(
        sum(avg_scores[k] for k in METRIC_KEYS) / len(METRIC_KEYS), 4
    )

    # Per-question keyword hit rate (None if no keywords defined)
    keyword_summary = [
        {
            "question":  r["question"],
            "hit_rate":  r["keyword_match"].get("hit_rate"),
            "hits":      r["keyword_match"].get("hits", {}),
        }
        for r in results
    ]

    return {
        "average_scores": avg_scores,
        "results": results,
        "keyword_summary": keyword_summary,
        "num_samples": len(results),
    }