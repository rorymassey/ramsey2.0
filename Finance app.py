from tkinter import *
from tkinter import ttk
from datetime import datetime
#from PIL import *

def calculate(*args):
    try:
        dollars_export = float(dollars.get())
        description_export = description.get()
        date_export = date.get()
        total.set(f"${round(dollars_export, 4)} added")
        with open("totaldollars.txt", "a" ) as file:
            #add Dollar value and date 
            file.write(f"Date added:{datetime.now()}, Amount: {dollars_export}, Description: {description_export}, Date of transaction: {date_export} \n")
            #todo build a dict with all the values to display 
            #total each up by month 
            #file.write(f"Inches: {value * 12}")
    except ValueError:
        pass

#def display():
 #   try: 
  #  except: 


root = Tk()
root.title("Balance Sheet")

mainframe = ttk.Frame(root, padding=(200, 200, 400, 400))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#mainframe.config(background="#360e40")

dollars = StringVar()
total = StringVar()
description = StringVar()
#amt of transaction 
dollars_entry = ttk.Entry(mainframe, width=10, textvariable=dollars)
dollars_entry.grid(column=2, row=2, sticky=(W, E))
#description of transaction 
description_entry = ttk.Entry(mainframe, width=10, textvariable=description)
description_entry.grid(column=2, row=3, sticky=(W, E))
#date of transaction (prepopulates with today's date but its modifiable)
date = StringVar()
ugly_date = datetime.now()
date =  str(ugly_date.month) + '-'+ str(ugly_date.day) + '-'+ str(ugly_date.year)
date = StringVar(value = date )
date_entry = ttk.Entry(mainframe, width=10, textvariable=date)
date_entry.grid(column=2, row=4, sticky=(W, E))

#displays the total added amt (maybe change this )
ttk.Label(mainframe, textvariable=total).grid(column=2, row=8, sticky=(W, E))
#ttk.Label(mainframe, textvariable=description).grid(column=2, row=5, sticky=(W, E))
#todo: add a place to put a discription of transaction 
#todo: add a place to put a date of Transaction
#todo: output the total of the month for starters and other handy reports like a balance sheet ect. 
#todo: have a month selector that can be used to look at each month. 
ttk.Label(mainframe, text="Addtional transactions").grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Dollars:").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Description:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Total").grid(column=1, row=8, sticky=E)
ttk.Label(mainframe, text="Date").grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Add", command=calculate).grid(column=3, row=4, sticky=W)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
mainframe.columnconfigure(2, weight=1)
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
dollars_entry.focus()

root.bind("<Return>", calculate)
root.mainloop()