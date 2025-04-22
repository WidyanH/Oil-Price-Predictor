# controllers/prediction_controller.py

from models.baseline_model import run_naive_baseline
from models.regression_model import run_linear_regression


class PredictionController:
    def __init__(self):
        self.data = None

    def load_dataset(self, file_path):
        from utils.data_loader import load_csv
        self.data = load_csv(file_path)
        return self.data

    def run_baseline_model(self):
        if self.data is not None:
            rmse, mae = run_naive_baseline(self.data)
            return f"Naive Baseline Results:\nRMSE: {rmse:.4f}\nMAE: {mae:.4f}"
        else:
            return "No dataset loaded yet."


    def run_linear_regression_model(self):
        if self.data is not None:
            rmse, mae, y_test, y_pred = run_linear_regression(self.data)
            return f"Linear Regression Results:\nRMSE: {rmse:.4f}\nMAE: {mae:.4f}"
        else:
            return "No dataset loaded yet."

    def run_linear_regression_model(self):
        if self.data is not None:
            rmse, mae, y_test, y_pred = run_linear_regression(self.data)
            result_text = f"Linear Regression Results:\nRMSE: {rmse:.4f}\nMAE: {mae:.4f}"
            return result_text, y_test, y_pred
        else:
            return " No dataset loaded yet.", None, None

