import sys
from pathlib import Path
sys.path.append(str(Path('backend').resolve()))

from data.loader import load_player_data

print("Checking CSV Data")
print("=" * 80)

df, logs = load_player_data()

print(f"\nTotal players in CSV: {len(df)}")
print(f"Columns: {list(df.columns)}")

print("\nFirst 3 players:")
for i, row in df.head(3).iterrows():
    print(f"\n{i+1}. {row.get('player')}")
    print(f"   Points: {row.get('points')}")
    print(f"   Rebounds: {row.get('rebounds')}")
    print(f"   Assists: {row.get('assists')}")
    print(f"   Team: {row.get('team')}")

print("\n" + "=" * 80)