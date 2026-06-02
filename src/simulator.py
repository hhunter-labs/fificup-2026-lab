"""
Tournament simulation engine for World Cup Match Lab.
Supports Smart, Chaos, Dark Horse, and Fan Favorite bracket modes.
"""

import numpy as np
import pandas as pd
from src.predictor import predict_match, calculate_team_strength
from src.config import RANDOM_SEED, DARK_HORSE_THRESHOLD


def fast_champion_probs(teams_df: pd.DataFrame, temperature: float = 3.0) -> dict:
    """
    Instant analytic approximation of champion probabilities.
    Uses temperature-scaled softmax over blended Elo + power score.

    Temperature > 1 flattens the distribution so mid-tier teams show
    meaningful probabilities instead of ~0%. Real bookmaker odds imply
    temperature ≈ 3 (Argentina ~28-33%, not 68%).
    """
    elo    = teams_df["elo"].astype(float).values
    power  = teams_df["power_score"].astype(float).values
    form   = teams_df["recent_form"].astype(float).values
    exp    = teams_df["tournament_experience"].astype(float).values

    combined = 0.40 * elo / 20 + 0.35 * power + 0.15 * form + 0.10 * exp
    # Divide by temperature before softmax — flattens distribution to realistic spread
    shifted  = (combined - combined.max()) / temperature
    exp_vals = np.exp(shifted)
    probs    = exp_vals / exp_vals.sum()

    result = dict(zip(teams_df["team"].tolist(), probs.tolist()))
    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


def simulate_match(
    team_a: pd.Series,
    team_b: pd.Series,
    mode: str = "smart",
    favorite_team: str = None,
    rng: np.random.Generator = None,
) -> pd.Series:
    """
    Simulate a single match and return the winning team row.
    Mode affects how probabilities are adjusted before sampling.
    """
    if rng is None:
        rng = np.random.default_rng(RANDOM_SEED)

    pred = predict_match(team_a, team_b, seed=int(rng.integers(0, 9999)))
    p_a = pred["prob_a_win"] + pred["prob_draw"] * 0.5  # draw splits equally in KO
    p_b = 1 - p_a

    if mode == "chaos":
        # Increase underdog chances
        p_a = p_a ** 0.7
        p_b = p_b ** 0.7
        total = p_a + p_b
        p_a /= total
        p_b /= total

    elif mode == "dark_horse":
        # Boost low-power-score team
        score_a = float(team_a.get("power_score", 75))
        score_b = float(team_b.get("power_score", 75))
        if score_a < DARK_HORSE_THRESHOLD and score_b >= DARK_HORSE_THRESHOLD:
            p_a = min(0.60, p_a * 1.4)
            p_b = 1 - p_a
        elif score_b < DARK_HORSE_THRESHOLD and score_a >= DARK_HORSE_THRESHOLD:
            p_b = min(0.60, p_b * 1.4)
            p_a = 1 - p_b

    elif mode == "fan_favorite" and favorite_team is not None:
        # Slightly boost the fan favorite team
        if team_a["team"] == favorite_team:
            p_a = min(0.85, p_a * 1.25)
            p_b = 1 - p_a
        elif team_b["team"] == favorite_team:
            p_b = min(0.85, p_b * 1.25)
            p_a = 1 - p_b

    winner = team_a if rng.random() < p_a else team_b
    return winner


def simulate_bracket(
    teams: list,
    mode: str = "smart",
    favorite_team: str = None,
    seed: int = RANDOM_SEED,
) -> dict:
    """
    Simulate a single-elimination bracket for a list of team rows (pd.Series).
    Returns bracket results with rounds, champion, upset count.
    """
    rng = np.random.default_rng(seed)

    # Pad to power of 2
    n = len(teams)
    size = 1
    while size < n:
        size *= 2
    # Use weakest teams as byes (they auto-advance if odd)
    bracket = list(teams)
    while len(bracket) < size:
        bracket.append(None)  # bye slot

    round_results = []
    upsets = 0
    current_round = bracket.copy()
    round_idx = 0

    def _round_name(n_matches: int) -> str:
        """Derive round name from match count — always correct regardless of bracket size."""
        if n_matches >= 16: return "Round of 32"
        if n_matches == 8:  return "Round of 16"
        if n_matches == 4:  return "Quarterfinals"
        if n_matches == 2:  return "Semifinals"
        if n_matches == 1:  return "🏆 The Final"
        return f"Round of {n_matches * 2}"

    while len([t for t in current_round if t is not None]) > 1:
        next_round = []
        active_count = len([t for t in current_round if t is not None])
        n_matches_this_round = active_count // 2
        round_label = _round_name(n_matches_this_round)
        round_matches = []

        active = [t for t in current_round if t is not None]
        # Re-pad if odd
        if len(active) % 2 == 1:
            active.append(active[0])  # give top seed a bye by repeating

        for i in range(0, len(active), 2):
            ta = active[i]
            tb = active[i + 1]
            if ta is None:
                next_round.append(tb)
                continue
            if tb is None:
                next_round.append(ta)
                continue

            winner = simulate_match(ta, tb, mode=mode, favorite_team=favorite_team, rng=rng)
            pred = predict_match(ta, tb, seed=int(rng.integers(0, 9999)))

            # Detect upset: lower power team wins
            power_a = float(ta.get("power_score", 75))
            power_b = float(tb.get("power_score", 75))
            if winner["team"] == ta["team"] and power_a < power_b - 5:
                upsets += 1
            elif winner["team"] == tb["team"] and power_b < power_a - 5:
                upsets += 1

            round_matches.append({
                "team_a": ta["team"],
                "flag_a": ta.get("flag", "🏳️"),
                "team_b": tb["team"],
                "flag_b": tb.get("flag", "🏳️"),
                "winner": winner["team"],
                "winner_flag": winner.get("flag", "🏳️"),
                "prob_a": round(pred["prob_a_win"], 3),
                "prob_b": round(pred["prob_b_win"], 3),
            })
            next_round.append(winner)

        round_results.append({"round": round_label, "matches": round_matches})
        current_round = next_round
        round_idx += 1  # kept for reference, not used for naming

    champion = current_round[0] if current_round else None

    # Path difficulty: average opponent power score vs champion
    if champion is not None:
        champ_name = champion["team"]
        opponent_powers = []
        for rnd in round_results:
            for m in rnd["matches"]:
                if m["winner"] == champ_name:
                    other = m["team_b"] if m["team_a"] == champ_name else m["team_a"]
                    # Find the power score from teams list
                    for t in teams:
                        if t["team"] == other:
                            opponent_powers.append(float(t.get("power_score", 70)))
        difficulty = round(np.mean(opponent_powers), 1) if opponent_powers else 0.0
    else:
        difficulty = 0.0

    return {
        "rounds": round_results,
        "champion": champion,
        "upsets": upsets,
        "difficulty": difficulty,
    }


def run_monte_carlo(
    teams: list,
    n_simulations: int = 1000,
    mode: str = "smart",
    seed: int = RANDOM_SEED,
) -> dict:
    """Run Monte Carlo simulations and return champion probability per team."""
    counts = {}
    for t in teams:
        counts[t["team"]] = 0

    for i in range(n_simulations):
        result = simulate_bracket(teams, mode=mode, seed=seed + i)
        if result["champion"] is not None:
            name = result["champion"]["team"]
            if name in counts:
                counts[name] += 1

    probs = {k: round(v / n_simulations, 4) for k, v in counts.items()}
    return dict(sorted(probs.items(), key=lambda x: x[1], reverse=True))


def estimate_champion_probabilities(teams_df: pd.DataFrame, n: int = 500) -> dict:
    """Estimate championship probabilities for all teams via Monte Carlo."""
    team_list = [row for _, row in teams_df.iterrows()]
    return run_monte_carlo(team_list, n_simulations=n)


def build_path_for_team(
    target_team: str,
    teams_df: pd.DataFrame,
    n_simulations: int = 200,
    seed: int = RANDOM_SEED,
) -> dict:
    """
    Estimate the realistic path and best/worst cases for a given team.
    Returns finish distribution and key opponents.
    """
    team_list = [row for _, row in teams_df.iterrows()]
    finish_counts = {"Champion": 0, "Runner-Up": 0, "Semifinal": 0, "Quarterfinal": 0, "Round of 16": 0, "Group Stage": 0}

    for i in range(n_simulations):
        result = simulate_bracket(team_list, mode="smart", seed=seed + i)
        champ_name = result["champion"]["team"] if result["champion"] is not None else ""

        # Track where team was eliminated
        eliminated_round = "Group Stage"
        for rnd in result["rounds"]:
            for m in rnd["matches"]:
                if m["winner"] == target_team:
                    eliminated_round = rnd["round"]
                elif (m["team_a"] == target_team or m["team_b"] == target_team) and m["winner"] != target_team:
                    eliminated_round = rnd["round"]

        if champ_name == target_team:
            finish_counts["Champion"] += 1
        elif eliminated_round == "Final":
            finish_counts["Runner-Up"] += 1
        elif eliminated_round == "Semifinal":
            finish_counts["Semifinal"] += 1
        elif eliminated_round == "Quarterfinal":
            finish_counts["Quarterfinal"] += 1
        elif eliminated_round in ("Round of 16", "Round of 32"):
            finish_counts["Round of 16"] += 1
        else:
            finish_counts["Group Stage"] += 1

    finish_probs = {k: round(v / n_simulations, 3) for k, v in finish_counts.items()}
    best_finish = max(finish_probs, key=finish_probs.get)

    return {"finish_probs": finish_probs, "best_realistic_finish": best_finish}
