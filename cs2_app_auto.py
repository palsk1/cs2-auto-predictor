import streamlit as st
import numpy as np

# Placeholder for auto-fetching match logic (replace with real API later)
matches = [
    {"team1": "Team Vitality", "team2": "G2 Esports", "stats": [62, 1.12, 74, 1.08, 58, 1.08, 72, 1.05]},
    {"team1": "NaVi", "team2": "Astralis", "stats": [57, 1.10, 70, 1.04, 53, 1.06, 68, 1.02]}
]

def predict(stats):
    t1_wr, t1_rt, t1_kast, t1_imp, t2_wr, t2_rt, t2_kast, t2_imp = stats
    score = (
        0.4 * (t1_wr - t2_wr) +
        0.2 * (t1_rt - t2_rt) * 100 +
        0.2 * (t1_kast - t2_kast) +
        0.2 * (t1_imp - t2_imp) * 100
    )
    prob = 1 / (1 + np.exp(-score / 100))
    return round(prob * 100, 2), round((1 - prob) * 100, 2)

st.set_page_config(page_title="CS2 Predictor", page_icon="🔮")
st.title("🔮 CS2 Match Predictor (Auto Fetch – Simulated)")

st.markdown("Click a match below to see predicted win chances based on recent form and player stats.")

for match in matches:
    if st.button(f"{match['team1']} vs {match['team2']}"):
        p1, p2 = predict(match['stats'])
        st.success(f"{match['team1']} win chance: {p1}%")
        st.success(f"{match['team2']} win chance: {p2}%")
