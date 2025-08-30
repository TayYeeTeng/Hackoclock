# tiktok_reward_dashboard.py
import streamlit as st
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# -------------------------------
# Load Environment Variables
# -------------------------------
load_dotenv()

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
        "video_id, url, views, likes, shares, bookmarks, engagement_rate, gifts, gifts_value, comments, video_points, creators(creator_id, username, follower_count, video_count, avg_engagement_rate, total_points)"
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
    v = video.get("views", 0)
    if 50_000 <= v < 100_000: credits["views"] = 1
    elif 100_000 <= v < 200_000: credits["views"] = 2
    elif 200_000 <= v < 400_000: credits["views"] = 3
    elif 400_000 <= v < 500_000: credits["views"] = 4
    elif v >= 500_000: credits["views"] = 5
    
    # Likes
    l = video.get("likes", 0)
    if 10_000 <= l < 20_000: credits["likes"] = 1
    elif 20_000 <= l < 50_000: credits["likes"] = 2
    elif 50_000 <= l < 100_000: credits["likes"] = 3
    elif 100_000 <= l < 200_000: credits["likes"] = 4
    elif l >= 200_000: credits["likes"] = 5
    
    # Shares
    s = video.get("shares", 0)
    if 10 <= s < 50: credits["shares"] = 1
    elif 50 <= s < 100: credits["shares"] = 2
    elif 100 <= s < 500: credits["shares"] = 3
    elif 500 <= s < 1000: credits["shares"] = 4
    elif s >= 1000: credits["shares"] = 5
    
    # Comments
    c = video.get("comments", 0)
    if 20 <= c < 100: credits["comments"] = 1
    elif 100 <= c < 300: credits["comments"] = 2
    elif 300 <= c < 1000: credits["comments"] = 3
    elif 1000 <= c < 5000: credits["comments"] = 4
    elif c >= 5000: credits["comments"] = 5
    
    # Gifts (fraud sensitive)
    g = video.get("gifts", 0)
    if 10 <= g < 50: credits["gifts"] = 1
    elif 50 <= g < 200: credits["gifts"] = 2
    elif 200 <= g < 500: credits["gifts"] = 3
    elif 500 <= g < 1000: credits["gifts"] = 4
    elif g >= 1000: credits["gifts"] = 5
    
    # Total credits
    total = sum(credits.values())
    
    # Bonus
    if total > 15:
        credits["bonus"] = 5
        total += 5
    else:
        credits["bonus"] = 0
        
    credits["total"] = total
    return credits

def reward_tier(total_credits):
    if total_credits >= 20:
        return "E-wallet $5 + Exposure 20 min"
    elif total_credits >= 12:
        return "Exposure 10 min on FYP"
    else:
        return "No reward / low exposure"

def check_fraud(video):
    alerts = []
    if video.get("gifts", 0) > 500:
        alerts.append("High gift spike")
    if video.get("views", 0) > 1000 and video.get("comments", 0) == 0:
        alerts.append("Bot-like engagement")
    if video.get("likes", 0) == 0 and video.get("views", 0) > 5000:
        alerts.append("Suspicious low likes")
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
.stButton>button { font-weight: bold; background-color: #FE2C55; color: white; border-radius: 8px; }
.stButton>button:hover { background-color: #25F4EE; color: black; }
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
    
    # Bonus Points Summary
    st.subheader("Bonus Points Summary")
    total_bonus = sum([v["bonus"] for v in videos["credits"]])
    st.metric("Total Bonus Points", total_bonus)
    
    st.subheader("Targets & Progress")
    
    views_sum = videos["views"].sum()
    gifts_sum = videos["gifts"].sum()
    comments_sum = videos["comments"].sum()
    
    st.write(f"Views: {views_sum}/1,500,000")
    st.progress(min(views_sum/1_500_000, 1.0))
    
    st.write(f"Gifts: {gifts_sum}/1,500")
    st.progress(min(gifts_sum/1_500, 1.0))
    
    st.write(f"Engagement: {comments_sum}/7,000")
    st.progress(min(comments_sum/7_000, 1.0))

# -------------------------------
# Videos & Rewards Tab
# -------------------------------
if tab_selected == "videos":
    st.header("Videos & Rewards")
    
    # Bonus Points Table (only videos with bonus > 0)
    bonus_videos = [
        {
            "Video ID": row["video_id"],
            "Creator": row["creators"]["username"],
            "Bonus Points": row["credits"]["bonus"],
            "Total Credits": row["credits"]["total"],
            "Reward Tier": row["reward"]
        }
        for _, row in videos.iterrows()
        if row["credits"]["bonus"] > 0
    ]
    
    if bonus_videos:
        st.subheader("Videos with Bonus Points")
        # Scrollable table with max 10 rows
        st.dataframe(bonus_videos, height=300)
    else:
        st.info("No videos have been awarded bonus points yet.")
    
    # Optional: Expanders for all videos (for reference)
    for index, row in videos.iterrows():
        with st.expander(f"Video {row['video_id']} - {row['url']}"):
            st.write(f"**Content Credits:** {row['credits']['total']}")
            st.write("**Credit Breakdown:**")
            for k,v in row['credits'].items():
                if k != "total":
                    st.write(f"- {k.capitalize()}: {v}")
            st.write(f"**Reward Tier:** {row['reward']}")
            st.write(f"**Fraud / Safety Alert:** {row['fraud_alert']}")
