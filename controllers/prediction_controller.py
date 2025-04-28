from models.baseline_model import run_naive_baseline
from models.regression_model import run_linear_regression, forecast_future_prices
from models.random_forest_model import run_random_forest
import pandas as pd

class PredictionController:
    def __init__(self):
        self.data = None
        self.inflation_df = None

    def load_dataset(self, file_path):
        from utils.data_loader import load_csv
        self.data = load_csv(file_path)
        return self.data

    def load_inflation_data(self, inflation_path):
        try:
            raw_df = pd.read_csv(inflation_path)
            melted = raw_df.melt(id_vars='Year', var_name='Month', value_name='Inflation')
            month_map = {
                'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
            }
            melted = melted[melted['Month'].isin(month_map)]
            melted['Date'] = pd.to_datetime(melted['Year'].astype(str) + '-' + melted['Month'].map(month_map) + '-01')
            self.inflation_df = melted[['Date', 'Inflation']].sort_values('Date').reset_index(drop=True)
        except Exception as e:
            print(f"[Error loading inflation data] {e}")
            self.inflation_df = None

    def run_baseline_model(self):
        if self.data is not None:
            rmse, mae, y_test, y_pred = run_naive_baseline(self.data)
            return rmse, mae, y_test, y_pred
        else:
            return 0.0, 0.0, None, None


    def run_linear_regression_model(self):
        if self.data is not None:
            rmse, mae, y_test, y_pred = run_linear_regression(self.data, self.inflation_df)
            return rmse, mae, y_test, y_pred
        else:
            return 0.0, 0.0, None, None

    def run_random_forest_model(self):
        if self.data is not None:
            rmse, mae, y_test, y_pred = run_random_forest(self.data, self.inflation_df)
            return rmse, mae, y_test, y_pred
        else:
            return 0.0, 0.0, None, None

    def forecast_next_months(self, n_months=12):
        if self.data is not None:
            return forecast_future_prices(self.data, self.inflation_df, n_months=n_months)
        else:
            return pd.DataFrame(columns=["Month", "Forecasted Price"])