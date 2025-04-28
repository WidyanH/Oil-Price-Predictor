import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk


def plot_predictions(root, actual, predicted):
    """
    Display actual vs predicted values in a Matplotlib chart embedded in Tkinter.
    """
    fig, ax = plt.subplots(figsize=(8, 4))

    # Styled plot
    ax.plot(actual, label='Actual', color='#1f77b4', marker='o', linestyle='-')
    ax.plot(predicted, label='Predicted', color='#ff7f0e', marker='x', linestyle='--')

    ax.set_title("📈 Actual vs Predicted Prices", fontsize=14, fontweight='bold')
    ax.set_xlabel("Time", fontsize=12)
    ax.set_ylabel("Price", fontsize=12)
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.5)

    fig.patch.set_facecolor('#f7f7f7')
    ax.set_facecolor('#ffffff')


    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=10)

    return canvas


def plot_volume_chart(parent_frame, dates, volumes):
    """
    Display a bar chart of trading volume over time.
    """
    fig, ax = plt.subplots(figsize=(8, 3))

    ax.bar(dates, volumes, color='#4caf50')
    ax.set_title("📊 Trading Volume", fontsize=12, fontweight='bold')
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    ax.tick_params(axis='x', labelrotation=45)
    ax.grid(axis='y', linestyle='--', alpha=0.5)
    fig.tight_layout()

    fig.patch.set_facecolor('#f7f7f7')
    ax.set_facecolor('#ffffff')

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

