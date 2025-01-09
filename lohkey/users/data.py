'''
from datetime import datetime, timezone
import json
import pandas as pd

with open("lohkey/static/historical_data.json", "r") as file:
    # Each coin in data have 3 metrics: prices, market_caps, and total_volumes.
    # Each metric contains info of the coin for 50 days, where the first element of info
    # is the timestamp in epoch format and the second is the value.
    # See historical_data.json to verify.
    data = json.load(file)

    # Retrieve row and column info first
    coins = list(data.keys())
    dates = [datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d") for ts, _ in data[coins[0]]["prices"]]

    # Create dataframes
    prices_df = pd.DataFrame(columns=dates, index=coins)
    market_caps_df = pd.DataFrame(columns=dates, index=coins)
    total_volumes_df = pd.DataFrame(columns=dates, index=coins)

    for coin, metrics in data.items():
        for metric, info in metrics.items():
            dates = []
            values = []
            for timestamp, value in info:
                dates.append(datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d"))
                values.append(value)
            
            # Add the data to the appropriate DataFrame
            if metric == "prices":
                prices_df.loc[coin, dates] = values
            elif metric == "market_caps":
                market_caps_df.loc[coin, dates] = values
            elif metric == "total_volumes":
                total_volumes_df.loc[coin, dates] = values

print(prices_df.head())
'''

from datetime import datetime, timezone
import json
import pandas as pd

with open("lohkey/static/historical_data.json", "r") as file:
    data = json.load(file)

    coins = list(data.keys())
    first_coin_timestamps = [ts for ts, _ in data[coins[0]]["prices"]]
    dates = [datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime("%Y-%m-%d") for ts in first_coin_timestamps]

    # Create a list to store the data for the combined DataFrame
    all_data = []

    for coin, metrics in data.items():
        for metric, info in metrics.items():
            for timestamp, value in info:
                date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
                all_data.append([coin, date, metric, value])

    # Create the combined DataFrame
    combined_df = pd.DataFrame(all_data, columns=['coin', 'date', 'metric', 'value'])

# Pivot the table to get the desired structure
combined_df = combined_df.pivot(index=['coin', 'date'], columns='metric', values='value').reset_index()

print(combined_df.head())

