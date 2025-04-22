from sklearn.ensemble import RandomForestRegressor
from utils.metrics import calculate_rmse, calculate_mae
import pandas as pd

def run_random_forest(df, n_lags=5):
    """
    Train a Random Forest model on lagged closing prices and return predictions and metrics.
    """

    # Find the appropriate column for price
    price_col = None
    for col in df.columns:
        if col.lower() in ['close', 'price', 'adj close']:
            price_col = col
            break

    if not price_col:
        raise ValueError("Dataset must contain a 'Close' or 'Price' column.")

    # Create lag features
    data = df[price_col].copy()
    for i in range(1, n_lags + 1):
        df[f'lag_{i}'] = data.shift(i)

    df.dropna(inplace=True)

    X = df[[f'lag_{i}' for i in range(1, n_lags + 1)]]
    y = df[price_col]

    # Train/test split
    split_index = int(len(df) * 0.8)
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]

    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Evaluate
    rmse = calculate_rmse(y_test, y_pred)
    mae = calculate_mae(y_test, y_pred)

    return rmse, mae, y_test, y_pred
