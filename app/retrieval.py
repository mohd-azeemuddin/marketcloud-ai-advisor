import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

_ef = DefaultEmbeddingFunction()
_col = chromadb.PersistentClient(path="data/chroma").get_collection("marketcloud")

def embed(texts):
    return [list(map(float, e)) for e in _ef(texts)]

def retrieve(query, k=5):
    res = _col.query(query_embeddings=embed([query]), n_results=k)
    return [{"text": d, "source": m["source"], "title": m["title"], "score": round(1 - dist, 3)}
            for d, m, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])]