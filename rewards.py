import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv

# --- LOAD ENV VARIABLES ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# --- INIT SUPABASE CLIENT ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# --- FETCH CREATOR POINTS ---
creator_id = 731557
response = supabase.table("creators").select("total_points").eq("creator_id", creator_id).execute()

if response.data and len(response.data) > 0:
    total_points = response.data[0]["total_points"]
else:
    total_points = 0  # fallback if no record found

# --- PAGE CONFIG ---
st.set_page_config(page_title="Creator Rewards", layout="wide")

# --- MOCK DATA ---
rewards = [
    {"title": "TikTok Merch", "cost": "200 coins", "icon": "🎁"},
    {"title": "Marketing Credits", "cost": "$50", "icon": "📢"},
    {"title": "Cash Bonus", "cost": "$10", "icon": "💸"},
]

transactions = [
    {"action": "Withdrawn $100 to DBS", "date": "Aug 27, 2025", "status": "Completed"},
    {"action": "Redeemed TikTok Hoodie", "date": "Aug 20, 2025", "status": "Completed"},
    {"action": "Redeemed $50 Marketing Credit", "date": "Aug 10, 2025", "status": "Completed"},
]

# --- CUSTOM CSS TO MATCH DESIGN ---
st.markdown(
    """
    <style>
    /* Hide Streamlit menu, header, and footer */
    header, footer, #MainMenu { 
        visibility: hidden; 
        height: 0px; 
    }

    /* Remove top padding of main content */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* Set full app background */
    .stApp {
        background-color: #000;
        color: #fff;
    }
    .reward-page {
      min-height: 100vh;
      background-color: #000;
      color: #fff;
      padding: 24px;
      font-family: Arial, sans-serif;
      margin-top: -1000px;
    }
    .header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 32px;
    }
    .title {
      color: #ec4899;
      font-size: 24px;
      font-weight: bold;
    }
    .profile {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .balance-card {
      background: linear-gradient(to right, #ec4899, #8b5cf6);
      border-radius: 16px;
      padding: 24px;
      margin-bottom: 32px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .small-text { font-size: 14px; }
    .large-text { font-size: 32px; font-weight: bold; }
    .balance-buttons { display: flex; gap: 12px; }
    .btn {
      padding: 10px 16px;
      border-radius: 8px;
      font-weight: 600;
      cursor: pointer;
      border: none;
    }
    .btn-light { background: #fff; color: #000; }
    .btn-dark { background: #000; border: 1px solid #fff; color: #fff; }
    .btn-pink { background: #ec4899; color: #fff; width: 100%; }
    .section-title {
      font-size: 20px;
      font-weight: bold;
      margin-bottom: 16px;
    }
    .rewards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 20px;
      margin-bottom: 40px;
    }
    .reward-card {
      background-color: #0f0f1f;
      border-radius: 16px;
      padding: 24px;
      text-align: center;
    }
    .reward-icon { font-size: 40px; margin-bottom: 12px; }
    .reward-title { font-size: 18px; font-weight: bold; }
    .reward-cost { color: #aaa; margin-bottom: 12px; }
    .transactions {
      background-color: #0f0f1f;
      padding: 20px;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .transaction {
      display: flex;
      justify-content: flex-start; /* align items to the left */
      border-bottom: 1px solid #333;
      padding-bottom: 8px;
      gap: 20px; /* space between columns */
    }
    .tx-action { 
      flex: 2; /* take up more space */
      min-width: 250px; /* optional for long actions */
    }
    .tx-date { 
      flex: 1; /* fixed width for alignment */
      min-width: 100px;
      font-size: 12px; 
      color: #aaa; 
    }
    .tx-status { 
      flex: 1; 
      font-size: 12px; 
      color: #22c55e; 
      font-weight: bold;
      text-align: right; /* keep status on the right */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- PAGE LAYOUT ---
st.markdown('<div class="reward-page">', unsafe_allow_html=True)

# Header
st.markdown(
    f"""
    <div class="header">
        <h1 class="title">Creator Rewards</h1>
    </div>
    """,
    unsafe_allow_html=True,
)

# Balance card
st.markdown(
    f"""
    <div class="balance-card">
      <div class="balance-info">
        <p class="small-text">Available Balance</p>
        <h2 class="large-text">${total_points}</h2>
      </div>
      <div class="balance-buttons">
        <button class="btn btn-light">Withdraw</button>
        <button class="btn btn-dark">Redeem Gifts</button>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# Rewards
st.markdown('<h2 class="section-title">Gifts to Redeem</h2>', unsafe_allow_html=True)

# Build grid HTML
grid_html = '<div class="rewards-grid">'
for r in rewards:
    grid_html += (
        '<div class="reward-card">'
        f'<span class="reward-icon">{r["icon"]}</span>'
        f'<h3 class="reward-title">{r["title"]}</h3>'
        f'<p class="reward-cost">{r["cost"]}</p>'
        '<button class="btn btn-pink">Redeem Now</button>'
        '</div>'
    )
grid_html += '</div>'

# Render the grid
st.markdown(grid_html, unsafe_allow_html=True)



# Transactions
st.markdown('<h2 class="section-title">Transaction History</h2>', unsafe_allow_html=True)

# Build transaction HTML
tx_html = '<div class="transactions">'
for tx in transactions:
    # Determine status color
    status_color = "#22c55e"  # green for completed
    if tx["status"].lower() == "pending":
        status_color = "#f59e0b"  # orange
    elif tx["status"].lower() == "failed":
        status_color = "#ef4444"  # red

    tx_html += (
        '<div class="transaction">'
        f'<span class="tx-action">{tx["action"]}</span>'
        f'<span class="tx-date">{tx["date"]}</span>'
        f'<span class="tx-status" style="color: {status_color}; font-weight: bold;">{tx["status"]}</span>'
        '</div>'
    )
tx_html += '</div>'

# Render transactions
st.markdown(tx_html, unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)  # close reward-page
