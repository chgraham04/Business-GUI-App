import tkinter as tk
from tkinter import ttk, messagebox
from utils import SQL

class PayrollManager:
    def __init__(self, window, db, back_callback, view_stack, bg_color='#a3b18a'):
        self.window = window
        self.db = db
        self.back_callback = back_callback
        self.view_stack = view_stack
        self.bg_color = bg_color

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def render_back_buttons(self):
        btn_frame = tk.Frame(self.window, bg=self.bg_color)
        btn_frame.pack(anchor='nw', padx=10, pady=10)

        back_btn = tk.Button(btn_frame, text='←', font=('Georgia', 16), bg='#800000', fg='white',
                             command=self.navigate_back)
        back_btn.pack(side='left')

        back_menu_btn = tk.Button(btn_frame, text="Back to Menu", command=self.back_callback,
                                  font=('Georgia', 10), bg="#800000", fg='white')
        back_menu_btn.pack(side='left', padx=5)

    def navigate_back(self):
        if self.view_stack:
            last_view = self.view_stack.pop()
            last_view()

    def payroll_menu(self):
        self.clear_window()
        self.render_back_buttons()
        tk.Label(self.window, text="Payroll Management", font=('Georgia', 20), bg=self.bg_color).pack(pady=20)

        tk.Button(self.window, text="Pay Employees", font=('Georgia', 14),
                  command=lambda: [self.view_stack.append(self.payroll_menu), self.pay_employees_placeholder()]).pack(pady=10)
        tk.Button(self.window, text="Browse Pay Periods", font=('Georgia', 14),
                  command=lambda: [self.view_stack.append(self.payroll_menu), self.browse_payroll_placeholder()]).pack(pady=10)
        tk.Button(self.window, text="Add Employee", font=('Georgia', 14),
                  command=lambda: [self.view_stack.append(self.payroll_menu), self.add_employee_placeholder()]).pack(pady=10)
        tk.Button(self.window, text="View Employee List", font=('Georgia', 14),
                  command=lambda: [self.view_stack.append(self.payroll_menu), self.view_employees_placeholder()]).pack(pady=10)
        tk.Button(self.window, text="Edit Employee Info", font=('Georgia', 14),
                  command=lambda: [self.view_stack.append(self.payroll_menu), self.edit_employees_placeholder()]).pack(pady=10)
        tk.Button(self.window, text="Back to Menu", font=('Georgia', 12), command=self.back_callback).pack(pady=20)

    def pay_employees_placeholder(self):
        messagebox.showinfo("Coming Soon", "Pay employees functionality will be implemented here.")

    def browse_payroll_placeholder(self):
        messagebox.showinfo("Coming Soon", "Browse pay periods functionality will be implemented here.")

    def add_employee_placeholder(self):
        messagebox.showinfo("Coming Soon", "Add employee functionality will be implemented here.")

    def view_employees_placeholder(self):
        messagebox.showinfo("Coming Soon", "View employees functionality will be implemented here.")

    def edit_employees_placeholder(self):
        messagebox.showinfo("Coming Soon", "Edit employee functionality will be implemented here.")
