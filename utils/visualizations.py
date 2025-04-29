import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def plot_predictions(frame, y_true, y_pred):
    fig, ax = plt.subplots(figsize=(12, 5))  # Wider figure
    ax.plot(y_true, label='Actual', color="#007acc", linewidth=2)
    ax.plot(y_pred, label='Predicted', color="#ff6600", linestyle='--', linewidth=2)
    ax.set_title('Actual vs Predicted Prices', fontsize=16)
    ax.set_xlabel('Time Steps', fontsize=13)
    ax.set_ylabel('Price', fontsize=13)
    ax.legend(fontsize=12)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    return canvas


def plot_volume_chart(frame, dates, volumes):
    fig, ax = plt.subplots(figsize=(12, 4))  # Wider and clean
    ax.bar(dates, volumes, color="#4caf50")
    ax.set_title('Volume over Last 30 Days', fontsize=16)
    ax.set_xlabel('Date', fontsize=13)
    ax.set_ylabel('Volume', fontsize=13)
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(True, linestyle="--", alpha=0.5)

    plt.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    return canvas



def plot_comparison_table(parent_frame, data):
    """
    Creates a Treeview table for company comparison (like price change, avg price).
    Expects `data` as a list of tuples: (Company, AvgPrice, PriceChange)
    """
    columns = ("Company", "Average Price", "Change")
    tree = ttk.Treeview(parent_frame, columns=columns, show="headings", height=5)

    # Style headers
    style = ttk.Style()
    style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=30)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150, anchor='center')

    for row in data:
        company, avg_price, change = row
        tree.insert('', tk.END, values=(company, f"${avg_price:.2f}", f"{change:+.2f}%"))

    tree.pack(pady=5)
    return tree

