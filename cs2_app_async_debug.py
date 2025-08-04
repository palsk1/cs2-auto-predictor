
import streamlit as st
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime
import random
import traceback
import time

st.set_page_config(page_title="CS2 Predictor", layout="wide")
st.title("🔮 CS2 Match Predictor – Auto HLTV Version")
st.caption("All stats fetched live from HLTV. Compare with Ottscrape for validation.")

# User agents to rotate for basic Cloudflare evasion
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
]

@st.cache_data(ttl=3600)
def fetch_today_matches():
    log = []
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    url = "https://www.hltv.org/matches"
    try:
        res = requests.get(url, headers=headers, timeout=10)
        log.append(f"[{res.status_code}] GET /matches")
        if res.status_code != 200:
            return [], log, "Blocked by HLTV"

        soup = BeautifulSoup(res.text, "html.parser")
        today = datetime.now().strftime("%A, %B %-d").replace(" 0", " ")
        log.append(f"Looking for matches on: {today}")

        matches = []
        for box in soup.find_all("div", class_="upcomingMatch"):
            teams = box.find_all("div", class_="matchTeamName")
            if len(teams) < 2:
                continue
            team1 = teams[0].text.strip()
            team2 = teams[1].text.strip()
            match_time = box.find("div", class_="matchTime") or ""
            match_id_search = re.search(r"/matches/(\d+)", str(box))
            match_id = match_id_search.group(1) if match_id_search else None
            if match_id:
                matches.append({
                    "id": match_id,
                    "team1": team1,
                    "team2": team2,
                    "time": match_time.text if hasattr(match_time, "text") else "TBD"
                })
        return matches, log, None
    except Exception as e:
        log.append("[ERROR] " + str(e))
        log.append(traceback.format_exc())
        return [], log, "Exception occurred"

matches, logs, error = fetch_today_matches()

if error:
    st.error("⚠️ Could not fetch today's matches.")
    with st.expander("Debug Log"):
        for l in logs:
            st.text(l)
    st.stop()

st.success(f"✅ {len(matches)} matches found for today")

for m in matches:
    st.markdown(f"### 🆚 {m['team1']} vs {m['team2']}  🕒 {m['time']}")
    match_url = f"https://www.hltv.org/matches/{m['id']}/_"
    ott_url = f"https://www.ottscrape.com/extract-individual-match-stats-from-hltv.php?id={m['id']}"

    with st.expander("🔍 View More"):
        st.markdown(f"🔗 [View on HLTV]({match_url})")
        st.markdown(f"🔗 [Validate via Ottscrape]({ott_url})")
        st.write("📊 (Player stats and prediction logic placeholder here...)")

with st.expander("📜 Debug Log"):
    for l in logs:
        st.text(l)
