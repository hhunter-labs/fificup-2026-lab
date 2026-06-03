# Contributing to World Cup Match Lab

Thank you for your interest in contributing. This document covers development setup, code standards, and the pull request process.

---

## Development Setup

```bash
git clone https://github.com/hhunter-labs/fificup-2026-lab.git
cd fificup-2026-lab

python -m venv venv
source venv/bin/activate          # macOS / Linux
# venv\Scripts\activate           # Windows

pip install -r requirements.txt
streamlit run app.py              # Opens at http://localhost:8501
```

---

## Running Tests

```bash
python -m pytest tests/ -v
```

All 40 tests should pass before opening a pull request.

---

## Code Standards

| Area | Standard |
|------|----------|
| Style | PEP 8. Functions under 60 lines. Descriptive variable names. |
| HTML in Streamlit | Never embed conditional logic inside `st.markdown()` f-strings. Pre-compute HTML variables in Python first. Use `st.html()` for complex multi-block HTML structures. |
| Plotly colors | Never pass `"transparent"` to a color property — use `"rgba(0,0,0,0)"` instead. |
| Session state | Never set a widget's session state key after that widget has already rendered in the current script run. Use the `_pending_page` two-rerun navigation pattern for cross-page routing. |
| Performance | All heavy computation must be behind `@st.cache_data`. Use `@st.fragment` to isolate live-updating sections from the rest of the page. |
| Data integrity | Sample data must remain clearly labeled. Never claim real-time data unless a live data pipeline is actually implemented. |

---

## Pull Request Process

1. Fork the repository and create a feature branch from `main`
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Make your changes following the code standards above
3. Run the full test suite and confirm all tests pass
4. Open a pull request against `main` using the provided PR template
5. A maintainer will review and respond within 48 hours

---

## Good First Contributions

- Add teams to `data/teams.csv` with accurate ratings
- Improve analyst narrative templates in `src/explainers.py`
- Add new chart types to `src/visualizations.py`
- Expand the test suite in `tests/test_core.py`
- Improve CSS responsiveness for mobile viewports

---

## Out of Scope

The following will not be accepted:

- Real-money wagering or odds integration
- Official FIFA data without verifiable licensing
- Changes that remove or weaken the sample data disclaimer
- Dependencies that require paid external API keys at runtime
