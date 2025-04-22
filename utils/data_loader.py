# utils/data_loader.py

import pandas as pd

def load_csv(file_path):
    """
    Loads and preprocesses a CSV file for oil & gas price prediction.
    Ensures date parsing, sorting, and handles missing values.
    """
    try:
        df = pd.read_csv(file_path)

        # Convert date column if present
        date_cols = [col for col in df.columns if col.lower() in ['date', 'timestamp']]
        if date_cols:
            df[date_cols[0]] = pd.to_datetime(df[date_cols[0]], errors='coerce')
            df = df.sort_values(by=date_cols[0])

        # Drop rows with all NaNs
        df.dropna(how='all', inplace=True)

        # Fill or drop missing values as needed
        df.fillna(method='ffill', inplace=True)
        df.dropna(inplace=True)

        return df

    except Exception as e:
        print(f"[Error loading CSV] {e}")
        return None
