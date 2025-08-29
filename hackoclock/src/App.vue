<template>
  <div class="reward-page">
    <!-- Header -->
    <div class="header">
      <h1 class="title">Creator Rewards</h1>
      <div class="profile">
        <span>Balance: <strong>$520</strong></span>
        <!-- <img src="/profile.png" alt="profile" class="profile-pic" /> -->
      </div>
    </div>

    <!-- Balance Card -->
    <div class="balance-card">
      <div class="balance-info">
        <p class="small-text">Available Balance</p>
        <h2 class="large-text">$520</h2>
      </div>
      <div class="balance-buttons">
        <button class="btn btn-light">Withdraw</button>
        <button class="btn btn-dark">Redeem Gifts</button>
      </div>
    </div>

    <!-- Gift Redemption -->
    <h2 class="section-title">Gifts to Redeem</h2>
    <div class="rewards-grid">
      <div v-for="(reward, i) in rewards" :key="i" class="reward-card">
        <span class="reward-icon">{{ reward.icon }}</span>
        <h3 class="reward-title">{{ reward.title }}</h3>
        <p class="reward-cost">{{ reward.cost }}</p>
        <button class="btn btn-pink">Redeem Now</button>
      </div>
    </div>

    <!-- Transaction History -->
    <h2 class="section-title">Transaction History</h2>
    <div class="transactions">
      <div v-for="(tx, i) in transactions" :key="i" class="transaction">
        <span>{{ tx.action }}</span>
        <span class="tx-date">{{ tx.date }}</span>
        <span class="tx-status">{{ tx.status }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
const rewards = [
  { title: "TikTok Merch", cost: "200 coins", icon: "🎁" },
  { title: "Marketing Credits", cost: "$50", icon: "📢" },
  { title: "Cash Bonus", cost: "$10", icon: "💸" },
];

const transactions = [
  { action: "Withdrawn $100 to DBS", date: "Aug 27, 2025", status: "Completed" },
  { action: "Redeemed TikTok Hoodie", date: "Aug 20, 2025", status: "Completed" },
  { action: "Redeemed $50 Marketing Credit", date: "Aug 10, 2025", status: "Completed" },
];
</script>

<style scoped>
.reward-page {
  min-height: 100vh;
  background-color: #000;
  color: #fff;
  padding: 24px;
  font-family: Arial, sans-serif;
}

/* Header */
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

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

/* Balance Card */
.balance-card {
  background: linear-gradient(to right, #ec4899, #8b5cf6);
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.balance-info .small-text {
  font-size: 14px;
}

.balance-info .large-text {
  font-size: 32px;
  font-weight: bold;
}

.balance-buttons {
  display: flex;
  gap: 12px;
}

.btn {
  padding: 10px 16px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  border: none;
}

.btn-light {
  background: #fff;
  color: #000;
}

.btn-dark {
  background: #000;
  border: 1px solid #fff;
  color: #fff;
}

.btn-pink {
  background: #ec4899;
  color: #fff;
  width: 100%;
}

/* Sections */
.section-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 16px;
}

/* Rewards Grid */
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

.reward-icon {
  font-size: 40px;
  margin-bottom: 12px;
}

.reward-title {
  font-size: 18px;
  font-weight: bold;
}

.reward-cost {
  color: #aaa;
  margin-bottom: 12px;
}

/* Transactions */
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
  justify-content: space-between;
  border-bottom: 1px solid #333;
  padding-bottom: 8px;
}

.tx-date {
  font-size: 12px;
  color: #aaa;
}

.tx-status {
  font-size: 12px;
  color: #22c55e;
}
</style>
