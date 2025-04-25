from sklearn.ensemble import RandomForestRegressor
from utils.metrics import calculate_rmse, calculate_mae
import pandas as pd

def run_random_forest(df, inflation_df=None, n_lags=5):
    """
    Train a Random Forest model on lagged closing prices and return predictions and metrics.
    Includes option for inflation rate
    """

    # Find the appropriate column for price
    price_col = None
    for col in df.columns:
        if col.lower() in ['close', 'price', 'adj close']:
            price_col = col
            break

    if not price_col:
        raise ValueError("Dataset must contain a 'Close' or 'Price' column.")

    # Inflation
    if inflation_df is not None and 'Date' in df.columns:
        df = pd.merge(df, inflation_df, on='Date', how='left')
        df['Inflation'].fillna(method='ffill', inplace=True)
        df['Inflation'].fillna(method='bfill', inplace=True)

    # Create lag features
    data = df[price_col].copy()
    for i in range(1, n_lags + 1):
        df[f'lag_{i}'] = data.shift(i)

    df.dropna(inplace=True)

    feature_cols = [f'lag_{i}' for i in range(1, n_lags + 1)]
    if 'Inflation' in df.columns:
        feature_cols.append('Inflation')

    X = df[feature_cols]
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
