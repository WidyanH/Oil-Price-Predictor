import pandas as pd

def load_brent_data():
    return pd.read_csv('data/processed/brent_cleaned.csv', parse_dates=['Date'])

