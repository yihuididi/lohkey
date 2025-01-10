import json
import requests

def fetch_coin_list():
    """
    Fetch top 50 cryptocurrencies by market cap and save them to a JSON file.
    Returns:
        list: List of cryptocurrencies or error message.
    """
    url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {"accept": "application/json"}
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50, "page": 1}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        with open("static/coin_list.json", "w") as file:
            json.dump(data, file, indent=4)
        return data
    except requests.RequestException as e:
        return {"error": str(e)}
