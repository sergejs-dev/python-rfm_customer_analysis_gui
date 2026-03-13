import customtkinter as ctk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from exporters.excel_exporter import export_excel
from rfm_engine import load_data, calculate_rfm, create_segments
from exporters.pdf_exporter import export_pdf
import sys
import os

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)




ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class RFMApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("RFM Customer Analysis Tool")
        self.geometry("1000x950")

        try:
            self.iconbitmap(resource_path("assets/icon.ico"))
        except:
            pass

        self.df = None
        self.rfm = None
        self.selected_file = None

        self.setup_ui()

    def setup_ui(self):

        title = ctk.CTkLabel(
            self,
            text="RFM Customer Analysis Tool",
            font=("Arial", 28)
        )
        title.pack(pady=20)

        self.select_btn = ctk.CTkButton(
            self,
            text="Select Orders CSV",
            command=self.select_file
        )
        self.select_btn.pack(pady=10)

        self.run_btn = ctk.CTkButton(
            self,
            text="Run RFM Analysis",
            command=self.run_rfm
        )
        self.run_btn.pack(pady=10)

        self.log_box = ctk.CTkTextbox(self, height=150)
        self.log_box.pack(fill="x", padx=20, pady=20)

        self.export_excel_button = ctk.CTkButton(self,
        text="Export Excel Report",
        command=self.export_excel_report
)
        self.export_excel_button.pack(pady=5)


        self.export_pdf_btn = ctk.CTkButton(
        self,
        text="Export PDF Report",
        command=self.export_pdf_report
)
        self.export_pdf_btn.pack(pady=5)





        self.chart_frame = ctk.CTkFrame(self)
        self.chart_frame.pack(fill="both", expand=True, padx=20, pady=20)

    def log(self, message):

        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")

    def select_file(self):

        file_path = filedialog.askopenfilename(
            filetypes=[("CSV files", "*.csv")]
        )

        if file_path:
            self.selected_file = file_path
            self.log(f"CSV selected: {file_path}")

    def run_rfm(self):

        if not self.selected_file:
            self.log("Please select CSV file first.")
            return

        try:

            self.log("Loading data...")
            self.df = load_data(self.selected_file)

            self.log("Calculating RFM metrics...")
            self.rfm = calculate_rfm(self.df)

            self.log("Creating customer segments...")
            self.rfm = create_segments(self.rfm)
            self.segment_counts = self.rfm["Segment"].value_counts()

            self.log("RFM analysis completed.")

            self.show_chart()

        except Exception as e:
            self.log(f"Error: {e}")

    def show_chart(self):

        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        segment_counts = self.rfm["Segment"].value_counts()

        fig, ax = plt.subplots(figsize=(9,5))
        segment_counts.plot(kind="bar", ax=ax)

        ax.set_title("Customer Segments")
        ax.set_ylabel("Customers")
        ax.set_xlabel("Segment")
        plt.xticks(rotation=0)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def export_excel_report(self):

        if self.rfm is None:
            self.log("Please run RFM analysis first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Excel Report"
    )

        if not file_path:
            return

        try:

            export_excel(
                self.df,
                self.rfm,
                self.segment_counts,
                file_path
        )

            self.log(f"Excel report saved: {file_path}")

        except Exception as e:
            self.log(f"Excel export error: {e}")

    def export_pdf_report(self):

        if self.rfm is None:
            self.log("Please run RFM analysis first.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF Report"
        )

        if not file_path:
            return

        try:

            export_pdf(
                self.rfm,
                self.segment_counts,
                file_path
            )

            self.log(f"PDF report saved: {file_path}")

        except Exception as e:
            self.log(f"PDF export error: {e}")




if __name__ == "__main__":

    app = RFMApp()
    app.mainloop()