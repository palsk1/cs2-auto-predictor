import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="CS2 Match Predictor – Auto HLTV Version", layout="centered")
st.title("🔮 CS2 Match Predictor – Auto HLTV Version")
st.caption("All stats fetched live from HLTV. Compare with Ottscrape for validation.")

mode = st.radio("Mode", ["Live HLTV Mode", "Test Mode"])

debug_log = []

def fetch_matches():
    url = "https://www.hltv.org/matches"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    try:
        debug_log.append(f"[INFO] Requesting {url}")
        debug_log.append(f"[HEADERS] {headers}")
        response = requests.get(url, headers=headers)
        debug_log.append(f"[STATUS] HTTP {response.status_code}")
        debug_log.append(f"[HTML length] {len(response.text)}")
        debug_log.append(f"[HTML snippet] {response.text[:300]}")
        if response.status_code == 403:
            st.error("⚠️ Could not fetch today's matches.")
        else:
            st.success("✅ Successfully fetched HLTV matches.")
    except Exception as e:
        st.error(f"Exception occurred: {e}")
        debug_log.append(f"[ERROR] {e}")

def run_test_mode():
    st.info("Test Mode Active. Simulating data...")
    st.success("✅ Simulated fetch of 3 matches.")
    debug_log.append("[TEST] Simulated match fetch success.")

if mode == "Live HLTV Mode":
    fetch_matches()
else:
    run_test_mode()

with st.expander("🔍 Debug Log"):
    for line in debug_log:
        st.text(line)
