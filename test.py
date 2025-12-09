
import tkinter as tk
from tkinter import ttk

def show_menu(event=None):
    # Position at the mouse or near the button
    x = root.winfo_pointerx()
    y = root.winfo_pointery()
    menu.tk_popup(x, y)

def on_pick(choice):
    selected_var.set(choice)
    print("Selected:", choice)

root = tk.Tk()
root.title("Popup Menu")

selected_var = tk.StringVar(value="(none)")
options = ["Red", "Green", "Blue", "Yellow"]

menu = tk.Menu(root, tearoff=False)
for opt in options:
    menu.add_command(label=opt, command=lambda o=opt: on_pick(o))

ttk.Label(root, textvariable=selected_var).pack(padx=10, pady=(10, 4))
btn = ttk.Button(root, text="Pick color", command=show_menu)
btn.pack(padx=10, pady=10)

root.mainloop()


#do we have a general idea or a goal of when that would
