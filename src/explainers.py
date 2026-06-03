"""
Rule-based narrative generator for World Cup Match Lab.
Sounds like a sports analyst, not a data scientist.
Designed so the LLM provider can be swapped in later via generate_narrative().
"""

import random
from src.config import EXCITEMENT_FLAMES, UPSET_LABELS


# ── Public abstraction point ──────────────────────────────────────────────────

def generate_narrative(prompt: str, context: dict, api_key: str = None) -> str:
    """
    Entry point for narrative generation.
    Pass api_key to activate AI narratives; falls back to rule-based if unavailable.
    """
    if api_key:
        try:
            import anthropic
            client = anthropic.Anthropic(api_key=api_key)
            system = (
                "You are an elite sports analyst covering the 2026 FIFA World Cup. "
                "Write punchy, confident, fan-friendly match previews in 3-4 sentences. "
                "No bullet points. No jargon. Sound like ESPN, not a textbook."
            )
            msg = client.messages.create(
                model="claude-opus-4-5",
                max_tokens=250,
                system=system,
                messages=[{"role": "user", "content": prompt}],
            )
            return msg.content[0].text
        except Exception as e:
            # Graceful fallback — never crash the app over a narrative
            pass
    return _rule_based_narrative(prompt, context)


def build_match_prompt(prediction: dict, team_a_row, team_b_row) -> str:
    """Build the LLM prompt for a match preview."""
    ta = prediction["team_a"]
    tb = prediction["team_b"]
    pa = prediction["prob_a_win"]
    pb = prediction["prob_b_win"]
    la = prediction["lambda_a"]
    lb = prediction["lambda_b"]
    score_a = prediction["likely_score_a"]
    score_b = prediction["likely_score_b"]
    return (
        f"Write a 3-sentence World Cup match preview for {ta} vs {tb}. "
        f"The model gives {ta} a {pa:.0%} win probability and {tb} {pb:.0%}. "
        f"Expected goals: {ta} {la:.1f}, {tb} {lb:.1f}. "
        f"Most likely scoreline: {score_a}–{score_b}. "
        f"Key factors: {ta} attack {int(team_a_row.get('attack',75))}/100, "
        f"{tb} defense {int(team_b_row.get('defense',75))}/100. "
        f"Make it exciting and accessible to a casual fan."
    )


# ── Match explanation ─────────────────────────────────────────────────────────

def generate_match_explanation(prediction: dict, team_a_row, team_b_row) -> str:
    ta = prediction["team_a"]
    tb = prediction["team_b"]
    pa = prediction["prob_a_win"]
    pb = prediction["prob_b_win"]
    pd_ = prediction["prob_draw"]
    la = prediction["lambda_a"]
    lb = prediction["lambda_b"]
    upset = prediction["upset_risk"]
    rnd = prediction["round"]

    favorite = ta if pa > pb else tb
    underdog = tb if pa > pb else ta
    fav_prob = max(pa, pb)
    dog_prob = min(pa, pb)

    att_a = float(team_a_row.get("attack", 75))
    att_b = float(team_b_row.get("attack", 75))
    def_a = float(team_a_row.get("defense", 75))
    def_b = float(team_b_row.get("defense", 75))
    form_a = float(team_a_row.get("recent_form", 75))
    form_b = float(team_b_row.get("recent_form", 75))

    lines = []

    # Opening hook
    if fav_prob > 0.70:
        lines.append(f"**{favorite}** comes in as a heavy favorite and the numbers back it up.")
    elif fav_prob > 0.55:
        lines.append(f"This is a genuine contest — **{favorite}** holds an edge, but **{underdog}** is dangerous.")
    else:
        lines.append(f"Buckle up. This matchup is almost too close to call. Either team can win this.")

    # Attack narrative
    if att_a > att_b + 8:
        lines.append(f"**{ta}**'s attack ({int(att_a)}) is the most potent weapon on the pitch — expect them to dominate possession in the final third.")
    elif att_b > att_a + 8:
        lines.append(f"**{tb}** brings a sharper attack ({int(att_b)}) and will look to exploit space with pace and creativity.")
    else:
        lines.append(f"Both teams carry genuine attacking threat — goals could come from either end.")

    # Defense narrative
    if def_a > 85 and def_b > 85:
        lines.append("Two elite defenses means this could be a cagey, tactical battle decided by a single moment.")
    elif def_a < 74:
        lines.append(f"**{ta}**'s defensive numbers are a concern — **{tb}** will look to press high and exploit gaps early.")
    elif def_b < 74:
        lines.append(f"**{tb}** has shown defensive vulnerabilities that **{ta}** will target relentlessly.")

    # Form narrative
    if form_a > 88:
        lines.append(f"**{ta}** arrives in scorching form — momentum is a powerful force at this stage.")
    if form_b > 88:
        lines.append(f"**{tb}** has hit top gear recently and will be difficult to stop.")

    # Round narrative
    if rnd == "Final":
        lines.append("The World Cup Final. Every player on that pitch has dreamed of this moment since childhood. Expect nerves, brilliance, and drama.")
    elif rnd == "Semifinal":
        lines.append("Semi-final pressure has a way of separating the great teams from the very good ones.")
    elif rnd == "Quarterfinal":
        lines.append("At the quarterfinal stage, tactical discipline often wins over raw talent.")

    # Upset narrative
    if upset == "very_high":
        lines.append(f"⚠️ **Upset Alert**: {underdog} has a real shot here at {dog_prob:.0%}. Don't sleep on this one.")
    elif upset == "high":
        lines.append(f"🔔 {underdog} is capable of an upset — their numbers suggest this is no foregone conclusion.")

    # Expected goals closer
    lines.append(
        f"The model projects **{la:.1f} expected goals** for {ta} and **{lb:.1f}** for {tb}. "
        f"Most likely scoreline: **{prediction['likely_score_a']}–{prediction['likely_score_b']}**."
    )

    return "\n\n".join(lines)


# ── Team summary ──────────────────────────────────────────────────────────────

def generate_team_summary(team_row) -> str:
    name = team_row.get("team", "This team")
    power = float(team_row.get("power_score", 75))
    attack = float(team_row.get("attack", 75))
    defense = float(team_row.get("defense", 75))
    form = float(team_row.get("recent_form", 75))
    exp = float(team_row.get("tournament_experience", 75))
    vol = float(team_row.get("volatility", 30))
    style = team_row.get("style_tag", "Unknown")

    lines = []

    if power >= 90:
        lines.append(f"**{name}** is a true World Cup contender. The model rates them among the top teams in the tournament.")
    elif power >= 80:
        lines.append(f"**{name}** is a legitimate threat — strong enough to beat anyone on their day.")
    elif power >= 70:
        lines.append(f"**{name}** sits in the solid mid-tier: dangerous to the elite, capable of deep runs in favorable brackets.")
    else:
        lines.append(f"**{name}** is the underdog story — every great tournament needs one.")

    if attack >= 88:
        lines.append(f"Their attack is world-class ({int(attack)}/100) — opposing defenses will be tested severely.")
    elif attack >= 78:
        lines.append(f"They carry a capable attacking unit that can punish defensive lapses.")

    if defense >= 85:
        lines.append(f"Defensively, they are elite — conceding is genuinely difficult against this side.")
    elif defense < 72:
        lines.append(f"Their defense is a vulnerability. Under sustained pressure, gaps can appear.")

    if form >= 88:
        lines.append("Recent form is excellent — they arrive in the tournament on a confidence high.")
    elif form < 72:
        lines.append("Recent form is a concern — they may need time to find their rhythm.")

    if vol >= 40:
        lines.append(f"High volatility ({int(vol)}) means they can be unpredictable — capable of stunning brilliance or a shock exit.")
    elif vol <= 25:
        lines.append(f"Low volatility ({int(vol)}) suggests a reliable, consistent performer. Few surprises from them.")

    lines.append(f"**Playing style:** {style}")

    # Biggest weakness
    attrs = {"Attack": attack, "Defense": defense, "Form": form, "Experience": exp}
    weakest = min(attrs, key=attrs.get)
    lines.append(f"**Biggest weakness to exploit:** {weakest} ({int(attrs[weakest])}/100)")

    return "\n\n".join(lines)


# ── Upset explanation ─────────────────────────────────────────────────────────

def generate_upset_explanation(match: dict) -> str:
    fav = match.get("favorite", "The favorite")
    dog = match.get("underdog", "The underdog")
    upset_prob = match.get("upset_prob", 0.25)
    dog_form = match.get("dog_form", 75)
    dog_defense = match.get("dog_defense", 75)
    fav_power = match.get("fav_power", 85)
    dog_power = match.get("dog_power", 70)
    gap = fav_power - dog_power

    lines = []

    if dog_form >= 85:
        lines.append(f"**{dog}** is in red-hot form right now — form beats reputation on the big stage.")
    if dog_defense >= 78:
        lines.append(f"Their defensive organization ({int(dog_defense)}/100) can neutralize even elite attacks.")
    if gap <= 10:
        lines.append(f"The power gap between these teams is smaller than the rankings suggest — just {int(gap)} points separates them.")
    if upset_prob >= 0.40:
        lines.append(f"At **{upset_prob:.0%}** upset probability, this isn't a fluke scenario — it's a genuine threat.")
    elif upset_prob >= 0.30:
        lines.append(f"**{upset_prob:.0%}** upset probability puts this firmly in 'trap game' territory.")

    lines.append(f"**{fav}** will need to bring their A-game or risk an early exit.")

    return " ".join(lines)


# ── Can My Team Win ───────────────────────────────────────────────────────────

def generate_can_team_win_summary(
    team_row,
    champion_prob: float,
    finish_data: dict,
) -> str:
    name = team_row.get("team", "Your team")
    flag = team_row.get("flag", "🏳️")
    power = float(team_row.get("power_score", 75))
    form = float(team_row.get("recent_form", 75))
    exp = float(team_row.get("tournament_experience", 75))
    vol = float(team_row.get("volatility", 30))

    best_finish = finish_data.get("best_realistic_finish", "Round of 16")
    finish_probs = finish_data.get("finish_probs", {})
    qf_plus = sum(finish_probs.get(k, 0) for k in ["Champion", "Runner-Up", "Semifinal", "Quarterfinal"])

    lines = []

    # Verdict
    if champion_prob >= 0.15:
        verdict = f"{flag} **Yes — {name} is a genuine World Cup contender.**"
    elif champion_prob >= 0.06:
        verdict = f"{flag} **Yes, but the path is difficult.** {name} has the quality to go deep."
    elif champion_prob >= 0.02:
        verdict = f"{flag} **Possible, but unlikely.** {name} would need several things to go right."
    else:
        verdict = f"{flag} **It's a long shot.** But that's what makes the World Cup magical."

    lines.append(verdict)

    # Realistic finish
    lines.append(
        f"**Best realistic finish:** {best_finish} | "
        f"**Quarterfinal or better chance:** {qf_plus:.0%}"
    )

    # Narrative
    if power >= 88:
        lines.append(f"{name} is a tournament-caliber side with the squad depth to handle adversity.")
    elif power >= 75:
        lines.append(f"{name} is capable of beating any mid-tier opponent and causing problems for elites on a good day.")
    else:
        lines.append(f"{name} will need a favorable bracket draw and near-perfect performances to advance deep.")

    if form >= 85:
        lines.append("Current form is a major asset — they arrive in confidence.")
    if exp >= 85:
        lines.append("Tournament experience means they won't be rattled by the big-stage pressure.")
    if vol >= 40:
        lines.append("High volatility is a double-edged sword — unpredictable enough to shock the world, but also capable of self-destructing.")

    # What needs to go right
    needs = []
    if form < 75:
        needs.append("find form quickly in the group stage")
    if exp < 70:
        needs.append("stay composed on the big stage")
    if power < 75:
        needs.append("get a favorable bracket draw")
    needs.append("stay injury-free through the knockout rounds")

    if needs:
        lines.append("**What needs to go right:** " + ", ".join(needs).capitalize() + ".")

    return "\n\n".join(lines)


# ── Internal ──────────────────────────────────────────────────────────────────

def _rule_based_narrative(prompt: str, context: dict) -> str:
    """Fallback rule-based narrative. Replace with LLM call when ready."""
    return f"[AI Preview] {context.get('summary', 'Match analysis coming soon.')}"
