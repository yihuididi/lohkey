from datetime import datetime, timezone
import json
import pandas as pd

def load_data(json_file):
    with open(json_file,"r") as file:
        data = json.load(file)
        all_data = []  # Process data into a list of lists
        for coin, metrics in data.items():
            for metric, info in metrics.items():
                for timestamp, value in info:
                    date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).strftime("%Y-%m-%d")
                    all_data.append([coin, date, metric, value])
    return pd.DataFrame(all_data, columns=["coin", "date", "metric", "value"])

def calculate_volatility(df):
    # Calculate daily returns
    returns = df.set_index(['coin', 'metric']).pct_change(axis=1)
    # Calculate volatility (standard deviation of returns)
    volatility = returns.std(axis=1)
    # Create a DataFrame for volatility results
    volatility_df = volatility.reset_index(name='volatility')
    return volatility_df

def categorize_risk(volatility):
    # Define risk categories based on volatility
    if volatility < 0.01:
        return 'Low Risk'
    elif 0.01 <= volatility < 0.05:
        return 'Moderate Risk'
    else:
        return 'High Risk'

def save_to_json(df, output_file):
    df.to_json(output_file, orient='records', lines=True)

def main():
    json_file = "lohkey/static/historical_data.json"  # Corrected file path
    output_file = "lohkey/static/volatility_data.json"  # Corrected file path

    # Load data
    df = load_data(json_file)
    # Group, pivot and calculate volatility
    df = df.groupby(["coin", "metric", "date"], as_index=False).mean()
    df = df.pivot(index=["coin", "metric"], columns="date", values="value").reset_index()
    # Calculate volatility
    volatility_df = calculate_volatility(df)
    # Categorize risk and create final DataFrame
    volatility_df['risk_category'] = volatility_df['volatility'].apply(categorize_risk)
    final_df = volatility_df[['coin', 'volatility', 'risk_category']]
    # Save to JSON
    save_to_json(final_df, output_file)

if __name__ == "__main__":
    main()
