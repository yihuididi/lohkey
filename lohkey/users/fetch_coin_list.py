import json
import requests

# Fetch the top 50 coins from coingecko
if __name__ == "__main__":
    url = "https://api.coingecko.com/api/v3/coins/markets"
    headers = {"accept": "application/json"}
    params = {"vs_currency": "usd", "order": "market_cap_desc", "per_page": 50, "page": 1}
    response = requests.get(url, headers=headers, params=params)
    data = json.loads(response.text)

    with open("lohkey/static/coin_list.json", "w") as file:
        json.dump(data, file, indent=4)
