import json
import requests
import time

def fetch_historical_data():
    """
    Fetch historical price data for cryptocurrencies in `coin_list.json`.
    Saves data to `historical_data.json`.
    """
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
        time.sleep(1)  # Avoid API rate limits

    with open("static/historical_data.json", "w") as file:
        json.dump(all_data, file, indent=4)

