# Contributing to World Cup Match Lab

Thanks for your interest in contributing! This document covers how to get set up, what we look for in contributions, and how to submit changes.

---

## 🚀 Development Setup

```bash
git clone https://github.com/hhunter-labs/fificup-2026-lab.git
cd fificup-2026-lab
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

---

## 📐 Code Standards

| Area | Standard |
|------|----------|
| Style | PEP 8. Functions < 60 lines. Clear variable names. |
| HTML in Streamlit | **Never** put conditional logic inside `st.markdown()` f-strings. Pre-compute HTML variables in Python first. Use `st.html()` for complex multi-block structures. |
| Plotly colors | Never use `"transparent"` — use `"rgba(0,0,0,0)"` |
| Session state | Never set a widget key that has already been rendered in the current run. Use the `_pending_page` pattern for cross-page navigation. |
| Performance | All heavy computation behind `@st.cache_data`. Use `@st.fragment` to isolate fast-changing sections. |
| Data | Keep sample data clearly labeled. Never claim real-time data unless actually implemented. |

---

## 🧪 Running Tests

```bash
cd fificup-2026-lab
python -m pytest tests/ -v
```

---

## 🔀 Pull Request Process

1. Fork the repo and create a branch: `git checkout -b feature/your-feature`
2. Make your changes following the code standards above
3. Run tests: `python -m pytest tests/`
4. Open a PR against `main` using the PR template
5. A maintainer will review within 48 hours

---

## 💡 Good First Issues

- Adding more teams to `data/teams.csv`
- Improving the rule-based analyst narratives in `src/explainers.py`
- Adding new visualizations to `src/visualizations.py`
- Writing additional unit tests in `tests/`
- Improving mobile CSS responsiveness

---

## ⚠️ Out of Scope

- Real-money wagering features
- Official FIFA data integration without proper licensing
- Any feature that removes the sample data disclaimer
