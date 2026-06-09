# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:25:50 2026

@author: Brian Green
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import os
import subprocess
import platform
import sys


class GradeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Grade Editor")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Handle window close button (X)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Internal data
        self.df = None
        self.file_path = None
        self.selected_column = None
        self.is_percentage = True
        self.updates_log = []
        
        # Name columns
        self.surname_col = None
        self.initials_col = None
        
        self.create_widgets()
        self.update_ui_state()
    
    def on_closing(self):
        """Called when user clicks the X button."""
        if messagebox.askokcancel("Quit", "Do you want to quit the application?"):
            self.root.quit()
            self.root.destroy()
            sys.exit(0)
    
    def create_widgets(self):
        # Main container with scrolling
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # --- File selection ---
        file_frame = ttk.LabelFrame(scrollable_frame, text="Load Excel File", padding=10)
        file_frame.pack(fill="x", padx=5, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.pack(side="left", fill="x", expand=True)
        
        self.load_btn = ttk.Button(file_frame, text="Browse...", command=self.load_excel)
        self.load_btn.pack(side="right", padx=5)
        
        # --- Column selection ---
        col_frame = ttk.LabelFrame(scrollable_frame, text="Choose Column to Edit", padding=10)
        col_frame.pack(fill="x", padx=5, pady=5)
        
        self.column_var = tk.StringVar()
        self.column_combo = ttk.Combobox(col_frame, textvariable=self.column_var, state="disabled", width=50)
        self.column_combo.pack(fill="x", padx=5, pady=5)
        self.column_combo.bind("<<ComboboxSelected>>", self.on_column_selected)
        
        # --- Mark type ---
        type_frame = ttk.LabelFrame(scrollable_frame, text="Mark Type", padding=10)
        type_frame.pack(fill="x", padx=5, pady=5)
        
        self.percentage_var = tk.BooleanVar(value=True)
        ttk.Radiobutton(type_frame, text="Marks are already percentages",
                        variable=self.percentage_var, value=True,
                        command=self.on_mark_type_changed).pack(anchor="w")
        ttk.Radiobutton(type_frame, text="Raw score (convert to percentage)",
                        variable=self.percentage_var, value=False,
                        command=self.on_mark_type_changed).pack(anchor="w")
        
        self.total_frame = ttk.Frame(type_frame)
        self.total_label = ttk.Label(self.total_frame, text="Test was out of:")
        self.total_label.pack(side="left", padx=(0, 5))
        self.total_entry = ttk.Entry(self.total_frame, width=10)
        self.total_entry.pack(side="left")
        self.total_entry.insert(0, "100")
        
        # --- Data entry ---
        entry_frame = ttk.LabelFrame(scrollable_frame, text="Enter Student Data", padding=10)
        entry_frame.pack(fill="x", padx=5, pady=5)
        
        # Student number
        ttk.Label(entry_frame, text="Student Number:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.student_entry = ttk.Entry(entry_frame, width=40)
        self.student_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        # NEW: Press Enter moves focus to mark field
        self.student_entry.bind("<Return>", lambda event: self.mark_entry.focus())
        
        # Mark
        ttk.Label(entry_frame, text="Mark/Score:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.mark_entry = ttk.Entry(entry_frame, width=40)
        self.mark_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        # NEW: Press Enter triggers update
        self.mark_entry.bind("<Return>", lambda event: self.add_update_student())
        
        self.add_btn = ttk.Button(entry_frame, text="Add / Update Student", command=self.add_update_student)
        self.add_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # --- Log ---
        log_frame = ttk.LabelFrame(scrollable_frame, text="Updates Made (this session)", padding=10)
        log_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        log_text_frame = ttk.Frame(log_frame)
        log_text_frame.pack(fill="both", expand=True)
        
        self.log_text = tk.Text(log_text_frame, height=10, wrap="word", state="disabled")
        log_scrollbar = ttk.Scrollbar(log_text_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # --- Action buttons ---
        action_frame = ttk.Frame(scrollable_frame)
        action_frame.pack(fill="x", padx=5, pady=10)
        
        self.done_btn = ttk.Button(
            action_frame, 
            text="✅ DONE - Export to Excel & CSV", 
            command=self.export_files,
            width=30
        )
        self.done_btn.pack(side="left", padx=5)
        
        self.clear_btn = ttk.Button(
            action_frame,
            text="🗑 Clear Log",
            command=self.clear_log,
            width=15
        )
        self.clear_btn.pack(side="left", padx=5)
        
        self.quit_btn = ttk.Button(
            action_frame, 
            text="Quit", 
            command=self.on_closing,
            width=10
        )
        self.quit_btn.pack(side="right", padx=5)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Status bar
        self.status_var = tk.StringVar(value="Ready. Please load an Excel file.")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief="sunken", anchor="w")
        status_bar.pack(side="bottom", fill="x")
        
        entry_frame.columnconfigure(1, weight=1)
    
    def clear_log(self):
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")
        self.updates_log.clear()
        self.status_var.set("Log cleared")
    
    def update_ui_state(self):
        loaded = self.df is not None
        state = "normal" if loaded else "disabled"
        self.column_combo.config(state="readonly" if loaded else "disabled")
        self.add_btn.config(state=state)
        self.done_btn.config(state=state)
        self.student_entry.config(state="normal" if loaded else "disabled")
        self.mark_entry.config(state="normal" if loaded else "disabled")
        if not loaded:
            self.column_combo.set("")
            self.column_var.set("")
    
    def on_mark_type_changed(self):
        if self.percentage_var.get():
            self.total_frame.pack_forget()
            self.is_percentage = True
        else:
            self.total_frame.pack(anchor="w", pady=(10, 0))
            self.is_percentage = False
    
    def detect_name_columns(self):
        surname_candidates = ["surname", "lastname", "last name", "family name"]
        given_candidates = ["initials", "firstname", "first name", "given name", "name"]
        col_lower = {col.lower(): col for col in self.df.columns}
        self.surname_col = None
        self.initials_col = None
        for cand in surname_candidates:
            if cand in col_lower:
                self.surname_col = col_lower[cand]
                break
        for cand in given_candidates:
            if cand in col_lower:
                self.initials_col = col_lower[cand]
                break
    
    def load_excel(self):
        file_path = filedialog.askopenfilename(
            title="Select Excel file",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if not file_path:
            return
        try:
            self.df = pd.read_excel(file_path)
            self.file_path = file_path
            self.status_var.set(f"Loaded: {os.path.basename(file_path)}")
            if 'Username' not in self.df.columns:
                messagebox.showerror("Missing Column", "The Excel file must contain a 'Username' column (email addresses).")
                self.df = None
                self.update_ui_state()
                return
            self.detect_name_columns()
            self.file_label.config(text=file_path, foreground="black")
            columns = list(self.df.columns)
            self.column_combo['values'] = columns
            self.column_combo.set("")
            self.column_var.set("")
            self.selected_column = None
            self.clear_log()
            self.update_ui_state()
            self.status_var.set(f"Loaded {len(self.df)} students. Select a column to edit.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load Excel file:\n{str(e)}")
            self.df = None
            self.update_ui_state()
    
    def on_column_selected(self, event=None):
        self.selected_column = self.column_var.get()
        if self.selected_column:
            self.status_var.set(f"Editing column: '{self.selected_column}'")
    
    def get_student_name_info(self, row_index):
        info_parts = []
        if self.surname_col and self.surname_col in self.df.columns:
            surname = self.df.iloc[row_index][self.surname_col]
            if pd.notna(surname):
                info_parts.append(str(surname).strip())
        if self.initials_col and self.initials_col in self.df.columns:
            name = self.df.iloc[row_index][self.initials_col]
            if pd.notna(name):
                info_parts.append(str(name).strip())
        if info_parts:
            return " (" + " ".join(info_parts) + ")"
        return ""
    
    def add_update_student(self):
        if self.df is None:
            messagebox.showwarning("No file", "Please load an Excel file first.")
            return
        if not self.selected_column:
            messagebox.showwarning("No column", "Please select a column to edit.")
            return
        student_num = self.student_entry.get().strip()
        if not student_num:
            messagebox.showwarning("Missing data", "Please enter a student number.")
            return
        email = f"{student_num}@tut4life.ac.za"
        mark_str = self.mark_entry.get().strip()
        if not mark_str:
            messagebox.showwarning("Missing data", "Please enter a mark/score.")
            return
        try:
            mark_value = float(mark_str)
        except ValueError:
            messagebox.showerror("Invalid number", f"'{mark_str}' is not a valid number.")
            return
        if self.is_percentage:
            percentage = mark_value
        else:
            try:
                total = float(self.total_entry.get().strip())
                if total <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Invalid total", "Please enter a positive number for 'out of' total.")
                return
            percentage = (mark_value / total) * 100
        percentage = max(0, min(100, percentage))
        mask = self.df['Username'] == email
        if not mask.any():
            messagebox.showerror("Student not found", f"No student with email '{email}'.\nCheck that the student number is correct.")
            return
        row_index = mask.idxmax()
        name_info = self.get_student_name_info(row_index)
        current_mark = self.df.loc[mask, self.selected_column].values[0]
        if pd.isna(current_mark):
            current_mark_str = "empty"
        else:
            current_mark_str = f"{current_mark:.2f}%" if isinstance(current_mark, (int, float)) else str(current_mark)
        self.df.loc[mask, self.selected_column] = percentage
        log_msg = (f"✓ Student: {student_num}{name_info}\n"
                   f"   Email: {email}\n"
                   f"   Old {self.selected_column}: {current_mark_str}\n"
                   f"   New {self.selected_column}: {percentage:.2f}%\n"
                   f"{'  (Entered as percentage)' if self.is_percentage else f'  (Converted from {mark_value} out of {self.total_entry.get()})'}\n"
                   f"{'-'*50}\n")
        self.updates_log.append(log_msg)
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, log_msg)
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")
        self.status_var.set(f"Updated {student_num}{name_info} → {percentage:.2f}%")
        self.student_entry.delete(0, tk.END)
        self.mark_entry.delete(0, tk.END)
        self.student_entry.focus()
    
    def export_files(self):
        if self.df is None:
            messagebox.showwarning("No file", "No data to export.")
            return
        if not self.updates_log:
            reply = messagebox.askyesno("No changes", "No updates were made. Do you still want to export the current file?")
            if not reply:
                return
        output_dir = filedialog.askdirectory(title="SELECT OUTPUT FOLDER for Excel and CSV files")
        if not output_dir:
            return
        if self.file_path:
            base_name = os.path.splitext(os.path.basename(self.file_path))[0]
        else:
            base_name = "grades_updated"
        excel_path = os.path.join(output_dir, f"{base_name}_updated.xlsx")
        csv_path = os.path.join(output_dir, f"{base_name}_updated.csv")
        try:
            self.df.to_excel(excel_path, index=False)
            self.df.to_csv(csv_path, index=False)
            result = messagebox.askyesno(
                "✅ EXPORT SUCCESSFUL!",
                f"Files saved successfully:\n\n"
                f"📊 Excel: {excel_path}\n"
                f"📄 CSV:   {csv_path}\n\n"
                f"Total updates in this session: {len(self.updates_log)}\n\n"
                f"Do you want to OPEN THE FOLDER containing these files?",
                icon="info"
            )
            if result:
                if platform.system() == "Windows":
                    os.startfile(output_dir)
                elif platform.system() == "Darwin":
                    subprocess.run(["open", output_dir])
                else:
                    subprocess.run(["xdg-open", output_dir])
            self.status_var.set(f"✓ Exported to {output_dir}")
            # FIXED: Properly handle continue/quit
            continue_editing = messagebox.askyesno(
                "Continue?",
                "Files exported successfully!\n\nDo you want to continue editing? (Click No to quit)"
            )
            if not continue_editing:
                self.on_closing()  # Call the proper quit method
        except Exception as e:
            messagebox.showerror("Export error", f"Failed to save files:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = GradeEditorApp(root)
    root.mainloop()