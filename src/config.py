"""Global configuration and constants for World Cup Match Lab."""

APP_TITLE = "World Cup Match Lab"
APP_TAGLINE = "Predict matches. Build brackets. Spot upsets before they happen."
APP_VERSION = "1.0.0"

RANDOM_SEED = 42

ROUNDS = [
    "Group Stage",
    "Round of 32",
    "Round of 16",
    "Quarterfinal",
    "Semifinal",
    "Final",
]

ROUND_PRESSURE = {
    "Group Stage": 1.0,
    "Round of 32": 1.05,
    "Round of 16": 1.10,
    "Quarterfinal": 1.15,
    "Semifinal": 1.20,
    "Final": 1.30,
}

ALTITUDE_IMPACT = {
    "Low": 0.0,
    "Medium": -0.03,
    "High": -0.07,
}

BRACKET_MODES = [
    "Smart Bracket",
    "Chaos Bracket",
    "Dark Horse Bracket",
    "Fan Favorite Bracket",
]

UPSET_LABELS = {
    "low": "Minor Risk",
    "medium": "Trap Game",
    "high": "Banana Peel Match",
    "very_high": "Chaos Alert 🚨",
}

EXCITEMENT_FLAMES = {1: "🔥", 2: "🔥🔥", 3: "🔥🔥🔥", 4: "🔥🔥🔥🔥", 5: "🔥🔥🔥🔥🔥"}

STYLE_TAG_COLORS = {
    "Total Football": "#00d4ff",
    "Counter-Attack Kings": "#ff6b35",
    "Samba Magic": "#ffd700",
    "Press & Pace": "#ffffff",
    "Tiki-Taka Evolved": "#c41e3a",
    "Star Power": "#8b0000",
    "Organized Chaos": "#000000",
    "Total Football DNA": "#ff6600",
    "Golden Generation": "#ff0000",
    "Midfield Maestros": "#ff0000",
    "Defensive Wall": "#0070bb",
    "Garra Charrúa": "#5eba00",
    "Energetic Underdogs": "#fcd116",
    "Athletic Press": "#b22234",
    "Technical Flair": "#006847",
    "Rising Force": "#ff0000",
    "High Press Collective": "#bc002d",
    "Industrial Runners": "#c60c30",
    "Desert Wolves": "#c1272d",
    "Physical Lions": "#00853f",
    "Black Stars Energy": "#fcd116",
    "Socceroos Grit": "#00843d",
    "Tactical Precision": "#ff0000",
    "Organized Power": "#c60c30",
    "Attack Minded": "#c6363c",
    "Lewandowski Effect": "#dc143c",
    "High Altitude Warriors": "#ffd100",
    "Pressing Machine": "#d52b1e",
    "Bafana Rising": "#007a4d",
    "Passionate Underdogs": "#e30a17",
    "Defensive Block": "#d52b1e",
    "Tactical Evolution": "#ed2939",
}

DARK_HORSE_THRESHOLD = 80  # power_score below this = dark horse candidate
UPSET_THRESHOLD = 0.30  # upset probability above this triggers alert

DATA_DISCLAIMER = (
    "⚠️ Sample data used for demo purposes. "
    "Ratings and predictions are illustrative, not official FIFA data."
)
