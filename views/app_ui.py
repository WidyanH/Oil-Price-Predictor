# views/app_ui.py
import tkinter as tk
from tkinter import filedialog, messagebox
from controllers.prediction_controller import PredictionController
from utils.visualizations import plot_predictions



class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Oil & Gas Price Prediction")
        self.root.geometry("800x600")

        self.create_widgets()
        self.controller = PredictionController()
        self.chart_canvas = None

    def create_widgets(self):
        # Title
        title = tk.Label(self.root, text="Oil & Gas Price Predictor", font=("Arial", 20))
        title.pack(pady=20)

        # Instructions
        instr = tk.Label(self.root, text="Upload a CSV file containing historical data:")
        instr.pack()

        # Upload button
        upload_btn = tk.Button(self.root, text="Upload CSV", command=self.upload_file)
        upload_btn.pack(pady=10)

        # Action buttons
        run_btn = tk.Button(self.root, text="Run Model", command=self.run_model)
        run_btn.pack(pady=10)

        lr_btn = tk.Button(self.root, text="Run Linear Regression", command=self.run_regression)
        lr_btn.pack(pady=5)

        # Output display area
        self.output_label = tk.Label(self.root, text="", fg="blue", wraplength=700, justify="left")
        self.output_label.pack(pady=20)

    def upload_file(self):

        file_path = filedialog.askopenfilename(
            title="Select CSV file",
            filetypes=(("CSV Files", "*.csv"),)
        )
        if file_path:
            df = self.controller.load_dataset(file_path)
            if df is not None:
                preview = df[['Date', 'Close']].head().to_string(index=False)
                self.output_label.config(text=f"✅ File loaded successfully!\n\nPreview:\n{preview}")
            else:
                messagebox.showerror("Error", "Failed to load CSV file.")
        else:
            messagebox.showwarning("No file", "No file selected.")

    def run_model(self):
        result = self.controller.run_baseline_model()
        self.output_label.config(text=result)

    def run_regression(self):
        result, y_test, y_pred = self.controller.run_linear_regression_model()
        self.output_label.config(text=result)

        # Clear previous chart
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
            self.chart_canvas = None

        # Plot new chart if data exists
        if y_test is not None and y_pred is not None:
            self.chart_canvas = plot_predictions(self.root, y_test.values, y_pred)



