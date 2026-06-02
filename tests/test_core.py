"""
Core test suite for World Cup Match Lab.
Run: pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
import numpy as np

from src.data_loader import load_teams, load_venues, get_team_row, get_venue_row
from src.predictor import (
    predict_match, generate_upset_matches,
    bootstrap_confidence_interval, feature_attribution,
    calculate_upset_risk,
)
from src.simulator import simulate_bracket, fast_champion_probs, build_path_for_team
from src.backtester import load_qatar_2022, run_backtest, compute_metrics
from src.explainers import (
    generate_match_explanation, generate_team_summary,
    generate_upset_explanation, generate_can_team_win_summary,
)


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture(scope="module")
def teams():
    return load_teams()

@pytest.fixture(scope="module")
def venues():
    return load_venues()

@pytest.fixture(scope="module")
def team_a(teams):
    return get_team_row(teams, "Argentina")

@pytest.fixture(scope="module")
def team_b(teams):
    return get_team_row(teams, "France")

@pytest.fixture(scope="module")
def team_weak(teams):
    return get_team_row(teams, "South Africa")


# ── Data Layer ────────────────────────────────────────────────────────────────

class TestDataLoader:
    def test_teams_count(self, teams):
        assert len(teams) == 32

    def test_venues_count(self, venues):
        assert len(venues) == 16

    def test_no_nulls_teams(self, teams):
        assert teams.isnull().sum().sum() == 0

    def test_no_nulls_venues(self, venues):
        assert venues.isnull().sum().sum() == 0

    def test_get_team_row(self, teams):
        row = get_team_row(teams, "Brazil")
        assert row["team"] == "Brazil"

    def test_get_team_row_missing_raises(self, teams):
        with pytest.raises(ValueError):
            get_team_row(teams, "Wakanda FC")

    def test_get_venue_row(self, venues):
        row = get_venue_row(venues, "Dallas")
        assert row["city"] == "Dallas"

    def test_get_venue_row_missing_returns_none(self, venues):
        assert get_venue_row(venues, "Atlantis") is None

    def test_qatar_2022_loads(self):
        results = load_qatar_2022()
        assert len(results) >= 30

    def test_team_ratings_in_range(self, teams):
        for col in ["elo", "power_score", "attack", "defense"]:
            assert teams[col].min() > 0
            assert teams[col].max() <= 2500  # Elo can be high


# ── Prediction Engine ─────────────────────────────────────────────────────────

class TestPredictor:
    def test_probs_sum_to_one(self, team_a, team_b):
        pred = predict_match(team_a, team_b, seed=42)
        total = pred["prob_a_win"] + pred["prob_b_win"] + pred["prob_draw"]
        assert abs(total - 1.0) < 0.01

    def test_strong_vs_weak_favored(self, team_a, team_weak):
        pred = predict_match(team_a, team_weak, seed=42)
        assert pred["prob_a_win"] > 0.5

    def test_excitement_range(self, team_a, team_b):
        pred = predict_match(team_a, team_b, seed=42)
        assert 1 <= pred["excitement"] <= 5

    def test_upset_risk_valid(self, team_a, team_b):
        pred = predict_match(team_a, team_b, seed=42)
        assert pred["upset_risk"] in ["low", "medium", "high", "very_high"]

    def test_scoreline_non_negative(self, team_a, team_b):
        pred = predict_match(team_a, team_b, seed=42)
        assert pred["likely_score_a"] >= 0
        assert pred["likely_score_b"] >= 0

    def test_venue_altitude_reduces_xg(self, team_a, team_b, venues):
        mexico = get_venue_row(venues, "Mexico City")
        dallas = get_venue_row(venues, "Dallas")
        pred_mex = predict_match(team_a, team_b, venue=mexico, seed=42)
        pred_dal = predict_match(team_a, team_b, venue=dallas, seed=42)
        assert pred_mex["lambda_a"] < pred_dal["lambda_a"]

    def test_final_higher_pressure_than_group(self, team_a, team_b):
        pred_final = predict_match(team_a, team_b, round_name="Final", seed=42)
        pred_group = predict_match(team_a, team_b, round_name="Group Stage", seed=42)
        assert pred_final["lambda_a"] > pred_group["lambda_a"]

    def test_bootstrap_ci_ordering(self, team_a, team_b):
        ci = bootstrap_confidence_interval(team_a, team_b, n=20)
        assert ci["ci_low"] < ci["mean"] < ci["ci_high"]

    def test_bootstrap_ci_valid_range(self, team_a, team_b):
        ci = bootstrap_confidence_interval(team_a, team_b, n=20)
        assert 0 < ci["mean"] < 1
        assert 0 < ci["ci_low"] < 1
        assert 0 < ci["ci_high"] < 1

    def test_feature_attribution_returns_list(self, team_a, team_b):
        attrs = feature_attribution(team_a, team_b)
        assert len(attrs) > 0
        for a in attrs:
            assert isinstance(a["contribution"], float)
            assert a["direction"] in ["Team A", "Team B", "Neutral"]

    def test_upset_risk_classifier(self):
        assert calculate_upset_risk(0.10) == "low"
        assert calculate_upset_risk(0.28) == "medium"
        assert calculate_upset_risk(0.38) == "high"
        assert calculate_upset_risk(0.48) == "very_high"

    def test_upset_matches_returns_list(self, teams):
        upsets = generate_upset_matches(teams, n=5)
        assert len(upsets) <= 5
        assert all("upset_prob" in m for m in upsets)

    def test_upset_matches_zero(self, teams):
        assert generate_upset_matches(teams, n=0) == []


# ── Simulation Engine ─────────────────────────────────────────────────────────

class TestSimulator:
    def _top_n(self, teams, n):
        return [row for _, row in teams.sort_values("power_score", ascending=False).head(n).iterrows()]

    def test_bracket_16_has_champion(self, teams):
        t = self._top_n(teams, 16)
        result = simulate_bracket(t, seed=42)
        assert result["champion"] is not None

    def test_bracket_16_round_names(self, teams):
        t = self._top_n(teams, 16)
        result = simulate_bracket(t, seed=42)
        round_names = {r["round"] for r in result["rounds"]}
        assert "🏆 The Final" in round_names
        assert "Semifinals" in round_names
        assert "Quarterfinals" in round_names

    def test_bracket_16_has_final_with_one_match(self, teams):
        t = self._top_n(teams, 16)
        result = simulate_bracket(t, seed=42)
        finals = [r for r in result["rounds"] if r["round"] == "🏆 The Final"]
        assert len(finals) == 1
        assert len(finals[0]["matches"]) == 1

    def test_bracket_8_no_round_of_16(self, teams):
        t = self._top_n(teams, 8)
        result = simulate_bracket(t, seed=42)
        round_names = {r["round"] for r in result["rounds"]}
        assert "Round of 16" not in round_names
        assert "🏆 The Final" in round_names

    def test_modes_produce_different_champions(self, teams):
        t = self._top_n(teams, 16)
        offsets = {"smart": 0, "chaos": 11111, "dark_horse": 22222, "fan_favorite": 33333}
        champions = set()
        for mode, offset in offsets.items():
            r = simulate_bracket(t, mode=mode, favorite_team="USA", seed=42 ^ offset)
            champions.add(r["champion"]["team"])
        assert len(champions) > 1, "All modes produced the same champion — mode offsets not working"

    def test_champion_probs_sum_to_one(self, teams):
        probs = fast_champion_probs(teams)
        assert abs(sum(probs.values()) - 1.0) < 0.01

    def test_argentina_is_top_team(self, teams):
        probs = fast_champion_probs(teams)
        top = list(probs.keys())[0]
        assert top in ["Argentina", "France", "Brazil"]

    def test_build_path_returns_valid_finish(self, teams):
        result = build_path_for_team("USA", teams, n_simulations=10, seed=42)
        valid = ["Champion", "Runner-Up", "Semifinal", "Quarterfinal", "Round of 16", "Group Stage"]
        assert result["best_realistic_finish"] in valid


# ── Backtest ──────────────────────────────────────────────────────────────────

class TestBacktester:
    def test_backtest_accuracy_range(self, teams):
        results = load_qatar_2022()
        bt = run_backtest(teams, results)
        metrics = compute_metrics(bt)
        assert 0.4 < metrics["overall_accuracy"] < 0.9

    def test_knockout_beats_group(self, teams):
        results = load_qatar_2022()
        bt = run_backtest(teams, results)
        metrics = compute_metrics(bt)
        assert metrics["knockout_accuracy"] > metrics["group_stage_accuracy"]

    def test_sufficient_matches(self, teams):
        results = load_qatar_2022()
        bt = run_backtest(teams, results)
        metrics = compute_metrics(bt)
        assert metrics["total_matches"] >= 30

    def test_calibration_has_buckets(self, teams):
        results = load_qatar_2022()
        bt = run_backtest(teams, results)
        metrics = compute_metrics(bt)
        assert len(metrics["calibration"]) > 0


# ── Explainers ────────────────────────────────────────────────────────────────

class TestExplainers:
    def test_match_explanation_not_empty(self, team_a, team_b):
        pred = predict_match(team_a, team_b, seed=42)
        expl = generate_match_explanation(pred, team_a, team_b)
        assert len(expl) > 100

    def test_match_explanation_mentions_teams(self, team_a, team_b):
        pred = predict_match(team_a, team_b, seed=42)
        expl = generate_match_explanation(pred, team_a, team_b)
        assert "Argentina" in expl
        assert "France" in expl

    def test_match_explanation_has_bold(self, team_a, team_b):
        pred = predict_match(team_a, team_b, seed=42)
        expl = generate_match_explanation(pred, team_a, team_b)
        assert "**" in expl

    def test_team_summary_not_empty(self, team_a):
        summary = generate_team_summary(team_a)
        assert len(summary) > 50

    def test_can_win_summary(self, team_a, teams):
        finish = build_path_for_team("Argentina", teams, n_simulations=5, seed=42)
        summary = generate_can_team_win_summary(team_a, 0.30, finish)
        assert len(summary) > 100
        assert "Argentina" in summary
