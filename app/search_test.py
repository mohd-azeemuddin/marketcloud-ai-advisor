import sys
import chromadb
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
col = chromadb.PersistentClient(path="data/chroma").get_collection("marketcloud")
q = " ".join(sys.argv[1:])
res = col.query(query_embeddings=model.encode([q], normalize_embeddings=True).tolist(), n_results=3)
for d, m, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
    print(f"\n[{1 - dist:.2f}] {m['source']}\n{d[:300]}")