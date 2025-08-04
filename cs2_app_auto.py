import streamlit as st
import numpy as np

# Dummy model to simulate prediction based on team/player stats
def predict_match(team1, team2):
    score = (
        0.4 * (team1['winrate'] - team2['winrate']) +
        0.2 * (team1['adr'] - team2['adr']) +
        0.2 * (team1['kast'] - team2['kast']) +
        0.2 * (team1['impact'] - team2['impact'])
    )
    prob = 1 / (1 + np.exp(-score / 100))
    return round(prob * 100, 2), round((1 - prob) * 100, 2)

st.set_page_config(page_title="CS2 Predictor", page_icon="🎯")
st.title("🎯 CS2 Match Predictor (Manual Input v1)")

st.header("Team 1 Stats")
t1_winrate = st.slider("Last Month Winrate (%)", 0, 100, 60)
t1_adr = st.slider("Team 1 ADR", 50, 120, 85)
t1_kast = st.slider("Team 1 KAST (%)", 50, 100, 75)
t1_impact = st.slider("Team 1 HLTV Impact Rating", 0.5, 2.0, 1.1)

st.header("Team 2 Stats")
t2_winrate = st.slider("Last Month Winrate (%)", 0, 100, 55)
t2_adr = st.slider("Team 2 ADR", 50, 120, 80)
t2_kast = st.slider("Team 2 KAST (%)", 50, 100, 70)
t2_impact = st.slider("Team 2 HLTV Impact Rating", 0.5, 2.0, 1.0)

if st.button("🔮 Predict Outcome"):
    team1 = {'winrate': t1_winrate, 'adr': t1_adr, 'kast': t1_kast, 'impact': t1_impact}
    team2 = {'winrate': t2_winrate, 'adr': t2_adr, 'kast': t2_kast, 'impact': t2_impact}
    p1, p2 = predict_match(team1, team2)
    st.success(f"Team 1 win chance: {p1}%")
    st.success(f"Team 2 win chance: {p2}%")
