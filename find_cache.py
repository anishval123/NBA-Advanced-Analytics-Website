import os
from pathlib import Path

# Check for cache files
for root, dirs, files in os.walk('backend'):
    for f in files:
        if f.endswith('.json'):
            path = Path(root) / f
            print(f"Found: {path}")
            if 'cache' in f:
                print(f"  -> This is a cache file!")
                # Read first few lines
                try:
                    content = path.read_text()[:500]
                    print(f"  Content preview: {content[:200]}")
                except:
                    pass