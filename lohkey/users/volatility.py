from datetime import datetime, timezone
import json
import pandas as pd

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
    returns = df.set_index(['coin', 'metric']).pct_change(axis=1)
    volatility = returns.std(axis=1)
    volatility_df = volatility.reset_index(name='volatility')
    return volatility_df

def categorize_risk(volatility):
    if volatility < 0.01:
        return 'Low Risk'
    elif 0.01 <= volatility < 0.2:
        return 'Moderate Risk'
    else:
        return 'High Risk'

def save_to_json(df, output_file):
    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    # Write the list of dictionaries to a JSON file
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=4) # indent for pretty printing (optional)


def main():
    json_file = "lohkey/static/historical_data.json"
    output_file = "lohkey/static/volatility_data.json"

    df = load_data(json_file)
    df = df.groupby(["coin", "metric", "date"], as_index=False).mean()
    df = df.pivot(index=["coin", "metric"], columns="date", values="value").reset_index()
    volatility_df = calculate_volatility(df)
    volatility_df['risk_category'] = volatility_df['volatility'].apply(categorize_risk)
    final_df = volatility_df[['coin', 'volatility', 'risk_category']]

    save_to_json(final_df, output_file)

if __name__ == "__main__":
    main()
