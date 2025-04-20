import streamlit as st
from portfolio_logic import fetch_pepuscan_tokens
from PIL import Image
import time

st.set_page_config(page_title="🍕 PizzaDay Portfolio Tracker", layout="wide")

# --- Intro Animation ---
st.markdown("## 🍕 Welcome to PizzaDay Tracker!")
st.image("assets/pizza_intro.gif", use_column_width=True)
time.sleep(2)  # Show effect pause
st.markdown("---")

# --- App Content ---
st.title("📊 PizzaDay Portfolio Tracker")
st.caption("Live from PEPU — Serious. Delicious. On-Chain.")

wallet_address = "0x97Cc38a7aa6DF2352830a3Dd228047d5FaC597fa"
df = fetch_pepuscan_tokens(wallet_address)

if df.empty:
    st.warning("No tokens found or API unavailable.")
else:
    st.subheader("💰 Live Wallet Tokens (PepuScan)")
    st.dataframe(df)

    if st.button("📥 Export as CSV"):
        df.to_csv("pepuscan_tokens_export.csv", index=False)
        st.success("Exported successfully!")