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
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df['date'] = pd.to_datetime(df['date'])  # Convert date to datetime
    return df

def calculate_liquidity_risk(df):
    if df.empty:
        return pd.DataFrame(columns=['coin', 'liquidity_risk'])

    df = df.sort_values(by=['coin', 'date'])
    df['volume_change'] = df.groupby('coin')['value'].pct_change()
    df['abs_volume_change'] = df['volume_change'].abs()

    liquidity_risk = df.groupby('coin')['abs_volume_change'].apply(lambda x: x.mean(skipna=True) if len(x) > 1 else np.nan)
    liquidity_risk = liquidity_risk.reset_index()
    liquidity_risk.columns = ['coin', 'liquidity_risk']
    return liquidity_risk

def categorize_liquidity_risk(liquidity_risk):
    if np.isnan(liquidity_risk):
        return 'Not Available'
    elif liquidity_risk < 0.05:
        return 'Low Liquidity Risk'
    elif 0.05 <= liquidity_risk < 0.15:
        return 'Moderate Liquidity Risk'
    else:
        return 'High Liquidity Risk'

def save_to_json(df, output_file):
    data = df.to_dict(orient='records')
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4)

def main():
    json_file = "lohkey/static/historical_data.json"
    output_file = "lohkey/static/liquidity_data.json"

    df = load_data(json_file)

    # Filter for volume data
    df_volume = df[df['metric'] == 'total_volumes'].copy() # Create a copy to avoid SettingWithCopyWarning
    
    if df_volume.empty:
        print("No volume data found. Liquidity risk cannot be calculated.")
        return

    df_volume = df_volume.groupby(["coin", "date"], as_index=False)["value"].mean()

    liquidity_df = calculate_liquidity_risk(df_volume)
    liquidity_df['liquidity_risk_category'] = liquidity_df['liquidity_risk'].apply(categorize_liquidity_risk)
    final_df = liquidity_df[['coin', 'liquidity_risk', 'liquidity_risk_category']]

    save_to_json(final_df, output_file)

if __name__ == "__main__":
    main()

