import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import uuid
from datetime import datetime

class HospitalManager:
    def __init__(self, root):  # Use double underscores here
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("1300x750")
        self.root.configure(bg="#e0e0e0")
        self.records = []
        self.medicines = ["Paracetamol", "Amoxicillin", "Ibuprofen", "Ciprofloxacin", "Aspirin"]
        self.precautions = [
            "Take rest and drink fluids",
            "Avoid strenuous activity",
            "Monitor blood pressure",
            "Maintain hygiene",
            "Follow dietary restrictions",
            "Report any unusual symptoms"
        ]
        self.load_records()
        self.create_widgets()


    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.LabelFrame(main_frame, text="Add Patient Record", padding="10")
        input_frame.grid(column=0, row=0, padx=20, pady=20)

        ttk.Label(input_frame, text="Patient Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.name_entry = ttk.Entry(input_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Medicine:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.medicine_var = tk.StringVar()
        self.medicine_combo = ttk.Combobox(input_frame, textvariable=self.medicine_var, values=self.medicines, state="readonly", width=38)
        self.medicine_combo.grid(row=1, column=1, padx=5, pady=5)
        self.medicine_combo.current(0)

        ttk.Label(input_frame, text="Date Admitted (DD-MM-YYYY):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.admit_entry = ttk.Entry(input_frame, width=40)
        self.admit_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Date of Discharge (DD-MM-YYYY):").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.discharge_entry = ttk.Entry(input_frame, width=40)
        self.discharge_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Precautions:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.precaution_var = tk.StringVar()
        self.precaution_combo = ttk.Combobox(input_frame, textvariable=self.precaution_var, values=self.precautions, state="readonly", width=38)
        self.precaution_combo.grid(row=4, column=1, padx=5, pady=5)
        self.precaution_combo.current(0)

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=5, column=0, columnspan=2, pady=15)

        add_button = ttk.Button(button_frame, text="Add Record", command=self.add_record)
        add_button.pack(side=tk.LEFT, padx=5)

        delete_button = ttk.Button(button_frame, text="Delete Selected", command=self.delete_record)
        delete_button.pack(side=tk.LEFT, padx=5)

        list_frame = ttk.LabelFrame(main_frame, text="Patient Records", padding="10")
        list_frame.grid(column=0, row=1, padx=20, pady=10, sticky="nsew")

        columns = ("Patient Name", "Medicine", "Date Admitted", "Date of Discharge", "Precautions")
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode="extended", height=20)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor=tk.CENTER, width=180)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        vertical_scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=vertical_scrollbar.set)
        vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        horizontal_scrollbar = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(xscroll=horizontal_scrollbar.set)
        horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.populate_tree()

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

    def add_record(self):
        name = self.name_entry.get().strip()
        medicine = self.medicine_var.get()
        admit_date = self.admit_entry.get().strip()
        discharge_date = self.discharge_entry.get().strip()
        precaution = self.precaution_var.get()

        if not all([name, medicine, admit_date, discharge_date, precaution]):
            messagebox.showerror("Invalid input", "Please fill all fields.")
            return

        if not self.validate_date(admit_date):
            messagebox.showerror("Invalid Date", "Date Admitted is not in DD-MM-YYYY format or is invalid.")
            return
        if not self.validate_date(discharge_date):
            messagebox.showerror("Invalid Date", "Date of Discharge is not in DD-MM-YYYY format or is invalid.")
            return

        admit_dt = datetime.strptime(admit_date, "%d-%m-%Y")
        discharge_dt = datetime.strptime(discharge_date, "%d-%m-%Y")
        if discharge_dt < admit_dt:
            messagebox.showerror("Invalid Dates", "Date of Discharge cannot be earlier than Date Admitted.")
            return

        record_id = str(uuid.uuid4())

        record = {
            "id": record_id,
            "name": name,
            "medicine": medicine,
            "admit_date": admit_date,
            "discharge_date": discharge_date,
            "precaution": precaution
        }
        self.records.append(record)
        self.save_records()
        self.tree.insert("", tk.END, iid=record_id, values=(name, medicine, admit_date, discharge_date, precaution))
        self.clear_entries()
        messagebox.showinfo("Success", "Record added successfully.")

    def clear_entries(self):
        self.name_entry.delete(0, tk.END)
        self.admit_entry.delete(0, tk.END)
        self.discharge_entry.delete(0, tk.END)
        self.medicine_combo.current(0)
        self.precaution_combo.current(0)

    def validate_date(self, date_text):
        try:
            datetime.strptime(date_text, "%d-%m-%Y")
            return True
        except ValueError:
            return False

    def populate_tree(self):
        self.tree.delete(*self.tree.get_children())
        for record in self.records:
            name = record.get("name", "N/A")
            medicine = record.get("medicine", "N/A")
            admit_date = record.get("admit_date", "N/A")
            discharge_date = record.get("discharge_date", "N/A")
            precaution = record.get("precaution", "N/A")

            self.tree.insert("", tk.END, iid=record["id"], values=(name, medicine, admit_date, discharge_date, precaution))

    def delete_record(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("No selection", "Please select at least one record to delete.")
            return

        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete the selected record(s)?")
        if confirm:
            for item in selected_items:
                self.tree.delete(item)
                self.records = [record for record in self.records if record["id"] != item]
            self.save_records()
            messagebox.showinfo("Success", "Selected record(s) deleted successfully.")

    def save_records(self):
        with open("patient_records.json", "w") as f:
            json.dump(self.records, f)

    def load_records(self):
        if os.path.exists("patient_records.json"):
            with open("patient_records.json", "r") as f:
                self.records = json.load(f)

root = tk.Tk()
app = HospitalManager(root)
root.mainloop()