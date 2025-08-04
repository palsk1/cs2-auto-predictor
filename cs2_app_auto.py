import streamlit as st
import requests
from bs4 import BeautifulSoup
import random
import time
from datetime import datetime
import traceback

st.set_page_config(page_title="CS2 Predictor", page_icon="🎯")
st.title("🎯 CS2 Predictor – Stable Scraper Build")

# Cache results in memory
@st.cache_data(ttl=3600)
def fetch_today_matches():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    ]

    headers = {
        "User-Agent": random.choice(user_agents)
    }

    url = "https://www.hltv.org/matches"
    retries = 3
    for attempt in range(retries):
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code == 403:
                st.warning(f"403 Forbidden – attempt {attempt + 1}, retrying...")
                time.sleep(1 + attempt * 2)
                continue
            elif res.status_code != 200:
                return [], f"Error {res.status_code}"
            soup = BeautifulSoup(res.text, "html.parser")
            today = datetime.now().strftime("%A, %B %-d").replace(" 0", " ")
            st.text(f"📅 Matching section for: {today}")
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
                return [], "No section found for today"
            return matches, None
        except Exception as e:
            if attempt == retries - 1:
                return [], str(e)
            time.sleep(1 + attempt * 2)
    return [], "Failed after retries"

try:
    matches, err = fetch_today_matches()
    if err:
        st.error(f"❌ Error: {err}")
    elif not matches:
        st.warning("⚠️ No matches found for today.")
    else:
        st.success(f"✅ Found {len(matches)} matches for today.")
        for team1, team2, event in matches:
            st.markdown(f"### {team1} vs {team2} ({event})")
except Exception as e:
    st.error("❌ Critical error during scraping")
    st.code(traceback.format_exc())
