
import streamlit as st
import asyncio
from hltv_async_api.endpoints.matches import get_upcoming_matches

st.set_page_config(page_title="CS2 Predictor – Async Debug", layout="centered")

st.title("🔍 CS2 Predictor – Async Scraper Debug Build")
debug_log = []

async def fetch_matches():
    try:
        debug_log.append("[INFO] Fetching upcoming matches...")
        matches = await get_upcoming_matches()
        debug_log.append(f"[SUCCESS] Retrieved {len(matches)} matches.")
        for match in matches:
            st.write(f"🆚 {match['team1']['name']} vs {match['team2']['name']}")
    except Exception as e:
        debug_log.append(f"[ERROR] {e}")
        st.error("❌ Failed to fetch matches")

# Run the async function in event loop
asyncio.run(fetch_matches())

with st.expander("📜 Debug Log"):
    for line in debug_log:
        st.text(line)
