import streamlit as st
import requests
import numpy as np
import traceback

MATCHES_URL = "https://hltv-api.vercel.app/api/matches"

def fetch_matches():
    try:
        res = requests.get(MATCHES_URL, timeout=10)
        if res.status_code == 200:
            return res.json(), None
        else:
            return None, f"HTTP {res.status_code}: {res.text}"
    except Exception as e:
        return None, traceback.format_exc()

def fake_fetch_team_stats(team):
    return {
        "winrate": np.random.randint(45, 70),
        "rating": round(np.random.uniform(0.95, 1.15), 2),
        "kast": np.random.randint(68, 76),
        "adr": np.random.randint(75, 92),
        "impact": round(np.random.uniform(0.95, 1.20), 2),
        "form": [np.random.choice(["W", "L"]) for _ in range(5)]
    }

def predict(t1, t2):
    score = (
        0.3 * (t1['winrate'] - t2['winrate']) +
        0.2 * (t1['rating'] - t2['rating']) * 100 +
        0.15 * (t1['kast'] - t2['kast']) +
        0.15 * (t1['adr'] - t2['adr']) +
        0.2 * (t1['impact'] - t2['impact']) * 100
    )
    prob = 1 / (1 + np.exp(-score / 100))
    return round(prob * 100, 2), round((1 - prob) * 100, 2)

def form_text(form_list):
    return " ".join(form_list)

st.set_page_config(page_title="CS2 Predictor", page_icon="🎯")
st.title("🎯 CS2 Auto Match Predictor")

matches, error = fetch_matches()
if not matches:
    st.error("❌ Failed to fetch real matches from HLTV API.")
    if error:
        st.code(error, language="bash")
    st.stop()

for m in matches[:5]:
    team1 = m.get("team1", {}).get("name", "Team A")
    team2 = m.get("team2", {}).get("name", "Team B")
    if st.button(f"{team1} vs {team2}"):
        stats1 = fake_fetch_team_stats(team1)
        stats2 = fake_fetch_team_stats(team2)
        p1, p2 = predict(stats1, stats2)

        st.markdown(f"## 🔮 Prediction")
        st.success(f"**{team1}** win chance: {p1}%")
        st.error(f"**{team2}** win chance: {p2}%")

        st.markdown("### 📊 View More")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{team1}**")
            st.write(stats1)
            st.text("Form: " + form_text(stats1['form']))
        with col2:
            st.markdown(f"**{team2}**")
            st.write(stats2)
            st.text("Form: " + form_text(stats2['form']))

        if abs(p1 - p2) > 10:
            better = team1 if p1 > p2 else team2
            st.markdown(f"💡 **{better} is favored by the model.**")
