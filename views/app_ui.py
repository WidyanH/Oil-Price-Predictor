<<<<<<< Updated upstream
=======
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from controllers.prediction_controller import PredictionController
from utils.visualizations import plot_predictions, plot_volume_chart, plot_comparison_table

class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Oil & Gas Price Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f2f2f2")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6, relief="flat", background="#4caf50", foreground="white")
        style.map("TButton", background=[('active', '#45a049')])
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TCombobox", padding=5)

        self.controller = PredictionController()
        self.chart_canvas = None
        self.volume_canvas = None
        self.df = None

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self.root, text="\U0001F6E2 Oil & Gas Stock Market Overview", font=("Segoe UI", 20, "bold"), bg="#f2f2f2")
        title.pack(pady=10)

        top_frame = tk.Frame(self.root, bg="#f2f2f2")
        top_frame.pack(pady=5)

        self.file_label = tk.Label(top_frame, text="No CSV loaded", fg="gray", bg="#f2f2f2")
        self.file_label.grid(row=0, column=0, padx=10)

        ttk.Button(top_frame, text="Upload CSV", command=self.upload_file).grid(row=0, column=1, padx=10)

        ttk.Label(top_frame, text="Select Model:").grid(row=0, column=2, padx=10)
        self.model_var = tk.StringVar()
        model_dropdown = ttk.Combobox(top_frame, textvariable=self.model_var, state="readonly")
        model_dropdown['values'] = ["Naive Baseline", "Linear Regression", "Random Forest"]
        model_dropdown.grid(row=0, column=3)

        ttk.Button(top_frame, text="Run", command=self.run_selected_model).grid(row=0, column=4, padx=10)

        ttk.Label(top_frame, text="Select Company:").grid(row=0, column=5, padx=10)
        self.company_var = tk.StringVar()
        company_dropdown = ttk.Combobox(top_frame, textvariable=self.company_var, state="readonly")
        company_dropdown['values'] = ["Chevron", "EOG Resources", "Occidental", "ConocoPhillips"]
        company_dropdown.grid(row=0, column=6)

        metric_frame = tk.Frame(self.root, bg="#f2f2f2")
        metric_frame.pack(pady=10)

        self.avg_label = self.create_metric_card(metric_frame, "Average Price", "$--", 0)
        self.high_label = self.create_metric_card(metric_frame, "Highest", "$--", 1)
        self.low_label = self.create_metric_card(metric_frame, "Lowest", "$--", 2)
        self.rmse_label = self.create_metric_card(metric_frame, "RMSE", "--", 3)
        self.mae_label = self.create_metric_card(metric_frame, "MAE", "--", 4)

        self.chart_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.chart_frame.pack(pady=10)

        self.volume_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.volume_frame.pack(pady=10)

        self.table_frame = tk.Frame(self.root, bg="#f2f2f2")
        self.table_frame.pack(pady=10)

    def create_metric_card(self, parent, title, value, col):
        frame = tk.LabelFrame(parent, text=title, padx=20, pady=10, bg="#ffffff", fg="#333333", font=("Segoe UI", 10, "bold"))
        frame.grid(row=0, column=col, padx=10)
        label = tk.Label(frame, text=value, font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#4caf50")
        label.pack()
        return label

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.df = self.controller.load_dataset(file_path)
            if self.df is not None:
                self.file_label.config(text=f"\U0001F4C1 {file_path.split('/')[-1]}")
                self.update_metric_cards()
            else:
                messagebox.showerror("Error", "Failed to load CSV file.")

    def update_metric_cards(self):
        price_col = self.get_price_col()
        if price_col:
            prices = self.df[price_col]
            self.avg_label.config(text=f"${prices.mean():.2f}")
            self.high_label.config(text=f"${prices.max():.2f}")
            self.low_label.config(text=f"${prices.min():.2f}")

    def get_price_col(self):
        for col in self.df.columns:
            if col.lower() in ['close', 'price']:
                return col
        return None

    def run_selected_model(self):
        model = self.model_var.get()
        if not model:
            messagebox.showwarning("Warning", "Select a model.")
            return

        if self.df is None:
            messagebox.showerror("Error", "Please upload a CSV first.")
            return

        if model == "Naive Baseline":
            rmse, mae, *_ = self.controller.run_baseline_model()
        elif model == "Linear Regression":
            rmse, mae, y_test, y_pred = self.controller.run_linear_regression_model()
            self.show_plot(y_test, y_pred)
        elif model == "Random Forest":
            rmse, mae, y_test, y_pred = self.controller.run_random_forest_model()
            self.show_plot(y_test, y_pred)
        else:
            messagebox.showerror("Model Error", "Model not recognized.")
            return

        self.rmse_label.config(text=f"{rmse:.2f}")
        self.mae_label.config(text=f"{mae:.2f}")

        self.show_volume_chart()

        comparison_data = [
            ("Chevron", 157.92, 3.92),
            ("EOG Resources", 567.19, 1.24),
            ("Occidental", 123.00, 0.84),
            ("Phillips 66", 441.10, -2.76),
        ]
        self.show_comparison_table(comparison_data)

    def show_plot(self, y_true, y_pred):
        if self.chart_canvas:
            self.chart_canvas.get_tk_widget().destroy()
        self.chart_canvas = plot_predictions(self.chart_frame, y_true, y_pred)

    def show_volume_chart(self):
        for widget in self.volume_frame.winfo_children():
            widget.destroy()

        if 'Date' in self.df.columns and 'Volume' in self.df.columns:
            dates = self.df['Date'].tail(30)
            volumes = self.df['Volume'].tail(30)
            self.volume_canvas = plot_volume_chart(self.volume_frame, dates, volumes)

    def show_comparison_table(self, data):
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        plot_comparison_table(self.table_frame, data)

if __name__ == "__main__":
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()
>>>>>>> Stashed changes
