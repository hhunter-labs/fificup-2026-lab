"""
Streamlit UI components — FAANG-grade dark sports broadcast design.
Glassmorphism + neon glow + premium typography.
"""

import streamlit as st
from src.config import EXCITEMENT_FLAMES


def inject_custom_css():
    st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Reset & base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"], .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    background: #05070f !important;
    color: #e2e8f0;
}

/* ── Animated background ── */
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 20% 0%, rgba(0,212,255,0.07) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 80% 100%, rgba(123,47,255,0.06) 0%, transparent 60%),
        #05070f !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 1.5rem 2rem 3rem 2rem !important;
    max-width: 1280px !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0d1117; }
::-webkit-scrollbar-thumb { background: rgba(0,212,255,0.3); border-radius: 2px; }

/* ══════════════════════════════════════════
   SIDEBAR
══════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #080c18 0%, #05070f 100%) !important;
    border-right: 1px solid rgba(0,212,255,0.12) !important;
}
[data-testid="stSidebar"] > div { padding-top: 0 !important; }

/* Sidebar nav radio — hide default bullets, style as pills */
[data-testid="stSidebar"] .stRadio > div {
    gap: 2px !important;
    flex-direction: column;
}
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    padding: 10px 16px !important;
    border-radius: 8px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #94a3b8 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(0,212,255,0.08) !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
[data-testid="stSidebar"] .stRadio label[data-selected="true"] {
    background: rgba(0,212,255,0.12) !important;
    color: #00d4ff !important;
}
[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] {
    display: none !important;
}
[data-testid="stSidebarContent"] { padding: 0 12px 12px 12px; }

/* ══════════════════════════════════════════
   HERO
══════════════════════════════════════════ */
.hero-outer {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    margin-bottom: 2rem;
    padding: 3rem 2.5rem 2.5rem;
    background: linear-gradient(135deg, #0d1226 0%, #0f0a20 40%, #0d1226 100%);
    border: 1px solid rgba(0,212,255,0.15);
    box-shadow:
        0 0 0 1px rgba(0,212,255,0.05),
        0 20px 60px rgba(0,0,0,0.6),
        inset 0 1px 0 rgba(255,255,255,0.05);
}
.hero-outer::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 80% at 50% -20%, rgba(0,212,255,0.12) 0%, transparent 70%),
        radial-gradient(ellipse 40% 40% at 90% 90%, rgba(123,47,255,0.1) 0%, transparent 60%);
    pointer-events: none;
}
.hero-outer::after {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.4), transparent);
}
.hero-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(0,212,255,0.08);
    border: 1px solid rgba(0,212,255,0.2);
    color: #00d4ff;
    padding: 5px 14px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.8rem, 6vw, 4.5rem);
    line-height: 0.95;
    letter-spacing: 3px;
    background: linear-gradient(135deg, #ffffff 0%, #e2e8f0 30%, #00d4ff 60%, #7b2fff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 1rem;
    text-transform: uppercase;
}
.hero-tagline {
    font-size: 1.05rem;
    color: #64748b;
    font-weight: 400;
    letter-spacing: 0.5px;
    max-width: 540px;
}

/* ══════════════════════════════════════════
   PAGE HEADERS
══════════════════════════════════════════ */
.page-hero {
    position: relative;
    overflow: hidden;
    border-radius: 16px;
    padding: 2rem 2rem 1.8rem;
    margin-bottom: 1.8rem;
    background: linear-gradient(135deg, #0d1226 0%, #0f0a20 100%);
    border: 1px solid rgba(255,255,255,0.06);
}
.page-hero::after {
    content: '';
    position: absolute;
    top: 0; left: 8%; right: 8%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.35), transparent);
}
.page-eyebrow {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #00d4ff;
    margin-bottom: 0.5rem;
    opacity: 0.8;
}
.page-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.6rem;
    letter-spacing: 2px;
    color: #fff;
    line-height: 1;
    margin-bottom: 0.4rem;
}
.page-sub {
    font-size: 0.9rem;
    color: #64748b;
}

/* ══════════════════════════════════════════
   SECTION HEADERS
══════════════════════════════════════════ */
.section-hd {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 3px;
    color: #e2e8f0;
    text-transform: uppercase;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: relative;
}
.section-hd::after {
    content: '';
    position: absolute;
    bottom: -1px; left: 0;
    width: 48px; height: 2px;
    background: linear-gradient(90deg, #00d4ff, transparent);
}

/* ══════════════════════════════════════════
   KPI CARDS
══════════════════════════════════════════ */
.kpi-card {
    position: relative;
    overflow: hidden;
    background: rgba(13,18,38,0.7);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 14px;
    padding: 1.25rem 1.1rem 1.1rem;
    text-align: center;
    transition: border-color 0.2s, transform 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    margin-bottom: 0.75rem;
}
.kpi-card:hover {
    border-color: rgba(0,212,255,0.3);
    transform: translateY(-2px);
    box-shadow: 0 8px 32px rgba(0,212,255,0.08), 0 4px 24px rgba(0,0,0,0.4);
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 20%; right: 20%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.2), transparent);
}
.kpi-lbl {
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 0.45rem;
}
.kpi-val {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.45rem;
    letter-spacing: 1px;
    color: #f1f5f9;
    line-height: 1.1;
}
.kpi-sub {
    font-size: 11px;
    color: #00d4ff;
    margin-top: 0.3rem;
    font-weight: 500;
}

/* ══════════════════════════════════════════
   GLASS CARDS (general)
══════════════════════════════════════════ */
.glass-card {
    background: rgba(13,18,38,0.6);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.6rem;
    box-shadow: 0 8px 32px rgba(0,0,0,0.5);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.08), transparent);
}

/* ══════════════════════════════════════════
   TEAM CARD
══════════════════════════════════════════ */
.team-hero-card {
    background: linear-gradient(135deg, rgba(13,18,38,0.9) 0%, rgba(15,10,32,0.9) 100%);
    border: 1px solid rgba(0,212,255,0.15);
    border-radius: 20px;
    padding: 2rem 1.8rem;
    box-shadow:
        0 0 0 1px rgba(0,212,255,0.05),
        0 20px 60px rgba(0,0,0,0.6),
        inset 0 1px 0 rgba(255,255,255,0.04);
    position: relative;
    overflow: hidden;
}
.team-hero-card::before {
    content: '';
    position: absolute;
    top: -60px; left: -60px;
    width: 200px; height: 200px;
    background: radial-gradient(circle, rgba(0,212,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.team-flag-xl { font-size: 4rem; line-height: 1; display: block; margin-bottom: 0.75rem; }
.team-name-xl {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.4rem;
    letter-spacing: 2px;
    color: #fff;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.team-conf { font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #475569; margin-bottom: 1rem; }
.power-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 4.5rem;
    line-height: 1;
    background: linear-gradient(135deg, #00d4ff 0%, #7b2fff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    display: block;
}
.power-label { font-size: 10px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; color: #475569; }

/* ══════════════════════════════════════════
   UPSET CARDS
══════════════════════════════════════════ */
.upset-wrapper {
    background: rgba(10,5,18,0.8);
    border: 1px solid rgba(255,34,68,0.18);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    margin-bottom: 0.85rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
    box-shadow: 0 4px 20px rgba(0,0,0,0.5);
}
.upset-wrapper:hover {
    border-color: rgba(255,34,68,0.4);
    box-shadow: 0 8px 32px rgba(255,34,68,0.08);
}
.upset-wrapper::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, rgba(255,34,68,0.5), transparent);
}
.upset-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 12px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.upset-pill-chaos  { background: rgba(255,34,68,0.2);  border: 1px solid rgba(255,34,68,0.4);  color: #ff2244; }
.upset-pill-high   { background: rgba(255,102,0,0.15); border: 1px solid rgba(255,102,0,0.35); color: #ff6600; }
.upset-pill-medium { background: rgba(255,170,0,0.12); border: 1px solid rgba(255,170,0,0.3);  color: #ffaa00; }
.upset-pill-low    { background: rgba(51,102,153,0.15);border: 1px solid rgba(51,102,153,0.3); color: #6699cc; }
.upset-matchup {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.6rem;
    letter-spacing: 1px;
    color: #f1f5f9;
    margin-bottom: 0.3rem;
    line-height: 1.1;
}
.upset-prob {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.15rem;
    font-weight: 700;
    color: #ff6b35;
}
.upset-body {
    font-size: 12px;
    color: #64748b;
    margin-top: 0.5rem;
    line-height: 1.5;
}

/* ══════════════════════════════════════════
   PROBABILITY METERS
══════════════════════════════════════════ */
.prob-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}
.prob-label { font-size: 12px; color: #94a3b8; font-weight: 500; white-space: nowrap; min-width: 120px; }
.prob-track {
    flex: 1;
    background: rgba(255,255,255,0.04);
    border-radius: 100px;
    height: 8px;
    overflow: hidden;
}
.prob-fill {
    height: 100%;
    border-radius: 100px;
    transition: width 0.6s cubic-bezier(0.4,0,0.2,1);
}
.prob-pct { font-size: 12px; font-weight: 700; min-width: 36px; text-align: right; }

/* ══════════════════════════════════════════
   SCORELINE
══════════════════════════════════════════ */
.scoreline-wrap {
    text-align: center;
    padding: 1.5rem 0 1rem;
}
.scoreline-teams {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1.5rem;
}
.scoreline-team { font-size: 12px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #475569; }
.scoreline-digits {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 5rem;
    letter-spacing: 8px;
    color: #fff;
    line-height: 1;
    text-shadow: 0 0 40px rgba(0,212,255,0.3);
}
.scoreline-sep { font-family: 'Bebas Neue', sans-serif; font-size: 3rem; color: #1e293b; }
.scoreline-caption {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #334155;
    margin-top: 0.5rem;
}

/* ══════════════════════════════════════════
   FLAME RATING
══════════════════════════════════════════ */
.flame-wrap {
    text-align: center;
    padding: 0.5rem 0;
}
.flame-emoji { font-size: 1.8rem; letter-spacing: 4px; }
.flame-caption { font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #334155; margin-top: 4px; }

/* ══════════════════════════════════════════
   MATCH HEADER BANNER
══════════════════════════════════════════ */
.matchup-banner {
    background: linear-gradient(135deg, #0d1226, #0f0a20);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.5rem 2rem;
    text-align: center;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.matchup-banner::after {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.25), transparent);
}
.matchup-vs-text {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    letter-spacing: 2px;
    color: #fff;
    line-height: 1.1;
}
.matchup-vs-sep { color: #1e293b; margin: 0 0.4rem; }
.matchup-meta { font-size: 11px; font-weight: 600; letter-spacing: 2px; text-transform: uppercase; color: #475569; margin-top: 0.3rem; }

/* ══════════════════════════════════════════
   VERDICT CARD (Can My Team Win)
══════════════════════════════════════════ */
.verdict-card {
    border-radius: 20px;
    padding: 2rem 1.8rem;
    margin-bottom: 1rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.verdict-emoji { font-size: 3.5rem; display: block; margin-bottom: 0.75rem; }
.verdict-question { font-size: 0.95rem; font-weight: 600; color: #94a3b8; margin-bottom: 0.5rem; letter-spacing: 0.5px; }
.verdict-answer {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    letter-spacing: 2px;
    line-height: 1.1;
    margin-bottom: 1rem;
}
.verdict-stats {
    display: flex;
    justify-content: center;
    gap: 2.5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    padding-top: 1.2rem;
    margin-top: 0.5rem;
}
.verdict-stat-lbl { font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #475569; margin-bottom: 0.3rem; }
.verdict-stat-val { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; letter-spacing: 1px; }

/* ══════════════════════════════════════════
   CHAMPION BANNER (Bracket)
══════════════════════════════════════════ */
.champ-banner {
    background: linear-gradient(135deg, #0f0a20 0%, #0d1226 100%);
    border: 1px solid rgba(255,215,0,0.25);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 0 60px rgba(255,215,0,0.06), 0 20px 60px rgba(0,0,0,0.6);
}
.champ-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,215,0,0.35), transparent);
}
.champ-flag { font-size: 3.5rem; display: block; margin-bottom: 0.5rem; }
.champ-name {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 3px;
    color: #ffd700;
    text-shadow: 0 0 30px rgba(255,215,0,0.4);
    margin-bottom: 0.3rem;
}
.champ-sub { font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #475569; }
.champ-stats { display: flex; justify-content: center; gap: 2.5rem; margin-top: 1.2rem; }
.champ-stat { text-align: center; }
.champ-stat-lbl { font-size: 9px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #475569; margin-bottom: 0.3rem; }
.champ-stat-val { font-family: 'Bebas Neue', sans-serif; font-size: 1.8rem; letter-spacing: 1px; }

/* ══════════════════════════════════════════
   BRACKET MATCH CARDS
══════════════════════════════════════════ */
.bracket-card {
    background: rgba(13,18,38,0.7);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 0.9rem 1rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.15s;
}
.bracket-card:hover { border-color: rgba(0,212,255,0.2); }
.bracket-team-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 4px 0;
    font-size: 13px;
}
.bracket-team-name { font-weight: 600; color: #94a3b8; }
.bracket-team-name.winner { color: #ffd700; font-weight: 700; }
.bracket-team-prob { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: #334155; }
.bracket-divider { border: none; border-top: 1px solid rgba(255,255,255,0.04); margin: 3px 0; }

/* ══════════════════════════════════════════
   BADGE CHIPS
══════════════════════════════════════════ */
.chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ══════════════════════════════════════════
   CTA CARDS (Home)
══════════════════════════════════════════ */
.cta-grid-card {
    background: rgba(13,18,38,0.6);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 1.8rem 1.5rem;
    text-align: center;
    transition: all 0.2s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 24px rgba(0,0,0,0.4);
}
.cta-grid-card:hover {
    border-color: rgba(0,212,255,0.25);
    transform: translateY(-3px);
    box-shadow: 0 12px 40px rgba(0,212,255,0.08), 0 4px 24px rgba(0,0,0,0.4);
}
.cta-grid-card::before {
    content: '';
    position: absolute;
    top: 0; left: 15%; right: 15%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,212,255,0.2), transparent);
}
.cta-icon-wrap { font-size: 2.2rem; margin-bottom: 0.8rem; }
.cta-label { font-family: 'Bebas Neue', sans-serif; font-size: 1.3rem; letter-spacing: 2px; color: #f1f5f9; margin-bottom: 0.4rem; }
.cta-desc { font-size: 12px; color: #475569; line-height: 1.5; }

/* ══════════════════════════════════════════
   BACK TO HOME BUTTON (top of every inner page)
══════════════════════════════════════════ */
/* Target the specific back-home button by its data-testid prefix */
[data-testid^="stButton"] button[kind="secondary"]:has-text("← Home"),
button[data-testid*="back_home"] {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 100px !important;
    color: #475569 !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    padding: 4px 14px !important;
    width: auto !important;
    display: inline-flex !important;
    transition: all 0.15s !important;
    margin-bottom: 0.5rem !important;
}
/* Simpler universal override — style ALL secondary buttons at the page top
   that contain "← Home" text */
div[data-testid="stButton"] button {
    transition: all 0.15s ease !important;
}
/* The back-home button sits in its own stButton div right before page-hero */
.back-home-btn {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 6px 14px 6px 10px;
    border-radius: 100px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    color: #64748b;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 0.5px;
    cursor: pointer;
    text-decoration: none;
    transition: all 0.15s ease;
    margin-bottom: 0.75rem;
    user-select: none;
}
.back-home-btn:hover {
    background: rgba(0,212,255,0.08);
    border-color: rgba(0,212,255,0.25);
    color: #00d4ff;
}
.back-home-arrow { font-size: 14px; line-height: 1; }

/* ══════════════════════════════════════════
   VENUE CARD
══════════════════════════════════════════ */
.venue-detail-card {
    background: rgba(13,18,38,0.7);
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 16px;
    padding: 1.5rem;
    position: relative;
    overflow: hidden;
}
.venue-city-name { font-family: 'Bebas Neue', sans-serif; font-size: 2rem; letter-spacing: 2px; color: #fff; margin-bottom: 0.2rem; }
.venue-country { font-size: 11px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #475569; margin-bottom: 0.75rem; }
.venue-desc { font-size: 13px; color: #64748b; line-height: 1.55; margin-bottom: 1.2rem; }

/* ══════════════════════════════════════════
   BUTTONS
══════════════════════════════════════════ */
.stButton > button {
    font-family: 'Bebas Neue', sans-serif !important;
    letter-spacing: 2px !important;
    font-size: 1rem !important;
    border-radius: 10px !important;
    transition: all 0.2s ease !important;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #0077aa, #0099cc) !important;
    border: none !important;
    box-shadow: 0 4px 20px rgba(0,153,204,0.3) !important;
}
.stButton > button[kind="primary"]:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 30px rgba(0,153,204,0.4) !important;
}

/* ══════════════════════════════════════════
   FORM ELEMENTS
══════════════════════════════════════════ */
.stSelectbox > label, .stSlider > label, .stToggle > label, .stNumberInput > label {
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1.5px !important;
    text-transform: uppercase !important;
    color: #475569 !important;
}
[data-baseweb="select"] > div:first-child {
    background: rgba(13,18,38,0.8) !important;
    border-color: rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] > div:first-child:hover { border-color: rgba(0,212,255,0.3) !important; }

/* ══════════════════════════════════════════
   TABS
══════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(13,18,38,0.5) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255,255,255,0.05) !important;
    gap: 2px !important;
    padding: 4px !important;
}
.stTabs [data-baseweb="tab"] {
    font-size: 12px !important;
    font-weight: 600 !important;
    letter-spacing: 0.5px !important;
    color: #475569 !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
}
.stTabs [aria-selected="true"] {
    color: #00d4ff !important;
    background: rgba(0,212,255,0.1) !important;
}

/* ══════════════════════════════════════════
   EXPANDER
══════════════════════════════════════════ */
.streamlit-expanderHeader {
    background: rgba(13,18,38,0.5) !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
}

/* ══════════════════════════════════════════
   DATAFRAME
══════════════════════════════════════════ */
[data-testid="stDataFrame"] { border-radius: 12px; overflow: hidden; }

/* ══════════════════════════════════════════
   DISCLAIMER
══════════════════════════════════════════ */
.disclaimer-bar {
    font-size: 13px;
    color: #94a3b8;
    text-align: center;
    padding: 1.25rem 2rem;
    border-top: 1px solid rgba(255,255,255,0.10);
    margin-top: 3rem;
    letter-spacing: 0.3px;
    line-height: 1.7;
    background: rgba(255,255,255,0.03);
    border-radius: 0 0 8px 8px;
}

/* ══════════════════════════════════════════
   HOW IT WORKS — code blocks
══════════════════════════════════════════ */
.arch-block {
    background: rgba(0,0,0,0.4);
    border: 1px solid rgba(0,212,255,0.1);
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: #64748b;
    line-height: 1.7;
    overflow-x: auto;
}
.arch-block .hl { color: #00d4ff; }
.arch-block .hl2 { color: #7b2fff; }
.arch-block .hl3 { color: #ffd700; }
</style>
""", unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────

def hero_section(
    title="WORLD CUP<br>MATCH LAB",
    tagline="Predict matches. Build brackets. Spot upsets before they happen.",
    ball_image_path: str = None,
):
    """
    Hero section. Uses st.html() + base64 image embedding so the ball renders
    identically on local and Streamlit Cloud — no static URL routing dependency.
    """
    import os, base64

    # Locate ball: prefer passed path, then look in static/ relative to this file
    _path = ball_image_path
    if not _path or not os.path.exists(_path):
        _path = os.path.join(os.path.dirname(__file__), "..", "static", "ball.png")

    # Encode to base64 so the image is self-contained in the HTML — works everywhere
    if os.path.exists(_path):
        with open(_path, "rb") as f:
            ball_b64 = base64.b64encode(f.read()).decode()
        ball_src  = f"data:image/png;base64,{ball_b64}"
        has_ball  = True
    else:
        has_ball  = False
        ball_src  = ""

    # Use st.html() — bypasses Streamlit's markdown sanitizer entirely,
    # so complex HTML with animations and base64 images renders without issues.
    if has_ball:
        st.html(f"""
<style>
@keyframes ballFloat {{
    0%,100% {{ transform:translateY(0px) rotate(0deg); }}
    50%      {{ transform:translateY(-10px) rotate(4deg); }}
}}
@keyframes ballReveal {{
    from {{ opacity:0; transform:translateX(40px) scale(0.88); }}
    to   {{ opacity:1; transform:translateX(0)    scale(1);    }}
}}
.hero-ball-b64 {{
    position:relative; z-index:1;
    width:280px; height:auto;
    display:block; margin-left:auto;
    -webkit-mask-image:linear-gradient(to right,
        transparent 0%, rgba(0,0,0,0.05) 10%,
        rgba(0,0,0,0.5) 35%, black 58%);
    mask-image:linear-gradient(to right,
        transparent 0%, rgba(0,0,0,0.05) 10%,
        rgba(0,0,0,0.5) 35%, black 58%);
    filter:drop-shadow(0 0 28px rgba(0,212,255,0.35))
           drop-shadow(0 12px 36px rgba(0,0,0,0.6));
    animation:ballReveal 0.9s cubic-bezier(0.2,0,0,1) both,
              ballFloat  6s ease-in-out 1.2s infinite;
}}
</style>
<div style="
    position:relative; overflow:hidden; border-radius:20px;
    margin-bottom:2rem;
    background:linear-gradient(135deg,#0d1226 0%,#0f0a20 45%,#0d1226 100%);
    border:1px solid rgba(0,212,255,0.15);
    box-shadow:0 0 0 1px rgba(0,212,255,0.05),0 20px 60px rgba(0,0,0,0.6);
    display:flex; align-items:center; min-height:190px;
">
  <div style="position:absolute;top:0;left:8%;right:8%;height:1px;
    background:linear-gradient(90deg,transparent,rgba(0,212,255,0.45),transparent);"></div>
  <div style="flex:1;padding:2rem 1rem 2rem 2.5rem;position:relative;z-index:2;min-width:0;">
    <div style="font-size:10px;font-weight:700;letter-spacing:3px;text-transform:uppercase;
                color:#00d4ff;margin-bottom:.4rem;opacity:.8;">
      ⚽ 2026 FIFA World Cup · AI Prediction
    </div>
    <div style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
                color:#475569;margin-bottom:.75rem;">
      By Harry Hunter, PhD, MPH
    </div>
    <h1 style="font-family:'Bebas Neue',sans-serif;
               font-size:clamp(2.8rem,6vw,4.5rem);line-height:0.95;letter-spacing:3px;
               background:linear-gradient(135deg,#ffffff 0%,#e2e8f0 30%,#00d4ff 60%,#7b2fff 100%);
               -webkit-background-clip:text;-webkit-text-fill-color:transparent;
               background-clip:text;margin:0 0 .75rem 0;text-transform:uppercase;">
      {title}
    </h1>
    <p style="font-size:1.05rem;color:#64748b;font-weight:400;letter-spacing:.5px;margin:0;">
      {tagline}
    </p>
  </div>
  <div style="flex:0 0 300px;position:relative;display:flex;align-items:center;
              justify-content:flex-end;padding-right:1.5rem;align-self:stretch;overflow:visible;">
    <div style="position:absolute;right:0;top:50%;transform:translateY(-50%);
                width:340px;height:340px;border-radius:50%;pointer-events:none;
                background:radial-gradient(circle,rgba(0,212,255,0.13) 0%,
                rgba(123,47,255,0.09) 48%,transparent 70%);"></div>
    <img class="hero-ball-b64" src="{ball_src}" alt="FIFA 2026 Ball">
  </div>
</div>
""")

    else:
        # Fallback: text-only
        st.markdown(f"""
<div class="hero-outer">
  <div class="hero-eyebrow">⚽ 2026 FIFA World Cup · AI Prediction</div>
  <div style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;
              color:#475569;margin-bottom:.75rem;">By Harry Hunter, PhD, MPH</div>
  <h1 class="hero-title">{title}</h1>
  <p class="hero-tagline">{tagline}</p>
</div>""", unsafe_allow_html=True)


def page_hero(eyebrow, title, sub=""):
    # ── Back to Home button — prominent cyan pill, impossible to miss ──────────
    btn_key = f"back_home_{abs(hash(title)) % 99999}"

    # Inject scoped CSS that styles THIS button as a glowing cyan pill.
    # We target the immediately-following stButton by wrapping it in a div.
    st.markdown("""
<style>
.home-btn-wrap + div [data-testid="stBaseButton-secondary"] {
    background: rgba(0,212,255,0.12) !important;
    border: 1.5px solid rgba(0,212,255,0.55) !important;
    border-radius: 100px !important;
    color: #00d4ff !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 6px 20px !important;
    box-shadow: 0 0 16px rgba(0,212,255,0.18) !important;
    transition: all 0.18s ease !important;
    width: auto !important;
    display: inline-flex !important;
}
.home-btn-wrap + div [data-testid="stBaseButton-secondary"]:hover {
    background: rgba(0,212,255,0.22) !important;
    border-color: #00d4ff !important;
    box-shadow: 0 0 28px rgba(0,212,255,0.35) !important;
    color: #ffffff !important;
}
</style>
<div class="home-btn-wrap"></div>
""", unsafe_allow_html=True)

    if st.button("← Back to Home", key=btn_key):
        import streamlit as _st
        _st.session_state["_pending_page"]  = "🏠  Home"
        _st.session_state["_pending_state"] = {}
        _st.rerun()

    st.markdown(f"""
<div class="page-hero">
  <div class="page-eyebrow">{eyebrow}</div>
  <div class="page-title">{title}</div>
  {"<div class='page-sub'>" + sub + "</div>" if sub else ""}
</div>""", unsafe_allow_html=True)


# ── Section header ────────────────────────────────────────────────────────────

def section_header(text):
    st.markdown(f'<div class="section-hd">{text}</div>', unsafe_allow_html=True)


# ── KPI card ──────────────────────────────────────────────────────────────────

def metric_card(label, value, sub=""):
    st.markdown(f"""
<div class="kpi-card">
  <div class="kpi-lbl">{label}</div>
  <div class="kpi-val">{value}</div>
  {"<div class='kpi-sub'>" + sub + "</div>" if sub else ""}
</div>""", unsafe_allow_html=True)


# ── Team card header ──────────────────────────────────────────────────────────

def team_card_header(team_row):
    flag   = team_row.get("flag", "🏳️")
    name   = team_row.get("team", "Unknown")
    power  = team_row.get("power_score", 0)
    conf   = team_row.get("confederation", "")
    style  = team_row.get("style_tag", "")
    st.markdown(f"""
<div class="team-hero-card">
  <span class="team-flag-xl">{flag}</span>
  <div class="team-name-xl">{name}</div>
  <div class="team-conf">{conf} · {style}</div>
  <span class="power-number">{power}</span>
  <div class="power-label">Power Score</div>
</div>""", unsafe_allow_html=True)


# ── Upset card ────────────────────────────────────────────────────────────────

def upset_card(match, explanation=""):
    risk = match.get("risk", "low")
    pill_class = {"low": "upset-pill-low", "medium": "upset-pill-medium",
                  "high": "upset-pill-high", "very_high": "upset-pill-chaos"}.get(risk, "upset-pill-low")
    pill_label = {"low": "Minor Risk", "medium": "🪤 Trap Game",
                  "high": "🍌 Banana Peel", "very_high": "🚨 Chaos Alert"}.get(risk, "Risk")
    pct = int(match.get("upset_prob", 0) * 100)
    st.markdown(f"""
<div class="upset-wrapper">
  <span class="upset-pill {pill_class}">{pill_label}</span>
  <div class="upset-matchup">
    {match.get("underdog_flag","🏳️")} {match.get("underdog","?")}
    <span style="color:#1e293b;"> vs </span>
    {match.get("favorite_flag","🏳️")} {match.get("favorite","?")}
  </div>
  <div class="upset-prob">{pct}% upset probability</div>
  <div class="upset-body">{explanation}</div>
</div>""", unsafe_allow_html=True)


# ── Probability meter ─────────────────────────────────────────────────────────

def probability_meter(label, value, color="#00d4ff"):
    pct = int(min(1.0, max(0.0, value)) * 100)
    st.markdown(f"""
<div class="prob-row">
  <span class="prob-label">{label}</span>
  <div class="prob-track">
    <div class="prob-fill" style="width:{pct}%; background: linear-gradient(90deg, {color}88, {color});"></div>
  </div>
  <span class="prob-pct" style="color:{color};">{pct}%</span>
</div>""", unsafe_allow_html=True)


# ── Scoreline ─────────────────────────────────────────────────────────────────

def scoreline_display(goals_a, goals_b, team_a="", team_b=""):
    st.markdown(f"""
<div class="scoreline-wrap">
  <div class="scoreline-teams">
    <span class="scoreline-team">{team_a}</span>
    <div class="scoreline-digits">{goals_a}<span class="scoreline-sep"> – </span>{goals_b}</div>
    <span class="scoreline-team">{team_b}</span>
  </div>
  <div class="scoreline-caption">Most Likely Scoreline</div>
</div>""", unsafe_allow_html=True)


# ── Excitement ────────────────────────────────────────────────────────────────

def excitement_display(rating):
    flames = EXCITEMENT_FLAMES.get(rating, "🔥")
    st.markdown(f"""
<div class="flame-wrap">
  <div class="flame-emoji">{flames}</div>
  <div class="flame-caption">Excitement Rating {rating} / 5</div>
</div>""", unsafe_allow_html=True)


# ── Matchup banner ────────────────────────────────────────────────────────────

def matchup_banner(flag_a, team_a, flag_b, team_b, subtitle=""):
    st.markdown(f"""
<div class="matchup-banner">
  <div class="matchup-vs-text">
    {flag_a} {team_a}
    <span class="matchup-vs-sep"> vs </span>
    {team_b} {flag_b}
  </div>
  {"<div class='matchup-meta'>" + subtitle + "</div>" if subtitle else ""}
</div>""", unsafe_allow_html=True)


# ── Bracket match card ────────────────────────────────────────────────────────

def bracket_match_card(match):
    ta = match.get("team_a", "")
    tb = match.get("team_b", "")
    fa = match.get("flag_a", "🏳️")
    fb = match.get("flag_b", "🏳️")
    winner = match.get("winner", "")
    pa = int(match.get("prob_a", 0.5) * 100)
    pb = int(match.get("prob_b", 0.5) * 100)

    def row(flag, name, prob, is_w):
        cls = "winner" if is_w else ""
        trophy = "🏆 " if is_w else "      "
        return f'<div class="bracket-team-row"><span class="bracket-team-name {cls}">{flag} {trophy}{name}</span><span class="bracket-team-prob">{prob}%</span></div>'

    st.markdown(f"""
<div class="bracket-card">
  {row(fa, ta, pa, winner == ta)}
  <hr class="bracket-divider">
  {row(fb, tb, pb, winner == tb)}
</div>""", unsafe_allow_html=True)


# ── Champion banner ───────────────────────────────────────────────────────────

def champion_banner(champion_row, champ_prob, upsets, difficulty):
    flag = champion_row.get("flag", "🏳️") if champion_row is not None else "🏆"
    name = champion_row["team"] if champion_row is not None else "Unknown"

    # ── Build all pieces in Python first — no logic inside f-string ─────────
    if champ_prob >= 0.05:
        prob_val  = f"{champ_prob:.0%}"
        prob_note_html = ""
    elif champ_prob >= 0.01:
        prob_val  = f"{champ_prob:.1%}"
        prob_note_html = "<div style='font-size:10px;color:#475569;margin-top:2px;'>Dark horse run</div>"
    else:
        prob_val  = "Shock Winner"
        prob_note_html = "<div style='font-size:10px;color:#475569;margin-top:2px;'>That's chaos for you</div>"

    if difficulty >= 88:   diff_label = "Brutal"
    elif difficulty >= 83: diff_label = "Hard"
    elif difficulty >= 78: diff_label = "Moderate"
    else:                  diff_label = "Favourable"

    diff_note_html = f"<div style='font-size:10px;color:#475569;margin-top:2px;'>avg opp {difficulty:.0f}/100</div>"

    # Use st.html() — bypasses the markdown parser entirely.
    # st.markdown() runs content through Python-Markdown first; a blank line
    # from an empty variable terminates the HTML block, causing the rest to
    # render as escaped text. st.html() skips that step completely.
    st.html(f"""
<div class="champ-banner">
  <span class="champ-flag">{flag}</span>
  <div class="champ-name">🏆 {name}</div>
  <div class="champ-sub">Simulated World Cup Champion</div>
  <div class="champ-stats">
    <div class="champ-stat">
      <div class="champ-stat-lbl">Pre-Tournament Odds</div>
      <div class="champ-stat-val" style="color:#ffd700;">{prob_val}</div>
      {prob_note_html}
    </div>
    <div class="champ-stat">
      <div class="champ-stat-lbl">Path Difficulty</div>
      <div class="champ-stat-val" style="color:#00d4ff;">{diff_label}</div>
      {diff_note_html}
    </div>
    <div class="champ-stat">
      <div class="champ-stat-lbl">Upsets Along the Way</div>
      <div class="champ-stat-val" style="color:#ff6b35;">{upsets}</div>
    </div>
  </div>
</div>""")


# ── Verdict card ──────────────────────────────────────────────────────────────

def verdict_card(flag, team, champ_prob, verdict_text, verdict_color, best_finish, verdict_emoji):
    st.markdown(f"""
<div class="verdict-card glass-card" style="border-color: rgba({_hex_rgb(verdict_color)}, 0.25);
     box-shadow: 0 0 60px rgba({_hex_rgb(verdict_color)}, 0.06);">
  <span class="verdict-emoji">{flag} {verdict_emoji}</span>
  <div class="verdict-question">Can {team} win the World Cup?</div>
  <div class="verdict-answer" style="color:{verdict_color};">{verdict_text}</div>
  <div class="verdict-stats">
    <div>
      <div class="verdict-stat-lbl">Champion Probability</div>
      <div class="verdict-stat-val" style="color:{verdict_color};">{champ_prob:.1%}</div>
    </div>
    <div>
      <div class="verdict-stat-lbl">Best Realistic Finish</div>
      <div class="verdict-stat-val" style="color:#00d4ff; font-size:1.3rem; padding-top:4px;">{best_finish}</div>
    </div>
  </div>
</div>""", unsafe_allow_html=True)


def _hex_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16)
    return f"{r},{g},{b}"


# ── Disclaimer ────────────────────────────────────────────────────────────────

def disclaimer():
    st.markdown("""
<div class="disclaimer-bar">
  ⚠️ <strong>Sample data used for demonstration purposes only.</strong>
  Not affiliated with FIFA or any official organization.
  <span style="margin: 0 0.5rem; color: rgba(148,163,184,0.3);">|</span>
  Built with Excitement &nbsp;·&nbsp; Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; Plotly &nbsp;·&nbsp; SciPy
</div>""", unsafe_allow_html=True)
