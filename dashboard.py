# tiktok_reward_dashboard.py
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()  # Load .env file in local dev

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    st.error("Supabase credentials not found. Please check your .env file.")
    st.stop()

supabase: Client = create_client(url, key)

# -------------------------------
# Fetch Videos + Creators
# -------------------------------
def fetch_videos():
    response = supabase.table("videos").select(
        "id, title, views, likes, shares, watch_time, comments, gifts, "
        "streamers(age, ip_address)"
    ).execute()
    if response.data:
        return pd.DataFrame(response.data)
    return pd.DataFrame([])

videos = fetch_videos()

if videos.empty:
    st.error("No video data found in Supabase.")
    st.stop()

# -------------------------------
# Helper Functions
# -------------------------------
def calculate_credits(video):
    credits = {}
    
    # Views
    v = video["views"]
    if 50_000 <= v < 100_000: credits["views"] = 1
    elif 100_000 <= v < 200_000: credits["views"] = 2
    elif 200_000 <= v < 400_000: credits["views"] = 3
    elif 400_000 <= v < 500_000: credits["views"] = 4
    elif v >= 500_000: credits["views"] = 5
    
    # Likes
    l = video["likes"]
    if 10_000 <= l < 20_000: credits["likes"] = 1
    elif 20_000 <= l < 50_000: credits["likes"] = 2
    elif 50_000 <= l < 100_000: credits["likes"] = 3
    elif 100_000 <= l < 200_000: credits["likes"] = 4
    elif l >= 200_000: credits["likes"] = 5
    
    # Shares
    s = video["shares"]
    if 10 <= s < 50: credits["shares"] = 1
    elif 50 <= s < 100: credits["shares"] = 2
    elif 100 <= s < 500: credits["shares"] = 3
    elif 500 <= s < 1000: credits["shares"] = 4
    elif s >= 1000: credits["shares"] = 5
    
    # Watch Time
    r = video["watch_time"]
    if 20 <= r < 100: credits["retention"] = 1
    elif 100 <= r < 300: credits["retention"] = 2
    elif 300 <= r < 1000: credits["retention"] = 3
    elif 1000 <= r < 5000: credits["retention"] = 4
    elif r >= 5000: credits["retention"] = 5
    
    # Comments
    c = video["comments"]
    if 20 <= c < 100: credits["comments"] = 1
    elif 100 <= c < 300: credits["comments"] = 2
    elif 300 <= c < 1000: credits["comments"] = 3
    elif 1000 <= c < 5000: credits["comments"] = 4
    elif c >= 5000: credits["comments"] = 5
    
    # Total credits
    total = sum(credits.values())
    
    # Bonus
    if total > 40:
        credits["bonus"] = 10
        total += 10
    else:
        credits["bonus"] = 0
        
    credits["total"] = total
    return credits

def reward_tier(total_credits):
    if total_credits >= 70:
        return "E-wallet $5 + Exposure 20 min"
    elif total_credits >= 40:
        return "Exposure 10 min on FYP"
    else:
        return "No reward / low exposure"

def check_fraud(video):
    alerts = []
    streamer = video.get("streamers") or {}
    age = streamer.get("age")
    ip = streamer.get("ip_address")

    if age and age < 18:
        alerts.append("Below age threshold")
    if video["gifts"] > 500:
        alerts.append("High gift spike")
    if video["views"] > 1000 and video["comments"] == 0:
        alerts.append("Bot-like engagement")
    return ", ".join(alerts) if alerts else "None"

# Apply functions
videos["credits"] = videos.apply(calculate_credits, axis=1)
videos["reward"] = videos["credits"].apply(lambda x: reward_tier(x["total"]))
videos["fraud_alert"] = videos.apply(check_fraud, axis=1)

# -------------------------------
# Streamlit Layout
# -------------------------------
st.set_page_config(page_title="TikTok Reward Dashboard", layout="wide")
st.title("TikTok Creator Reward Dashboard")

# TikTok Styling
st.markdown("""
<style>
body { background-color: #010101; color: white; }
.stButton>button { font-weight: bold; color: black; }
.stButton>button:hover { background-color: #FE2C55; color: white; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Top Tab Buttons
# -------------------------------
tab_selected = st.session_state.get("tab", "overview")
col1, col2 = st.columns(2)
with col1:
    if st.button("Overview & Goals"):
        st.session_state["tab"] = "overview"
with col2:
    if st.button("Videos & Rewards"):
        st.session_state["tab"] = "videos"
tab_selected = st.session_state.get("tab", "overview")

# -------------------------------
# Overview Tab
# -------------------------------
if tab_selected == "overview":
    st.header("Overview & Goals")
    
    total_points = sum([v["total"] for v in videos["credits"]])
    st.metric("Total Points Across Videos", total_points)
    
    st.subheader("Bonus Points & Achievements")
    for index, row in videos.iterrows():
        st.write(f"{row['title']}: +{row['credits']['bonus']} bonus points")
    
    st.subheader("Targets & Progress")
    st.write("Views Target")
    st.progress(min(videos["views"].sum()/1_500_000,1.0))
    st.write("Gifts Target")
    st.progress(min(videos["gifts"].sum()/1_500,1.0))
    st.write("Engagement Target")
    st.progress(min(videos["comments"].sum()/7_000,1.0))

# -------------------------------
# Videos & Rewards Tab
# -------------------------------
if tab_selected == "videos":
    st.header("Videos & Rewards")
    
    for index, row in videos.iterrows():
        with st.expander(f"{row['title']}"):
            st.write(f"**Content Credits:** {row['credits']['total']}")
            st.write("**Credit Breakdown:**")
            for k,v in row['credits'].items():
                if k != "total":
                    st.write(f"- {k.capitalize()}: {v}")
            st.write(f"**Reward Tier:** {row['reward']}")
            st.write(f"**Fraud / Safety Alert:** {row['fraud_alert']}")
