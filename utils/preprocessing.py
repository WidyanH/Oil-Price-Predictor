import pandas as pd
import yfinance as yf
import os

# === Brent Preprocessing ===
def preprocess_brent_data(path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/raw/brent_crude.csv'):
    df = pd.read_csv(path)

    try:
        df['Date'] = df['Date'].astype(str).str.strip('"')
        df['Date'] = pd.to_datetime(df['Date'], format='mixed')
    except Exception as e:
        print("Date parsing failed:", e)
        print("Sample of 'Date' column:", df['Date'].unique()[:5])
        raise e

    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Price'] = df['Price'].ffill()

    for i in range(1, 31):
        df[f'lag_{i}'] = df['Price'].shift(i)

    df['rolling_7'] = df['Price'].rolling(window=7).mean()
    df['rolling_30'] = df['Price'].rolling(window=30).mean()
    df.dropna(inplace=True)

    output_dir = '/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'brent_cleaned.csv')
    df.to_csv(output_path, index=False)

    print(f"Saved cleaned Brent data to: {output_path}")
    return df


# === WTI Preprocessing ===
def preprocess_wti_data(path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/raw/wti_crude.csv'):
    df = pd.read_csv(path)

    df['date'] = pd.to_datetime(df['date']).dt.date
    df['date'] = pd.to_datetime(df['date'])
    df.rename(columns={'date': 'Date', 'price': 'Price'}, inplace=True)

    df.sort_values('Date', inplace=True)
    df.reset_index(drop=True, inplace=True)
    df['Price'] = df['Price'].ffill()

    for i in range(1, 31):
        df[f'lag_{i}'] = df['Price'].shift(i)

    df['rolling_7'] = df['Price'].rolling(window=7).mean()
    df['rolling_30'] = df['Price'].rolling(window=30).mean()
    df.dropna(inplace=True)

    output_dir = '/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'wti_cleaned.csv')
    df.to_csv(output_path, index=False)

    print(f"Saved cleaned WTI data to: {output_path}")
    return df


# === Merge Brent with CPI macro dataset ===
def merge_cpi_with_brent(
    brent_path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed/brent_cleaned.csv',
    cpi_path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/raw/cpi_usa.csv'
):
    # Load cleaned Brent data
    brent = pd.read_csv(brent_path)
    brent['Date'] = pd.to_datetime(brent['Date'])
    brent = brent[brent['Date'] >= '2000-01-01']  # Align to CPI start date

    # Load CPI data
    cpi = pd.read_csv(cpi_path)
    cpi.rename(columns={cpi.columns[0]: 'Date', cpi.columns[1]: 'CPI_USA'}, inplace=True)
    cpi['Date'] = pd.to_datetime(cpi['Date'])

    # Forward-fill CPI to daily data
    merged = pd.merge_asof(brent.sort_values('Date'), cpi.sort_values('Date'), on='Date', direction='backward')

    # Save merged dataset
    output_dir = '/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'brent_merged_with_cpi.csv')
    merged.to_csv(output_path, index=False)

    print(f"Merged Brent with CPI saved to: {output_path}")
    return merged

def merge_interest_rate(
    brent_cpi_path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed/brent_merged_with_cpi.csv',
    fedfunds_path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/raw/fedfunds.csv'
):
    # Load existing Brent + CPI dataset
    df = pd.read_csv(brent_cpi_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Load FEDFUNDS data
    fed = pd.read_csv(fedfunds_path)
    fed.rename(columns={fed.columns[0]: 'Date', fed.columns[1]: 'Fed_Funds_Rate'}, inplace=True)
    fed['Date'] = pd.to_datetime(fed['Date'])

    # Merge using backward fill for daily alignment
    merged = pd.merge_asof(df.sort_values('Date'), fed.sort_values('Date'), on='Date', direction='backward')

    # Save updated dataset
    output_dir = '/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'brent_with_cpi_interest.csv')
    merged.to_csv(output_path, index=False)

    print(f"Merged Brent + CPI + Interest Rate saved to: {output_path}")
    return merged

def merge_eia_data(
    brent_macro_path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed/brent_with_cpi_interest.csv',
    eia_path='/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/raw/eia_data.csv'
):
    # Load existing Brent + CPI + Interest Rate dataset
    df = pd.read_csv(brent_macro_path)
    df['Date'] = pd.to_datetime(df['Date'])

    # Load EIA data (skip first 2 rows as we saw)
    eia = pd.read_csv(eia_path, skiprows=2)

    # Select relevant columns
    eia = eia[['Date', 'Weekly U.S. Ending Stocks of Crude Oil  (Thousand Barrels)']]
    eia['Date'] = pd.to_datetime(eia['Date'])
    eia.rename(columns={'Weekly U.S. Ending Stocks of Crude Oil  (Thousand Barrels)': 'Crude_Stocks'}, inplace=True)

    # Merge with backward fill (align weekly data to daily Brent data)
    merged = pd.merge_asof(df.sort_values('Date'), eia.sort_values('Date'), on='Date', direction='backward')

    # Save final dataset
    output_dir = '/Users/salma.abbady/Documents/GitHub/Oil-Price-Predictor/data/processed'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'brent_with_all_macros.csv')
    merged.to_csv(output_path, index=False)

    print(f"Final dataset with EIA data saved to: {output_path}")
    return merged
