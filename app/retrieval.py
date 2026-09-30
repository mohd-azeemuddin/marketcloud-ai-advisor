import chromadb
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("all-MiniLM-L6-v2")
_col = chromadb.PersistentClient(path="data/chroma").get_collection("marketcloud")

def retrieve(query, k=5):
    res = _col.query(query_embeddings=_model.encode([query], normalize_embeddings=True).tolist(), n_results=k)
    return [{"text": d, "source": m["source"], "title": m["title"], "score": round(1 - dist, 3)}
            for d, m, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])]
