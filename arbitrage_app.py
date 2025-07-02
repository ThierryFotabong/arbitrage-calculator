import streamlit as st

def calculate_arbitrage(odds, total_stake):
    inv_sum = sum(1/o for o in odds)
    arbitrage_exists = inv_sum < 1

    if not arbitrage_exists:
        return False, [], 0, 0, 0

    stakes = [(1/o) / inv_sum * total_stake for o in odds]
    payout = stakes[0] * odds[0]  # Same for any outcome
    profit = payout - total_stake
    roi = (profit / total_stake) * 100

    return True, stakes, payout, profit, roi

# Streamlit UI
st.title("🎯 Arbitrage Betting Calculator")

st.markdown("""
Enter the best available odds for each possible outcome of an event, and the app will tell you whether an arbitrage opportunity exists and how much to bet on each outcome.
""")

num_outcomes = st.number_input("Number of outcomes", min_value=2, max_value=10, value=2, step=1)
total_stake = st.number_input("Total stake (€)", min_value=1.0, value=100.0, step=1.0)

odds = []
st.subheader("Enter odds for each outcome:")
for i in range(num_outcomes):
    odd = st.number_input(f"Outcome {i+1} odds", min_value=1.01, value=2.0, step=0.01)
    odds.append(odd)

if st.button("Calculate"):
    arbitrage, stakes, payout, profit, roi = calculate_arbitrage(odds, total_stake)

    if arbitrage:
        st.success("✅ Arbitrage Opportunity Found!")
        st.write(f"**Total Stake:** €{total_stake:.2f}")
        st.write(f"**Guaranteed Return:** €{payout:.2f}")
        st.write(f"**Guaranteed Profit:** €{profit:.2f}")
        st.write(f"**ROI:** {roi:.2f}%")

        st.markdown("### Stake per outcome:")
        for i, (o, s) in enumerate(zip(odds, stakes), 1):
            st.write(f"- Outcome {i}: Bet €{s:.2f} at odds {o}")
    else:
        st.error("❌ No arbitrage opportunity detected with these odds.")

