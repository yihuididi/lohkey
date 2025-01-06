import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# Market Risk Prediction
def predict_market_risk(stock_ticker):
    try:
        # Fetch stock data
        stock_data = yf.download(stock_ticker, period="6mo", interval="1d")
        if stock_data.empty:
            return f"Error: No data found for stock {stock_ticker}."

        # Prepare data
        stock_data['Date'] = pd.to_datetime(stock_data.index)
        stock_data['Close'] = stock_data['Close'].fillna(method='ffill')
        train_data = stock_data['Close'][:int(0.8 * len(stock_data))]
        test_data = stock_data['Close'][int(0.8 * len(stock_data)):]

        # Fit ARIMA model
        model = ARIMA(train_data, order=(1, 1, 1))
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=len(test_data))

        # Plot results
        plt.figure(figsize=(10, 6))
        plt.plot(train_data, label="Train Data")
        plt.plot(test_data, label="Test Data")
        plt.plot(test_data.index, forecast, label="Forecast", color='red')
        plt.legend()
        plt.title(f"{stock_ticker} - Market Risk Prediction")
        plt.show()

        return forecast
    except Exception as e:
        return f"An error occurred: {e}"

# Credit Risk Prediction (Logistic Regression)
def predict_credit_risk_logistic(loan_amount, income, credit_score, debt_to_income_ratio):
    # Sample dataset
    data = pd.DataFrame({
        'loan_amount': [10000, 20000, 30000, 40000, 50000],
        'income': [50000, 60000, 70000, 80000, 90000],
        'credit_score': [700, 650, 600, 550, 500],
        'debt_to_income_ratio': [0.2, 0.25, 0.3, 0.35, 0.4],
        'default_status': [0, 0, 1, 1, 1]
    })

    # Train-Test Split
    X = data[['loan_amount', 'income', 'credit_score', 'debt_to_income_ratio']]
    y = data['default_status']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Logistic Regression Model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predict on user input
    input_data = pd.DataFrame({
        'loan_amount': [loan_amount],
        'income': [income],
        'credit_score': [credit_score],
        'debt_to_income_ratio': [debt_to_income_ratio]
    })
    prediction = model.predict_proba(input_data)[0][1]  # Probability of default

    return f"Probability of default: {prediction * 100:.2f}%"

# Credit Risk Prediction (Random Forest)
def predict_credit_risk_random_forest(loan_amount, income, credit_score, debt_to_income_ratio):
    # Sample dataset
    data = pd.DataFrame({
        'loan_amount': [10000, 20000, 30000, 40000, 50000],
        'income': [50000, 60000, 70000, 80000, 90000],
        'credit_score': [700, 650, 600, 550, 500],
        'debt_to_income_ratio': [0.2, 0.25, 0.3, 0.35, 0.4],
        'default_status': [0, 0, 1, 1, 1]
    })

    # Train-Test Split
    X = data[['loan_amount', 'income', 'credit_score', 'debt_to_income_ratio']]
    y = data['default_status']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict on user input
    input_data = pd.DataFrame({
        'loan_amount': [loan_amount],
        'income': [income],
        'credit_score': [credit_score],
        'debt_to_income_ratio': [debt_to_income_ratio]
    })
    prediction = model.predict_proba(input_data)[0][1]  # Probability of default

    return f"Probability of default: {prediction * 100:.2f}%"
