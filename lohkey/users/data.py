from datetime import datetime, timezone
import json
import pandas as pd

with open("lohkey/static/historical_data.json", "r") as file:
    data = json.load(file)

    all_data = []

    # Each coin in data have 3 metrics: prices, market_caps, and total_volumes.
    for coin, metrics in data.items():
        # Each metric contains info of the coin for 50 days, where the first element of info
        # is the timestamp in epoch format and the second is the value.
        for metric, info in metrics.items():
            for timestamp, value in info:
                date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
                all_data.append([coin, date, metric, value])

df = pd.DataFrame(all_data, columns=["coin", "date", "metric", "value"])
df = df.groupby(["coin", "metric", "date"], as_index=False).mean()
df = df.pivot(index=["coin", "metric"], columns="date", values="value").reset_index()

df.to_csv("lohkey/static/historical_data.csv", index=False)
