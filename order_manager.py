import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from utils import SQL, is_valid_date, create_scrollable_frame

class OrderManager:
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

        back_btn = tk.Button(
            btn_frame, text='←', font=('Georgia', 16), bg='#800000', fg='white',
            command=self.navigate_back)
        back_btn.pack(side='left')

        back_menu_btn = tk.Button(
            btn_frame, text="Back to Menu", command=self.back_callback,
            font=('Georgia', 10), bg="#800000", fg='white')
        back_menu_btn.pack(side='left', padx=5)

    def navigate_back(self):
        if self.view_stack:
            last_view = self.view_stack.pop()
            last_view()

    def place_order(self):
        self.clear_window()
        self.render_back_buttons()
        tk.Label(self.window, text="Select Vendor", font=('Georgia', 20), bg=self.bg_color).pack(pady=(10, 30))

        center = tk.Frame(self.window, bg=self.bg_color)
        center.pack(pady=40)

        vendors = [
            ("Warwick", "WarwickFlavors"),
            ("Crescent Ridge", "CrescentFlavors"),
            ("Cold Fusion", "cfFlavors")
        ]
        for vendor, table_name in vendors:
            tk.Button(center, text=vendor, font=('Georgia', 16), width=18,
                command=lambda tbl=table_name, vnd=vendor: [
                    self.view_stack.append(self.place_order),
                    self.load_flavor_form(tbl, vnd)
                ]
            ).pack(pady=12)

    def load_flavor_form(self, table_name, vendor_name):
        self.clear_window()
        self.render_back_buttons()

        scrollable_frame = create_scrollable_frame(self.window, self.bg_color)

        # --- This is the centering trick! ---
        center_outer = tk.Frame(scrollable_frame, bg=self.bg_color)
        center_outer.pack(expand=True)

        form_center = tk.Frame(center_outer, bg=self.bg_color)
        form_center.pack(anchor='center')

        row_idx = 0

        # Title
        tk.Label(form_center, text=f"{vendor_name} Order", font=('Georgia', 20), bg=self.bg_color)\
            .grid(row=row_idx, column=0, columnspan=2, pady=10)
        row_idx += 1

        # Seasonal filter checkboxes
        include_winter = tk.BooleanVar(value=True)
        include_summer = tk.BooleanVar(value=True)

        filter_frame = tk.Frame(form_center, bg=self.bg_color)
        filter_frame.grid(row=row_idx, column=0, columnspan=2, pady=(5, 10))

        tk.Checkbutton(filter_frame, text="Include Winter Flavors", variable=include_winter, bg=self.bg_color)\
            .pack(side="left", padx=10)
        tk.Checkbutton(filter_frame, text="Include Summer Flavors", variable=include_summer, bg=self.bg_color)\
            .pack(side="left", padx=10)
        row_idx += 1

        all_flavors = self.db.fetch(SQL["get_flavors_sorted"].format(table=table_name))
        entry_widgets = {}

        def render_flavors():
            # Remove all widgets in rows after filter_frame
            for widget in list(form_center.grid_slaves()):
                info = widget.grid_info()
                if int(info['row']) > 1:  # Only rows after filter_frame
                    widget.destroy()

            r = row_idx  # Start placing rows after checkboxes
            for fid, name, unit_price, season in all_flavors:
                if (season == "winter" and not include_winter.get()) or (season == "summer" and not include_summer.get()):
                    continue
                tk.Label(form_center, text=name, width=30, anchor='e', font=('Georgia', 12), bg=self.bg_color)\
                    .grid(row=r, column=0, pady=2, sticky='e')
                entry = tk.Entry(form_center, width=5, justify='center')
                entry.grid(row=r, column=1, pady=2, padx=5)
                entry_widgets[fid] = entry
                r += 1

            # --- Date field and buttons always come after all flavors ---
            tk.Label(form_center, text="Enter Order Date (MM-DD-YYYY):", font=('Georgia', 14), bg=self.bg_color)\
                .grid(row=r, column=0, pady=(20, 5), sticky='e', columnspan=1)
            date_entry = tk.Entry(form_center, font=('Georgia', 12), justify='center')
            date_entry.grid(row=r, column=1, pady=(20, 5), sticky='w')
            date_entry.insert(0, datetime.today().strftime('%m-%d-%Y'))
            r += 1

            err_label = tk.Label(form_center, text="", font=('Georgia', 10), fg="red", bg=self.bg_color)
            err_label.grid(row=r, column=0, columnspan=2)
            r += 1

            def finalize_order():
                date_str = date_entry.get().strip()
                if not is_valid_date(date_str):
                    err_label.config(text="Invalid date format. Use MM-DD-YYYY.")
                    return

                try:
                    self.db.execute(SQL["insert_order"], (date_str, vendor_name, 0.0))
                    order_id = self.db.cur.lastrowid

                    total_price = 0.0
                    for fid, entry in entry_widgets.items():
                        qty_str = entry.get().strip()
                        try:
                            qty = int(qty_str) if qty_str else 0
                            if qty > 0:
                                unit_price = self.db.fetch(SQL["get_unit_price"].format(table=table_name), (fid,))[0][0]
                                total_price += unit_price * qty
                                self.db.execute(SQL["insert_order_detail"], (order_id, fid, qty))
                        except ValueError:
                            continue

                    self.db.execute(SQL["update_order_total"], (total_price, order_id))

                except Exception as e:
                    messagebox.showerror("Database Error", str(e))
                    return

                self.back_callback()

            tk.Button(form_center, text="Place Order", font=('Georgia', 14), command=finalize_order)\
                .grid(row=r, column=0, columnspan=2, pady=20)

        render_flavors()
        include_winter.trace_add("write", lambda *a: render_flavors())
        include_summer.trace_add("write", lambda *a: render_flavors())

    def review_orders(self):
        self.clear_window()
        self.render_back_buttons()

        vendor_map = {
            "Warwick": "WarwickFlavors",
            "Crescent Ridge": "CrescentFlavors",
            "Cold Fusion": "cfFlavors"
        }

        for vendor, table in vendor_map.items():
            tk.Label(self.window, text=f"{vendor} Orders", font=('Georgia', 16, 'bold'), bg=self.bg_color).pack(pady=(20, 10))
            container = tk.Frame(self.window, bg=self.bg_color)
            container.pack()

            orders = self.db.fetch(SQL["get_orders_by_vendor"], (vendor,))
            for order_id, date, total in orders:
                row = tk.Frame(container, bg=self.bg_color)
                row.pack(anchor='w', pady=2)

                tk.Label(row, text=date, width=18, anchor='w', font=('Georgia', 12), bg=self.bg_color).pack(side='left', padx=5)
                tk.Label(row, text=f"${total:.2f}", width=15, anchor='e', font=('Georgia', 12), bg=self.bg_color).pack(side='left', padx=5)

                # Green arrow: details
                tk.Button(
                    row, text="→", bg="green", fg="white", font=('Georgia', 14, 'bold'), width=3,
                    command=lambda oid=order_id, tbl=table, vend=vendor, tot=total, odt=date: [
                        self.view_stack.append(self.review_orders),
                        self.review_order_details(oid, tbl, vend, tot, odt)
                    ]
                ).pack(side='left', padx=(10, 2))

                # Red X: delete
                tk.Button(
                    row, text="❌", bg="red", fg="white", font=('Georgia', 14, 'bold'), width=3,
                    command=lambda oid=order_id: self.delete_order(oid)
                ).pack(side='left', padx=2)

    def delete_order(self, order_id):
        if messagebox.askyesno("Delete Order", "Are you sure you want to delete this order? This cannot be undone."):
            self.db.execute(SQL["delete_order_details"], (order_id,))
            self.db.execute(SQL["delete_order"], (order_id,))
            self.review_orders()  # Refresh

    def review_order_details(self, order_id, table, vendor, order_total, order_date):
        self.clear_window()
        self.render_back_buttons()
        tk.Label(
            self.window,
            text=f"{vendor} Order ({order_date})",
            font=('Georgia', 20), bg=self.bg_color
        ).pack(pady=20)

        # Get all flavor details for this order
        flavors = self.db.fetch(SQL["get_order_flavors"].format(table=table), (order_id,))

        details_container = tk.Frame(self.window, bg=self.bg_color)
        details_container.pack(pady=10)

        for _, name, qty, unit_price in flavors:
            row = tk.Frame(details_container, bg=self.bg_color)
            row.pack(anchor='w')
            line_price = qty * unit_price
            tk.Label(row, text=name, width=30, anchor='w', font=('Georgia', 12), bg=self.bg_color).pack(side='left', padx=5)
            tk.Label(row, text=str(qty), width=8, anchor='center', font=('Georgia', 12), bg=self.bg_color).pack(side='left', padx=5)
            tk.Label(row, text=f"${line_price:.2f}", width=12, anchor='e', font=('Georgia', 12), bg=self.bg_color).pack(side='left', padx=5)

        # Bottom row for total
        total_row = tk.Frame(details_container, bg=self.bg_color)
        total_row.pack(anchor='e', pady=(10,0))
        tk.Label(total_row, text="Order Total:", font=('Georgia', 12, 'bold'), bg=self.bg_color).pack(side='left', padx=5)
        tk.Label(total_row, text=f"${order_total:.2f}", font=('Georgia', 12, 'bold'), bg=self.bg_color).pack(side='left', padx=5)
