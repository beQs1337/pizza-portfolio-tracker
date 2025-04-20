import requests
import pandas as pd

def fetch_pepuscan_tokens(wallet_address):
    url = f"https://pepuscan.com/api?module=account&action=tokenlist&address={wallet_address}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        tokens = data.get("result", [])
        parsed = []
        for token in tokens:
            token_type = token.get("type")
            if token_type == "ERC-20":
                try:
                    decimals = int(token.get("decimals", 18))
                    balance = int(token["balance"]) / (10 ** decimals)
                    formatted_balance = round(balance, 2)
                except Exception:
                    formatted_balance = token["balance"]
            elif token_type == "ERC-721":
                formatted_balance = token["balance"]
            else:
                formatted_balance = "?"
            parsed.append({
                "name": token.get("name"),
                "symbol": token.get("symbol"),
                "balance": formatted_balance,
                "type": token_type
            })
        return pd.DataFrame(parsed)
    except Exception as e:
        print(f"PepuScan API Error: {e}")
        return pd.DataFrame()