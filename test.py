
import tkinter as tk
from tkinter import messagebox

def ask_yes_no():
    answer = messagebox.askyesno("Confirmation", "Do you want to continue?")
    if answer:
        print("User clicked Yes")
    else:
        print("User clicked No")

root = tk.Tk()
root.title("Yes/No Example")
root.geometry("300x200")

button = tk.Button(root, text="Ask Yes/No", command=ask_yes_no)
button.pack(pady=20)

root.mainloop()
