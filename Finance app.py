from tkinter import *
from tkinter import ttk
from datetime import datetime

#used for putting a background on (doesn't work currently)
#from PIL import *
import sqlite3
import ctypes

# Connect to an existing database or create a new one



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


#add values from input to table
def add_to_table(*args):
    try:
        conn = sqlite3.connect("transactions.db")
        cursor  = conn.cursor()
        auto_date = datetime.now()
        dollars_db = float(dollars.get())
        description_db = description.get()
        date_db = date.get()
        cursor.execute(
            """CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, date_added TEXT, amount TEXT, date_of_transaction TEXT, description TEXT, hide INTEGER )"""
        )
        cursor.execute(
            "INSERT INTO  transactions (date_added, amount, date_of_transaction,description, hide) VALUES (?,?,?,?,?)", (str(auto_date),str(dollars_db),str(date_db),str(description_db), 1)
        )
        conn.commit()
        conn.close()
    except ValueError:
        pass


#display total
def display(*args):
    try: 
        with open("totaldollars.txt", "r" ) as file:
            x = file.read().split("\n")
            total_of_file = 0.00
            #calculate total
            for y in x:
                start = 'Amount:'
                end = ', Description'
                start_index = y.find(start) + len(start)
                end_index = y.find(end)
                temp = y[start_index:end_index]
                if temp:
                    total_of_file += float(temp)
            #pass value out to tkinter        
            total_of_file1.set(f"${total_of_file}")    
    except: 
        pass

def display_line_items(*args):
    conn = sqlite3.connect("transactions.db")
    cursor  = conn.cursor()
    cursor.execute("select * From transactions")
# Fetch all rows
    rows = cursor.fetchall()
# Convert to dictionary (id as key, name as value)
    result_dict = {row[0]: (row[2],row[3],row[4]) for row in rows}
    #display all active lines in tk form 

    #print(result_dict)
    conn.commit()
    conn.close()
    return result_dict


def run_all_funcs():
    try:
        calculate()
        display()
        add_to_table()
        display_line_items()
       
     
    except:
        pass

#change the icon for windows 


ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("fi.mycompany.334488jksethut")

root = Tk()
root.title("Balance Sheet")
root.iconbitmap("money.ico")
mainframe = ttk.Frame(root, padding=(200, 200, 400, 400))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
#mainframe.config(background="#721888")
dollars = StringVar()
total = StringVar()
description = StringVar()
total_of_file1 = StringVar()
#amt of transaction 
display()
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
ttk.Label(mainframe, textvariable=total_of_file1).grid(column=2, row=9, sticky=(W, E))
ttk.Label(mainframe, textvariable=total).grid(column=2, row=8, sticky=(W, E))


# Create box to display the whole dang list
listbox = Listbox(mainframe, height=20, width=100)
listbox.grid(row=11, column =0, sticky = 'ns')

# Add items to Listbox
#for i in range(50):
 #   listbox.insert(END, f"Item {i+1}")


# display all results of active transactions
all_display_items = display_line_items()
#prevent garabage collection of the var values 
vars_list = []
y = 23
#for loop to print out the values 
for i in all_display_items:
    #print(test[i])
    temp = all_display_items[i]
    #print(temp)
    var = StringVar()
    vars_list.append(var)
    var = all_display_items[i]
    print(var)
    #ttk.Label(mainframe, textvariable=var).grid(column=2, row=y, sticky=(W, E))
    listbox.insert(END, f"Amount: {var[0]} Date: {var[1]} Description: {var[2]}")
    y+= 1 

# Create Scrollbar
scrollbar = Scrollbar(mainframe, orient=VERTICAL)
scrollbar.grid(row=11, column =1, sticky = 'ns')
#TODO: maybe create a horrizontal scroll bar later? 

# Link Scrollbar and Listbox
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

#ttk.Label(mainframe, textvariable=description).grid(column=2, row=5, sticky=(W, E))
#todo: add a place to put a discription of transaction 
#todo: add a place to put a date of Transaction
#todo: output the total of the month for starters and other handy reports like a balance sheet ect. 
#todo: have a month selector that can be used to look at each month. 
ttk.Label(mainframe, text="Addtional transactions").grid(column=2, row=1, sticky=W)
ttk.Label(mainframe, text="Dollars:").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="Description:").grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text="Total").grid(column=1, row=9, sticky=E)
ttk.Label(mainframe, text="Date").grid(column=1, row=4, sticky=W)
ttk.Button(mainframe, text="Add", command=run_all_funcs).grid(column=3, row=4, sticky=W)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

mainframe.columnconfigure(2, weight=1)


for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
dollars_entry.focus()



root.bind("<Return>", run_all_funcs)
root.mainloop()