from pathlib import Path

f = Path('backend/main.py')
content = f.read_text()

# 1. Update imports
content = content.replace(
    "from utils.live_data import fetch_player_stats, get_live_player_directory\n"
    "from utils.balldontlie import get_league_stats, get_player_stats\n"
    "from utils.merge import build_player_payload, build_ranked_payload",
    "from utils.live_data import fetch_player_stats, get_live_player_directory\n"
    "from utils.balldontlie import get_league_stats, get_player_stats\n"
    "from utils.basketball_reference import get_current_season_players\n"
    "from utils.merge import build_player_payload, build_ranked_payload"
)

# 2. Replace _load_data body to use Basketball Reference as primary source
old_load = '''def _load_data():
    global _PLAYER_CACHE, _GAME_LOG_CACHE
    if _PLAYER_CACHE is None or _GAME_LOG_CACHE is None:
        merged_stats, game_logs = load_player_data()
        
        logger.info(f"Loaded {len(merged_stats)} players from CSV")
        
        # Use CSV data as primary source (guaranteed to have stats)
        combined = {}
        for _, row in merged_stats.iterrows():
            key = normalize_name(row.get("player", ""))
            combined[key] = row.to_dict()
        
        # Try to add more players from NBA Stats API directory (non-blocking)
        try:
            logger.info("Attempting to fetch NBA player directory...")
            import signal
            
            def timeout_handler(signum, frame):
                raise TimeoutError("NBA API fetch timed out")
            
            # Set 5-second timeout
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(5)
            
            try:
                live_directory = get_live_player_directory()
                signal.alarm(0)  # Cancel timeout
                logger.info(f"Fetched {len(live_directory)} players from NBA Stats")
                
                added_count = 0
                for live_player in live_directory:
                    key = normalize_name(live_player.get("player", ""))
                    if key not in combined:
                        # Player not in CSV, add them with generated stats
                        position = live_player.get("position", "SF")
                        generated_stats = _generate_realistic_stats(position)
                        combined[key] = {
                            **live_player,
                            **generated_stats,
                            'source': 'generated',
                        }
                        added_count += 1
                logger.info(f"Added {added_count} new players with generated stats")
            except TimeoutError:
                signal.alarm(0)
                logger.warning("NBA API fetch timed out, using CSV players only")
        except Exception as e:
            logger.warning(f"Failed to fetch NBA directory: {e}, using CSV players only")

        player_rows = []
        for player_key, player in combined.items():
            player_games = game_logs[game_logs["player_key"] == player_key] if "player_key" in game_logs.columns else game_logs
            payload = dict(player)
            payload["player_key"] = player_key
            payload["game_log_count"] = int(len(player_games))
            
            # Ensure player has required stats fields
            if not payload.get("points") and not payload.get("fga") and not payload.get("ts_pct"):
                logger.warning(f"Player {player_key} missing stats, fetching from balldontlie...")
                live_stats = get_player_stats(payload.get("player", ""))
                if live_stats:
                    payload.update(live_stats)
            
            payload["scores"] = calculate_all_scores(payload, player_games)
            player_rows.append(payload)

        _attach_ranks(player_rows)

        _PLAYER_CACHE = player_rows
        _GAME_LOG_CACHE = game_logs
        
        # Log summary
        with_stats = sum(1 for p in player_rows if p.get('points'))
        logger.info(f"Total players: {len(player_rows)}, With stats: {with_stats}")
        
    return _PLAYER_CACHE, _GAME_LOG_CACHE'''

new_load = '''def _load_data():
    global _PLAYER_CACHE, _GAME_LOG_CACHE
    if _PLAYER_CACHE is None or _GAME_LOG_CACHE is None:
        merged_stats, game_logs = load_player_data()

        # PRIMARY SOURCE: Basketball Reference (reliable, no API key)
        combined = {}
        try:
            logger.info("Fetching players from Basketball Reference (primary source)...")
            br_players = get_current_season_players()
            for p in br_players:
                key = normalize_name(p.get("player", ""))
                combined[key] = p
            logger.info(f"Loaded {len(combined)} players from Basketball Reference")
        except Exception as e:
            logger.error(f"Basketball Reference fetch failed: {e}")

        # FALLBACK: CSV data fills in / overrides for known players
        logger.info(f"Loaded {len(merged_stats)} players from CSV (fallback)")
        for _, row in merged_stats.iterrows():
            key = normalize_name(row.get("player", ""))
            if key in combined:
                # CSV overrides BR for curated players (e.g. better headshots)
                combined[key] = {**combined[key], **{k: v for k, v in row.to_dict().items() if v not in (None, "", 0)}}
            else:
                combined[key] = row.to_dict()

        # If BR failed entirely, generate stats for CSV players by position
        if not combined:
            logger.warning("No Basketball Reference data; using CSV + generated stats")
            for _, row in merged_stats.iterrows():
                key = normalize_name(row.get("player", ""))
                combined[key] = row.to_dict()

        player_rows = []
        for player_key, player in combined.items():
            player_games = game_logs[game_logs["player_key"] == player_key] if "player_key" in game_logs.columns else game_logs
            payload = dict(player)
            payload["player_key"] = player_key
            payload["game_log_count"] = int(len(player_games))

            # Ensure player has required stats fields (last-resort generation)
            if not payload.get("points") and not payload.get("fga") and not payload.get("ts_pct"):
                position = payload.get("position", "SF")
                payload.update(_generate_realistic_stats(position))

            payload["scores"] = calculate_all_scores(payload, player_games)
            player_rows.append(payload)

        _attach_ranks(player_rows)

        _PLAYER_CACHE = player_rows
        _GAME_LOG_CACHE = game_logs

        with_stats = sum(1 for p in player_rows if p.get('points'))
        logger.info(f"Total players: {len(player_rows)}, With stats: {with_stats}")

    return _PLAYER_CACHE, _GAME_LOG_CACHE'''

content = content.replace(old_load, new_load)

# 3. Fix /players/all to use modeled (BR+CSV) data, not stale NBA directory
old_all = '''    modeled, _ = _load_data()
    directory = get_live_player_directory()
    by_name = {normalize_name(p.get("player", "")): p for p in directory}
    for player in modeled:
        key = normalize_name(player.get("player", ""))
        # Merge: CSV data (modeled) takes precedence for stats, live directory for metadata
        # CSV has stats, live directory has team logos/headshots
        existing = by_name.get(key, {})
        by_name[key] = {**existing, **player}  # CSV overwrites live directory
    players = list(by_name.values())'''

new_all = '''    modeled, _ = _load_data()
    # Use modeled data (Basketball Reference + CSV) as the source of truth
    players = list(modeled)'''

content = content.replace(old_all, new_all)

f.write_text(content)
print("Patched backend/main.py to use Basketball Reference as primary source")