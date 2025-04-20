import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="🍕 PizzaDay Portfolio Tracker", layout="wide")
st.title("📊 PizzaDay Portfolio Tracker")
st.caption("Serious. Delicious. Transparent.")

wallet = "0xA36D2861E036b897bA6C6E3448d123Ec25FA451A"

# -- Blockscout API (Stable) --
def fetch_blockscout_tokens(wallet_address):
    url = f"https://gnosisscan.io/api?module=account&action=tokenlist&address={wallet_address}"
    try:
        response = requests.get(url, timeout=5)
        result = response.json()
        tokens = result.get("result", [])

        if not isinstance(tokens, list):
            st.error(f"Unexpected response from Blockscout:\n{tokens}")
            return pd.DataFrame()

        df = pd.DataFrame([{
            "name": t.get("name"),
            "symbol": t.get("symbol"),
            "balance": float(t.get("balance")) / 10**int(t.get("decimals", 18)),
            "value_usd": float(t.get("quote", 0.0))
        } for t in tokens])
        return df
    except Exception as e:
        st.error(f"Blockscout API Error: {e}")
        return pd.DataFrame()

tokens_df = fetch_blockscout_tokens(wallet)

if tokens_df.empty:
    st.warning("No token data found or unable to fetch from Blockscout.")
else:
    st.subheader("💰 Token Holdings")
    st.dataframe(tokens_df)

    if st.button("📥 Export Tokens as CSV"):
        tokens_df.to_csv("tokens_export.csv", index=False)
        st.success("Tokens exported!")

    if "value_usd" in tokens_df.columns:
        total_value = tokens_df["value_usd"].sum()
        st.metric("📈 Total Value (USD)", f"${total_value:,.2f}")
    else:
        st.info("No USD values available in the data.")