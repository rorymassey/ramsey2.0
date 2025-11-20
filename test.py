
import tkinter as tk

def on_item_click(event):
    # Get selected index
    selection = listbox.curselection()
    if selection:
        index = selection[0]
        value = listbox.get(index)
        print(f"Clicked item value: {value}")
        # You can return or process this value here

root = tk.Tk()

listbox = tk.Listbox(root)
listbox.pack()

# Add items
items = ["Line1", "Line2", "Line3"]
for item in items:
    listbox.insert(tk.END, item)

# Bind click event
listbox.bind("<Button-1>", on_item_click)

root.mainloop()
