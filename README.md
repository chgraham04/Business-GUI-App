# TPC App

## Overview

This app is a user-friendly inventory and payroll management system with a modern Python Tkinter GUI. It helps a small business place and review  orders from various vendors, track specific items from vendors, and manage employee payroll in a centralized, efficient way.

---

## Features

### Inventory Management
- **Manage Flavors:**  
  - Add, edit, and delete flavors for three vendors: Warwick, Crescent Ridge, and Cold Fusion.
  - Seasonal tagging: Label flavors as year-round, winter, or summer, and filter accordingly to ensure orders are as efficient as possible.

- **Place Orders:**  
  - Quickly place new orders by vendor, with an easy-to-use, centered order entry form.
  - Automatic calculation of total order cost (tax included).
  - Smart filtering for seasonal flavors to avoid item redundancy.

- **Review Orders:**  
  - Browse prior orders, grouped by vendor.
  - View order details, including itemized breakdown and total price.
  - Delete orders when needed.

### Payroll Management
- **Employee Records:**  
  - Add, edit, and view employee information.
  - Track pay periods, including hours worked, overtime, and sick time.
  - Automatically calculates payroll for each period.

---
## Future Additions

### Automated C++ Scheduling Program
- Allow user to generate weekly schedule for all employees using algorithm which considers every employee's
  - preferred shift times
  - number of desired shifts per week
  - priority in shift consideration
  - strength
  - ability to open and close the business
  - willingness/ability to work doubles
  
## Getting Started

### Prerequisites

- Python 3.8 or higher
- Required packages:
  - `tkinter`
  - `sqlite3`

You can install any extra requirements (if needed) with:
```bash
pip install -r requirements.txt
