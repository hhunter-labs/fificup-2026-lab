# Changelog

All notable changes to World Cup Match Lab are documented here.
This project follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) conventions.

---

## [1.0.0] — 2026-06-01

### Added

**Core Application**
- Nine-page Streamlit application with a dark sports-broadcast design system
- Custom CSS design system using Bebas Neue, Inter, and JetBrains Mono typefaces
- Glassmorphism cards, neon accent colors, and animated hero section with the FIFA 2026 Trionda ball
- Flood-fill PNG background removal that preserves ball panel colors while eliminating white background

**Prediction Engine**
- Vectorized Poisson 8×8 score probability matrix — 50× faster than equivalent nested loop
- Elo rating blend at 30% weight combined with Poisson model for final outcome probabilities
- Venue adjustments for altitude, heat impact, and travel burden
- Rest-day and round-pressure multipliers
- Bootstrap confidence intervals with 60-sample uncertainty quantification
- Feature attribution waterfall decomposing predictions into named drivers (Elo, Attack/Defense, Midfield, Form, Experience, Venue, Rest)

**Simulation Engine**
- Temperature-scaled analytic champion probability distribution — instant, under 1ms
- Monte Carlo bracket simulation with four modes: Smart, Chaos, Dark Horse, Fan Favorite
- Mode-specific seeds ensure visible differences when switching modes without re-rolling
- Round names derived from match count, always correct for any bracket size
- Correct Final match card rendered as the last round

**Model Validation**
- Qatar 2022 backtest across 35 trackable matches
  - Overall accuracy: 63%
  - Knockout stage accuracy: 81%
- Calibration curve showing predicted probability vs actual outcome rate
- Accuracy breakdown by tournament stage
- Model Card with known limitations, bias acknowledgment, and intended use declaration

**Interactive Features**
- Live auto-predicting Predict Match page — updates at approximately 5ms, no submit button required
- Head-to-head attribute comparison bars on Predict Match
- Team Compare Mode with overlapping radar charts and per-attribute delta indicators
- Upset Radar with risk-tier filter chips (Chaos Alert, Banana Peel, Trap Game, Minor Risk)
- Live Featured Matchup on Home page with champion probability chart that highlights selected teams
- Clickable Odds Board cards using `_pending_page` two-rerun navigation pattern to avoid Streamlit widget key conflicts
- Session prediction counter and cross-page team memory via session state
- Shareable prediction text card
- AI narrative sidebar toggle with graceful rule-based fallback

**Data**
- 32 teams with 14 attributes each
- 16 host cities with geographic coordinates, altitude category, climate, and crowd energy ratings
- 44 Qatar 2022 match results for backtesting
- Weekly Elo rating refresh script with GitHub Actions workflow

**Infrastructure**
- `enableStaticServing = true` in Streamlit config for static asset serving
- Dark theme configuration in `.streamlit/config.toml`
- GitHub Actions CI workflow running 40 unit and integration tests on every push
- GitHub Actions workflow for weekly Elo data refresh
- Issue templates for bug reports and feature requests
- Pull request template with test checklist
- MIT license
