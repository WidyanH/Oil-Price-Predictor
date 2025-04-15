# models/baseline_model.py

from utils.metrics import calculate_rmse, calculate_mae

def run_naive_baseline(df):
    """
    Assumes next value equals current value (naive prediction).
    Uses 'Close' column for price if available.
    """
    price_col = None
    for col in df.columns:
        if col.lower() == 'close':
            price_col = col
            break

    if not price_col:
        raise ValueError("Dataset must contain a 'Close' column for price.")

    actual = df[price_col].values[1:]
    predicted = df[price_col].values[:-1]

    rmse = calculate_rmse(actual, predicted)
    mae = calculate_mae(actual, predicted)

    return rmse, mae
