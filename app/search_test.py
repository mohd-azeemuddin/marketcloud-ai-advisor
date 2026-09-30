import sys
from app.retrieval import retrieve

for r in retrieve(" ".join(sys.argv[1:]), k=3):
    print(f"\n[{r['score']:.2f}] {r['source']}\n{r['text'][:300]}")