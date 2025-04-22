<<<<<<< Updated upstream
=======
from models.baseline_model import run_naive_baseline
from models.regression_model import run_linear_regression
from models.random_forest_model import run_random_forest

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
            return rmse, mae
        else:
            return 0.0, 0.0

    def run_linear_regression_model(self):
        if self.data is not None:
            rmse, mae, y_test, y_pred = run_linear_regression(self.data)
            return rmse, mae, y_test, y_pred
        else:
            return 0.0, 0.0, None, None

    def run_random_forest_model(self):
        if self.data is not None:
            rmse, mae, y_test, y_pred = run_random_forest(self.data)
            return rmse, mae, y_test, y_pred
        else:
            return 0.0, 0.0, None, None
>>>>>>> Stashed changes
