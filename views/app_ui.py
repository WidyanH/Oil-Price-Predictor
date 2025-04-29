import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from controllers.prediction_controller import PredictionController
from utils.visualizations import plot_predictions, plot_volume_chart, plot_comparison_table
import pandas as pd


class AppUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Oil & Gas Price Dashboard")
        # Maximize the window automatically
        try:
            self.root.state('zoomed')  # Windows
        except:
            self.root.attributes('-fullscreen', True)  # Mac/Linux fallback

        self.root.configure(bg="#f2f2f2")

        self.controller = PredictionController()
        self.chart_canvas = None
        self.volume_canvas = None
        self.df = None
        self.pred_df = None
        self.forecast_df = None

        # Create scrollable canvas structure
        self.main_canvas = tk.Canvas(self.root, bg="#f2f2f2")

        self.scroll_y = ttk.Scrollbar(self.root, orient="vertical", command=self.main_canvas.yview)
        self.scrollable_frame = tk.Frame(self.main_canvas, bg="#f2f2f2")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
        )

        self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.main_canvas.configure(yscrollcommand=self.scroll_y.set)

        self.main_canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TButton",
                        font=("Segoe UI", 11),
                        padding=8,
                        relief="flat",
                        background="#1976D2",  # Blue
                        foreground="white")
        style.map("TButton",
                  background=[('active', '#1565C0')])

        style.configure("TLabel",
                        font=("Segoe UI", 11),
                        background="#f2f2f2")

        style.configure("TCombobox",
                        padding=8,
                        font=("Segoe UI", 11))

        self.create_widgets()

    def add_log(self, message, tag="info"):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')


    def create_widgets(self):
        # Title
        title = tk.Label(self.scrollable_frame, text="\U0001F6E2 Oil & Gas Stock Market Overview",
                         font=("Segoe UI", 32, "bold"), bg="#f2f2f2", fg="#003366")
        title.pack(pady=30)

        # Instructions Frame
        instructions_frame = tk.Frame(self.scrollable_frame, bg="#e7f0f7", bd=2, relief="ridge")
        instructions_frame.pack(padx=20, pady=(10, 20), fill="x")

        instructions_title = tk.Label(instructions_frame, text="📋 How to Use the Dashboard",
                                      font=("Segoe UI", 14, "bold"), bg="#e7f0f7", anchor="w")
        instructions_title.pack(fill="x", padx=10, pady=(5, 2))

        instructions_text = (
            "🔹 1. Upload your **Price Data CSV**:\n"
            "   - Required Columns: 'Date' and 'Close'.\n"
            "   - 'Close' refers to the closing stock or oil price for each day (the final price at market close).\n"
            "   - Optional but Recommended Columns: 'Open', 'High', 'Low', 'Volume', 'Symbol', 'Currency'.\n"
            "   - The 'Date' column must be in YYYY-MM-DD format (e.g., 2022-01-15).\n"
            "\n"
            "🔹 2. (Optional) Upload your **Inflation Data CSV**:\n"
            "   - Format: One row per year, with columns for each month ('Jan', 'Feb', ..., 'Dec').\n"
            "   - Example headers: 'Year', 'Jan', 'Feb', ..., 'Dec'.\n"
            "\n"
            "🔹 3. Select a **Prediction Model**:\n"
            "   - Options: Naive Baseline, Linear Regression, or Random Forest.\n"
            "\n"
            "🔹 4. Click **Run**:\n"
            "   - The dashboard will process the data, run the selected model, and generate predictions.\n"
            "\n"
            "🔹 5. View Results:\n"
            "   - Metrics: RMSE (Root Mean Squared Error), MAE (Mean Absolute Error), Accuracy (%).\n"
            "   - Charts: Predicted vs Actual Prices, Volume Trend Chart.\n"
            "   - Tables: 12-Month Price Forecast, Company Price Comparison.\n"
            "\n"
            "🔹 6. Export Files:\n"
            "   - Save the Predictions and Forecasts into CSV files for further analysis.\n"
            "\n"
            "🔹 7. Check the **Log Panel**:\n"
            "   - Displays all steps performed, model training summary, and final evaluation results."
        )

        instructions_label = tk.Label(instructions_frame, text=instructions_text, justify="left", font=("Segoe UI", 10),
                                      bg="#e7f0f7")
        instructions_label.pack(padx=10, pady=(0, 10))

        # What to Expect Section
        expectations_frame = tk.Frame(self.scrollable_frame, bg="#fdf6e3", bd=2, relief="ridge")
        expectations_frame.pack(padx=20, pady=(0, 20), fill="x")

        expectations_title = tk.Label(expectations_frame, text="🔍 What You Will See After Running the Model",
                                      font=("Segoe UI", 14, "bold"), bg="#fdf6e3", anchor="w")
        expectations_title.pack(fill="x", padx=10, pady=(5, 2))

        expectations_text = (
            "• Metrics: RMSE (Root Mean Squared Error), MAE (Mean Absolute Error), and Accuracy.\n"
            "• Graph 1: Actual vs Predicted Prices (Line Graph).\n"
            "• Graph 2: Recent Volume Trends (Bar Chart for last 30 days).\n"
            "• Forecast Table: Next 12 months' forecasted prices.\n"
            "• Company Comparison Table: Prices and % change of major oil companies.\n"
            "• Logs Panel: Full detailed logs of steps, metrics, and final summary.\n\n"
            "You can also export the Predictions and Forecasts as CSV files."
        )
        expectations_label = tk.Label(expectations_frame, text=expectations_text, justify="left", font=("Segoe UI", 10),
                                      bg="#fdf6e3")
        expectations_label.pack(padx=10, pady=(0, 10))

        # Top Controls
        top_frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
        top_frame.pack(pady=20, fill="x", padx=30)

        # === Log Section (After Top Frame, Before Metrics) ===
        log_frame = tk.LabelFrame(self.scrollable_frame, text="Logs and Calculations", bg="#f2f2f2",
                                  font=("Segoe UI", 14, "bold"))
        log_frame.pack(pady=10, fill="x", padx=30)

        self.log_text = tk.Text(log_frame, height=8, bg="#ffffff", fg="#333333", font=("Consolas", 11))
        self.log_text.pack(fill="both", expand=True)
        self.log_text.config(state='disabled')

        # Define different text tag colors
        self.log_text.tag_config("info", foreground="#333333")
        self.log_text.tag_config("success", foreground="#4caf50")
        self.log_text.tag_config("error", foreground="#e53935")
        self.log_text.tag_config("calculation", foreground="#3f51b5")



        top_frame.columnconfigure((0, 1, 2, 3, 4, 5, 6, 7), weight=1)

        # Upload Price Data
        ttk.Label(top_frame, text="Price Data 📈:", font=("Segoe UI", 13)).grid(row=0, column=0, sticky="e", padx=10,
                                                                               pady=10)
        ttk.Button(top_frame, text="Upload", command=self.upload_file).grid(row=0, column=1, sticky="w", padx=10,
                                                                            pady=10)

        # Upload Inflation Data
        ttk.Label(top_frame, text="Inflation Data 🌡️:", font=("Segoe UI", 13)).grid(row=0, column=2, sticky="e",
                                                                                    padx=10, pady=10)
        ttk.Button(top_frame, text="Upload", command=self.upload_inflation_file).grid(row=0, column=3, sticky="w",
                                                                                      padx=10, pady=10)

        # Select Model
        ttk.Label(top_frame, text="Model:", font=("Segoe UI", 13)).grid(row=1, column=0, sticky="e", padx=10, pady=10)
        self.model_var = tk.StringVar()
        model_dropdown = ttk.Combobox(top_frame, textvariable=self.model_var, state="readonly", font=("Segoe UI", 12))
        model_dropdown['values'] = ["Naive Baseline", "Linear Regression", "Random Forest"]
        model_dropdown.grid(row=1, column=1, sticky="ew", padx=10, pady=10)

        # Run Model
        run_button = ttk.Button(top_frame, text="Run Model 🚀", command=self.run_selected_model)
        run_button.grid(row=1, column=2, sticky="w", padx=10, pady=10)

        # Select Company
        ttk.Label(top_frame, text="Company:", font=("Segoe UI", 13)).grid(row=1, column=3, sticky="e", padx=10, pady=10)
        self.company_var = tk.StringVar()
        company_dropdown = ttk.Combobox(top_frame, textvariable=self.company_var, state="readonly",
                                        font=("Segoe UI", 12))
        company_dropdown['values'] = ["Chevron", "EOG Resources", "Occidental", "ConocoPhillips"]
        company_dropdown.grid(row=1, column=4, sticky="ew", padx=10, pady=10)

        # File Label
        self.file_label = tk.Label(self.scrollable_frame, text="No Price CSV Loaded", fg="gray",
                                   bg="#f2f2f2", font=("Segoe UI", 13))
        self.file_label.pack(pady=10)

        # Metric Cards
        metric_frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
        metric_frame.pack(pady=30, fill="x", padx=30)

        metric_frame.columnconfigure((0, 1, 2, 3, 4, 5), weight=1)

        self.avg_label = self.create_metric_card(metric_frame, "Average Price", "$--", 0)
        self.high_label = self.create_metric_card(metric_frame, "Highest Price", "$--", 1)
        self.low_label = self.create_metric_card(metric_frame, "Lowest Price", "$--", 2)
        self.rmse_label = self.create_metric_card(metric_frame, "RMSE", "--", 3)
        self.mae_label = self.create_metric_card(metric_frame, "MAE", "--", 4)
        self.acc_label = self.create_metric_card(metric_frame, "Accuracy", "--", 5)

        # Charts and Tables
        self.chart_frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
        self.chart_frame.pack(pady=30, fill="both", expand=True)

        self.volume_frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
        self.volume_frame.pack(pady=30, fill="both", expand=True)

        self.table_frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
        self.table_frame.pack(pady=30, fill="both", expand=True)

        # Prediction Export Frame
        pred_export_frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
        pred_export_frame.pack(pady=20)

        self.pred_table_frame = tk.Frame(pred_export_frame, bg="#f2f2f2")
        self.pred_table_frame.grid(row=0, column=0, padx=10)

        self.export_button = ttk.Button(pred_export_frame, text="Export Predictions to CSV",
                                        command=self.export_predictions)
        self.export_button.grid(row=0, column=1, padx=10, sticky='n')
        self.export_button.config(state='disabled')

        # Forecast Export Frame
        forecast_export_frame = tk.Frame(self.scrollable_frame, bg="#f2f2f2")
        forecast_export_frame.pack(pady=20)



        self.forecast_table_frame = tk.Frame(forecast_export_frame, bg="#f2f2f2")
        self.forecast_table_frame.grid(row=0, column=0, padx=10)

        self.export_forecast_button = ttk.Button(forecast_export_frame, text="Export Forecast to CSV",
                                                 command=self.export_forecast)
        self.export_forecast_button.grid(row=0, column=1, padx=10, sticky='n')
        self.export_forecast_button.config(state='disabled')

    def run_selected_model(self):
        model = self.model_var.get()
        if not model:
            messagebox.showwarning("Warning", "Select a model.")
            return

        if self.df is None:
            messagebox.showerror("Error", "Please upload a CSV first.")
            return

        self.add_log(f"🚀 Running model: {model}", "info")

        if model == "Naive Baseline":
            rmse, mae, y_test, y_pred = self.controller.run_baseline_model()
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

        if y_test is not None and y_pred is not None:
            self.show_predictions_table(y_test, y_pred)
            accuracy = 100.0 - (mae / y_test.mean() * 100)
            self.acc_label.config(text=f"{accuracy:.2f}%")
            self.export_button.config(state='normal')

            # Log calculation results
            self.add_log(f"🔵 Model Results:", "calculation")
            self.add_log(f"• RMSE: {rmse:.2f}", "calculation")
            self.add_log(f"• MAE: {mae:.2f}", "calculation")
            self.add_log(f"• Accuracy: {accuracy:.2f}%", "calculation")

            # 🔥 Full Final Summary block
            summary_lines = []
            summary_lines.append("\n🧾 Final Summary Report:")
            summary_lines.append(f"• Selected Model: {model}")
            summary_lines.append(f"• Uploaded Price Data: {self.file_label.cget('text')}")
            summary_lines.append(
                f"• Inflation Data Used: {'Yes' if self.controller.inflation_df is not None else 'No'}")
            summary_lines.append(f"• RMSE (Root Mean Squared Error): {rmse:.2f}")
            summary_lines.append(f"• MAE (Mean Absolute Error): {mae:.2f}")
            summary_lines.append(f"• Accuracy (estimated): {accuracy:.2f}%")

            # Optional comment based on accuracy
            if accuracy >= 90:
                summary_lines.append("• 📈 Excellent prediction accuracy! Your model fits the data very well.")
            elif accuracy >= 80:
                summary_lines.append(
                    "• 📈 Good prediction, but there is room for improvement (e.g., feature engineering).")
            else:
                summary_lines.append(
                    "• ⚠️ Prediction is weak. Consider adding more features, tuning model parameters, or using different models.")

            summary_lines.append("• Forecast for next 12 months generated successfully.")
            summary_lines.append("• Volume trend and company comparisons displayed.")

            for line in summary_lines:
                self.add_log(line, "calculation")

        self.show_forecast_table()
        self.show_volume_chart()
        self.show_comparison_table([
            ("Chevron", 157.92, 3.92),
            ("EOG Resources", 567.19, 1.24),
            ("Occidental", 123.00, 0.84),
            ("Phillips 66", 441.10, -2.76),
        ])

    def show_forecast_table(self):
        for widget in self.forecast_table_frame.winfo_children():
            widget.destroy()

        forecast_df = self.controller.forecast_next_months()
        self.forecast_df = forecast_df

        if forecast_df.empty:
            tk.Label(self.forecast_table_frame, text="No forecast available.", bg="#f2f2f2").pack()
            return

        self.export_forecast_button.config(state='normal')

        # Add title
        title = tk.Label(self.forecast_table_frame, text="🔮 Forecasted Prices (Next 12 Months)",
                         font=("Segoe UI", 16, "bold"), bg="#f2f2f2", anchor="w")
        title.pack(fill="x", padx=20, pady=(10, 5))

        table = ttk.Treeview(self.forecast_table_frame, columns=("Month", "Forecasted Price"), show="headings",
                             height=8)
        table.heading("Month", text="Month")
        table.heading("Forecasted Price", text="Forecasted Price")
        table.column("Month", width=200, anchor='center')
        table.column("Forecasted Price", width=200, anchor='center')

        table.pack(fill="x", padx=20, pady=10)

        for i in range(min(12, len(forecast_df))):
            row = forecast_df.iloc[i]
            table.insert('', tk.END, values=(row["Month"].strftime('%Y-%m-%d'), f"{row['Forecasted Price']:.2f}"))

    def create_metric_card(self, parent, title, value, col):
        frame = tk.Frame(parent, bg="#ffffff", bd=2, relief="ridge", padx=20, pady=20)
        frame.grid(row=0, column=col, padx=15, pady=10, sticky="nsew")

        # Title
        title_label = tk.Label(frame, text=title, font=("Segoe UI", 14, "bold"), bg="#ffffff", fg="#555555")
        title_label.pack(pady=(0, 10))

        # Value
        value_label = tk.Label(frame, text=value, font=("Segoe UI", 24, "bold"), bg="#ffffff", fg="#4caf50")
        value_label.pack()

        return value_label

    def upload_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.add_log(f"📂 Uploading price data: {file_path.split('/')[-1]}", "info")  # LOG BEFORE loading
            self.df = self.controller.load_dataset(file_path)
            if self.df is not None:
                self.file_label.config(text=f"\U0001F4C1 {file_path.split('/')[-1]}")
                self.update_metric_cards()
                self.add_log(f"✅ Price data loaded successfully.", "success")
            else:
                messagebox.showerror("Error", "Failed to load CSV file.")
                self.add_log(f"❌ Error: Failed to load price data.", "error")

    def upload_inflation_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if file_path:
            self.add_log(f"📂 Uploading inflation data: {file_path.split('/')[-1]}", "info")  # LOG BEFORE loading
            self.controller.load_inflation_data(file_path)
            messagebox.showinfo("Success", "Inflation data loaded.")
            self.add_log(f"✅ Inflation data loaded successfully.", "success")

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

        # Add title
        title = tk.Label(self.table_frame, text="🏢 Company Comparison Table", font=("Segoe UI", 16, "bold"),
                         bg="#f2f2f2", anchor="w")
        title.pack(fill="x", padx=20, pady=(10, 5))

        table = ttk.Treeview(self.table_frame, columns=("Company", "Price", "Change"), show="headings", height=8)
        table.heading("Company", text="Company")
        table.heading("Price", text="Price ($)")
        table.heading("Change", text="Change (%)")

        table.column("Company", width=200, anchor='center')
        table.column("Price", width=150, anchor='center')
        table.column("Change", width=150, anchor='center')

        table.pack(fill="x", padx=20, pady=10)

        for company, price, change in data:
            table.insert('', tk.END, values=(company, price, change))

    def show_predictions_table(self, y_true, y_pred):
        for widget in self.pred_table_frame.winfo_children():
            widget.destroy()

        # Add title above table
        title = tk.Label(self.pred_table_frame, text="📈 Predictions vs Actual", font=("Segoe UI", 16, "bold"),
                         bg="#f2f2f2", anchor="w")
        title.pack(fill="x", padx=20, pady=(10, 5))

        self.pred_df = pd.DataFrame({"Actual": y_true, "Predicted": y_pred})
        df = self.pred_df.round(2).reset_index(drop=True)

        table = ttk.Treeview(self.pred_table_frame, columns=("Actual", "Predicted"), show="headings", height=8)
        table.heading("Actual", text="Actual")
        table.heading("Predicted", text="Predicted")
        table.column("Actual", width=150, anchor='center')
        table.column("Predicted", width=150, anchor='center')

        table.pack(fill="x", padx=20, pady=10)

        for i in range(min(50, len(df))):
            table.insert('', tk.END, values=(df.loc[i, "Actual"], df.loc[i, "Predicted"]))

    def export_predictions(self):
        if self.pred_df is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                self.pred_df.to_csv(file_path, index=False)
                messagebox.showinfo("Export Complete", f"Predictions exported to {file_path}")

    def export_forecast(self):
        if self.forecast_df is not None and not self.forecast_df.empty:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
            if file_path:
                df_to_export = self.forecast_df.copy()
                df_to_export["Month"] = df_to_export["Month"].dt.strftime("%Y-%m-%d")
                df_to_export.to_csv(file_path, index=False)
                messagebox.showinfo("Export Complete", f"Forecast exported to {file_path}")


if __name__ == "__main__":
    root = tk.Tk()
    app = AppUI(root)
    root.mainloop()

