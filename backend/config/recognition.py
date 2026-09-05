"""Curated recognition / exposure data for high-profile players.

These fields feed the Underrated model's `recognition_penalty` so that players
with large public recognition (All-Star selections, major awards, jersey sales,
career reputation) are not mistakenly tagged as "underrated" unless their true
impact genuinely exceeds public perception.
"""

# Normalized player keys (via loader.normalize_name) that should be fully
# excluded from the site (e.g. retired / explicitly removed players).
EXCLUDED_PLAYERS = {
    "russellwestbrook",  # retired
}

# normalized name -> recognition fields.
# - all_star_selections: career All-Star appearances (bigger = more famous)
# - awards: weighted major-award count (MVP, FMVP, DPOY, ROY, All-NBA, ...)
# - career_reputation: 0-1 legacy / superstar standing
# - jersey_sales: 0-1 merch / pop-culture footprint
RECOGNITION_VALUES = {
    "lebronjames": {"all_star_selections": 20, "awards": 4, "career_reputation": 1.0, "jersey_sales": 1.0},
    "stephencurry": {"all_star_selections": 10, "awards": 3, "career_reputation": 0.95, "jersey_sales": 0.9},
    "kevindurant": {"all_star_selections": 14, "awards": 3, "career_reputation": 0.9, "jersey_sales": 0.7},
    "giannisantetokounmpo": {"all_star_selections": 8, "awards": 3, "career_reputation": 0.85, "jersey_sales": 0.6},
    "nikolajokic": {"all_star_selections": 6, "awards": 3, "career_reputation": 0.85, "jersey_sales": 0.4},
    "lukadoncic": {"all_star_selections": 5, "awards": 1, "career_reputation": 0.78, "jersey_sales": 0.5},
    "joelembiid": {"all_star_selections": 4, "awards": 2, "career_reputation": 0.7, "jersey_sales": 0.45},
    "shaigilgeousalexander": {"all_star_selections": 3, "awards": 1, "career_reputation": 0.72, "jersey_sales": 0.5},
    "anthonydavis": {"all_star_selections": 5, "awards": 0, "career_reputation": 0.72, "jersey_sales": 0.5},
    "victorwembanyama": {"all_star_selections": 2, "awards": 2, "career_reputation": 0.82, "jersey_sales": 0.8},
    "kyrieirving": {"all_star_selections": 4, "awards": 0, "career_reputation": 0.7, "jersey_sales": 0.5},
    "jaylenbrown": {"all_star_selections": 2, "awards": 1, "career_reputation": 0.52, "jersey_sales": 0.35},
    "devinbooker": {"all_star_selections": 3, "awards": 0, "career_reputation": 0.62, "jersey_sales": 0.5},
    "damianlillard": {"all_star_selections": 4, "awards": 0, "career_reputation": 0.64, "jersey_sales": 0.4},
    "jamorant": {"all_star_selections": 2, "awards": 0, "career_reputation": 0.62, "jersey_sales": 0.55},
    "kawhileonard": {"all_star_selections": 3, "awards": 1, "career_reputation": 0.7, "jersey_sales": 0.4},
    "paulgeorge": {"all_star_selections": 4, "awards": 0, "career_reputation": 0.6, "jersey_sales": 0.4},
    "jalenbrunson": {"all_star_selections": 2, "awards": 0, "career_reputation": 0.55, "jersey_sales": 0.45},
    "jaysontatum": {"all_star_selections": 5, "awards": 1, "career_reputation": 0.72, "jersey_sales": 0.55},
    "donovanmitchell": {"all_star_selections": 3, "awards": 0, "career_reputation": 0.6, "jersey_sales": 0.4},
}