# utils/metrics.py

import numpy as np

def calculate_rmse(actual, predicted):
    return np.sqrt(np.mean((np.array(actual) - np.array(predicted)) ** 2))

def calculate_mae(actual, predicted):
    return np.mean(np.abs(np.array(actual) - np.array(predicted)))
