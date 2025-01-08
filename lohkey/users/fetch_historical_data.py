import json
import requests
import time

# WARNING: running this script takes several minutes
# Fetch historical prices of the top 50 coins
if __name__ == "__main__":
    with open("lohkey/static/coin_list.json", "r") as file:
        coin_list = json.load(file)

    headers = {"accept": "application/json"}
    params = {
        "vs_currency": "usd",
        "days": 50, # Number of days worth of data
        "interval": "daily",
        "precision": "4"
    }

    all_data = {}
    for index, coin in enumerate(coin_list):
        coin_id = coin["id"]
        url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
        response = requests.get(url, headers=headers, params=params)
        all_data[coin_id] = response.json()

        # Repect API rate limit
        time.sleep(15)

    with open("lohkey/static/historical_data.json", "w") as file:
        json.dump(all_data, file, indent=4)
