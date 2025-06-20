import streamlit as st
import pandas as pd
import random

# Load price data
df = pd.read_csv("price_simulation.csv")

# Session state initialization
if 'day' not in st.session_state:
    st.session_state.day = 1
    st.session_state.wallet = 70000
    st.session_state.health = 100
    st.session_state.stress = 0
    st.session_state.history = []
    st.session_state.advice = ""

st.title("💰 Budget or Inflation Survival Game")
st.subheader("Can you survive 30 days on ₦70,000?")

# Fetch today's prices
today = df[df['Day'] == st.session_state.day].to_dict('records')[0]
st.markdown(f"### 📅 Day {today['Day']} - Inflation Rate: {today['InflationRate']}%")

# Show wallet, health, and stress levels
col1, col2, col3 = st.columns(3)
col1.metric("Wallet", f"₦{st.session_state.wallet}")
col2.metric("Health", f"{st.session_state.health} 💓")
col3.metric("Stress", f"{st.session_state.stress} 😣")

# User decision making
st.markdown("#### 🛒 Daily Choices")
choices = {}
for item in ['Food', 'Transport', 'Utilities', 'Airtime/Data']:
    choices[item] = st.checkbox(f"Buy {item} for ₦{today[item]}", value=True)

# Emergency check
emergency_cost = today['Emergency']
if emergency_cost > 0:
    st.warning(f"🚨 Emergency occurred! You must pay ₦{emergency_cost} for an unexpected expense.")
    choices['Emergency'] = True
else:
    choices['Emergency'] = False

# AI Budget Coach (rules-based)
def ai_budget_advice(choices, wallet, health, stress):
    advice = []
    if not choices['Food']:
        advice.append("⚠️ Skipping food daily will reduce your health fast. Try to eat something, even if small.")
    if wallet < 5000:
        advice.append("💡 You're running low on cash. Consider skipping non-essential spending tomorrow.")
    if stress > 70:
        advice.append("🧘 High stress levels! Reduce your load by prioritizing only essentials.")
    if not advice:
        advice.append("👍 You're making smart decisions. Keep it up!")
    return random.choice(advice)

# Submit choices
if st.button("Submit Day Choices"):
    day_spend = 0
    health_penalty = 0
    stress_gain = 0

    for item, chosen in choices.items():
        if chosen:
            day_spend += today[item]
        else:
            if item == 'Food':
                health_penalty += 15
                stress_gain += 5
            elif item == 'Transport':
                stress_gain += 5
            elif item == 'Utilities':
                stress_gain += 3
            elif item == 'Airtime/Data':
                stress_gain += 2

    if st.session_state.wallet < day_spend:
        st.error("You can't afford this! Reduce your choices.")
    else:
        st.session_state.wallet -= day_spend
        st.session_state.health -= health_penalty
        st.session_state.stress += stress_gain

        # Generate AI coach advice
        st.session_state.advice = ai_budget_advice(choices, st.session_state.wallet, st.session_state.health, st.session_state.stress)

        # Game Over Check
        if st.session_state.wallet <= 0 or st.session_state.health <= 0 or st.session_state.stress >= 100:
            st.error("💀 You didn't survive the month. Game Over!")
        else:
            st.success("✅ You survived today!")
            st.session_state.history.append({
                "Day": today['Day'],
                "Spend": day_spend,
                "Health": st.session_state.health,
                "Stress": st.session_state.stress,
                "Wallet": st.session_state.wallet
            })
            st.session_state.day += 1

# Show AI Coach advice
if st.session_state.advice:
    st.info(f"🧠 AI Coach says: {st.session_state.advice}")

# Show history
if st.checkbox("📊 Show Spending History"):
    hist_df = pd.DataFrame(st.session_state.history)
    st.dataframe(hist_df)

# Reset game
if st.button("🔄 Restart Game"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
