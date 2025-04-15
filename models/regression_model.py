# models/regression_model.py

import pandas as pd
from sklearn.linear_model import LinearRegression
from utils.metrics import calculate_rmse, calculate_mae

def run_linear_regression(df, n_lags=5):
    """
    Uses previous 'n_lags' closing prices to predict the next closing price.
    """
    if 'Close' not in df.columns:
        raise ValueError("Dataset must contain a 'Close' column.")

    data = df['Close'].copy()

    # Create lag features
    for i in range(1, n_lags + 1):
        df[f'lag_{i}'] = data.shift(i)

    df.dropna(inplace=True)

    # Features: lag_1 to lag_n
    X = df[[f'lag_{i}' for i in range(1, n_lags + 1)]]
    y = df['Close']

    # Train/test split (80/20)
    split_index = int(len(df) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Train model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluate
    rmse = calculate_rmse(y_test, y_pred)
    mae = calculate_mae(y_test, y_pred)

    return rmse, mae, y_test, y_pred
