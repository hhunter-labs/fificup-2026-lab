"""
Model backtesting engine — validates predictions against Qatar 2022 results.
This is the credibility layer: shows the model's real-world accuracy.
"""

import os
import numpy as np
import pandas as pd
from src.predictor import predict_match
from src.data_loader import get_team_row

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


def load_qatar_2022() -> pd.DataFrame:
    path = os.path.join(DATA_DIR, "qatar_2022_results.csv")
    return pd.read_csv(path)


def run_backtest(teams_df: pd.DataFrame, results_df: pd.DataFrame) -> pd.DataFrame:
    """
    Run the prediction model on every Qatar 2022 match and compare
    predicted outcome to actual outcome. Returns enriched results DataFrame.
    """
    records = []
    for _, row in results_df.iterrows():
        ta_name = row["team_a"]
        tb_name = row["team_b"]

        # Skip teams not in our sample data (e.g. Qatar, Costa Rica)
        try:
            ta = get_team_row(teams_df, ta_name)
            tb = get_team_row(teams_df, tb_name)
        except ValueError:
            continue

        pred = predict_match(ta, tb, round_name=row["stage"], seed=42)

        # Determine predicted winner
        prob_a = pred["prob_a_win"]
        prob_b = pred["prob_b_win"]
        prob_d = pred["prob_draw"]

        if prob_a > prob_b and prob_a > prob_d:
            predicted = ta_name
        elif prob_b > prob_a and prob_b > prob_d:
            predicted = tb_name
        else:
            predicted = "Draw"

        actual = row["actual_winner"]
        knockout_winner = row["knockout_winner"]

        # For knockout stages, draws resolved by penalty — use knockout_winner
        stage = row["stage"]
        is_knockout = stage not in ("Group Stage",)
        comparison_actual = knockout_winner if is_knockout else actual

        correct = (predicted == comparison_actual) or (
            predicted == "Draw" and actual == "Draw"
        )

        # Upset detection: underdog won
        fav = ta_name if prob_a > prob_b else tb_name
        actual_winner_clean = knockout_winner if is_knockout else actual
        upset_occurred = (actual_winner_clean not in (fav, "Draw")) and actual_winner_clean != "Draw"

        records.append({
            "team_a": ta_name,
            "team_b": tb_name,
            "stage": stage,
            "actual_winner": actual,
            "knockout_winner": knockout_winner,
            "predicted_winner": predicted,
            "prob_a": round(prob_a, 3),
            "prob_draw": round(prob_d, 3),
            "prob_b": round(prob_b, 3),
            "correct": correct,
            "is_knockout": is_knockout,
            "upset_occurred": upset_occurred,
            "fav_team": fav,
            "predicted_prob_winner": round(max(prob_a, prob_b), 3),
        })

    return pd.DataFrame(records)


def compute_metrics(bt: pd.DataFrame) -> dict:
    """Compute summary accuracy metrics from backtest results."""
    if len(bt) == 0:
        return {}

    overall_acc      = bt["correct"].mean()
    group_acc        = bt[~bt["is_knockout"]]["correct"].mean() if len(bt[~bt["is_knockout"]]) else 0
    knockout_acc     = bt[bt["is_knockout"]]["correct"].mean() if len(bt[bt["is_knockout"]]) else 0

    upsets           = bt[bt["upset_occurred"]]
    non_upsets       = bt[~bt["upset_occurred"] & (bt["actual_winner"] != "Draw")]

    upset_detected   = 0
    if len(upsets) > 0:
        upset_detected = (upsets["predicted_winner"] != upsets["fav_team"]).mean()

    # Calibration: bucket predicted probabilities, compute actual win rate
    bt2 = bt.copy()
    bt2["bucket"] = pd.cut(bt2["predicted_prob_winner"],
                           bins=[0, 0.45, 0.55, 0.65, 0.75, 1.01],
                           labels=["<45%","45-55%","55-65%","65-75%",">75%"])
    calibration = bt2.groupby("bucket", observed=True)["correct"].agg(["mean","count"]).reset_index()
    calibration.columns = ["bucket","actual_rate","n"]

    return {
        "overall_accuracy": round(overall_acc, 3),
        "group_stage_accuracy": round(group_acc, 3),
        "knockout_accuracy": round(knockout_acc, 3),
        "total_matches": len(bt),
        "correct_predictions": int(bt["correct"].sum()),
        "upsets_in_data": len(upsets),
        "calibration": calibration,
    }
