from datetime import datetime, timezone
import json
import pandas as pd
import numpy as np

def load_data(json_file):
    with open(json_file, "r") as file:
        data = json.load(file)
        all_data = []
        for coin, metrics in data.items():
            for metric, info in metrics.items():
                for timestamp, value in info:
                    date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
                    all_data.append([coin, date, metric, value])
    return pd.DataFrame(all_data, columns=["coin", "date", "metric", "value"])

def calculate_volatility(df):
    # Calculate daily returns for each coin
    returns = df.groupby('coin').apply(lambda x: x.set_index('date')['value'].pct_change())
    # Calculate the mean of returns for each coin for each date
    returns = returns.groupby(level=0).apply(lambda x: x.groupby(level=0).mean())
    # Calculate volatility (standard deviation of returns) for each coin
    volatility = returns.groupby(level=0).std()
    volatility = volatility.reset_index()
    volatility.columns = ['coin', 'volatility']
    return volatility

def categorize_risk(volatility):
    if np.isnan(volatility):
        return 'Not Available'
    elif volatility < 0.01:
        return 'Low Risk'
    elif 0.01 <= volatility < 0.2:
        return 'Moderate Risk'
    else:
        return 'High Risk'

def save_to_json(df, output_file):
    data = df.to_dict(orient='records')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    json_file = "lohkey/static/historical_data.json"
    output_file = "lohkey/static/volatility_data.json"

    df = load_data(json_file)
    # Group by coin and date and calculate the mean of the values
    df = df.groupby(["coin", "date"], as_index=False).mean()

    volatility_df = calculate_volatility(df)
    volatility_df['risk_category'] = volatility_df['volatility'].apply(categorize_risk)
    final_df = volatility_df[['coin', 'volatility', 'risk_category']]

    save_to_json(final_df, output_file)

if __name__ == "__main__":
    main()
