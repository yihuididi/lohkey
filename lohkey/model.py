# Import libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt


# Market Risk Prediction: Time-Series Forecasting
def predict_market_risk():
    # Load historical price data
    data = pd.read_csv('crypto_prices.csv')  # Replace with actual data path
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Train-Test Split
    train_data = data['Close'][:int(0.8*len(data))]
    test_data = data['Close'][int(0.8*len(data)):]

    # Fit ARIMA model
    model = ARIMA(train_data, order=(1, 1, 1))  # Adjust (p, d, q) based on data
    model_fit = model.fit()

    # Forecast
    forecast = model_fit.forecast(steps=len(test_data))

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(train_data, label="Train Data")
    plt.plot(test_data, label="Test Data")
    plt.plot(test_data.index, forecast, label="Forecast", color='red')
    plt.legend()
    plt.title("Market Risk Forecast (ARIMA)")
    plt.show()

    print("Market Risk Forecast Complete!")


# Credit Risk Prediction: Logistic Regression
def predict_credit_risk_logistic():
    # Load dataset
    data = pd.read_csv('credit_data.csv')  # Replace with actual data path

    # Feature selection
    features = ['loan_amount', 'income', 'credit_score', 'debt_to_income_ratio']
    target = 'default_status'

    # Split into train-test sets
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Logistic Regression Model
    log_model = LogisticRegression()
    log_model.fit(X_train, y_train)

    # Predictions
    y_pred = log_model.predict(X_test)

    # Model Evaluation
    print("\nLogistic Regression - Credit Risk")
    print("Accuracy:", accuracy_score(y_test, y_pred))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
    print("Classification Report:\n", classification_report(y_test, y_pred))


# Credit Risk Prediction: Random Forest
def predict_credit_risk_random_forest():
    # Load dataset
    data = pd.read_csv('credit_data.csv')  # Replace with actual data path

    # Feature selection
    features = ['loan_amount', 'income', 'credit_score', 'debt_to_income_ratio']
    target = 'default_status'

    # Split into train-test sets
    X = data[features]
    y = data[target]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Random Forest Model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)

    # Predictions
    y_pred_rf = rf_model.predict(X_test)

    # Model Evaluation
    print("\nRandom Forest - Credit Risk")
    print("Accuracy:", accuracy_score(y_test, y_pred_rf))
    print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))
    print("Classification Report:\n", classification_report(y_test, y_pred_rf))


# Main Execution
if __name__ == "__main__":
    print("Choose a model to run:")
    print("1. Predict Market Risk (ARIMA)")
    print("2. Predict Credit Risk (Logistic Regression)")
    print("3. Predict Credit Risk (Random Forest)")

    choice = input("Enter your choice (1/2/3): ")

    if choice == '1':
        predict_market_risk()
    elif choice == '2':
        predict_credit_risk_logistic()
    elif choice == '3':
        predict_credit_risk_random_forest()
    else:
        print("Invalid choice. Exiting.")
