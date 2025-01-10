import os
import json
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timezone
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.api import SimpleExpSmoothing
import yfinance as yf
from datetime import timedelta

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

crypto_to_yahoo_symbol = {
    "bitcoin": "BTC-USD",
    "ethereum": "ETH-USD",
    "tether": "USDT-USD",
    "ripple": "XRP-USD",
    "binancecoin": "BNB-USD",
    "solana": "SOL-USD",
    "dogecoin": "DOGE-USD",
    "usd-coin": "USDC-USD",
    "cardano": "ADA-USD",
    "staked-ether": "STETH-USD",
    "tron": "TRX-USD",
    "avalanche-2": "AVAX-USD",
    "sui": "SUI-USD",
    "wrapped-steth": "WSTETH-USD",
    "the-open-network": "TON-USD",
    "chainlink": "LINK-USD",
    "shiba-inu": "SHIB-USD",
    "wrapped-bitcoin": "WBTC-USD",
    "stellar": "XLM-USD",
    "hedera-hashgraph": "HBAR-USD",
    "polkadot": "DOT-USD",
    "weth": "WETH-USD",
    "bitcoin-cash": "BCH-USD",
    "leo-token": "LEO-USD",
    "uniswap": "UNI-USD",
    "litecoin": "LTC-USD",
    "bitget-token": "BGB-USD",
    "pepe": "PEPE-USD",
    "hyperliquid": "HYPE-USD",
    "wrapped-eeth": "WEETH-USD",
    "near": "NEAR-USD",
    "usds": "USDS-USD",
    "ethena-usde": "USDE-USD",
    "internet-computer": "ICP-USD",
    "aptos": "APT-USD",
    "aave": "AAVE-USD",
    "mantle": "MNT-USD",
    "render-token": "RNDR-USD",
    "mantra-dao": "OM-USD",
    "polygon-ecosystem-token": "POL-USD",
    "crypto-com-chain": "CRO-USD",
    "ethereum-classic": "ETC-USD",
    "vechain": "VET-USD",
    "bittensor": "TAO-USD",
    "monero": "XMR-USD",
    "fetch-ai": "FET-USD"
}


def fetch_wallet_balances_with_prices(wallet_address, chain_id):
    """
    Fetch wallet balances and include pricing data using the balances_v2 endpoint.
    Args:
        wallet_address (str): The wallet address.
        chain_id (str): Blockchain chain ID (e.g., "eth-mainnet").
    Returns:
        list: List of token balances with pricing data.
    """
    url = f"{BASE_URL}/{chain_id}/address/{wallet_address}/balances_v2/"
    params = {"key": GOLDRUSH_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("data", {}).get("items", [])
    except requests.RequestException as e:
        print(f"Error fetching balances with prices: {e}")
        return []


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
    Fetch wallet data across selected blockchains, including current token prices.
    """
    portfolio = {"balances": {}, "transactions": {}}

    for chain_name in selected_chains:
        chain_id = SUPPORTED_CHAINS[chain_name]

        # Fetch balances with pricing data
        balances = fetch_wallet_balances_with_prices(wallet_address, chain_id)

        # Add balances to portfolio
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
    try:
        yf_symbol = crypto_to_yahoo_symbol.get(crypto_symbol.lower())
        if not yf_symbol:
            return {"error": f"No Yahoo Finance symbol available for {crypto_symbol}"}

        # Fetch historical data
        data = yf.download(yf_symbol, period="1y", interval="1d")
        if data.empty:
            return {"error": "No data available for this cryptocurrency."}

        # Reset index and check for missing dates
        data.reset_index(inplace=True)

        # Prepare data for prediction
        x = np.arange(len(data))[:, np.newaxis]
        y = data['Close'].values

        # Linear regression for price prediction
        model = LinearRegression().fit(x, y)
        forecast_x = np.arange(len(data), len(data) + 14)[:, np.newaxis]
        forecast_y = model.predict(forecast_x)

        # Generate forecast dates
        last_date = pd.to_datetime(data["Date"].iloc[-1])
        forecast_dates = [
            (last_date + pd.Timedelta(days=i + 1)).strftime("%Y-%m-%d") for i in range(14)
        ]

        # return last 30 rows (most recent 30 days)
        recent_data = data.tail(30)
        historical_prices = [{"price": row["Close"]} for _, row in recent_data.iterrows()]


        # Return historical and predicted prices
        return {
            "historical_prices": historical_prices,
            "predicted_prices": [{"date": d, "price": p} for d, p in zip(forecast_dates, forecast_y)],
        }
    except Exception as e:
        print(f"Error fetching predictions: {e}")
        return {"error": str(e)}

    
def get_crypto_metrics(crypto_symbol):
    """
    Fetches historical price data for a cryptocurrency and calculates key investment metrics.

    Args:
        crypto_symbol (str): The symbol of the cryptocurrency (e.g., 'BTC-USD').

    Returns:
        dict: A dictionary with key metrics like volatility, moving averages, RSI, and more.
    """
    yf_symbol = crypto_to_yahoo_symbol.get(crypto_symbol.lower())
    if not yf_symbol:
        return {"error": f"No Yahoo Finance symbol available for {crypto_id}"}
    try:
        # Fetch historical data for the crypto
        crypto_data = yf.download(yf_symbol, period="6mo", interval="1d")
        if crypto_data.empty:
            return {"error": f"No data found for {yf_symbol}."}

        # Calculate current price
        current_price = crypto_data['Close'].iloc[-1]

        # Calculate daily returns
        crypto_data['Daily Returns'] = crypto_data['Close'].pct_change()

        # Calculate annualized volatility
        volatility = crypto_data['Daily Returns'].std() * np.sqrt(252)

        # Calculate moving averages
        crypto_data['7-Day MA'] = crypto_data['Close'].rolling(window=7).mean()
        crypto_data['30-Day MA'] = crypto_data['Close'].rolling(window=30).mean()

        # Calculate Relative Strength Index (RSI)
        delta = crypto_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        crypto_data['RSI'] = 100 - (100 / (1 + rs))
        rsi = crypto_data['RSI'].iloc[-1]

        # Calculate All-Time High (ATH) and drawdown
        ath = crypto_data['Close'].max()
        drawdown = ((ath - current_price) / ath) * 100

        # Calculate trading volume
        average_volume = crypto_data['Volume'].mean()

        # Return metrics
        return {
            "current_price": current_price,
            "volatility": volatility,
            "7_day_moving_average": crypto_data['7-Day MA'].iloc[-1],
            "30_day_moving_average": crypto_data['30-Day MA'].iloc[-1],
            "rsi": rsi,
            "all_time_high": ath,
            "drawdown": drawdown,
            "average_volume": average_volume,
            "message": f"Calculated key metrics for {crypto_symbol}.",
        }
    except Exception as e:
        return {"error": f"An error occurred: {e}"}




# Save data dynamically during app execution
if __name__ == "__main__":
    print("This script is intended to be used as part of a Django application where wallet address input is handled by the frontend.")
