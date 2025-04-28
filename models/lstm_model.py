import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
from utils.metrics import calculate_rmse, calculate_mae

def run_lstm_model(df, epochs=10, batch_size=32):
    """
    Trains an LSTM model to predict the next price value.
    Accepts either 'Close' or 'Price' column for price data.
    """
    # 1. Identify price column
    price_col = None
    for col in df.columns:
        col_lower = col.lower()
        if col_lower in ['close', 'price', 'closing price', 'adj close']:
            price_col = col
            break

    if not price_col:
        raise ValueError("Dataset must contain a 'Close' or 'Price' column for price.")

    prices = df[price_col].values.reshape(-1, 1)

    # 2. Normalize prices for faster training
    scaler = MinMaxScaler()
    prices_scaled = scaler.fit_transform(prices)

    # 3. Prepare sequences (X: previous step, y: next step)
    X, y = [], []
    for i in range(len(prices_scaled) - 1):
        X.append(prices_scaled[i])
        y.append(prices_scaled[i + 1])

    X = np.array(X)
    y = np.array(y)

    X = X.reshape((X.shape[0], 1, X.shape[1]))  # LSTM expects 3D input

    # 4. Build model
    model = Sequential()
    model.add(LSTM(50, activation='relu', input_shape=(X.shape[1], X.shape[2])))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')

    # 5. Train
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)

    # 6. Predict
    y_pred_scaled = model.predict(X)

    # 7. Inverse scale to original prices
    actual = scaler.inverse_transform(y)
    predicted = scaler.inverse_transform(y_pred_scaled)

    # 8. Calculate metrics
    rmse = calculate_rmse(actual.flatten(), predicted.flatten())
    mae = calculate_mae(actual.flatten(), predicted.flatten())

    return rmse, mae, actual.flatten(), predicted.flatten()
