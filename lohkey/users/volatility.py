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
    df = pd.DataFrame(all_data, columns=["coin", "date", "metric", "value"])
    df['value'] = pd.to_numeric(df['value'], errors='coerce')  # Convert 'value' to numeric
    df['date'] = pd.to_datetime(df['date'])  # Convert 'date' to datetime
    return df

def calculate_volatility(df):
    if df.empty:
        return pd.DataFrame(columns=['coin', 'volatility'])

    df = df.sort_values(by=['coin', 'date'])
    returns = df.groupby('coin')['value'].pct_change()
    volatility = returns.groupby('coin').apply(lambda x: x.std(skipna=True) if len(x) > 1 else np.nan)
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

    # Correct way: Group and then select the 'value' column for mean calculation
    df = df.groupby(["coin", "date"], as_index=False)["value"].mean()

    volatility_df = calculate_volatility(df)
    volatility_df['risk_category'] = volatility_df['volatility'].apply(categorize_risk)
    final_df = volatility_df[['coin', 'volatility', 'risk_category']]

    save_to_json(final_df, output_file)

if __name__ == "__main__":
    main()
