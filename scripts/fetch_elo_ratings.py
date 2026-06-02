"""
Real Elo rating fetcher — updates teams.csv with live data.
Source: eloratings.net (public, no API key required)

Usage:
    python scripts/fetch_elo_ratings.py

Run this weekly to keep ratings current. Gracefully falls back to
existing sample data if the fetch fails.
"""

import os
import time
import pandas as pd
import urllib.request
from html.parser import HTMLParser

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "teams.csv")
ELO_URL   = "https://www.eloratings.net/en.xml"   # public XML feed

# Mapping from Elo site team names to our CSV team names
NAME_MAP = {
    "Argentina":     "Argentina",
    "France":        "France",
    "Brazil":        "Brazil",
    "England":       "England",
    "Spain":         "Spain",
    "Portugal":      "Portugal",
    "Germany":       "Germany",
    "Netherlands":   "Netherlands",
    "Belgium":       "Belgium",
    "Croatia":       "Croatia",
    "Italy":         "Italy",
    "Uruguay":       "Uruguay",
    "Colombia":      "Colombia",
    "United States": "USA",
    "Mexico":        "Mexico",
    "Canada":        "Canada",
    "Japan":         "Japan",
    "South Korea":   "South Korea",
    "Morocco":       "Morocco",
    "Senegal":       "Senegal",
    "Ghana":         "Ghana",
    "Australia":     "Australia",
    "Switzerland":   "Switzerland",
    "Denmark":       "Denmark",
    "Serbia":        "Serbia",
    "Poland":        "Poland",
    "Ecuador":       "Ecuador",
    "Chile":         "Chile",
    "South Africa":  "South Africa",
    "Turkey":        "Turkey",
    "Paraguay":      "Paraguay",
    "Austria":       "Austria",
}


class EloXMLParser(HTMLParser):
    """Simple XML parser for eloratings.net feed."""
    def __init__(self):
        super().__init__()
        self.ratings = {}
        self._current_name = None
        self._current_rating = None
        self._in_name = False
        self._in_rating = False

    def handle_starttag(self, tag, attrs):
        if tag == "name":     self._in_name = True
        if tag == "rating":   self._in_rating = True

    def handle_endtag(self, tag):
        if tag == "name":     self._in_name = False
        if tag == "rating":   self._in_rating = False
        if tag == "team" and self._current_name and self._current_rating:
            self.ratings[self._current_name] = self._current_rating
            self._current_name = None
            self._current_rating = None

    def handle_data(self, data):
        if self._in_name:   self._current_name = data.strip()
        if self._in_rating:
            try: self._current_rating = int(data.strip())
            except ValueError: pass


def fetch_elo_ratings() -> dict:
    """Fetch live Elo ratings. Returns {team_name: elo_rating}."""
    print("Fetching Elo ratings from eloratings.net ...")
    try:
        req = urllib.request.Request(ELO_URL, headers={"User-Agent": "WorldCupMatchLab/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml = resp.read().decode("utf-8")
        parser = EloXMLParser()
        parser.feed(xml)
        print(f"  Fetched {len(parser.ratings)} team ratings")
        return parser.ratings
    except Exception as e:
        print(f"  Fetch failed: {e}")
        return {}


def update_teams_csv(elo_ratings: dict) -> int:
    """Merge fetched Elo ratings into teams.csv. Returns count of updates."""
    if not os.path.exists(DATA_PATH):
        print(f"  teams.csv not found at {DATA_PATH}")
        return 0

    df = pd.read_csv(DATA_PATH)
    updated = 0

    for elo_name, csv_name in NAME_MAP.items():
        if elo_name in elo_ratings and csv_name in df["team"].values:
            new_elo = elo_ratings[elo_name]
            old_elo = df.loc[df["team"] == csv_name, "elo"].values[0]
            df.loc[df["team"] == csv_name, "elo"] = new_elo
            print(f"  {csv_name}: {old_elo} → {new_elo}")
            updated += 1

    df.to_csv(DATA_PATH, index=False)
    print(f"\n✅ Updated {updated} teams in {DATA_PATH}")
    return updated


if __name__ == "__main__":
    ratings = fetch_elo_ratings()
    if ratings:
        update_teams_csv(ratings)
    else:
        print("Using existing sample Elo data — no changes made.")
    print("\nDeploy tip: Add a GitHub Action to run this weekly:")
    print("  cron: '0 6 * * 1'  # Every Monday at 6am UTC")
