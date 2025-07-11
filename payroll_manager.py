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

    def add_employee(self):
        self.clear_window()
        self.render_back_buttons()

        tk.Label(self.window, text="Add New Employee", font=('Georgia', 20), bg=self.bg_color).pack(pady=20)

        frame = tk.Frame(self.window, bg=self.bg_color)
        frame.pack(pady=20)

        # First Name
        tk.Label(frame, text="First Name:", font=('Georgia', 14), bg=self.bg_color).grid(row=0, column=0, sticky='e', pady=5)
        f_name_entry = tk.Entry(frame, font=('Georgia', 12))
        f_name_entry.grid(row=0, column=1, pady=5)

        # Last Name
        tk.Label(frame, text="Last Name:", font=('Georgia', 14), bg=self.bg_color).grid(row=1, column=0, sticky='e', pady=5)
        l_name_entry = tk.Entry(frame, font=('Georgia', 12))
        l_name_entry.grid(row=1, column=1, pady=5)

        # Wage
        tk.Label(frame, text="Hourly Wage:", font=('Georgia', 14), bg=self.bg_color).grid(row=2, column=0, sticky='e', pady=5)
        wage_entry = tk.Entry(frame, font=('Georgia', 12))
        wage_entry.grid(row=2, column=1, pady=5)

        # Shift Priority
        tk.Label(frame, text="Shift Priority (1–5):", font=('Georgia', 14), bg=self.bg_color).grid(row=3, column=0, sticky='e', pady=5)
        shift_priority_entry = tk.Entry(frame, font=('Georgia', 12))
        shift_priority_entry.grid(row=3, column=1, pady=5)

        # Strength
        tk.Label(frame, text="Strength (1–10):", font=('Georgia', 14), bg=self.bg_color).grid(row=4, column=0, sticky='e', pady=5)
        strength_entry = tk.Entry(frame, font=('Georgia', 12))
        strength_entry.grid(row=4, column=1, pady=5)

        # Desired Weekly Shifts
        tk.Label(frame, text="Desired Weekly Shifts:", font=('Georgia', 14), bg=self.bg_color).grid(row=5, column=0, sticky='e', pady=5)
        weekly_shifts_entry = tk.Entry(frame, font=('Georgia', 12))
        weekly_shifts_entry.grid(row=5, column=1, pady=5)

        # Senior Server
        is_senior_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Senior Server?", variable=is_senior_var, bg=self.bg_color)\
            .grid(row=6, column=0, columnspan=2, sticky='w', pady=5)

        # Double Shift Eligible
        double_eligible_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Double Shift Eligible?", variable=double_eligible_var, bg=self.bg_color)\
            .grid(row=7, column=0, columnspan=2, sticky='w', pady=5)

        # Preferred Shift
        tk.Label(frame, text="Preferred Shift:", font=('Georgia', 14), bg=self.bg_color).grid(row=8, column=0, sticky='e', pady=5)
        preferred_shift_var = tk.StringVar(value='day')
        ttk.Combobox(frame, textvariable=preferred_shift_var, values=['day', 'night'], state='readonly').grid(row=8, column=1, pady=5)

        # Error label
        err_label = tk.Label(frame, text="", font=('Georgia', 10), fg="red", bg=self.bg_color)
        err_label.grid(row=9, column=0, columnspan=2)

        def submit():
            # Grab & validate inputs
            f_name = f_name_entry.get().strip()
            l_name = l_name_entry.get().strip()
            try:
                wage = float(wage_entry.get().strip())
                shift_priority = int(shift_priority_entry.get().strip())
                strength = int(strength_entry.get().strip())
                weekly_shifts = int(weekly_shifts_entry.get().strip())
            except Exception:
                err_label.config(text="Please enter valid numeric values.")
                return

            if not f_name or not l_name:
                err_label.config(text="First and last name required.")
                return
            if not (1 <= shift_priority <= 5):
                err_label.config(text="Shift Priority must be 1–5.")
                return
            if not (1 <= strength <= 10):
                err_label.config(text="Strength must be 1–10.")
                return
            if wage <= 0 or weekly_shifts <= 0:
                err_label.config(text="Wage and weekly shifts must be positive.")
                return

            # Insert into DB
            self.db.execute(
                SQL["insert_employee"],
                (
                    f_name,
                    l_name,
                    wage,
                    shift_priority,
                    strength,
                    weekly_shifts,
                    int(is_senior_var.get()),
                    int(double_eligible_var.get()),
                    preferred_shift_var.get()
                )
            )
            messagebox.showinfo("Success", f"Employee {f_name} {l_name} added.")
            self.payroll_menu()

        tk.Button(frame, text="Add Employee", font=('Georgia', 14), command=submit)\
            .grid(row=10, column=0, columnspan=2, pady=20)

    from utils import SQL  # make sure this is imported at the top

    def employee_info(self):
        self.clear_window()
        self.render_back_buttons()

        tk.Label(self.window, text="Employee Info", font=('Georgia', 20), bg=self.bg_color).pack(pady=20)

        columns = [
            ("First Name", "f_name"),
            ("Last Name", "l_name"),
            ("Wage", "wage"),
            ("Shift Priority", "shift_priority"),
            ("Strength", "strength"),
            ("Desired Shifts", "desired_weekly_shifts"),
            ("Senior", "is_senior"),
            ("Double Eligible", "double_eligible"),
            ("Preferred Shift", "preferred_shift")
        ]

        table_frame = tk.Frame(self.window, bg=self.bg_color)
        table_frame.pack(pady=10)

        for col, (label, _) in enumerate(columns):
            tk.Label(table_frame, text=label, font=('Georgia', 12, 'bold'), bg=self.bg_color).grid(row=0, column=col, padx=3, pady=4)
        tk.Label(table_frame, text="", bg=self.bg_color).grid(row=0, column=len(columns), padx=10)

        employees = self.db.fetch(SQL["get_all_employees"])
        for row_idx, (emp_id, f_name, l_name, wage, shift_priority, strength, desired, is_senior, double_eligible, preferred_shift) in enumerate(employees, 1):
            f_name_var = tk.StringVar(value=f_name)
            l_name_var = tk.StringVar(value=l_name)
            wage_var = tk.StringVar(value=f"{wage:.2f}")
            shift_priority_var = tk.StringVar(value=str(shift_priority))
            strength_var = tk.StringVar(value=str(strength))
            desired_var = tk.StringVar(value=str(desired))
            is_senior_var = tk.BooleanVar(value=bool(is_senior))
            double_eligible_var = tk.BooleanVar(value=bool(double_eligible))
            preferred_shift_var = tk.StringVar(value=preferred_shift)

            vars_list = [
                f_name_var, l_name_var, wage_var,
                shift_priority_var, strength_var, desired_var,
                is_senior_var, double_eligible_var, preferred_shift_var
            ]

            tk.Entry(table_frame, textvariable=f_name_var, width=12).grid(row=row_idx, column=0, padx=3, pady=2)
            tk.Entry(table_frame, textvariable=l_name_var, width=12).grid(row=row_idx, column=1, padx=3, pady=2)
            wage_frame = tk.Frame(table_frame, bg=self.bg_color)
            wage_frame.grid(row=row_idx, column=2, padx=3, pady=2, sticky='w')
            tk.Label(wage_frame, text="$", font=('Georgia', 12), bg=self.bg_color).pack(side='left')
            tk.Entry(wage_frame, textvariable=wage_var, width=8, justify='right').pack(side='left')

            tk.Entry(table_frame, textvariable=shift_priority_var, width=7, justify='center').grid(row=row_idx, column=3, padx=3)
            tk.Entry(table_frame, textvariable=strength_var, width=7, justify='center').grid(row=row_idx, column=4, padx=3)
            tk.Entry(table_frame, textvariable=desired_var, width=9, justify='center').grid(row=row_idx, column=5, padx=3)
            tk.Checkbutton(table_frame, variable=is_senior_var, bg=self.bg_color).grid(row=row_idx, column=6)
            tk.Checkbutton(table_frame, variable=double_eligible_var, bg=self.bg_color).grid(row=row_idx, column=7)
            ttk.Combobox(table_frame, textvariable=preferred_shift_var, values=['day', 'night'], state='readonly', width=8).grid(row=row_idx, column=8, padx=2)

            def make_save_fn(emp_id, vlist):
                def save():
                    try:
                        wage_val = float(vlist[2].get())
                        shift_priority_val = int(vlist[3].get())
                        strength_val = int(vlist[4].get())
                        desired_val = int(vlist[5].get())
                        if not (1 <= shift_priority_val <= 5):
                            raise ValueError("Shift Priority must be 1-5")
                        if not (1 <= strength_val <= 10):
                            raise ValueError("Strength must be 1-10")
                    except Exception:
                        messagebox.showerror("Invalid Input", "Check numeric values and required ranges.")
                        return
                    self.db.execute(
                        SQL["update_employee"],
                        (
                            vlist[0].get().strip(),
                            vlist[1].get().strip(),
                            wage_val,
                            shift_priority_val,
                            strength_val,
                            desired_val,
                            int(vlist[6].get()),
                            int(vlist[7].get()),
                            vlist[8].get(),
                            emp_id
                        )
                    )
                    messagebox.showinfo("Saved", "Employee updated.")
                return save

            tk.Button(table_frame, text="Save", bg="green", fg="white", width=5, command=make_save_fn(emp_id, vars_list)).grid(row=row_idx, column=9, padx=5)

            def make_delete_fn(emp_id):
                def delete():
                    if messagebox.askyesno("Delete Employee", "Are you sure?"):
                        self.db.execute(SQL["delete_employee"], (emp_id,))
                        self.employee_info()  # Refresh
                return delete

            tk.Button(table_frame, text="❌", bg="red", fg="white", width=3, command=make_delete_fn(emp_id)).grid(row=row_idx, column=10, padx=5)


    def pay_employees_placeholder(self):
        messagebox.showinfo("Coming Soon", "Pay employees functionality will be implemented here.")

    def browse_payroll_placeholder(self):
        messagebox.showinfo("Coming Soon", "Browse pay periods functionality will be implemented here.")

    def view_employees_placeholder(self):
        messagebox.showinfo("Coming Soon", "View employees functionality will be implemented here.")

    def edit_employees_placeholder(self):
        messagebox.showinfo("Coming Soon", "Edit employee functionality will be implemented here.")
