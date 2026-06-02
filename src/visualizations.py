"""
Plotly and Pydeck visualization components for World Cup Match Lab.
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px


# ── Probability bar chart ─────────────────────────────────────────────────────

def probability_bar_chart(
    team_a: str, team_b: str,
    prob_a: float, prob_draw: float, prob_b: float,
    flag_a: str = "🏳️", flag_b: str = "🏳️",
) -> go.Figure:
    labels = [f"{flag_a} {team_a}", "Draw", f"{flag_b} {team_b}"]
    values = [prob_a * 100, prob_draw * 100, prob_b * 100]
    colors = ["#00d4ff", "#888888", "#ff6b35"]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(color=colors, line=dict(color="rgba(0,0,0,0)", width=0)),
        text=[f"{v:.1f}%" for v in values],
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(size=16, color="white", family="Arial Black"),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white", size=14),
        xaxis=dict(
            range=[0, 100],
            showgrid=False,
            showticklabels=False,
            zeroline=False,
        ),
        yaxis=dict(showgrid=False, tickfont=dict(size=15, family="Arial Black")),
        margin=dict(l=10, r=10, t=10, b=10),
        height=180,
        bargap=0.25,
    )
    return fig


# ── Team radar chart ─────────────────────────────────────────────────────────

def team_radar_chart(team_row: pd.Series, color: str = "#00d4ff") -> go.Figure:
    attrs = ["Attack", "Defense", "Midfield", "Goalkeeping", "Depth", "Recent Form", "Tournament Exp"]
    keys = ["attack", "defense", "midfield", "goalkeeping", "depth", "recent_form", "tournament_experience"]
    values = [float(team_row.get(k, 70)) for k in keys]
    values_closed = values + [values[0]]
    attrs_closed = attrs + [attrs[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=attrs_closed,
        fill="toself",
        fillcolor=f"rgba({_hex_to_rgb(color)}, 0.25)",
        line=dict(color=color, width=2.5),
        name=str(team_row.get("team", "Team")),
        hovertemplate="%{theta}: %{r}<extra></extra>",
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[50, 100], showticklabels=False, gridcolor="rgba(255,255,255,0.1)"),
            angularaxis=dict(tickfont=dict(size=12, color="white"), gridcolor="rgba(255,255,255,0.1)"),
            bgcolor="rgba(0,0,0,0)",
        ),
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=60, r=60, t=40, b=40),
        height=360,
    )
    return fig


def _hex_to_rgb(hex_color: str) -> str:
    hex_color = hex_color.lstrip("#")
    r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
    return f"{r},{g},{b}"


# ── Team strength bar chart ───────────────────────────────────────────────────

def team_strength_bar_chart(team_row: pd.Series) -> go.Figure:
    attrs = ["Power Score", "Attack", "Defense", "Midfield", "Goalkeeping", "Depth", "Form", "Experience"]
    keys = ["power_score", "attack", "defense", "midfield", "goalkeeping", "depth", "recent_form", "tournament_experience"]
    values = [float(team_row.get(k, 70)) for k in keys]

    cmap = px.colors.sample_colorscale("plasma", [v / 100 for v in values])

    fig = go.Figure(go.Bar(
        x=attrs,
        y=values,
        marker=dict(color=cmap),
        text=[str(int(v)) for v in values],
        textposition="outside",
        textfont=dict(color="white", size=13),
        hovertemplate="%{x}: %{y}<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(showgrid=False, tickfont=dict(size=12)),
        yaxis=dict(range=[0, 110], showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        margin=dict(l=10, r=10, t=10, b=10),
        height=300,
    )
    return fig


# ── Venue map (Plotly scatter_geo) ────────────────────────────────────────────

def venue_map(venues_df: pd.DataFrame, selected_city: str = None) -> go.Figure:
    df = venues_df.copy()
    df["size"] = df["crowd_energy"].clip(60, 100)
    df["label"] = df["city"] + " (" + df["country"] + ")"
    df["color"] = df["crowd_energy"]

    fig = go.Figure()

    # All cities
    fig.add_trace(go.Scattergeo(
        lat=df["lat"],
        lon=df["lon"],
        text=df["label"],
        customdata=df[["city", "country", "climate_vibe", "crowd_energy", "altitude_category"]].values,
        hovertemplate=(
            "<b>%{customdata[0]}, %{customdata[1]}</b><br>"
            "Climate: %{customdata[2]}<br>"
            "Crowd Energy: %{customdata[3]}/100<br>"
            "Altitude: %{customdata[4]}<extra></extra>"
        ),
        mode="markers+text",
        textposition="top center",
        textfont=dict(size=9, color="white"),
        marker=dict(
            size=df["size"] / 7,
            color=df["color"],
            colorscale="Plasma",
            cmin=70,
            cmax=100,
            line=dict(color="white", width=0.5),
            opacity=0.85,
        ),
        name="Venues",
    ))

    # Highlight selected
    if selected_city:
        sel = df[df["city"] == selected_city]
        if len(sel) > 0:
            fig.add_trace(go.Scattergeo(
                lat=sel["lat"],
                lon=sel["lon"],
                text=sel["city"],
                mode="markers+text",
                textposition="top center",
                textfont=dict(size=12, color="#ffd700", family="Arial Black"),
                marker=dict(size=22, color="#ffd700", symbol="star", line=dict(color="white", width=1)),
                name=selected_city,
                hoverinfo="skip",
            ))

    fig.update_layout(
        geo=dict(
            scope="north america",
            showland=True,
            landcolor="rgb(15,20,35)",
            showocean=True,
            oceancolor="rgb(8,12,28)",
            showcountries=True,
            countrycolor="rgba(255,255,255,0.15)",
            showcoastlines=True,
            coastlinecolor="rgba(255,255,255,0.2)",
            projection_type="natural earth",
            center=dict(lat=35, lon=-100),
            lonaxis_range=[-140, -55],
            lataxis_range=[15, 60],
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        margin=dict(l=0, r=0, t=0, b=0),
        height=480,
        showlegend=False,
    )
    return fig


# ── Champion probability donut ─────────────────────────────────────────────────

def champion_probability_chart(probs: dict, top_n: int = 10) -> go.Figure:
    items = sorted(probs.items(), key=lambda x: x[1], reverse=True)[:top_n]
    labels = [i[0] for i in items]
    values = [i[1] * 100 for i in items]

    fig = go.Figure(go.Bar(
        x=values,
        y=labels,
        orientation="h",
        marker=dict(
            color=values,
            colorscale="Plasma",
            showscale=False,
        ),
        text=[f"{v:.1f}%" for v in values],
        textposition="outside",
        textfont=dict(color="white", size=12),
        hovertemplate="%{y}: %{x:.1f}%<extra></extra>",
    ))

    max_val = max(values) if values else 10
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(range=[0, max_val * 1.35], showgrid=False, showticklabels=False),
        yaxis=dict(autorange="reversed", tickfont=dict(size=13)),
        margin=dict(l=10, r=90, t=10, b=10),
        height=380,
    )
    return fig


# ── Upset probability scatter ──────────────────────────────────────────────────

def upset_scatter(upset_matches: list) -> go.Figure:
    if not upset_matches:
        return go.Figure()

    labels = [f"{m['underdog']} vs {m['favorite']}" for m in upset_matches]
    probs = [m["upset_prob"] * 100 for m in upset_matches]
    colors = ["#ff2244" if p > 40 else "#ff8800" if p > 30 else "#ffd700" for p in probs]

    fig = go.Figure(go.Bar(
        x=probs,
        y=labels,
        orientation="h",
        marker=dict(color=colors),
        text=[f"{p:.0f}%" for p in probs],
        textposition="outside",
        textfont=dict(color="white", size=12),
        hovertemplate="%{y}: %{x:.1f}% upset chance<extra></extra>",
    ))

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        xaxis=dict(range=[0, 60], showgrid=True, gridcolor="rgba(255,255,255,0.08)"),
        yaxis=dict(autorange="reversed", tickfont=dict(size=12)),
        margin=dict(l=10, r=60, t=10, b=10),
        height=max(300, len(upset_matches) * 42),
    )
    return fig
