# TPC App

## Overview

**TPC App** is a user-friendly inventory and payroll management system with a modern Python Tkinter GUI. It helps small businesses track ice cream and gelato flavors, place and review vendor orders, and manage employee payroll in a centralized, efficient way.

---

## Features

### Inventory Management
- **Manage Flavors:**  
  - Add, edit, and delete flavors for three vendors: Warwick, Crescent Ridge, and Cold Fusion.
  - Seasonal tagging: Label flavors as year-round, winter, or summer, and filter accordingly.

- **Place Orders:**  
  - Quickly place new orders by vendor, with an easy-to-use, centered order entry form.
  - Automatic calculation of total order cost.
  - Smart filtering for seasonal flavors.

- **Review Orders:**  
  - Browse historical orders, grouped by vendor.
  - View order details, including itemized breakdown and total price.
  - Delete orders with a single click.

### Payroll Management
- **Employee Records:**  
  - Add, edit, and view employee information.
  - Track pay periods, including hours worked, overtime, and sick time.
  - Automatically calculates payroll for each period.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required packages:
  - `tkinter`
  - `sqlite3`

You can install any extra requirements (if needed) with:
```bash
pip install -r requirements.txt
