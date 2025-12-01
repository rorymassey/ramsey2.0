
import tkinter as tk
from tkinter import ttk

root = tk.Tk()
root.title("Show selector on button click")

items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]

def show_combobox():
    if not hasattr(show_combobox, "created"):
        combo = ttk.Combobox(root, values=items, state="readonly")
        combo.current(0)
        combo.pack(padx=10, pady=10)
        show_combobox.created = True


tk.Button(root, text="Show Combobox", command=show_combobox).pack(pady=6)

root.mainloop()
