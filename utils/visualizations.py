<<<<<<< Updated upstream
=======
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk

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


def plot_volume_chart(parent_frame, dates, volumes):
    """
    Display a bar chart of trading volume over time.
    """
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.bar(dates, volumes, color='skyblue')
    ax.set_title("Trading Volume")
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    ax.tick_params(axis='x', labelrotation=45)

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=5)

    return canvas


def plot_comparison_table(parent_frame, data):
    """
    Creates a Treeview table for company comparison (like price change, avg price).
    Expects `data` as a list of tuples: (Company, AvgPrice, PriceChange)
    """
    columns = ("Company", "Average Price", "Change")
    tree = ttk.Treeview(parent_frame, columns=columns, show="headings", height=5)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor='center')

    for row in data:
        company, avg_price, change = row
        tree.insert('', tk.END, values=(company, f"${avg_price:.2f}", f"{change:+.2f}%"))

    tree.pack(pady=5)
    return tree
>>>>>>> Stashed changes
