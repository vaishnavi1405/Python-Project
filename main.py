from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db import Database

# Initializes a connection to a database named EmployeeDB with the credentials provided.
db = Database(host="localhost", database="EmployeeDB", user="root", password="root")

root = Tk()
root.title("Employee Management System")
root.geometry("1920x1080+0+0")
root.config(bg="#2c3e50")
root.state("zoomed")

name = StringVar()
age = StringVar()
contact = StringVar()
address = StringVar()

# Entries Frame
entries_frame = Frame(root, bg="#535c68")
entries_frame.pack(side=TOP, fill=X)
title = Label(entries_frame, text="Employee Management System", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
title.grid(row=0, columnspan=2, padx=10, pady=20, sticky="w")

lblName = Label(entries_frame, text="Name", font=("Calibri", 16), bg="#535c68", fg="white")
lblName.grid(row=1, column=0, padx=10, pady=10, sticky="w")
txtName = Entry(entries_frame, textvariable=name, font=("Calibri", 16), width=30)
txtName.grid(row=1, column=1, padx=10, pady=10, sticky="w")

lblAge = Label(entries_frame, text="Age", font=("Calibri", 16), bg="#535c68", fg="white")
lblAge.grid(row=1, column=2, padx=10, pady=10, sticky="w")
txtAge = Entry(entries_frame, textvariable=age, font=("Calibri", 16), width=30)
txtAge.grid(row=1, column=3, padx=10, pady=10, sticky="w")

lblContact = Label(entries_frame, text="Contact No", font=("Calibri", 16), bg="#535c68", fg="white")
lblContact.grid(row=2, column=0, padx=10, pady=10, sticky="w")
txtContact = Entry(entries_frame, textvariable=contact, font=("Calibri", 16), width=30)
txtContact.grid(row=2, column=1, padx=10, pady=10, sticky="w")

lblAddress = Label(entries_frame, text="Address", font=("Calibri", 16), bg="#535c68", fg="white")
lblAddress.grid(row=3, column=0, padx=10, pady=10, sticky="w")

txtAddress = Text(entries_frame, width=85, height=5, font=("Calibri", 16))
txtAddress.grid(row=4, column=0, columnspan=4, padx=10, sticky="w")

# Fetches data from the selected row in the Treeview (table) and populates the entry fields with that data.
def getData(event):
    selected_row = tv.focus()
    data = tv.item(selected_row)
    global row
    row = data["values"]
    # Debug output
    print("Selected row data:", row)
    name.set(row[1])
    age.set(row[2])
    contact.set(row[3])
    txtAddress.delete(1.0, END)
    txtAddress.insert(END, row[4].strip())

def displayAll():
    tv.delete(*tv.get_children())
    for row in db.fetch():
        print("Fetched row data:", row)  # Debug output
        tv.insert("", END, values=row)

def add_employee():
    if txtName.get() == "" or txtAge.get() == "" or txtContact.get() == "" or txtAddress.get(1.0, END).strip() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return
    db.insert(txtName.get(), txtAge.get(), txtContact.get(), txtAddress.get(1.0, END).strip())
    messagebox.showinfo("Success", "Record Inserted")
    clearAll()
    displayAll()

def update_employee():
    if txtName.get() == "" or txtAge.get() == "" or txtContact.get() == "" or txtAddress.get(1.0, END).strip() == "":
        messagebox.showerror("Error in Input", "Please Fill All the Details")
        return
    db.update(row[0], txtName.get(), txtAge.get(), txtContact.get(), txtAddress.get(1.0, END).strip())
    messagebox.showinfo("Success", "Record Updated")
    clearAll()
    displayAll()

def delete_employee():
    db.remove(row[0])
    clearAll()
    displayAll()

def clearAll():
    name.set("")
    age.set("")
    contact.set("")
    txtAddress.delete(1.0, END)

btn_frame = Frame(entries_frame, bg="#535c68")
btn_frame.grid(row=5, column=0, columnspan=4, padx=10, pady=10, sticky="w")
btnAdd = Button(btn_frame, command=add_employee, text="Add Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#16a085", bd=0).grid(row=0, column=0)
btnEdit = Button(btn_frame, command=update_employee, text="Update Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#2980b9", bd=0).grid(row=0, column=1, padx=10)
btnDelete = Button(btn_frame, command=delete_employee, text="Delete Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#c0392b", bd=0).grid(row=0, column=2, padx=10)
btnClear = Button(btn_frame, command=clearAll, text="Clear Details", width=15, font=("Calibri", 16, "bold"), fg="white", bg="#f39c12", bd=0).grid(row=0, column=3, padx=10)

# Table Frame
tree_frame = Frame(root, bg="#ecf0f1")
tree_frame.place(x=0, y=480, width=1700, height=520)
style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 18), rowheight=50)  # Modify the font of the body
style.configure("mystyle.Treeview.Heading", font=('Calibri', 18))  # Modify the font of the headings

tv = ttk.Treeview(tree_frame, columns=(1, 2, 3, 4, 5), style="mystyle.Treeview")
tv.heading("1", text="ID")
tv.column("1", width=10, anchor='center')
tv.heading("2", text="Name")
tv.column("2", width=75, anchor='w')
tv.heading("3", text="Age")
tv.column("3", width=50, anchor='center')
tv.heading("4", text="Contact")
tv.column("4", width=100, anchor='w')
tv.heading("5", text="Address")
tv.column("5", width=950, anchor='center')  # Increase width for Address

tv['show'] = 'headings'
tv.bind("<ButtonRelease-1>", getData)
tv.pack(fill=X)

#Starts the GUI event loop, which waits for user interactions and updates the interface accordingly.
displayAll()
root.mainloop()
