import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="🍕 PizzaDay Portfolio Tracker", layout="wide")
st.title("📊 PizzaDay Portfolio Tracker")
st.caption("Serious. Delicious. Transparent.")

# -- Fetch data from PepuScan (hypothetical API) --
def fetch_pepuscan_tokens(wallet_address):
    url = f"https://api.pepuscan.com/portfolio?wallet={wallet_address}"
    try:
        response = requests.get(url)
        result = response.json()
        tokens = result.get("tokens", [])
        return pd.DataFrame(tokens)
    except Exception as e:
        st.error(f"API Error: {e}")
        return pd.DataFrame()

wallet = "0xA36D2861E036b897bA6C6E3448d123Ec25FA451A"
tokens_df = fetch_pepuscan_tokens(wallet)

if tokens_df.empty:
    st.warning("No token data found or unable to fetch from PepuScan.")
else:
    # Token Holdings
    st.subheader("💰 Token Holdings")
    st.dataframe(tokens_df)
    if st.button("📥 Export Tokens as CSV"):
        tokens_df.to_csv("tokens_export.csv", index=False)
        st.success("Tokens exported!")

    # Total value estimate
    if "value_usd" in tokens_df.columns:
        total_value = tokens_df["value_usd"].sum()
        st.metric("📈 Total Value (USD)", f"${total_value:,.2f}")
    else:
        st.info("No USD values available in the data.")