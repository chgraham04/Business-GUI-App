import tkinter as tk
from tkinter import ttk, messagebox
from utils import SQL

class FlavorManager:
    def __init__(self, window, db, back_callback, view_stack, bg_color='#a3b18a'):
        self.window = window
        self.db = db
        self.back_callback = back_callback  # Should be TPCApp.show_main_menu
        self.view_stack = view_stack        # This is shared with the whole app!
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

    def manage_flavors_menu(self):
        self.clear_window()
        self.render_back_buttons()

        tk.Label(self.window, text="Manage Flavors", font=('Georgia', 20), bg=self.bg_color).pack(pady=30)

        center = tk.Frame(self.window, bg=self.bg_color)
        center.pack()

        tk.Button(center, text="Add Flavor", font=('Georgia', 14),
                  command=lambda: [self.view_stack.append(self.manage_flavors_menu), self.add_flavor()]).pack(pady=10)
        tk.Button(center, text="View Flavors", font=('Georgia', 14),
                  command=lambda: [self.view_stack.append(self.manage_flavors_menu), self.view_flavors()]).pack(pady=10)

    def view_flavors(self):
        self.clear_window()
        self.render_back_buttons()

        vendor_map = {
            "WarwickFlavors": "Warwick",
            "CrescentFlavors": "Crescent Ridge",
            "cfFlavors": "Cold Fusion"
        }

        for table, vendor in vendor_map.items():
            tk.Label(self.window, text=f"{vendor} Flavors", font=('Georgia', 16, 'bold'), bg=self.bg_color).pack(pady=(20, 10))

            container = tk.Frame(self.window, bg=self.bg_color)
            container.pack()

            flavors = sorted(
                self.db.fetch(SQL["get_flavors_sorted"].format(table=table)), 
                key=lambda x: x[1].lower()
            )

            for fid, name, price, season in flavors:
                row = tk.Frame(container, bg=self.bg_color)
                row.pack(anchor='w', pady=2)

                name_var = tk.StringVar(value=name)
                price_var = tk.StringVar(value=f"{price:.2f}")
                season_var = tk.StringVar(value=season)

                tk.Entry(row, textvariable=name_var, width=30).pack(side='left', padx=5)

                # Unit Price with $ prefix
                price_frame = tk.Frame(row, bg=self.bg_color)
                price_frame.pack(side='left', padx=5)
                tk.Label(price_frame, text="$", font=('Georgia', 12), bg=self.bg_color).pack(side='left')
                tk.Entry(price_frame, textvariable=price_var, width=8, justify='right').pack(side='left')

                season_menu = ttk.Combobox(row, textvariable=season_var, values=["year_round", "winter", "summer"], state="readonly", width=12)
                season_menu.pack(side='left', padx=5)

                def make_save_fn(old_id, table, name_var=name_var, price_var=price_var, season_var=season_var):
                    def save():
                        new_name = name_var.get().strip()
                        new_id = new_name.lower().replace(" ", "_")
                        try:
                            new_price = float(price_var.get())
                        except ValueError:
                            messagebox.showerror("Invalid Price", "Enter a valid price.")
                            return

                        new_season = season_var.get()
                        flavor_type = "gelato" if table == "cfFlavors" else "ice cream"

                        if new_id != old_id:
                            # Check for duplicate flavor_id
                            if self.db.fetch(SQL["flavor_exists"].format(table=table), (new_id,)):
                                messagebox.showerror("Duplicate ID", f"A flavor with ID '{new_id}' already exists.")
                                return
                            self.db.execute(SQL["delete_flavor"].format(table=table), (old_id,))
                            self.db.execute(SQL["insert_flavor"].format(table=table),
                                            (new_id, new_name, flavor_type, new_price, new_season))
                        else:
                            self.db.execute(SQL["update_flavor"].format(table=table),
                                            (new_name, new_price, new_season, old_id))
                        self.view_flavors()
                    return save

                tk.Button(row, text="Save", bg="green", fg="white", command=make_save_fn(fid, table)).pack(side='left', padx=5)

                def make_delete_fn(fid, table):
                    def delete():
                        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this flavor?"):
                            self.db.execute(SQL["delete_flavor"].format(table=table), (fid,))
                            self.view_flavors()
                    return delete

                tk.Button(row, text="❌", bg="red", fg="white", command=make_delete_fn(fid, table)).pack(side='left', padx=5)

    def add_flavor(self):
        self.clear_window()
        self.render_back_buttons()

        tk.Label(self.window, text="Add New Flavor", font=('Georgia', 20), bg=self.bg_color).pack(pady=10)

        content = tk.Frame(self.window, bg=self.bg_color)
        content.pack(pady=10)

        # Vendor Selection
        tk.Label(content, text="Select Vendor:", font=('Georgia', 14), bg=self.bg_color).pack()
        vendor_var = tk.StringVar(value="Warwick")
        friendly_to_table = {
            "Warwick": "WarwickFlavors",
            "Crescent Ridge": "CrescentFlavors",
            "Cold Fusion": "cfFlavors"
        }
        vendor_dropdown = ttk.Combobox(content, textvariable=vendor_var,
                                       values=list(friendly_to_table.keys()), state='readonly')
        vendor_dropdown.pack(pady=5)

        # Flavor Name
        tk.Label(content, text="Flavor Name:", font=('Georgia', 14), bg=self.bg_color).pack()
        name_entry = tk.Entry(content, font=('Georgia', 12))
        name_entry.pack()

        # Unit Price
        tk.Label(content, text="Unit Price:", font=('Georgia', 14), bg=self.bg_color).pack()
        price_entry = tk.Entry(content, font=('Georgia', 12))
        price_entry.pack()

        # Seasonal Option
        seasonal_var = tk.BooleanVar()
        season_var = tk.StringVar(value="winter")
        tk.Checkbutton(content, text="Seasonal?", variable=seasonal_var, bg=self.bg_color,
                       command=lambda: season_frame.pack() if seasonal_var.get() else season_frame.pack_forget()
                       ).pack(pady=(10, 5))

        season_frame = tk.Frame(content, bg=self.bg_color)
        season_dropdown = ttk.Combobox(season_frame, textvariable=season_var,
                                       values=["winter", "summer"], state='readonly')
        season_dropdown.pack()
        season_frame.pack_forget()

        def submit():
            friendly = vendor_var.get()
            table = friendly_to_table.get(friendly)
            if not table:
                messagebox.showerror("Selection Error", "Please select a valid vendor.")
                return

            name = name_entry.get().strip()
            price_str = price_entry.get().strip()

            if not name:
                messagebox.showerror("Input Error", "Flavor name is required.")
                return
            try:
                price = float(price_str)
                if price < 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Input Error", "Enter a valid non-negative price.")
                return

            flavor_id = name.lower().replace(" ", "_")
            flavor_type = "gelato" if table == "cfFlavors" else "ice cream"
            season = season_var.get() if seasonal_var.get() else "year_round"

            if self.db.fetch(SQL["flavor_exists"].format(table=table), (flavor_id,)):
                messagebox.showerror("Duplicate", "Flavor already exists.")
                return

            self.db.execute(SQL["add_flavor"].format(table=table), (flavor_id, name, flavor_type, price, season))
            messagebox.showinfo("Success", f"Added '{name}' to {friendly}.")
            self.manage_flavors_menu()

        tk.Button(content, text="Add Flavor", font=('Georgia', 14), command=submit).pack(pady=10)
