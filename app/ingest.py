import json
from pathlib import Path
from collections import Counter
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction

CHUNK_WORDS, OVERLAP = 180, 30
client = chromadb.PersistentClient(path="data/chroma")
_ef = DefaultEmbeddingFunction()

def chunks(text):
    w = text.split()
    for i in range(0, max(len(w), 1), CHUNK_WORDS - OVERLAP):
        piece = " ".join(w[i:i + CHUNK_WORDS])
        if len(piece.split()) > 25:
            yield piece

KEEP_ALL = ("contact-us", "about-us")

def load_docs():
    raw = [json.loads(f.read_text(encoding="utf-8")) for f in Path("data/raw").glob("*.json")]
    counts = Counter(l for d in raw for l in set(d["text"].split("\n")))
    limit = max(3, int(0.25 * len(raw)))
    for d in raw:
        lines = d["text"].split("\n")
        kept = lines if any(k in d["url"] for k in KEEP_ALL) else [l for l in lines if counts[l] <= limit]
        yield d["url"], d["title"], " ".join(kept)
    for f in Path("data/manual").glob("*.md"):
        yield f"manual:{f.name}", f.stem.replace("_", " ").title(), f.read_text(encoding="utf-8")

def main():
    try:
        client.delete_collection("marketcloud")
    except Exception:
        pass
    col = client.create_collection("marketcloud", metadata={"hnsw:space": "cosine"})
    ids, docs, metas = [], [], []
    for url, title, text in load_docs():
        for c in chunks(text):
            ids.append(str(len(ids))); docs.append(c)
            metas.append({"source": url, "title": title})
    emb = []
    for i in range(0, len(docs), 8):
        emb.extend([list(map(float, e)) for e in _ef(docs[i:i + 8])])
    col.add(ids=ids, documents=docs, metadatas=metas, embeddings=emb)
    print(f"Indexed {len(docs)} chunks")

if __name__ == "__main__":
    main()