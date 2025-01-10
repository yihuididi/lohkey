import os
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.api import SimpleExpSmoothing

# Constants for API
GOLDRUSH_API_KEY = "cqt_rQgtjvHXk8jbYRWfJTcQycmBTqh3"
BASE_URL = "https://api.covalenthq.com/v1"
SUPPORTED_CHAINS = {
    "Ethereum Mainnet": "eth-mainnet",
    "Binance Smart Chain": "bsc-mainnet",
    "Polygon Mainnet": "polygon-mainnet",
    "Avalanche Mainnet": "avalanche-mainnet",
    "Fantom Opera": "fantom-mainnet",
    "Arbitrum One": "arbitrum-mainnet",
    "Optimism": "optimism-mainnet",
    "Solana Mainnet": "solana-mainnet",
    "Moonbeam Mainnet": "moonbeam-mainnet",
    "Harmony Mainnet": "harmony-mainnet",
    "Celo Mainnet": "celo-mainnet",
    "Klaytn Mainnet": "klaytn-mainnet",
    "Cronos Mainnet": "cronos-mainnet",
    "Gnosis Chain": "gnosis-mainnet",
    "Astar Mainnet": "astar-mainnet",
    "Algorand Mainnet": "algorand-mainnet",
    "Near Protocol": "near-mainnet",
    "Tezos Mainnet": "tezos-mainnet",
    "Tron Mainnet": "tron-mainnet",
    "Cardano Mainnet": "cardano-mainnet"
}

# Fetch Wallet Data
def fetch_wallet_balances(wallet_address, chain_id):
    url = f"{BASE_URL}/{chain_id}/address/{wallet_address}/balances_v2/"
    params = {"key": GOLDRUSH_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", {}).get("items", [])
    except requests.RequestException as e:
        return {"error": str(e)}

def fetch_transaction_history(wallet_address, chain_id):
    url = f"{BASE_URL}/{chain_id}/address/{wallet_address}/transactions_v2/"
    params = {"key": GOLDRUSH_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", {}).get("items", [])
    except requests.RequestException as e:
        return {"error": str(e)}

def multi_chain_query(wallet_address, selected_chains):
    """
    Fetch wallet data across selected blockchains.
    """
    portfolio = {"balances": {}, "transactions": {}}

    for chain_name in selected_chains:
        chain_id = SUPPORTED_CHAINS[chain_name]

        # Fetch balances
        balances = fetch_wallet_balances(wallet_address, chain_id)
        portfolio["balances"][chain_name] = balances

        # Fetch transactions
        transactions = fetch_transaction_history(wallet_address, chain_id)
        portfolio["transactions"][chain_name] = transactions

    return portfolio


# Fetch Coin List
def fetch_coin_list():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        with open("static/coin_list.json", "w") as file:
            json.dump(data, file, indent=4)
        return data
    except requests.RequestException as e:
        return {"error": str(e)}

# Fetch Historical Data
def fetch_historical_data():
    with open("static/coin_list.json", "r") as file:
        coin_list = json.load(file)
    headers = {"accept": "application/json"}
    all_data = {}
    for coin in coin_list:
        url = f"https://api.coingecko.com/api/v3/coins/{coin['id']}/market_chart"
        params = {"vs_currency": "usd", "days": 50, "interval": "daily"}
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            all_data[coin['id']] = response.json()
        except requests.RequestException as e:
            print(f"Error fetching data for {coin['id']}: {e}")
    with open("static/historical_data.json", "w") as file:
        json.dump(all_data, file, indent=4)

# Liquidity Analysis
def analyze_liquidity(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
    liquidity_data = []
    for coin, metrics in data.items():
        liquidity_risk = np.mean([x['value'] for x in metrics.get('liquidity', [])])
        liquidity_data.append({"coin": coin, "liquidity_risk": liquidity_risk})
    return liquidity_data

# Volatility Analysis
def analyze_volatility(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
    volatility_data = []
    for coin, metrics in data.items():
        volatility_risk = np.std([x['value'] for x in metrics.get('volatility', [])])
        volatility_data.append({"coin": coin, "volatility_risk": volatility_risk})
    return volatility_data

# Price Predictions
def get_crypto_predictions(crypto_symbol):
    data = yf.download(crypto_symbol, period="1y", interval="1d")
    if data.empty:
        return {"error": "No data available for this cryptocurrency."}
    data.reset_index(inplace=True)
    x = np.arange(len(data))[:, np.newaxis]
    y = data['Close'].values
    model = LinearRegression().fit(x, y)
    forecast_x = np.arange(len(data), len(data) + 14)[:, np.newaxis]
    forecast_y = model.predict(forecast_x)
    return {
        "historical_prices": y.tolist(),
        "predicted_prices": forecast_y.tolist(),
    }

# Save data dynamically during app execution
if __name__ == "__main__":
    print("This script is intended to be used as part of a Django application where wallet address input is handled by the frontend.")
