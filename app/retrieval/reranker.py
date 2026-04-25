model = None

def get_model():
    global model
    if model is None:
        from sentence_transformers import CrossEncoder
        model = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
    return model


def rerank(query, docs, top_k=5):
    if not docs:
        return []

    model = get_model()

    pairs = [(query, d.page_content) for d in docs]
    scores = model.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)
    return [d for d, _ in ranked[:top_k]]
