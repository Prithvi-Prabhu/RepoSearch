from app.retrieval.retriever import retrieve
from app.chains.rag_chain import run
from app.utils.helpers import get_repo_id

from app.evaluation.metrics import (
    faithfulness_score,
    answer_relevancy,
    context_precision,
    context_recall
)

# ---------------------------
# Evaluate single sample
# ---------------------------
def evaluate_sample(sample):
    repo_id = get_repo_id(sample["repo_url"])

    docs = retrieve(repo_id, sample["question"])
    answer, _ = run(repo_id, sample["question"])

    # Combine context safely
    context = "\n\n".join([doc.page_content for doc in docs]) if docs else ""

    if not answer:
        print("Empty answer for:", sample["question"])

    results = {
        "question": sample["question"],
        "faithfulness": faithfulness_score(sample["question"], context, answer),
        "answer_relevancy": answer_relevancy(sample["question"], answer),
        "context_precision": context_precision(sample["question"], context),
        "context_recall": context_recall(sample["expected_answer"], context),
    }

    print("Eval Result:", results)
    return results


# ---------------------------
# Run full evaluation
# ---------------------------
def run_evaluation(dataset):
    results = []

    for sample in dataset:
        try:
            results.append(evaluate_sample(sample))
        except Exception as e:
            print("Error evaluating sample:", e)
            results.append({
                "question": sample["question"],
                "faithfulness": 0.0,
                "answer_relevancy": 0.0,
                "context_precision": 0.0,
                "context_recall": 0.0,
            })

    return results