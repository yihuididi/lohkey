import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.api import SimpleExpSmoothing


def get_crypto_predictions(crypto_symbol):
    """
    fetches historical price data for a cryptocurrency and predicts prices for the next 14 days.

    args:
        crypto_symbol (str): the symbol of the cryptocurrency (e.g., 'BTC-USD').

    returns:
        dict: a dictionary with historical data, forecasted prices, and a message if there's an error.
    """
    try:
        # fetch historical data for the crypto
        crypto_data = yf.download(crypto_symbol, period="6mo", interval="1d")
        if crypto_data.empty:
            return {"error": f"no data found for {crypto_symbol}."}

        # prepare the data for prediction
        crypto_data['Date'] = pd.to_datetime(crypto_data.index)
        crypto_data['Close'] = crypto_data['Close'].fillna(method='ffill')  # fill missing values

        # prepare for linear regression
        crypto_data['Days'] = (crypto_data['Date'] - crypto_data['Date'].min()).dt.days
        X = crypto_data[['Days']]
        y = crypto_data['Close']

        # train linear regression model
        model = LinearRegression()
        model.fit(X, y)

        # predict next 14 days
        future_days = np.array(range(X['Days'].max() + 1, X['Days'].max() + 15)).reshape(-1, 1)
        future_prices = model.predict(future_days)

        # return historical data and predictions
        return {
            "historical_prices": crypto_data[['Date', 'Close']].to_dict(orient='records'),
            "predicted_prices": future_prices.tolist(),
            "message": f"predicted next 14 days prices for {crypto_symbol}."
        }
    except Exception as e:
        return {"error": f"an error occurred: {e}"}


def get_crypto_metrics(crypto_symbol):
    """
    fetches historical price data for a cryptocurrency and calculates key investment metrics.

    args:
        crypto_symbol (str): the symbol of the cryptocurrency (e.g., 'BTC-USD').

    returns:
        dict: a dictionary with key metrics like volatility, moving averages, rsi, and more.
    """
    try:
        # fetch historical data for the crypto
        crypto_data = yf.download(crypto_symbol, period="6mo", interval="1d")
        if crypto_data.empty:
            return {"error": f"no data found for {crypto_symbol}."}

        # calculate current price
        current_price = crypto_data['Close'].iloc[-1]

        # calculate daily returns
        crypto_data['Daily Returns'] = crypto_data['Close'].pct_change()

        # calculate annualized volatility
        volatility = crypto_data['Daily Returns'].std() * np.sqrt(252)

        # calculate moving averages
        crypto_data['7-Day MA'] = crypto_data['Close'].rolling(window=7).mean()
        crypto_data['30-Day MA'] = crypto_data['Close'].rolling(window=30).mean()

        # calculate relative strength index (rsi)
        delta = crypto_data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        crypto_data['RSI'] = 100 - (100 / (1 + rs))
        rsi = crypto_data['RSI'].iloc[-1]

        # calculate all-time high (ath) and drawdown
        ath = crypto_data['Close'].max()
        drawdown = ((ath - current_price) / ath) * 100

        # calculate trading volume
        average_volume = crypto_data['Volume'].mean()

        # return metrics
        return {
            "current_price": current_price,
            "volatility": volatility,
            "7_day_moving_average": crypto_data['7-Day MA'].iloc[-1],
            "30_day_moving_average": crypto_data['30-Day MA'].iloc[-1],
            "rsi": rsi,
            "all_time_high": ath,
            "drawdown": drawdown,
            "average_volume": average_volume,
            "message": f"calculated key metrics for {crypto_symbol}."
        }
    except Exception as e:
        return {"error": f"an error occurred: {e}"}


# example usage (comment this out in production):
if __name__ == "__main__":
    crypto_symbol = input("enter the cryptocurrency symbol (e.g., BTC-USD): ")

    print("\nfetching predictions...")
    predictions = get_crypto_predictions(crypto_symbol)
    print(predictions)

    print("\nfetching investment metrics...")
    metrics = get_crypto_metrics(crypto_symbol)
    print(metrics)
