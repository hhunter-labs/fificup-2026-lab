"""Data loading utilities for World Cup Match Lab."""

import os
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_teams() -> pd.DataFrame:
    """Load team data with fallback to minimal inline sample."""
    path = os.path.join(DATA_DIR, "teams.csv")
    try:
        df = pd.read_csv(path)
        df = df.fillna(0)
        return df
    except Exception:
        # Minimal inline fallback
        return pd.DataFrame({
            "team": ["Argentina", "France", "Brazil", "England", "Spain"],
            "flag": ["🇦🇷", "🇫🇷", "🇧🇷", "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "🇪🇸"],
            "confederation": ["CONMEBOL", "UEFA", "CONMEBOL", "UEFA", "UEFA"],
            "elo": [2142, 2127, 2112, 2054, 2048],
            "power_score": [94, 93, 92, 88, 87],
            "attack": [91, 93, 94, 87, 83],
            "defense": [88, 87, 85, 84, 86],
            "midfield": [90, 91, 92, 86, 90],
            "goalkeeping": [89, 88, 86, 85, 82],
            "depth": [85, 90, 82, 86, 80],
            "recent_form": [92, 90, 88, 85, 86],
            "tournament_experience": [97, 95, 96, 90, 88],
            "volatility": [25, 28, 30, 35, 22],
            "style_tag": [
                "Total Football", "Counter-Attack Kings",
                "Samba Magic", "Press & Pace", "Tiki-Taka Evolved"
            ],
        })


def load_venues() -> pd.DataFrame:
    """Load venue/city data with fallback."""
    path = os.path.join(DATA_DIR, "venues.csv")
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return pd.DataFrame({
            "city": ["New York/New Jersey", "Los Angeles", "Dallas", "Miami", "Mexico City"],
            "country": ["USA", "USA", "USA", "USA", "Mexico"],
            "lat": [40.814, 34.016, 32.748, 25.958, 19.303],
            "lon": [-74.075, -118.287, -96.808, -80.239, -99.151],
            "altitude_category": ["Low", "Low", "Low", "Low", "High"],
            "climate_vibe": ["Variable", "Sunny & Warm", "Hot & Dry", "Tropical", "Mild"],
            "travel_burden": [2, 2, 3, 3, 4],
            "crowd_energy": [92, 90, 87, 89, 91],
            "heat_impact": [4, 5, 9, 8, 3],
            "altitude_impact": [1, 1, 1, 1, 10],
            "description": ["The Final venue.", "LA sunshine.", "Texas heat.", "Tropical energy.", "Legendary altitude."],
        })


def load_sample_matches() -> pd.DataFrame:
    """Load sample match data with fallback."""
    path = os.path.join(DATA_DIR, "sample_matches.csv")
    try:
        df = pd.read_csv(path)
        return df
    except Exception:
        return pd.DataFrame({
            "team_a": ["Argentina", "Brazil", "France"],
            "team_b": ["France", "England", "Spain"],
            "venue": ["New York/New Jersey", "Los Angeles", "Dallas"],
            "round": ["Final", "Semifinal", "Quarterfinal"],
            "team_a_rest_days": [7, 4, 4],
            "team_b_rest_days": [7, 4, 4],
        })


def get_team_row(teams_df: pd.DataFrame, team_name: str) -> pd.Series:
    """Safely fetch a team row by name."""
    match = teams_df[teams_df["team"] == team_name]
    if len(match) == 0:
        raise ValueError(f"Team '{team_name}' not found in dataset.")
    return match.iloc[0]


def get_venue_row(venues_df: pd.DataFrame, city_name: str) -> pd.Series:
    """Safely fetch a venue row by city name."""
    match = venues_df[venues_df["city"] == city_name]
    if len(match) == 0:
        return None
    return match.iloc[0]
