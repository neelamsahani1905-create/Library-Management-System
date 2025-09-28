# Importing modules
import mysql.connector as a
from mysql.connector import Error
from datetime import date
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox as message

# Establishing connection Python and  MySQL
con = a.connect(host="localhost", user="root", password="neelam", database="library")

#Creating the GUI window
root = tk.Tk()
root.title("Library Management System")
root.geometry("400x400")

# Add Book
def addbook():
    bn = book_name.get()
    bcode =book_code.get()
    subject=book_subject.get()
    
    try:
        total = int(book_total.get())
    except ValueError:
        message.showerror("Error"," Total should a number only")
        return

    data = (bn, bcode, total, subject)
    sql = 'INSERT INTO books VALUES(%s, %s, %s, %s)'

    try:
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
       
        message.showinfo("Book Added Successfully")
    except Error as e:
        message.showerror("Database Error: ", str(e))

def open_addbook_window():
    global top, book_name, book_code, book_total, book_subject
    top = tk.Toplevel(root)
    top.title("Add Book")

    tk.Label(top, text="Book name").pack()
    book_name = tk.Entry(top)
    book_name.pack()

    tk.Label(top, text="Book code").pack()
    book_code = tk.Entry(top)
    book_code.pack()

    tk.Label(top, text="Book total").pack()
    book_total = tk.Entry(top)
    book_total.pack()

    tk.Label(top, text="Subject").pack()
    book_subject = tk.Entry(top)
    book_subject.pack()

    tk.Button(top, text="Add Book into the library", command=addbook).pack(pady=10)



# Issue Book
def issueb():
    name = issuer_name.get()
    regno = registration_number.get()
    bcode = book_code.get()
    today = date.today()

    data = (name, regno, bcode, today)
    sql = "INSERT INTO issue VALUES(%s, %s, %s, %s)"

    try:
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
     
        message.showinfo(f"Book issued to: {name}")
        bookup(bcode, -1)
        top.destroy()
    except Error as e:
        message.showerror("Database Error: ", str(e))

def open_issuebook_window():
    global top, issuer_name, registration_number, book_code
    top = tk.Toplevel(root)
    top.title("Issue Book")

    tk.Label(top, text="Issuer name").pack()
    issuer_name = tk.Entry(top)
    issuer_name.pack()

    tk.Label(top, text="Registration number").pack()
    registration_number = tk.Entry(top)
    registration_number.pack()

    tk.Label(top, text="Book Code").pack()
    book_code = tk.Entry(top)
    book_code.pack()

    tk.Button(top, text="Issue Book", command=issueb).pack(pady=10)
    
# Submit Book
def submitb():
    name = submitter_name.get()
    regno = registration_number.get()
    bcode =book_code.get()
    today = date.today()

    data = (name, regno, bcode, today)
    sql = "INSERT INTO submit VALUES(%s, %s, %s, %s)"

    try:
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
        
        message.showinfo(f"Book submitted by: {name}")
        bookup(bcode, 1)
        top.destroy()
    except Error as e:
        message.showerror("Database Error: ", str(e))

def open_submitbook_window():
    global top, submitter_name, registration_number, book_code
    top = tk.Toplevel(root)
    top.title("Submit Book")

    tk.Label(top, text="Submitter name").pack()
    submitter_name = tk.Entry(top)
    submitter_name.pack()

    tk.Label(top, text="Registration number").pack()
    registration_number = tk.Entry(top)
    registration_number.pack()

    tk.Label(top, text="Book code").pack()
    book_code = tk.Entry(top)
    book_code.pack()

    tk.Button(top, text="Submit Book", command=submitb).pack(pady=10)
    
# Update book count
def bookup(bcode, change):
    sql = "SELECT TOTAL FROM books WHERE BCODE=%s"
    data = (bcode,)
    cur = con.cursor()
    cur.execute(sql, data)
    result = cur.fetchone()

    if result:
        new_total = result[0] + change

        if new_total<0:
            message.showwarning(f"Stock unavailable whose book code is: {bcode}")
            return
        update_sql = "UPDATE books SET TOTAL=%s WHERE BCODE=%s"
        up = (new_total, bcode)
        cur.execute(update_sql, up)
        con.commit()
    else:
        message.showerror("No such book exists in library. Please check the Book Code again.")

# Delete Book
def dbook():
    global delete_book_code, top
    bcode = delete_book_code.get()
    sql = "DELETE FROM books WHERE BCODE=%s"
    data = (bcode,)
    try:
        cur = con.cursor()
        cur.execute(sql, data)
        con.commit()
        if cur.rowcount > 0:
            message.showinfo("Success", "Book deleted successfully.")
        else:
            message.showwarning("Warning", f"No book with code '{bcode}' exists")
        top.destroy()
    except Error as e:
        message.showerror("Database error", str(e))

def open_deletebook_window():
    global top, delete_book_code
    top = tk.Toplevel(root)
    top.title("Delete Book")

    tk.Label(top, text="Book Code to Delete").pack()
    delete_book_code = tk.Entry(top)
    delete_book_code.pack()

    tk.Button(top, text="Delete Book", command=dbook).pack(pady=10)

# Display All Books
def dispbook():
    top=tk.Toplevel(root)
    top.title("Display Books")
    
    sql = "SELECT * FROM books"
    cur = con.cursor()
    cur.execute(sql)
    result = cur.fetchall()

    for i in result:
        tk.Label(top,text=f"Book name: {i[0]}, Book Code: {i[1]}, Total: {i[2]}, Subject: {i[3]}").pack()
        
# Main Menu
def main():
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Library Management : Main Menu")
    root.geometry("350x350")

    tk.Label(root,text="Library Manager",font=("Times New Roman", 20 , "bold")).pack(pady=15)

    tk.Button(root, text="Add Book", width=25, command=open_addbook_window).pack(pady=5)
    tk.Button(root, text="Issue Book", width=25, command=open_issuebook_window).pack(pady=5)
    tk.Button(root, text="Submit Book", width=25, command=open_submitbook_window).pack(pady=5)
    tk.Button(root, text="Delete Book", width=25, command=open_deletebook_window).pack(pady=5)
    tk.Button(root, text="Display All Books", width=25, command=dispbook).pack(pady=5)
    tk.Button(root, text="Exit", width=25, command=root.destroy).pack(pady=5)
    
    
    
# Password Check
def pswd():
    ps = simpledialog.askstring("Password","Enter password: ",show='*')
    if ps == "Lib@1234":
        main()
    else:
        message.showerror("Error:"," Wrong Password. Try again!!")
        root.after(100,pswd)
    

# Start the Program
pswd()
root.mainloop()
