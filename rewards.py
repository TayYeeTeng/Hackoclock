# import os
# import streamlit as st
# from supabase import create_client, Client
# from dotenv import load_dotenv
# from datetime import datetime

# # --- LOAD ENV VARIABLES ---
# load_dotenv()
# SUPABASE_URL = os.getenv("SUPABASE_URL")
# SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# # --- INIT SUPABASE CLIENT ---
# supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# # --- CREATOR INFO ---
# creator_id = 731557

# # --- FETCH CREATOR POINTS ---
# def get_creator_points():
#     response = supabase.table("creators").select("total_points").eq("creator_id", creator_id).execute()
#     return response.data[0]["total_points"] if response.data else 0

# total_points = get_creator_points()

# # --- MOCK OR DYNAMIC REWARDS ---
# # You can fetch rewards dynamically from a 'rewards' table if needed
# rewards = [
#     {"id": 1, "title": "TikTok Merch", "cost": 200, "icon": "🎁"},
#     {"id": 2, "title": "Marketing Credits", "cost": 50, "icon": "📢"},
#     {"id": 3, "title": "Cash Bonus", "cost": 10, "icon": "💸"},
# ]

# # --- FETCH TRANSACTIONS FROM REDEMPTIONS ---
# tx_resp = (
#     supabase.table("redemptions")
#     .select("*")
#     .eq("creator_id", creator_id)
#     .order("creation_date", desc=True)
#     .execute()
# )
# transactions = tx_resp.data if tx_resp.data else []

# # --- REDEEM LOGIC ---
# def redeem_reward(reward_id, reward_title, reward_cost):
#     global total_points
#     if total_points >= reward_cost:
#         # 1. Deduct points in creators table
#         total_points -= reward_cost
#         supabase.table("creators").update({"total_points": total_points}).eq("creator_id", creator_id).execute()

#         # 2. Add redemption record
#         supabase.table("redemptions").insert({
#             "creator_id": creator_id,
#             "reward_id": reward_id,
#             "amount": reward_cost,
#             "exposure": reward_title,
#             "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         }).execute()

#         st.success(f"Successfully redeemed {reward_title}!")
#         st.experimental_rerun()  # refresh page to update balance and transactions
#     else:
#         st.error("Not enough points to redeem this reward.")

# # --- PAGE CONFIG ---
# st.set_page_config(page_title="Creator Rewards", layout="wide")

# # --- CSS STAYS EXACTLY THE SAME ---
# st.markdown(
#     """
#     <style>
#     header, footer, #MainMenu { visibility: hidden; height: 0px; }
#     .block-container { padding-top: 0rem; padding-bottom: 0rem; padding-left: 2rem; padding-right: 2rem; }
#     .stApp { background-color: #000; color: #fff; }
#     .reward-page { min-height: 100vh; background-color: #000; color: #fff; padding: 24px; font-family: Arial, sans-serif; margin-top: -1000px; }
#     .header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }
#     .title { color: #ec4899; font-size: 24px; font-weight: bold; }
#     .profile { display: flex; align-items: center; gap: 12px; }
#     .balance-card { background: linear-gradient(to right, #ec4899, #8b5cf6); border-radius: 16px; padding: 24px; margin-bottom: 32px; display: flex; justify-content: space-between; align-items: center; }
#     .small-text { font-size: 14px; }
#     .large-text { font-size: 32px; font-weight: bold; }
#     .balance-buttons { display: flex; gap: 12px; }
#     .btn { padding: 10px 16px; border-radius: 8px; font-weight: 600; cursor: pointer; border: none; }
#     .btn-light { background: #fff; color: #000; }
#     .btn-dark { background: #000; border: 1px solid #fff; color: #fff; }
#     .btn-pink { background: #ec4899; color: #fff; width: 100%; }
#     .section-title { font-size: 20px; font-weight: bold; margin-bottom: 16px; }
#     .rewards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 40px; }
#     .reward-card { background-color: #0f0f1f; border-radius: 16px; padding: 24px; text-align: center; }
#     .reward-icon { font-size: 40px; margin-bottom: 12px; }
#     .reward-title { font-size: 18px; font-weight: bold; }
#     .reward-cost { color: #aaa; margin-bottom: 12px; }
#     .transactions { background-color: #0f0f1f; padding: 20px; border-radius: 16px; display: flex; flex-direction: column; gap: 12px; }
#     .transaction { display: flex; justify-content: flex-start; border-bottom: 1px solid #333; padding-bottom: 8px; gap: 20px; }
#     .tx-action { flex: 2; min-width: 250px; }
#     .tx-date { flex: 1; min-width: 100px; font-size: 12px; color: #aaa; }
#     .tx-status { flex: 1; font-size: 12px; color: #22c55e; font-weight: bold; text-align: right; }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # --- PAGE LAYOUT ---
# st.markdown('<div class="reward-page">', unsafe_allow_html=True)

# # Header
# st.markdown(f"""
# <div class="header">
#     <h1 class="title">Creator Rewards</h1>
# </div>
# """, unsafe_allow_html=True)

# # Balance card
# st.markdown(f"""
# <div class="balance-card">
#   <div class="balance-info">
#     <p class="small-text">Available Balance</p>
#     <h2 class="large-text">${total_points}</h2>
#   </div>
# </div>
# """, unsafe_allow_html=True)

# # Rewards
# st.markdown('<h2 class="section-title">Gifts to Redeem</h2>', unsafe_allow_html=True)

# # Rewards grid
# grid_html = '<div class="rewards-grid">'
# for r in rewards:
#     if st.button(f"Redeem {r['title']}", key=f"redeem_{r['id']}"):
#         redeem_reward(r["id"], r["title"], r["cost"])
#     grid_html += (
#         '<div class="reward-card">'
#         f'<span class="reward-icon">{r["icon"]}</span>'
#         f'<h3 class="reward-title">{r["title"]}</h3>'
#         f'<p class="reward-cost">{r["cost"]} coins</p>'
#         '<button class="btn btn-pink">Redeem Now</button>'
#         '</div>'
#     )
# grid_html += '</div>'
# st.markdown(grid_html, unsafe_allow_html=True)

# # Transactions
# st.markdown('<h2 class="section-title">Transaction History</h2>', unsafe_allow_html=True)
# tx_html = '<div class="transactions">'
# for tx in transactions:
#     status_color = "#22c55e"  # completed
#     tx_html += (
#         '<div class="transaction">'
#         f'<span class="tx-action">Redeemed {tx["exposure"]}</span>'
#         f'<span class="tx-date">{tx["creation_date"]}</span>'
#         f'<span class="tx-status" style="color: {status_color}; font-weight: bold;">Completed</span>'
#         '</div>'
#     )
# tx_html += '</div>'
# st.markdown(tx_html, unsafe_allow_html=True)

# st.markdown('</div>', unsafe_allow_html=True)




# NEW CODE
import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
from datetime import datetime

# --- LOAD ENV VARIABLES ---
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

creator_id = 731557

# --- FETCH CREATOR POINTS ---
def get_creator_points():
    response = supabase.table("creators").select("total_points").eq("creator_id", creator_id).execute()
    return response.data[0]["total_points"] if response.data else 0

total_points = get_creator_points()

# --- REWARDS LIST ---
rewards = [
    {"id": 1, "title": "TikTok Merch", "cost": 200, "icon": "🎁"},
    {"id": 2, "title": "Marketing Credits", "cost": 50, "icon": "📢"},
    {"id": 3, "title": "Cash Bonus", "cost": 10, "icon": "💸"},
]

# --- FETCH TRANSACTIONS ---
tx_resp = (
    supabase.table("redemptions")
    .select("*")
    .eq("creator_id", creator_id)
    .order("creation_date", desc=True)
    .execute()
)
transactions = tx_resp.data if tx_resp.data else []

# --- REDEEM FUNCTION ---
def redeem_reward(reward_id, reward_title, reward_cost):
    global total_points
    try:
        if total_points >= reward_cost:
            total_points -= reward_cost
            supabase.table("creators").update({"total_points": total_points}).eq("creator_id", creator_id).execute()
            supabase.table("redemptions").insert({
                "creator_id": creator_id,
                "reward_id": reward_id,
                "amount": reward_cost,
                "exposure": reward_title,
                "creation_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }).execute()
            st.success(f"Successfully redeemed {reward_title}!")
        else:
            st.error(f"Not enough points to redeem {reward_title}.")
    except Exception as e:
        st.error(f"Unable to redeem {reward_title}.")
        print(f"Error redeeming reward: {e}")

# --- PAGE CONFIG ---
st.set_page_config(page_title="Creator Rewards", layout="wide")

# --- CSS ---
st.markdown("""
<style>
/* Hide Streamlit menu, header, footer */
header, footer, #MainMenu { 
    visibility: hidden; 
    height: 0px; 
}

/* Remove top/bottom padding of main content */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    padding-left: 2rem;
    padding-right: 2rem;
}

/* Full app background */
.stApp {
    background-color: #000;
    color: #fff;
}

/* Reward page styles */
.reward-page {
    min-height: 100vh;
    background-color: #000;
    color: #fff;
    padding: 24px;
    font-family: Arial, sans-serif;
    margin-top: -1500px;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    flex-wrap: wrap;
}

.header h1.title {
    margin-top: 0;
    margin-bottom: 0;
}

.title {
    color: #ec4899;
    font-size: 24px;
    font-weight: bold;
}

.balance-card {
    background: linear-gradient(to right, #ec4899, #8b5cf6);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 32px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 16px;
}

.small-text { font-size: 14px; }
.large-text { font-size: 32px; font-weight: bold; }
.balance-buttons { display: flex; gap: 12px; flex-wrap: wrap; }

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
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
    overflow-x: auto;
    margin-bottom: 50px;
}

.transaction {
    display: flex;
    justify-content: flex-start;
    border-bottom: 1px solid #333;
    padding-bottom: 8px;
    gap: 20px;
    flex-wrap: wrap;
}

.tx-action { flex: 2; min-width: 150px; }
.tx-date { flex: 1; min-width: 100px; font-size: 12px; color: #aaa; }
.tx-status { flex: 1; min-width: 80px; font-size: 12px; color: #22c55e; font-weight: bold; text-align: right; }

/* Responsive adjustments */
@media screen and (max-width: 480px) {
    .large-text { font-size: 24px; }
    .title { font-size: 20px; }
    .reward-card { padding: 16px; }
    .balance-card { flex-direction: column; align-items: flex-start; }
    .balance-buttons { width: 100%; justify-content: space-between; }
}

/* Streamlit button overrides */
div.stButton > button {
    background: #ec4899;
    color: #fff;
    border: none;
    padding: 10px 16px;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;
    width: 100%;
}
div.stButton > button:hover {
    background: #db2777;
}
div.stButton > button:active {
    background: #be185d !important;
    color: #fff !important;
}
</style>
""", unsafe_allow_html=True)

# --- PAGE CONTENT ---
st.markdown('<div class="reward-page">', unsafe_allow_html=True)

# Header
st.markdown('<div class="header"><h1 class="title">Creator Rewards</h1></div>', unsafe_allow_html=True)

# Balance card
st.markdown(f"""
<div class="balance-card">
  <div class="balance-info">
    <p class="small-text">Available Balance</p>
    <h2 class="large-text">{total_points} coins</h2>
  </div>
</div>
""", unsafe_allow_html=True)

# Rewards grid
st.markdown('<h2 class="section-title">Gifts to Redeem</h2>', unsafe_allow_html=True)
st.markdown('<div class="rewards-grid">', unsafe_allow_html=True)

cols = st.columns(len(rewards))
for idx, r in enumerate(rewards):
    with cols[idx]:
        st.markdown(f"""
        <div class="reward-card">
            <div class="reward-icon">{r["icon"]}</div>
            <div class="reward-title">{r["title"]}</div>
            <div class="reward-cost">{r["cost"]} coins</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Redeem", key=f"redeem_{r['id']}"):
            redeem_reward(r["id"], r["title"], r["cost"])

st.markdown('</div>', unsafe_allow_html=True)

# Transactions
st.markdown('<h2 class="section-title">Transaction History</h2>', unsafe_allow_html=True)
tx_html = '<div class="transactions">'
for tx in transactions:
    tx_html += (
        '<div class="transaction">'
        f'<span class="tx-action">Redeemed {tx["exposure"]}</span>'
        f'<span class="tx-date">{tx["creation_date"]}</span>'
        f'<span class="tx-status">Completed</span>'
        '</div>'
    )
tx_html += '</div>'
st.markdown(tx_html, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
