import re

# Read the current file content
from pathlib import Path
f = Path('backend/utils/basketball_reference.py')
content = f.read_text()

# Fix: strip HTML comments before parsing the table
old = '''    table_match = re.search(r'<table[^>]*id="per_game"[^>]*>(.*?)</table>', html, re.DOTALL)
    if not table_match:
        # Try broader match
        table_match = re.search(r'<table[^>]*id="per_game".*?</table>', html, re.DOTALL)
    if not table_match:
        logger.warning("Could not find per_game table in HTML")
        return []'''

new = '''    # Basketball Reference wraps tables in HTML comments to hide from bots.
    # Strip comment markers so the table HTML is parseable.
    html = html.replace("<!--", "").replace("-->", "")

    table_match = re.search(r'<table[^>]*id="per_game"[^>]*>(.*?)</table>', html, re.DOTALL)
    if not table_match:
        # Try broader match
        table_match = re.search(r'<table[^>]*id="per_game".*?</table>', html, re.DOTALL)
    if not table_match:
        logger.warning("Could not find per_game table in HTML")
        return []'''

content = content.replace(old, new)
f.write_text(content)
print("Patched parser to strip HTML comments")