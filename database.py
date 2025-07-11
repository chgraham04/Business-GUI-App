import sqlite3
from utils import SQL

class DatabaseManager:
    def __init__(self, db_name="icecream_orders.db"):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.init_tables()

    def init_tables(self):
        # Flavor Tables
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS WarwickFlavors (
            flavor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            unit_price REAL
        )""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS CrescentFlavors (
            flavor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            unit_price REAL
        )""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS cfFlavors (
            flavor_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            unit_price REAL
        )""")

        try:
            self.cur.execute("ALTER TABLE WarwickFlavors ADD COLUMN season TEXT DEFAULT 'year_round'")
        except sqlite3.OperationalError:
            pass
        try:
            self.cur.execute("ALTER TABLE CrescentFlavors ADD COLUMN season TEXT DEFAULT 'year_round'")
        except sqlite3.OperationalError:
            pass
        try:
            self.cur.execute("ALTER TABLE cfFlavors ADD COLUMN season TEXT DEFAULT 'year_round'")
        except sqlite3.OperationalError:
            pass

        # Orders
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            vendor TEXT NOT NULL,
            total REAL
        )""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS OrderDetails (
            order_id INTEGER,
            flavor_id TEXT,
            quantity INTEGER NOT NULL,
            FOREIGN KEY(order_id) REFERENCES Orders(order_id)
        )""")

        # Employees
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS Employee (
            employee_id INTEGER PRIMARY KEY,
            f_name TEXT NOT NULL,
            l_name TEXT NOT NULL,
            wage REAL NOT NULL,
            shift_priority INTEGER DEFAULT 3,
            strength INTEGER DEFAULT 5,
            desired_weekly_shifts INTEGER NOT NULL,
            is_senior INTEGER DEFAULT 0,
            double_eligible INTEGER DEFAULT 0, 
            preferred_shift TEXT DEFAULT 'day'
        )""")
        try: self.cur.execute("ALTER TABLE Employee ADD COLUMN shift_priority INTEGER DEFAULT 3")
        except sqlite3.OperationalError: pass
        try: self.cur.execute("ALTER TABLE Employee ADD COLUMN strength INTEGER DEFAULT 5")
        except sqlite3.OperationalError: pass
        try: self.cur.execute("ALTER TABLE Employee ADD COLUMN desired_weekly_shifts INTEGER DEFAULT 5")
        except sqlite3.OperationalError: pass
        try: self.cur.execute("ALTER TABLE Employee ADD COLUMN is_senior INTEGER DEFAULT 0")
        except sqlite3.OperationalError: pass
        try: self.cur.execute("ALTER TABLE Employee ADD COLUMN double_eligible INTEGER DEFAULT 0")
        except sqlite3.OperationalError: pass
        try: self.cur.execute("ALTER TABLE Employee ADD COLUMN preferred_shift TEXT DEFAULT 'day'")
        except sqlite3.OperationalError: pass

        
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS PayPeriods (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            pay_period TEXT,
            hours_worked REAL,
            overtime_hours REAL,
            sick_hours REAL,
            FOREIGN KEY (employee_id) REFERENCES Employee(employee_id)
        )""")
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS PayrollSummary (
            pay_period TEXT PRIMARY KEY,
            total_payout REAL
        )""")

        self.conn.commit()

    def fetch(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def execute(self, query, params=()):
        self.cur.execute(query, params)
        self.conn.commit()

    def close(self):
        self.conn.close()
