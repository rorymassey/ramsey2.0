
import tkinter as tk

root = tk.Tk()
root.title("Scrollable List")

# Frame to hold Listbox and Scrollbar
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Create Listbox
listbox = tk.Listbox(frame, height=10, width=30)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Add items to Listbox
for i in range(50):
    listbox.insert(tk.END, f"Item {i+1}")

# Create Scrollbar
scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Link Scrollbar and Listbox
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

root.mainloop()
