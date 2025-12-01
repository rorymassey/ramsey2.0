from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


#used for putting a background on (doesn't work currently)
#from PIL import *
import sqlite3
import ctypes

# Connect to an existing database or create a new one
#TODO: remove the inital function used to populate the txt total and create a sql function to calc the total 
#TODO: create a button that lets you export a csv of your data. 
#TODO: abstract some functions out into another page, starting with just one funct. 



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
            "INSERT INTO  transactions (date_added, amount, date_of_transaction,description, hide) VALUES (?,?,?,?,?)", (str(auto_date),str(dollars_db),str(date_db),str(description_db), 0)
        )
        conn.commit()
        conn.close()
    except ValueError:
        pass


#TODO: this used to display total, change this to create an exported csv only when a button is clicked. 
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
            #total_of_file1.set(f"${total_of_file}")    
    except: 
        pass

#same function as display total but uses sql not the csv file. 
def total_calculate():
    conn = sqlite3.connect("transactions.db")
    cursor  = conn.cursor()
    cursor.execute("select sum(amount) From transactions where hide = 0")
    # Fetch all rows
    rows = cursor.fetchall()
    rows_tup = rows[0]
    # Convert to dictionary (id as key, name as value)
    #total_calculate = rows
    total_of_file1.set(f"${rows_tup[0]}")
    #display all active lines in tk form 
    #print(result_dict)
    conn.commit()
    conn.close()
    #return total_calculate


def display_line_items(*args):
    conn = sqlite3.connect("transactions.db")
    cursor  = conn.cursor()
    #retrive list of active IDs 
    pretty_list = filter_id()
    #initialize dict for displayed items. 
    result_dict ={}
    cursor.execute("select * From transactions where hide = 0")
    # Convert to dictionary (id as key, name as value)
     # Fetch all rows
    rows = cursor.fetchall()
    for row in rows:
        if row[0] in pretty_list:
            result_dict[row[0]] = (row[2],row[3],row[4])
   

    #display all active lines in tk form 
    #print(result_dict)
    conn.commit()
    conn.close() 
    return result_dict

def reload_list():
    listbox.delete(0, END)
    # Retrieve all results of active transactions
    all_display_items = display_line_items()
    #prevent garabage collection of the var values 
    vars_list = []
    #for loop to print out the values 
    for i in all_display_items:
        var = StringVar()
        vars_list.append(var)
        var = all_display_items[i]
        listbox.insert(END, f"id:{i}          Amount:   {var[0]}          Date:   {var[1]}           Description:   {var[2]}")


    
#hiding lines from the view 
def delete_row(event):
    # Get selected index
    selection = listbox.curselection()
    #print(selection)
    if selection:
        x = ask_yes_no()
        if x == 'y':
            index = selection[0]
            value = listbox.get(index)
            start = 'id:'
            end = ' '
            start_index = value.find(start) + len(start)
            end_index = value.find(end)
            transaction_id = value[start_index:end_index]
            #debug print
            #print(f"Clicked item value: {transaction_id}")
            #remove items from db 
            conn = sqlite3.connect("transactions.db")
            cursor  = conn.cursor()
            cursor.execute("update transactions set hide = 1 where id = ?", (transaction_id,))
            conn.commit()
            conn.close()
            reload_list()
#yes no function parired with delete_row to confirm deletion of a line. 
def ask_yes_no():
    answer = messagebox.askyesno("Confirmation", "DO YOU WANT TO DELETE?")
    if answer:
        return "y"
    else:
        return "n"

#function to show all months and then let you select one also have it update a global variable for month and year. 
def select_month():
    items = ["Apple", "Banana", "Cherry", "Date", "Elderberry"]
    if not hasattr(select_month, "created"):
        combo = ttk.Combobox(root, values=items, state="readonly")
        combo.current(0)
        combo.grid(column=4, row=10, sticky=E)
        select_month.created = True
      

#function to filter out what displays and total so that we can add button functionality easier.
# TODO: get these id's to be used for the default display (need to be cleaned up and used for the totatl_calculate function adn the display line items list. ) 
def filter_id(month=None, year=None):
    sql_month = 0
    sql_year = 0 
    if month == None and year == None:
        sql_month = datetime.now().strftime("%m")
        sql_year = datetime.now().strftime("%Y")
    conn = sqlite3.connect("transactions.db")
    cursor  = conn.cursor()
    cursor.execute("""select id from transactions where strftime('%m', date_of_transaction) = ?
                    and strftime('%Y', date_of_transaction) = ? and hide = 0""", (sql_month, sql_year))
    rows = cursor.fetchall()
    pretty_rows = []
    for i in rows:
        pretty_rows.append(i[0])
    conn.commit()
    conn.close()
    return pretty_rows

def run_all_funcs(*args):
    try:
        calculate()
        total_calculate()
        #display()
        add_to_table()
        display_line_items()
        reload_list()
        filter_id()
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
total_calculate()

dollars_entry = ttk.Entry(mainframe, width=10, textvariable=dollars)
dollars_entry.grid(column=2, row=2, sticky=(W, E))

#description of transaction 
description_entry = ttk.Entry(mainframe, width=10, textvariable=description)
description_entry.grid(column=2, row=3, sticky=(W, E))

#date of transaction (prepopulates with today's date but its modifiable)
date = StringVar()
ugly_date = datetime.now()
date = ugly_date.strftime("%Y-%m-%d")
date = StringVar(value = date )
date_entry = ttk.Entry(mainframe, width=10, textvariable=date)
date_entry.grid(column=2, row=4, sticky=(W, E))

#displays the total added amt (maybe change this )
ttk.Label(mainframe, textvariable=total_of_file1).grid(column=2, row=9, sticky=(W, E))
ttk.Label(mainframe, textvariable=total).grid(column=2, row=8, sticky=(W, E))


# Create box to display the whole dang list
listbox = Listbox(mainframe, height=50, width=70)
listbox.grid(row=11, column =2, sticky = (W, E))
#runs function to delete row
listbox.bind("<Button-1>", delete_row)

# Create Scrollbar
#TODO: fix the scroll bar 
##scrollbar = Scrollbar(mainframe, orient=VERTICAL)
##scrollbar.grid(row=11, column =3, sticky = (W, E))
#TODO: maybe create a horrizontal scroll bar later? 

#Link Scrollbar and Listbox
#TODO: fix the scroll bar 
##listbox.config(yscrollcommand=scrollbar.set)
##scrollbar.config(command=listbox.yview)

#TODO: have a month selector that can be used to look at each month mayhaps other date selectors ect. 
    #TODO: get the month and year to open a box that will add a value into filter_id function line 162
# Create box to display a list of months 
ttk.Button(mainframe, text="Month", command=select_month).grid(column=4, row=9, sticky=W)
#Create a box to select years

ttk.Button(mainframe, text="Year").grid(column=3, row=9, sticky=E)

#call reload list to populate list on open
reload_list()

#(default to display current month/year)
    #TODO: make the removed lines all show up in a hidden column or when you select hide and you can click them to restore
#TODO: organize list so that it is pretty
#TODO: buttons for handy reports like a balance sheet ect. 


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