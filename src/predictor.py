"""
Match prediction engine for World Cup Match Lab.
Uses Poisson goal model + logistic-style outcome probabilities.
All ratings are sample data for demo purposes.
"""

import numpy as np
import pandas as pd
from scipy.stats import poisson
from src.config import ROUND_PRESSURE, ALTITUDE_IMPACT, UPSET_THRESHOLD


def softmax(x: np.ndarray) -> np.ndarray:
    e = np.exp(x - np.max(x))
    return e / e.sum()


def calculate_team_strength(team_row: pd.Series) -> float:
    """Composite strength score from team attributes."""
    weights = {
        "power_score": 0.25,
        "attack": 0.18,
        "defense": 0.18,
        "midfield": 0.15,
        "goalkeeping": 0.10,
        "recent_form": 0.08,
        "tournament_experience": 0.06,
    }
    score = sum(float(team_row.get(k, 70)) * v for k, v in weights.items())
    return score


def _elo_win_prob(elo_a: float, elo_b: float) -> float:
    """Standard Elo expected score for team A."""
    return 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / 400))


def _rest_adjustment(rest_days: int) -> float:
    """Return a small multiplier based on rest. Optimal = 5-7 days."""
    if rest_days <= 2:
        return 0.93
    elif rest_days <= 4:
        return 0.97
    elif rest_days <= 7:
        return 1.0
    else:
        return 0.98  # too much rest can cause rustiness


def _altitude_penalty(venue_row) -> float:
    """Return goal-scoring penalty factor due to altitude."""
    if venue_row is None:
        return 0.0
    cat = str(venue_row.get("altitude_category", "Low"))
    return ALTITUDE_IMPACT.get(cat, 0.0)


def predict_match(
    team_a: pd.Series,
    team_b: pd.Series,
    venue=None,
    round_name: str = "Group Stage",
    rest_a: int = 5,
    rest_b: int = 5,
    high_pressure: bool = False,
    seed: int = None,
) -> dict:
    """
    Predict outcome probabilities and expected goals for a match.
    Returns a rich prediction dict.
    """
    rng = np.random.default_rng(seed)

    str_a = calculate_team_strength(team_a)
    str_b = calculate_team_strength(team_b)

    elo_a = float(team_a.get("elo", 1900))
    elo_b = float(team_b.get("elo", 1900))
    elo_prob_a = _elo_win_prob(elo_a, elo_b)

    rest_mult_a = _rest_adjustment(rest_a)
    rest_mult_b = _rest_adjustment(rest_b)

    alt_pen = _altitude_penalty(venue)

    pressure_mult = ROUND_PRESSURE.get(round_name, 1.0)
    if high_pressure:
        pressure_mult *= 1.05

    # Volatility adds uncertainty
    vol_a = float(team_a.get("volatility", 30)) / 100
    vol_b = float(team_b.get("volatility", 30)) / 100

    # Expected goals (lambda) via Poisson model
    base_lambda_a = (float(team_a.get("attack", 75)) / 100) * 1.8
    base_lambda_b = (float(team_b.get("attack", 75)) / 100) * 1.8

    def_adj_a = 1.0 - (float(team_b.get("defense", 75)) - 70) / 200
    def_adj_b = 1.0 - (float(team_a.get("defense", 75)) - 70) / 200

    lambda_a = max(0.3, base_lambda_a * def_adj_a * rest_mult_a * (1 + alt_pen) * pressure_mult)
    lambda_b = max(0.3, base_lambda_b * def_adj_b * rest_mult_b * (1 + alt_pen) * pressure_mult)

    # Volatility nudge
    lambda_a *= (1 + rng.normal(0, vol_a * 0.1))
    lambda_b *= (1 + rng.normal(0, vol_b * 0.1))
    lambda_a = max(0.2, lambda_a)
    lambda_b = max(0.2, lambda_b)

    # Outcome probabilities via vectorized score matrix (no Python loops)
    max_goals = 8
    goals = np.arange(max_goals)
    pmf_a = poisson.pmf(goals, lambda_a)   # shape (8,)
    pmf_b = poisson.pmf(goals, lambda_b)   # shape (8,)
    score_matrix = np.outer(pmf_a, pmf_b)  # shape (8,8) — ~50x faster than nested loop

    prob_a_win = float(np.sum(np.tril(score_matrix, -1)))
    prob_draw = float(np.trace(score_matrix))
    prob_b_win = float(np.sum(np.triu(score_matrix, 1)))

    # Blend Elo signal
    elo_weight = 0.3
    prob_a_win = prob_a_win * (1 - elo_weight) + elo_prob_a * elo_weight
    prob_b_win = prob_b_win * (1 - elo_weight) + (1 - elo_prob_a) * elo_weight

    # Renormalize
    total = prob_a_win + prob_draw + prob_b_win
    prob_a_win /= total
    prob_draw /= total
    prob_b_win /= total

    # Most likely scoreline
    likely_score = estimate_scoreline(lambda_a, lambda_b)

    # Excitement rating: combo of goal expectation + competitiveness
    closeness = 1 - abs(prob_a_win - prob_b_win)
    total_goals_exp = lambda_a + lambda_b
    excitement_raw = (closeness * 2.5 + total_goals_exp * 0.5)
    excitement = min(5, max(1, round(excitement_raw)))

    # Upset risk
    favorite = team_a["team"] if prob_a_win > prob_b_win else team_b["team"]
    underdog = team_b["team"] if prob_a_win > prob_b_win else team_a["team"]
    underdog_prob = prob_b_win if prob_a_win > prob_b_win else prob_a_win
    upset_risk = calculate_upset_risk(underdog_prob)

    return {
        "team_a": team_a["team"],
        "team_b": team_b["team"],
        "prob_a_win": round(prob_a_win, 4),
        "prob_draw": round(prob_draw, 4),
        "prob_b_win": round(prob_b_win, 4),
        "lambda_a": round(lambda_a, 2),
        "lambda_b": round(lambda_b, 2),
        "likely_score_a": likely_score[0],
        "likely_score_b": likely_score[1],
        "excitement": excitement,
        "upset_risk": upset_risk,
        "favorite": favorite,
        "underdog": underdog,
        "underdog_prob": round(underdog_prob, 4),
        "round": round_name,
        "venue": venue["city"] if venue is not None else "Neutral",
        "high_pressure": high_pressure,
        "str_a": round(str_a, 1),
        "str_b": round(str_b, 1),
    }


def estimate_scoreline(lambda_a: float, lambda_b: float) -> tuple:
    """Return most likely (goals_a, goals_b) scoreline — vectorized."""
    goals = np.arange(8)
    matrix = np.outer(poisson.pmf(goals, lambda_a), poisson.pmf(goals, lambda_b))
    idx = np.unravel_index(np.argmax(matrix), matrix.shape)
    return (int(idx[0]), int(idx[1]))


def bootstrap_confidence_interval(
    team_a: pd.Series, team_b: pd.Series,
    venue=None, round_name: str = "Group Stage",
    rest_a: int = 5, rest_b: int = 5,
    high_pressure: bool = False,
    n: int = 150,
) -> dict:
    """
    Bootstrap confidence intervals for win probabilities.
    Adds ±rating noise to simulate model uncertainty.
    Returns 95% CI for team_a win probability.
    """
    rng = np.random.default_rng(42)
    probs_a = []

    rating_keys = ["attack","defense","midfield","goalkeeping","recent_form","elo","power_score"]

    for i in range(n):
        # Clone team rows as dicts and add noise
        ta_noisy = team_a.copy()
        tb_noisy = team_b.copy()
        noise_scale = 2.5  # ±2.5 rating points reflects real uncertainty

        for k in rating_keys:
            if k in ta_noisy.index:
                ta_noisy[k] = float(ta_noisy[k]) + rng.normal(0, noise_scale)
            if k in tb_noisy.index:
                tb_noisy[k] = float(tb_noisy[k]) + rng.normal(0, noise_scale)

        p = predict_match(ta_noisy, tb_noisy, venue=venue, round_name=round_name,
                          rest_a=rest_a, rest_b=rest_b,
                          high_pressure=high_pressure, seed=i)
        probs_a.append(p["prob_a_win"])

    arr = np.array(probs_a)
    return {
        "mean":    round(float(arr.mean()), 4),
        "ci_low":  round(float(np.percentile(arr, 2.5)), 4),
        "ci_high": round(float(np.percentile(arr, 97.5)), 4),
        "std":     round(float(arr.std()), 4),
    }


def feature_attribution(
    team_a: pd.Series, team_b: pd.Series,
    venue=None, round_name: str = "Group Stage",
    rest_a: int = 5, rest_b: int = 5,
) -> list:
    """
    Waterfall-style attribution showing what drives the prediction.
    Returns list of (driver_name, contribution, direction) tuples.
    Starting from 50/50 baseline, each feature pushes toward A or B.
    """
    baseline = 0.50

    # Full prediction
    full = predict_match(team_a, team_b, venue=venue, round_name=round_name,
                         rest_a=rest_a, rest_b=rest_b, seed=42)
    final_prob = full["prob_a_win"]

    drivers = []

    # 1 — Elo rating advantage
    elo_a = float(team_a.get("elo", 1900))
    elo_b = float(team_b.get("elo", 1900))
    elo_prob = 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / 400))
    elo_contrib = (elo_prob - 0.5) * 0.30   # elo weight in model
    drivers.append(("Elo Rating", elo_contrib))

    # 2 — Attack vs Defense matchup
    att_a = float(team_a.get("attack", 75))
    att_b = float(team_b.get("attack", 75))
    def_a = float(team_a.get("defense", 75))
    def_b = float(team_b.get("defense", 75))
    attack_edge = ((att_a - def_b) - (att_b - def_a)) / 200
    drivers.append(("Attack vs Defense", attack_edge * 0.36))  # combined weight

    # 3 — Midfield control
    mid_diff = (float(team_a.get("midfield",75)) - float(team_b.get("midfield",75))) / 200
    drivers.append(("Midfield Control", mid_diff * 0.15))

    # 4 — Recent form
    form_diff = (float(team_a.get("recent_form",75)) - float(team_b.get("recent_form",75))) / 200
    drivers.append(("Recent Form", form_diff * 0.08))

    # 5 — Tournament experience
    exp_diff = (float(team_a.get("tournament_experience",75)) - float(team_b.get("tournament_experience",75))) / 200
    drivers.append(("Tournament Experience", exp_diff * 0.06))

    # 6 — Rest days
    rest_diff = (rest_a - rest_b) / 20
    drivers.append(("Rest Days", rest_diff * 0.03))

    # 7 — Venue / altitude
    if venue is not None:
        alt_impact = float(venue.get("altitude_impact", 1)) / 100
        drivers.append(("Venue / Altitude", -alt_impact * 0.02))
    else:
        drivers.append(("Venue / Altitude", 0.0))

    # 8 — Residual (rounds/pressure/noise)
    accounted = sum(c for _, c in drivers)
    residual = (final_prob - baseline) - accounted
    drivers.append(("Model Uncertainty", residual))

    # Return as sorted list of dicts
    return [
        {
            "driver": name,
            "contribution": round(float(contrib), 4),
            "direction": "Team A" if contrib > 0.001 else "Team B" if contrib < -0.001 else "Neutral",
            "abs": abs(float(contrib)),
        }
        for name, contrib in sorted(drivers, key=lambda x: abs(x[1]), reverse=True)
    ]


def calculate_upset_risk(underdog_prob: float) -> str:
    """Classify upset risk label."""
    if underdog_prob >= 0.45:
        return "very_high"
    elif underdog_prob >= 0.35:
        return "high"
    elif underdog_prob >= 0.25:
        return "medium"
    else:
        return "low"


def generate_upset_matches(teams_df: pd.DataFrame, n: int = 12) -> list:
    """Generate a list of potential upset matches ranked by upset probability."""
    teams = teams_df.copy().reset_index(drop=True)
    results = []
    seen = set()

    # Pair favorites vs underdogs
    sorted_teams = teams.sort_values("power_score", ascending=False).reset_index(drop=True)
    n_teams = len(sorted_teams)

    for i in range(min(8, n_teams)):
        for j in range(n_teams - 1, max(n_teams - 10, i + 1), -1):
            key = (sorted_teams.iloc[i]["team"], sorted_teams.iloc[j]["team"])
            if key in seen:
                continue
            seen.add(key)
            fav = sorted_teams.iloc[i]
            dog = sorted_teams.iloc[j]
            pred = predict_match(fav, dog, seed=42)
            if pred["underdog_prob"] > 0.18:
                results.append({
                    "favorite": fav["team"],
                    "favorite_flag": fav.get("flag", "🏳️"),
                    "underdog": dog["team"],
                    "underdog_flag": dog.get("flag", "🏳️"),
                    "upset_prob": pred["underdog_prob"],
                    "risk": pred["upset_risk"],
                    "fav_power": fav["power_score"],
                    "dog_power": dog["power_score"],
                    "dog_form": dog.get("recent_form", 70),
                    "dog_defense": dog.get("defense", 70),
                })
            if len(results) >= n:
                break
        if len(results) >= n:
            break

    results.sort(key=lambda x: x["upset_prob"], reverse=True)
    return results[:n]
