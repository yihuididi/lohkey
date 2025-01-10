import requests
import json

# GoldRush API Key
GOLDRUSH_API_KEY = "cqt_rQgtjvHXk8jbYRWfJTcQycmBTqh3"
BASE_URL = "https://api.covalenthq.com/v1"

# Define the supported blockchains
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


def fetch_wallet_balances(wallet_address, chain_name):
    """
    Fetch wallet balances for a specific blockchain.
    Args:
        wallet_address (str): The wallet address.
        chain_name (str): The chain name (e.g., 'eth-mainnet').
    Returns:
        list: A list of token balances or an error message.
    """
    url = f"{BASE_URL}/{chain_name}/address/{wallet_address}/balances_v2/"
    params = {"key": GOLDRUSH_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", {}).get("items", [])
    except requests.RequestException as e:
        return {"error": str(e)}


def fetch_transaction_history(wallet_address, chain_name):
    """
    Fetch transaction history for a specific blockchain.
    Args:
        wallet_address (str): The wallet address.
        chain_name (str): The chain name (e.g., 'eth-mainnet').
    Returns:
        list: A list of transactions or an error message.
    """
    url = f"{BASE_URL}/{chain_name}/address/{wallet_address}/transactions_v2/"
    params = {"key": GOLDRUSH_API_KEY}
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json().get("data", {}).get("items", [])
    except requests.RequestException as e:
        return {"error": str(e)}


def multi_chain_query(wallet_address):
    """
    Query wallet data across multiple blockchains and aggregate results.
    Args:
        wallet_address (str): The wallet address to query.
    Returns:
        dict: Aggregated portfolio data including balances and transactions.
    """
    portfolio = {"balances": {}, "transactions": {}}

    for chain_name, chain_id in SUPPORTED_CHAINS.items():
        # Fetch balances
        balances = fetch_wallet_balances(wallet_address, chain_id)
        portfolio["balances"][chain_name] = balances

        # Fetch transactions
        transactions = fetch_transaction_history(wallet_address, chain_id)
        portfolio["transactions"][chain_name] = transactions

    return portfolio
