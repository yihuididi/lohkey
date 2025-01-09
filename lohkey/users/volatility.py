from datetime import datetime, timezone
import json
import pandas as pd

def load_data(json_file):
    with open(json_file, \"r\") as file:
        data = json.load(file)
        all_data = []
    # Process data into a list of lists
    for coin, metrics in data.items():
        for metric, info in metrics.items():
            for timestamp, value in info:
                date = datetime.fromtimestamp(timestamp \/ 1000, tz=timezone.utc).strftime(\"%Y-%m-%d\")
                all_data.append([coin, date, metric, value])
    return pd.DataFrame(all_data, columns=[\"coin\", \"date\", \"metric\", \"value\"])

def calculate_volatility(df):
    # Calculate daily returns
    returns = df.set_index(['coin', 'metric']).pct_change(axis=1)
    # Calculate volatility (standard deviation of returns)
    volatility = returns.std(axis=1)
    # Create a DataFrame for volatility results
    volatility_df = volatility.reset_index(name='volatility')
    return volatility_df

def save_to_json(df, output_file):
    df.to_json(output_file, orient='records', lines=True)

def main():
    json_file = \"lohkey\/static\/historical_data.json\"
    output_file = \"lohkey\/static\/volatility_data.json\"
    
    # Load data
    df = load_data(json_file)
    # Group, pivot and calculate volatility
    df = df.groupby([\"coin\", \"metric\", \"date\"], as_index=False).mean()
    df = df.pivot(index=[\"coin\", \"metric\"], columns=\"date\", values=\"value\").reset_index()
    # Calculate volatility
    result_df = calculate_volatility(df)
    # Save to JSON
    save_to_json(result_df, output_file)

if __name__ == \"__main__\":
    main()
