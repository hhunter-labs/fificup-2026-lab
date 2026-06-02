# Changelog

All notable changes to World Cup Match Lab are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.0.0] — 2026-06-01

### 🎉 Initial Release

#### Core Product
- 9-page Streamlit application with dark sports-broadcast design system
- Custom CSS design system (Bebas Neue + Inter + JetBrains Mono)
- Glassmorphism cards, neon accents, animated hero with FIFA 2026 ball

#### Prediction Engine
- Vectorized Poisson 8×8 score matrix (50× faster than nested loop)
- Elo rating blend (30% weight) for final outcome probabilities
- Venue altitude, heat, rest-day, and round-pressure adjustments
- Bootstrap confidence intervals (60-sample uncertainty quantification)
- Feature attribution waterfall (Elo, Attack/Defense, Form, Experience, Venue, Rest)

#### Simulation Engine
- Temperature-scaled analytic champion probabilities (instant, <1ms)
- Monte Carlo bracket simulation (4 modes: Smart, Chaos, Dark Horse, Fan Favorite)
- Mode-specific seeds so switching modes immediately shows different outcomes
- Correct round naming derived from match count (Round of 16 → Quarterfinals → Semifinals → 🏆 The Final)

#### Model Validation
- Qatar 2022 backtest: 63% overall accuracy, 81% knockout accuracy (35 trackable matches)
- Calibration curve and accuracy-by-stage charts
- Full model card with known limitations and bias acknowledgment

#### Interactive Features
- Auto-predicting Predict Match page (no button — updates at 5ms)
- Team Compare Mode with overlapping radar charts and attribute delta table
- Upset Radar with risk-tier filter chips (Chaos Alert / Banana Peel / Trap Game)
- Live Featured Matchup on Home with champion chart that highlights selected teams
- Clickable Odds Board cards with `_pending_page` navigation pattern
- Session prediction counter and cross-page team memory
- Shareable prediction text card
- Claude AI sidebar toggle with graceful fallback

#### Data
- 32 teams with 14 attributes each
- 16 host cities with geo coordinates, altitude, climate, and crowd energy
- 44 Qatar 2022 match results for backtesting
- Weekly Elo refresh script + GitHub Actions workflow

#### Deployment
- `enableStaticServing = true` for ball image
- `.streamlit/config.toml` dark theme configuration
- `.github/workflows/ci.yml` for automated testing
- `.github/workflows/update_elo.yml` for weekly data refresh
