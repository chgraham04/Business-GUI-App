import tkinter as tk
from tkinter import ttk, messagebox
from database import DatabaseManager
from order_manager import OrderManager
from flavor_manager import FlavorManager
# from payroll_manager import PayrollManager  # Uncomment if/when ready

class TPCApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("TPC App")
        self.window.geometry("1100x925")
        self.bg_color = "#a3b18a"
        self.window.configure(bg=self.bg_color)

        self.db = DatabaseManager()
        self.view_stack = []

        self.order_manager = OrderManager(
            self.window, self.db, self.show_main_menu, self.view_stack, self.bg_color
        )
        self.flavor_manager = FlavorManager(
            self.window, self.db, self.show_main_menu, self.view_stack, self.bg_color
        )
        # self.payroll_manager = PayrollManager(
        #     self.window, self.db, self.show_main_menu, self.view_stack, self.bg_color
        # )

        self.setup_styles()
        self.show_main_menu()
        self.window.mainloop()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TPC_button.TButton', font=('Georgia', 14), foreground='black', background="#ADADAD", padx=10)

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_window()
        tk.Label(self.window, text='TPC Master Application', font=('Georgia', 24), bg=self.bg_color).pack(pady=(10, 50))

        tk.Label(self.window, text='Inventory Management', font=('Georgia', 16, 'bold'), bg=self.bg_color).pack()
        inventory_menu = tk.Frame(self.window, bg=self.bg_color)
        inventory_menu.pack(pady=10)

        ttk.Button(
            inventory_menu, text='Place Order',
            command=self.order_manager.place_order,
            style='TPC_button.TButton'
        ).pack(side=tk.LEFT, padx=10)
        ttk.Button(inventory_menu, text='Review Old Orders', command=self.order_manager.review_orders, style='TPC_button.TButton').pack(side=tk.LEFT, padx=10)

        ttk.Button(
            inventory_menu, text='Manage Flavors',
            command=self.flavor_manager.manage_flavors_menu,
            style='TPC_button.TButton'
        ).pack(side=tk.LEFT, padx=10)

        tk.Label(self.window, text='Manage Payroll', font=('Georgia', 16, 'bold'), bg=self.bg_color).pack(pady=(40, 10))
        payroll_menu = tk.Frame(self.window, bg=self.bg_color)
        payroll_menu.pack(pady=10)

        ttk.Button(
            payroll_menu, text='Pay Employees',
            command=self.placeholder, style='TPC_button.TButton'
        ).pack(side=tk.LEFT, padx=10)
        ttk.Button(
            payroll_menu, text='Browse Pay Periods',
            command=self.placeholder, style='TPC_button.TButton'
        ).pack(side=tk.LEFT, padx=10)
        ttk.Button(
            payroll_menu, text='Add Employee',
            command=self.placeholder, style='TPC_button.TButton'
        ).pack(side=tk.LEFT, padx=10)
        ttk.Button(
            payroll_menu, text='View Employee List',
            command=self.placeholder, style='TPC_button.TButton'
        ).pack(side=tk.LEFT, padx=10)
        ttk.Button(
            payroll_menu, text='Edit Employee Info',
            command=self.placeholder, style='TPC_button.TButton'
        ).pack(side=tk.LEFT, padx=10)

    def placeholder(self):
        messagebox.showinfo("Under Construction", "This feature is being refactored.")

if __name__ == "__main__":
    TPCApp()
