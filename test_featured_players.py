import requests

base_url = 'http://127.0.0.1:8000'

print("Testing Featured Players Logic")
print("=" * 60)

try:
    # Fetch all ranking endpoints
    underrated = requests.get(f'{base_url}/underrated', timeout=5).json()
    overrated = requests.get(f'{base_url}/overrated', timeout=5).json()
    volatility = requests.get(f'{base_url}/volatility', timeout=5).json()
    role_compression = requests.get(f'{base_url}/role_compression', timeout=5).json()
    defense = requests.get(f'{base_url}/defensive_chaos', timeout=5).json()
    
    # Create featured players array (same logic as Home.jsx)
    featured = [
        { **underrated[0], 'category': 'Most Underrated', 'color': 'from-cyan-500 to-blue-600' },
        { **overrated[0], 'category': 'Most Overrated', 'color': 'from-rose-500 to-orange-500' },
        { **volatility[0], 'category': 'Most Volatile', 'color': 'from-amber-400 to-orange-600' },
        { **role_compression[0], 'category': 'Best Role Fit', 'color': 'from-violet-500 to-fuchsia-600' },
        { **defense[0], 'category': 'Defensive Chaos', 'color': 'from-emerald-500 to-teal-600' },
    ]
    
    featured = [p for p in featured if p and p.get('player')]
    
    print(f"\nFeatured Players ({len(featured)} total):")
    print("-" * 60)
    for i, player in enumerate(featured, 1):
        print(f"\n{i}. {player['category']}")
        print(f"   Player: {player.get('player')}")
        print(f"   Team: {player.get('team')}")
        print(f"   Position: {player.get('position')}")
        print(f"   Score: {player.get('score', 0):.2f}")
        print(f"   Points: {player.get('points')}")
        print(f"   Assists: {player.get('assists')}")
        print(f"   Headshot: {'✓' if player.get('headshot') else '✗'}")
    
    print("\n" + "=" * 60)
    print("✓ Featured players now show #1 ranked from each category")
    
except Exception as e:
    print(f"\n✗ ERROR: {e}")
    import traceback
    traceback.print_exc()