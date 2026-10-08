import pathlib

roots = [
    pathlib.Path("c:/Users/srini/video-editing-agent/frontend/src"),
    pathlib.Path("c:/Users/srini/video-editing-agent/frontend/index.html"),
    pathlib.Path("c:/Users/srini/video-editing-agent/backend/main.py"),
    pathlib.Path("c:/Users/srini/video-editing-agent/backend/models"),
    pathlib.Path("c:/Users/srini/video-editing-agent/backend/config"),
]
hits = 0
for root in roots:
    files = [root] if root.is_file() else [
        *root.rglob("*.js"), *root.rglob("*.jsx"), *root.rglob("*.py")
    ]
    for f in files:
        if "node_modules" in str(f) or "NflPredictions" in str(f):
            continue
        try:
            txt = f.read_text(encoding="utf-8")
        except Exception:
            continue
        for i, line in enumerate(txt.splitlines(), 1):
            if "\u2014" in line or "\\u2014" in line:
                hits += 1
                print(f"{f}:{i}: {line.strip()[:160]}")
print("TOTAL", hits)
