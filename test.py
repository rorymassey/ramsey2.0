
import sqlite3
import tkinter as tk
from tkinter import ttk
from tkinter.constants import W

root = tk.Tk()
mainframe = ttk.Frame(root)
mainframe.grid(sticky="nsew")

def on_month_change(event=None):
    # Access the stored combobox and print current selection
    combo = select_month.combo
    value = combo.get()        # selected text (e.g., "01", "02", ...)
    index = combo.current()    # selected index (0-based)
    print(f"Selected month: {value} (index {index})")

def select_month(*args):
    # 1) Read months from DB
    conn = sqlite3.connect("transactions.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT strftime('%m', date_of_transaction)
        FROM transactions
        WHERE hide = 0 
          AND strftime('%m', date_of_transaction) IS NOT NULL
        GROUP BY strftime('%m', date_of_transaction)
        ORDER BY strftime('%m', date_of_transaction)
    """)
    rows = cursor.fetchall()
    conn.close()

    items = [row[0] for row in rows]  # e.g., ['01','02','03', ...]

    # 2) Create combobox once, or update values if it already exists
    if not hasattr(select_month, "combo"):
        select_month.combo = ttk.Combobox(mainframe, values=items, state="readonly")
        select_month.combo.grid(column=4, row=9, sticky=W)

        # Optional initial selection (only the first time):
        if items:
            select_month.combo.current(0)

        # Bind to selection change so you get the user's choice immediately
        select_month.combo.bind("<<ComboboxSelected>>", on_month_change)
    else:
        # Just update the list of values; don't reset current selection unless you want to
        select_month.combo["values"] = items

    # If you still want to print the current value right after building/updating:
    # (Note: this will reflect the initial selection if user hasn’t picked yet.)
    print(select_month.combo.get())

# Build the UI and populate
select_month()

