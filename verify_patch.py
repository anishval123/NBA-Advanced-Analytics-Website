from pathlib import Path

f = Path('backend/main.py')
content = f.read_text()

print("=== Checking patch applied ===")
print("Has basketball_reference import:", "from utils.basketball_reference import get_current_season_players" in content)
print("Has BR primary source comment:", "PRIMARY SOURCE: Basketball Reference" in content)
print("Still has old NBA directory merge:", "directory = get_live_player_directory()" in content and "by_name[key] = {**existing, **player}" in content)

# Show the _load_data function
idx = content.find("def _load_data")
if idx > 0:
    print("\n=== _load_data (first 600 chars) ===")
    print(content[idx:idx+600])