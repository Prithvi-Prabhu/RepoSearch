from fastapi import APIRouter
from app.evaluation.evaluator import run_evaluation
from app.evaluation.dataset import EVAL_DATA

router = APIRouter()

@router.get("/eval")
def evaluate():
    results = run_evaluation(EVAL_DATA)

    if not results:
        return {"error": "No evaluation results"}

    avg_scores = {
        "faithfulness": sum(r["faithfulness"] for r in results) / len(results),
        "answer_relevancy": sum(r["answer_relevancy"] for r in results) / len(results),
        "context_precision": sum(r["context_precision"] for r in results) / len(results),
        "context_recall": sum(r["context_recall"] for r in results) / len(results),
    }

    return {
        "average_scores": avg_scores,
        "results": results
    }