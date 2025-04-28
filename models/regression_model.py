import pandas as pd
from sklearn.linear_model import LinearRegression
from utils.metrics import calculate_rmse, calculate_mae
import numpy as np

def run_linear_regression(df, inflation_df=None, n_lags=5):
    """
    Uses previous 'n_lags' prices to predict the next price.
    Accepts columns named 'Close', 'Price', or similar.
    Includes inflation rate 
    """

    # Try to locate the correct price column
    price_col = None
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['close', 'price', 'adj close', 'closing price']:
            price_col = col
            break

    if not price_col:
        raise ValueError("Dataset must contain a column named 'Close', 'Price', or similar.")

    data = df[price_col].copy()

    if inflation_df is not None and 'Date' in df.columns:
        df = pd.merge(df, inflation_df, on='Date', how='left')
        df['Inflation'].fillna(method='ffill', inplace=True)
        df['Inflation'].fillna(method='bfill', inplace=True)

    # Create lag features
    for i in range(1, n_lags + 1):
        df[f'lag_{i}'] = data.shift(i)

    df.dropna(inplace=True)

    # Features: lag_1 to lag_n
    # and inflation
    feature_cols = [f'lag_{i}' for i in range(1, n_lags + 1)]
    if 'Inflation' in df.columns:
        feature_cols.append('Inflation')

    X = df[feature_cols]
    y = df[price_col]


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

def forecast_future_prices(df, inflation_df=None, n_lags=5, n_months=12):
    """
    Forecast future prices using the trained linear regression model.
    """
    price_col = None
    for col in df.columns:
        if col.lower() in ['close', 'price', 'adj close', 'closing price']:
            price_col = col
            break

    if not price_col:
        raise ValueError("Dataset must contain a column named 'Close', 'Price', or similar.")

    df = df.copy()

    if inflation_df is not None and 'Date' in df.columns:
        df = pd.merge(df, inflation_df, on='Date', how='left')
        df['Inflation'].fillna(method='ffill', inplace=True)
        df['Inflation'].fillna(method='bfill', inplace=True)

    data = df[price_col].copy()
    latest_date = df['Date'].max() if 'Date' in df.columns else pd.Timestamp.today()

    for i in range(1, n_lags + 1):
        df[f'lag_{i}'] = data.shift(i)

    df.dropna(inplace=True)

    feature_cols = [f'lag_{i}' for i in range(1, n_lags + 1)]
    if 'Inflation' in df.columns:
        feature_cols.append('Inflation')

    X = df[feature_cols]
    y = df[price_col]

    model = LinearRegression()
    model.fit(X, y)

    future_prices = []
    last_known = df.iloc[-1]
    inflation_values = inflation_df.set_index('Date')['Inflation'] if inflation_df is not None else None

    lags = [last_known[f'lag_{i}'] for i in range(1, n_lags + 1)]

    for i in range(n_months):
        next_features = lags[-n_lags:]
        if inflation_values is not None:
            future_month = latest_date + pd.DateOffset(months=i+1)
            next_inflation = inflation_values.get(future_month, inflation_values.ffill().iloc[-1])
            next_features = next_features + [next_inflation]

        next_price = model.predict([next_features])[0]
        future_prices.append((latest_date + pd.DateOffset(months=i+1), next_price))
        lags.append(next_price)

    return pd.DataFrame(future_prices, columns=["Month", "Forecasted Price"])