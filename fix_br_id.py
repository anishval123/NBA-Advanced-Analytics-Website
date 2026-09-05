from pathlib import Path

f = Path('backend/utils/basketball_reference.py')
content = f.read_text()

# Fix table id from per_game to per_game_stats
content = content.replace('id="per_game"', 'id="per_game_stats"')

f.write_text(content)
print("Fixed table id to per_game_stats")