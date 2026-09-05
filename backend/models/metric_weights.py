METRIC_WEIGHTS = {
    "underrated": {
        "categories": {
            "impact": 0.40,
            "efficiency": 0.25,
            "defense": 0.20,
            "creation": 0.15,
        },
        "impact": {
            "bpm": 0.30,
            "epm": 0.30,
            "on_off": 0.20,
            "win_shares": 0.20,
        },
        "efficiency": {
            "ts_pct": 0.60,
            "turnover_rate": 0.20,
            "offensive_efficiency": 0.20,
        },
        "defense": {
            "dbpm": 0.40,
            "defensive_epm": 0.30,
            "stocks": 0.20,
            "defensive_win_shares": 0.10,
        },
        "creation": {
            "assist_rate": 0.70,
            "other_creation": 0.30,
        },
        "recognition_penalty": {
            "all_star_selections": 0.20,
            "awards": 0.25,
            "jersey_sales": 0.25,
            "career_reputation": 0.20,
            "ppg": 0.10,
        },
        "recognition_penalty_scale": 50.0,
    },
    "overrated": {
        "recognition": {
            "ppg": 0.40,
            "all_star_selections": 0.25,
            "awards": 0.20,
            "usage_rate": 0.15,
        },
        "impact": {
            "bpm": 0.30,
            "epm": 0.30,
            "on_off": 0.20,
            "ts_pct": 0.20,
        },
    },
    "volatility": {
        "categories": {
            "performance_variance": 0.40,
            "shooting_variance": 0.25,
            "impact_variance": 0.25,
            "availability_variance": 0.10,
        },
        "performance_variance": {
            "points_std": 1 / 3,
            "rebounds_std": 1 / 3,
            "assists_std": 1 / 3,
        },
        "shooting_variance": {
            "ts_pct_std": 0.60,
            "three_pct_std": 0.40,
        },
        "impact_variance": {
            "game_score_std": 0.50,
            "plus_minus_std": 0.50,
        },
        "availability_variance": {
            "minutes_std": 0.70,
            "games_missed": 0.30,
        },
    },
    "defensive_chaos": {
        "categories": {
            "defensive_disruption": 0.45,
            "rim_protection": 0.25,
            "defensive_versatility": 0.20,
            "team_defensive_impact": 0.10,
        },
        "defensive_disruption": {
            "steals": 0.30,
            "deflections": 0.30,
            "forced_turnovers": 0.20,
            "loose_balls": 0.20,
        },
        "rim_protection": {
            "blocks": 0.50,
            "rim_defense": 0.50,
        },
        "defensive_versatility": {
            "position_versatility": 0.35,
            "switch_ability": 0.35,
            "matchup_difficulty": 0.30,
        },
        "defensive_versatility_fallback": {
            "defensive_rebounds": 0.45,
            "minutes_guarded_multiple_positions": 0.30,
            "defensive_role": 0.25,
        },
        "team_defensive_impact": {
            "defensive_epm": 1 / 3,
            "defensive_on_off": 1 / 3,
            "team_defensive_rating_impact": 1 / 3,
        },
    },
}


ROLE_COMPRESSION_WEIGHTS = {
    "categories": {
        "playmaking": 0.30,
        "efficiency": 0.30,
        "impact": 0.25,
        "defense": 0.15,
    },
    "playmaking": {
        "assists": 0.50,
        "assist_rate": 0.50,
    },
    "efficiency": {
        "ts_pct": 0.55,
        "turnover_rate": 0.25,
        "usage_rate": 0.20,
    },
    "impact": {
        "on_off": 0.50,
        "bpm": 0.30,
        "win_shares": 0.20,
    },
    "defense": {
        "stocks": 0.60,
        "defensive_win_shares": 0.40,
    },
}


STAT_KEYS = {
    "all_star_selections": ["all_star_selections", "all_stars", "all_star"],
    "assist_rate": ["assist_rate", "ast_pct"],
    "assists": ["assists", "ast"],
    "awards": ["awards"],
    "blocks": ["blocks", "blk"],
    "bpm": ["bpm"],
    "career_reputation": ["career_reputation", "reputation"],
    "dbpm": ["dbpm"],
    "defensive_epm": ["defensive_epm", "d_epm"],
    "defensive_on_off": ["defensive_on_off", "on_off"],
    "defensive_rebounds": ["dreb", "defensive_rebounds"],
    "defensive_role": ["defensive_role"],
    "defensive_win_shares": ["defensive_win_shares", "dws"],
    "deflections": ["deflections"],
    "epm": ["epm"],
    "forced_turnovers": ["forced_turnovers"],
    "jersey_sales": ["jersey_sales", "jersey_rank"],
    "game_score": ["game_score", "gmsc"],
    "loose_balls": ["loose_balls_recovered", "loose_balls"],
    "matchup_difficulty": ["defensive_matchup_difficulty", "matchup_difficulty"],
    "minutes": ["minutes", "min"],
    "minutes_guarded_multiple_positions": ["minutes_guarded_multiple_positions"],
    "offensive_efficiency": ["offensive_efficiency", "ortg"],
    "on_off": ["on_off"],
    "other_creation": ["potential_assists", "usage_adjusted_playmaking"],
    "plus_minus": ["plus_minus", "plus/minus", "plusminus", "+/-"],
    "points": ["points", "pts", "ppg"],
    "points_std": ["points_std"],
    "position_versatility": ["position_versatility", "positional_versatility", "versatility"],
    "rim_defense": ["opponent_fg_pct_at_rim", "rim_contests", "rim_deterrence"],
    "steals": ["steals", "stl"],
    "stocks": ["stocks"],
    "rebounds_std": ["rebounds_std"],
    "assists_std": ["assists_std"],
    "ts_pct_std": ["ts_pct_std"],
    "three_pct_std": ["three_pct_std"],
    "game_score_std": ["game_score_std"],
    "plus_minus_std": ["plus_minus_std"],
    "minutes_std": ["minutes_std"],
    "games_missed": ["games_missed"],
    "box_score_fallback_std": ["box_score_fallback_std"],
    "switch_ability": ["switch_ability"],
    "team_defensive_rating_impact": ["team_defensive_rating_impact", "defensive_rating_impact"],
    "three_pct": ["three_pct", "fg3_pct"],
    "ts_pct": ["ts_pct", "true_shooting_pct"],
    "turnover_rate": ["turnover_rate", "tov_pct"],
    "usage_rate": ["usage_rate", "usage", "usg_pct"],
    "win_shares": ["win_shares", "ws"],
}
