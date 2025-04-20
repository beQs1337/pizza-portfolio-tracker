import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="🍕 PizzaDay Portfolio Tracker", layout="wide")
st.title("📊 PizzaDay Portfolio Tracker")
st.caption("Serious. Delicious. Transparent.")

wallet = "0xA36D2861E036b897bA6C6E3448d123Ec25FA451A"

# -- CoinGecko API integration for token prices --
def fetch_coingecko_token_prices():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    try:
        response = requests.get(url, params=params, timeout=5)
        data = response.json()
        df = pd.DataFrame([{
            "name": coin.get("name"),
            "symbol": coin.get("symbol"),
            "current_price": coin.get("current_price"),
            "market_cap": coin.get("market_cap"),
            "total_volume": coin.get("total_volume")
        } for coin in data])
        return df
    except Exception as e:
        st.error(f"CoinGecko API Error: {e}")
        return pd.DataFrame()

# Load data
tokens_df = fetch_coingecko_token_prices()

# Display
total_value = tokens_df["current_price"].sum() if not tokens_df.empty else 0

if tokens_df.empty:
    st.warning("No token data found or unable to fetch from CoinGecko.")
else:
    st.subheader("💰 Top Tokens by Market Cap (via CoinGecko)")
    st.dataframe(tokens_df)

    if st.button("📥 Export Token Prices as CSV"):
        tokens_df.to_csv("coingecko_tokens_export.csv", index=False)
        st.success("Token prices exported!")

    st.metric("📈 Combined Current Price Sum", f"${total_value:,.2f}")