from utils.metrics import calculate_rmse, calculate_mae

def run_naive_baseline(df):
    """
    Assumes next value equals current value (naive prediction).
    Accepts either 'Close' or 'Price' column for price data.
    """
    price_col = None
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['close', 'price', 'closing price', 'adj close']:
            price_col = col
            break

    if not price_col:
        raise ValueError("Dataset must contain a 'Close' or 'Price' column for price.")

    actual = df[price_col].values[1:]
    predicted = df[price_col].values[:-1]

    rmse = calculate_rmse(actual, predicted)
    mae = calculate_mae(actual, predicted)

    return rmse, mae, actual, predicted
