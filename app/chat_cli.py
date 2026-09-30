import sys
from app.graph import run

session = {}
for q in sys.argv[1:]:
    r = run(q, session)
    print("\nQ:", q)
    print("A:", r["answer"])
    print("Sources:", r.get("sources"))
    for t in r["trace"]:
        print("  -", t["agent"], "|", t["detail"])