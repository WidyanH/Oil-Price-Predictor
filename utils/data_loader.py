# utils/data_loader.py

import pandas as pd

def load_csv(file_path):
    """
    Load a CSV file into a pandas DataFrame.
    Returns: DataFrame or None if error occurs
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error loading file: {e}")
        return None
