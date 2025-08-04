import streamlit as st
import requests
from bs4 import BeautifulSoup
import numpy as np
import traceback
from datetime import datetime

st.set_page_config(page_title="CS2 Predictor", page_icon="🔍")
st.title("🔍 CS2 Predictor – Today's Matches Only")

try:
    st.text("🔍 Fetching HLTV matches...")
    res = requests.get("https://www.hltv.org/matches", headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    st.text(f"✅ Match page status: {res.status_code}")

    soup = BeautifulSoup(res.text, "html.parser")
    today = datetime.now().strftime("%A, %B %-d").replace(" 0", " ")
    st.text(f"📅 Filtering matches for: {today}")

    match_sections = soup.find_all("div", class_="standard-box")
    matches = []
    found_today = False

    for section in match_sections:
        header = section.find("span", class_="standard-headline")
        if header and today in header.text:
            found_today = True
            cards = section.find_all("div", class_="upcomingMatch")
            for card in cards:
                teams = card.find_all("div", class_="matchTeamName")
                if len(teams) == 2:
                    t1 = teams[0].text.strip()
                    t2 = teams[1].text.strip()
                    event = card.find("div", class_="matchEventName")
                    matches.append((t1, t2, event.text.strip() if event else "Unknown"))

    if not found_today:
        st.warning("⚠️ No section found for today's matches.")
    elif not matches:
        st.warning("⚠️ No matches found for today.")
    else:
        st.text(f"✅ Found {len(matches)} matches for today.")
        for m in matches:
            team1, team2, event = m
            st.markdown(f"### {team1} vs {team2} ({event})")

except Exception as e:
    st.error("❌ Error during scraping")
    st.code(traceback.format_exc())
