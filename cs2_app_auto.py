import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
import traceback

st.set_page_config(page_title="CS2 Predictor – Debug", page_icon="🛠️")
st.title("🛠️ CS2 Predictor – Deep Debug Build")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
]

@st.cache_data(ttl=3600)
def fetch_today_matches():
    logs = []
    headers = { "User-Agent": random.choice(user_agents) }
    url = "https://www.hltv.org/matches"

    try:
        logs.append(f"[INFO] Requesting {url}")
        logs.append(f"[HEADERS] {headers}")
        res = requests.get(url, headers=headers, timeout=10)
        logs.append(f"[STATUS] HTTP {res.status_code}")
        logs.append(f"[HTML length] {len(res.text)}")
        snippet = res.text[:500].replace('\n', ' ').replace('\r', '')
        logs.append(f"[HTML snippet] {snippet[:300]}...")

        if res.status_code != 200:
            return [], logs, f"HTTP {res.status_code}"

        soup = BeautifulSoup(res.text, "html.parser")
        today = datetime.now().strftime("%A, %B %-d").replace(" 0", " ")
        logs.append(f"[INFO] Searching for match section: {today}")

        match_sections = soup.find_all("div", class_="standard-box")
        matches = []
        for section in match_sections:
            header = section.find("span", class_="standard-headline")
            if header and today in header.text:
                cards = section.find_all("div", class_="upcomingMatch")
                for card in cards:
                    teams = card.find_all("div", class_="matchTeamName")
                    if len(teams) == 2:
                        t1 = teams[0].text.strip()
                        t2 = teams[1].text.strip()
                        event = card.find("div", class_="matchEventName")
                        matches.append((t1, t2, event.text.strip() if event else "Unknown"))
        return matches, logs, None

    except Exception as e:
        logs.append("[EXCEPTION]")
        logs.append(traceback.format_exc())
        return [], logs, str(e)

matches, logs, error = fetch_today_matches()

if error:
    st.error(f"❌ Error: {error}")

if matches:
    st.success(f"✅ Found {len(matches)} matches for today.")
    for team1, team2, event in matches:
        st.markdown(f"### {team1} vs {team2} ({event})")
else:
    st.warning("⚠️ No matches found.")

with st.expander("📜 Debug Log"):
    for log in logs:
        st.text(log)
