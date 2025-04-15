# utils/visualizations.py

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_predictions(root, actual, predicted):
    """
    Display actual vs predicted values in a Matplotlib chart embedded in Tkinter.
    """
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(actual, label='Actual', marker='o', linestyle='-')
    ax.plot(predicted, label='Predicted', marker='x', linestyle='--')
    ax.set_title("Actual vs Predicted Prices")
    ax.set_xlabel("Time")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(True)

    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    return canvas
