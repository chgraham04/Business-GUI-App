from tkinter import Frame, Canvas, Scrollbar, Label, Button, ttk
from datetime import datetime

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%m-%d-%Y')
        return True
    except ValueError:
        return False

def create_scrollable_frame(parent, bg_color='#a3b18a'):
    canvas = Canvas(parent, bg=bg_color, highlightthickness=0)
    scrollbar = Scrollbar(parent, orient="vertical", command=canvas.yview)
    scroll_frame = Frame(canvas, bg=bg_color)

    def _on_mousewheel(event):
        # For Windows
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        return "break"

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    scroll_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    window = canvas.create_window((0, 0), window=scroll_frame, anchor="n")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    return scroll_frame


def create_nav_buttons(window, back_callback, menu_callback):
    top_frame = Frame(window, bg=window['bg'])
    top_frame.pack(anchor='nw', pady=5, padx=5)

    back_arrow = Button(top_frame, text="⬅", font=("Arial", 18), bg="maroon", fg="white", width=2, command=back_callback)
    back_arrow.grid(row=0, column=0, padx=(0, 10))

    menu_button = Button(top_frame, text="Back to Menu", font=("Georgia", 12), bg="maroon", fg="white", command=menu_callback)
    menu_button.grid(row=1, column=0)


SQL = {
    # Orders
    "insert_order": "INSERT INTO Orders (date, vendor, total) VALUES (?, ?, ?)",
    "insert_order_detail": "INSERT INTO OrderDetails (order_id, flavor_id, quantity) VALUES (?, ?, ?)",
    "update_order_total": "UPDATE Orders SET total = ? WHERE order_id = ?",
    "get_unit_price": "SELECT unit_price FROM {table} WHERE flavor_id = ?",
    "get_orders_by_vendor": "SELECT order_id, date, total FROM Orders WHERE vendor = ? ORDER BY date DESC",
    "get_order_flavors": """
        SELECT od.flavor_id, f.name, od.quantity, f.unit_price
        FROM OrderDetails od
        JOIN {table} f ON od.flavor_id = f.flavor_id
        WHERE od.order_id = ?
        ORDER BY f.name ASC
    """,
    "get_order_total_quantity": """
        SELECT SUM(quantity) FROM OrderDetails WHERE order_id = ?
    """,
    "delete_order_details": "DELETE FROM OrderDetails WHERE order_id = ?",
    "delete_order": "DELETE FROM Orders WHERE order_id = ?",

    # Flavors
    "get_flavors": "SELECT flavor_id, name, unit_price, season FROM {table}",
    "get_flavors_sorted": "SELECT flavor_id, name, unit_price, season FROM {table} ORDER BY name ASC",
    "flavor_exists": "SELECT 1 FROM {table} WHERE flavor_id = ?",
    "add_flavor": "INSERT INTO {table} (flavor_id, name, type, unit_price, season) VALUES (?, ?, ?, ?, ?)",
    "delete_flavor": "DELETE FROM {table} WHERE flavor_id = ?",
    "update_flavor": "UPDATE {table} SET name = ?, unit_price = ?, season = ? WHERE flavor_id = ?",
    "insert_flavor": "INSERT INTO {table} (flavor_id, name, type, unit_price, season) VALUES (?, ?, ?, ?, ?)",

    # Employees
    "get_all_employees": "SELECT employee_id, f_name, l_name, wage FROM Employee ORDER BY employee_id",
    "insert_employee": "INSERT INTO Employee (f_name, l_name, wage) VALUES (?, ?, ?)",
    "update_employee": "UPDATE Employee SET f_name = ?, l_name = ?, wage = ? WHERE employee_id = ?",

    # Payroll
    "insert_payperiod": "INSERT INTO PayPeriods (employee_id, pay_period, hours_worked, overtime_hours, sick_hours) VALUES (?, ?, ?, ?, ?)",
    "update_summary": "INSERT OR REPLACE INTO PayrollSummary (pay_period, total_payout) VALUES (?, ?)",
    "get_summary": "SELECT pay_period, total_payout FROM PayrollSummary ORDER BY pay_period DESC"
}


