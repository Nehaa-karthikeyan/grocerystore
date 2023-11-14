import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import customtkinter
import mysql.connector
from PIL import Image, ImageTk



# Declare global variables for Tkinter elements
prod_name_entry = None
prod_price_entry = None
date_entry = None
product_name_entry = None
custName = None
# Added to fix the NameEntry for customers
entries = []  # Moved to the global scope

def fetch_items_from_database():
    items = []
    try:
        db = mysql.connector.connect(
            user="root",
            password="root",
            host="localhost",
            database="shop"
        )
        cursor = db.cursor()
        cursor.execute("SELECT item_name, price FROM items_table")
        items = cursor.fetchall()
        db.close()
    except Exception as e:
        print("Error fetching items from the database:", e)
    return items

def view_items():
    global items_window  # Access the global items_window
    items_window = tk.Toplevel()
    items_window.title("Available Items")

    image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/1000_F_203147182_a4bIFcRWzkriKrqGKl8VXAakDpxyq0CG.png")

    # Get the image dimensions
    image_width = image.width()
    image_height = image.height()

    # Set the window size to match the image dimensions
    items_window.geometry(f"{image_width}x{image_height}")

    items_list = fetch_items_from_database()

    items_label = tk.Label(items_window, text="Available Items:", font=('calibri', 12, 'bold'))
    items_label.pack()

    # Create a Treeview widget for the table
    tree = ttk.Treeview(items_window, columns=("Item", "Price (in rupees)"))
    tree.heading("#1", text="Item")
    tree.heading("#2", text="Price (in rupees)")
    tree.pack()

    for item, price in items_list:
        tree.insert("", "end", values=(item, price))

    items_window.mainloop()

# Function to add the product to the database
def add_product():
    pname = prod_name_entry.get()
    price = prod_price_entry.get()
    dt = date_entry.get()
    
    db = mysql.connector.connect(user="root", passwd="root", host="localhost", database='Shop')
    cursor = db.cursor()
    
    query = "INSERT INTO products (date, prodName, prodPrice) VALUES (%s, %s, %s)"
    details = (dt, pname, price)
    
    try:
        cursor.execute(query, details)
        db.commit()
        messagebox.showinfo('Success', 'Product added successfully')
    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Error", "Trouble adding data into Database")
    
    wn.destroy()

# Function to remove the product from the database
def remove_product():
    name = product_name_entry.get().lower()
    
    db = mysql.connector.connect(user="root", passwd="root", host="localhost", database='Shop')
    cursor = db.cursor()
    
    query = f"DELETE FROM products WHERE LOWER(prodName) = '{name}'"
    
    try:
        cursor.execute(query)
        db.commit()
        messagebox.showinfo('Success', 'Product Record Deleted Successfully')
    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Please check Product Name")
    
    wn.destroy()

# Function to show all the products in the database
def view_products():
    wn = tk.Toplevel()
    wn.title("PythonGeeks Shop Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")
    image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/apples-on-table-1200x800.png")

    # Get the image dimensions
    image_width = image.width()
    image_height = image.height()

    # Set the window size to match the image dimensions
    wn.geometry(f"{image_width}x{image_height}")

    # Create a label with the image and place it in the center of the window
    image_label = tk.Label(wn, image=image)
    image_label.pack(fill='both', expand=True)
    
    headingFrame1 = tk.Frame(wn, bg='old lace', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = tk.Label(headingFrame1, text="View Products", fg='black', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    labelFrame = tk.Frame(wn)
    labelFrame.place(relx=0.25, rely=0.3, relwidth=0.5, relheight=0.5)
    y = 0.25
    
    db = mysql.connector.connect(user="root", passwd="root", host="localhost", database='Shop')
    cursor = db.cursor()
    
    query = 'SELECT * FROM products'
    
    tk.Label(labelFrame, text="%-50s%-50s%-50s" % ('Date', 'Product', 'Price'), font=('calibri', 11, 'bold'), fg='black').place(relx=0.07, rely=0.1)
    tk.Label(labelFrame, text="----------------------------------------------------------------------------", fg='black').place(relx=0.05, rely=0.2)
    
    try:
        cursor.execute(query)
        res = cursor.fetchall()
        
        for i in res:
            tk.Label(labelFrame, text="%-50s%-50s%-50s" % (i[0], i[1], i[2]), fg='black').place(relx=0.07, rely=y)
            y += 0.1
    except Exception as e:
        print("The exception is:", e)
        messagebox.showinfo("Failed to fetch files from database")
    
    quit_button = tk.Button(wn, text="Quit", bg='#f7f1e3', fg='black', command=wn.destroy)
    quit_button.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)
    
    wn.mainloop()

def calculate_total(quantity, price):
    try:
        qty = int(quantity)
        price = int(price)
        return qty * price
    except ValueError:
        return 0

def bill():
    date = date_entry.get()
    cust_name = custName.get()
    total_bill = 0

    wn = tk.Toplevel()
    wn.title("PythonGeeks Shop Management System")
    wn.configure(bg='lavender blush2')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    headingFrame1 = tk.Frame(wn, bg="lavender blush2", bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
    headingLabel = tk.Label(headingFrame1, text="Bill", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = tk.Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    y = 0.35
    tk.Label(labelFrame, text="%-40s%-40s%-40s%-40s" % ('Product', 'Price', 'Quantity', 'Total'), font=('calibri', 11, 'bold'), fg='black').place(relx=0.07, rely=0.2)

    db = mysql.connector.connect(user="root", passwd="root", host="localhost", database='Shop')
    cursor = db.cursor()
    query = 'SELECT * FROM products'
    cursor.execute(query)
    res = cursor.fetchall()

    for i, entry in enumerate(entries):
        quantity = entry.get()
        if i < len(res) and quantity:
            product = res[i]
            total = calculate_total(quantity, product[2])
            tk.Label(labelFrame, text="%-40s%-40s%-40s%-40s" % (product[1], product[2], quantity, total), fg='black').place(relx=0.07, rely=y)
            total_bill += total
            y += 0.1
            query = "INSERT INTO sale(custName, date, prodName, qty, price) VALUES(%s, %s, %s, %s, %s)"
            details = (cust_name, date, product[1], quantity, total)
            cursor.execute(query, details)

    db.commit()
    db.close()

    total_label = tk.Label(labelFrame, text="%-40s%-40s%-40s%-40s" % ("", "", "Total Amount:", total_bill), font=('calibri', 11, 'bold'), fg='black')
    total_label.place(relx=0.07, rely=y + 0.1)  # Adjusted y position

    quit_button = tk.Button(wn, text="Quit", bg='snow', fg='black', command=wn.destroy)
    quit_button.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.08)

    wn.mainloop()

def newCust():
    global wn, date_entry, custName
    wn = tk.Tk()
    wn.title("PythonGeeks Shop Management System")
    wn.configure(bg='lavender blush2')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    
    
    headingFrame1 = tk.Frame(wn, bg="lavender blush2", bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
    headingLabel = tk.Label(headingFrame1, text="New Customer", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    label1 = tk.Label(wn, text="Date:", fg='black')
    label1.place(relx=0.05, rely=0.3)
    
    date_entry = tk.Entry(wn)
    date_entry.place(relx=0.3, rely=0.3, relwidth=0.62)
    
    label2 = tk.Label(wn, text="Customer Name:", fg='black')
    label2.place(relx=0.05, rely=0.4)
    
    custName = tk.Entry(wn)  # Fixed the name of the Entry widget
    custName.place(relx=0.3, rely=0.4, relwidth=0.62)
    
    labelFrame = tk.Frame(wn)
    labelFrame.place(relx=0.1, rely=0.45, relwidth=0.8, relheight=0.4)
    
    y = 0.3
    tk.Label(labelFrame, text="Please enter the quantity of the products you want to buy", font=('calibri', 11, 'bold'), fg='black').place(relx=0.07, rely=0.1)
    
    tk.Label(labelFrame, text="%-50s%-50s%-30s" % ('Product', 'Price', 'Quantity'), font=('calibri', 11, 'bold'), fg='black').place(relx=0.07, rely=0.2)
    
    db = mysql.connector.connect(user="root", passwd="root", host="localhost", database='Shop')
    cursor = db.cursor()
    query = 'SELECT * FROM products'
    cursor.execute(query)
    res = cursor.fetchall()
    
    for product in res:
        tk.Label(labelFrame, text="%-50s%-50s" % (product[1], product[2]), fg='black').place(relx=0.07, rely=y)
        entry = tk.Entry(labelFrame)
        entry.place(relx=0.6, rely=y, relwidth=0.2)
        entries.append(entry)  # Append the Entry widget to the list
        y += 0.1
    
    generate_bill_button = tk.Button(wn, text="Generate Bill", bg='#007FFF', fg='black', command=bill)
    generate_bill_button.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)
    
    quit_button = tk.Button(wn, text="Quit", bg='#007FFF', fg='black', command=wn.destroy)
    quit_button.place(relx=0.55, rely=0.9, relwidth=0.18, relheight=0.08)
    
    db.close()
    
    wn.mainloop()

# Function to manage the main menu


def manage_menu():
    wn = tk.Toplevel()
    wn.title("PythonGeeks Shop Management System")
    wn.configure(bg='linen')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    # Load the image
    image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/photo-1458917524587-d3236cc8c2c8.png")
    image_width = image.width()
    image_height = image.height()

    # Set the window size to match the image dimensions
    wn.geometry(f"{image_width}x{image_height}")
    image_label = tk.Label(wn, image=image)
    image_label.pack(fill='both', expand=True)

    # Heading
    headingFrame1 = tk.Frame(wn, bg='grey19', bd=5)
    headingFrame1.place(relx=0.4, rely=0.05, relwidth=0.2, relheight=0.1)
    heading_image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/ea1602_70c9cc97dee742cea812bb4dd4fabc47~mv2.png")
    heading_image_label = tk.Label(headingFrame1, image=heading_image)
    heading_image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    # Buttons without gaps
    add_product_button = tk.Button(wn, text="Add Product", bg='#F5F5DC', fg='black', command=add_product_window)
    add_product_button.place(relx=0.28, rely=0.25, relwidth=0.4, relheight=0.1)

    remove_product_button = tk.Button(wn, text="Remove Product", bg='#FFE4C4', fg='black', command=remove_product_window)
    remove_product_button.place(relx=0.28, rely=0.36, relwidth=0.4, relheight=0.1)

    view_products_button = tk.Button(wn, text="View Products", bg='#EED5B7', fg='black', command=view_products)
    view_products_button.place(relx=0.28, rely=0.47, relwidth=0.4, relheight=0.1)

    view_items_button = tk.Button(wn, text="View Items", command=view_items, bg='#f7f1e3', fg='black')
    view_items_button.place(relx=0.28, rely=0.58, relwidth=0.4, relheight=0.1)

    new_customer_button = tk.Button(wn, text="New Customer", bg='#8B7D6B', fg='black', command=newCust)
    new_customer_button.place(relx=0.28, rely=0.69, relwidth=0.4, relheight=0.1)

    quit_button = tk.Button(wn, text="Quit", bg='snow', fg='black', command=wn.destroy)
    quit_button.place(relx=0.28, rely=0.8, relwidth=0.4, relheight=0.1)

    wn.mainloop()

# Function to add a product window
# Function to open the "Add Product" window
def add_product_window():
    global prod_name_entry, prod_price_entry, date_entry
    wn = tk.Toplevel()
    wn.title("PythonGeeks Shop Management System")
    wn.configure(bg='mint cream')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    # Load the image
    image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/1000_F_203147182_a4bIFcRWzkriKrqGKl8VXAakDpxyq0CG.png")

    # Get the image dimensions
    image_width = image.width()
    image_height = image.height()

    # Set the window size to match the image dimensions
    wn.geometry(f"{image_width}x{image_height}")

    # Create a label with the image and place it in the center of the window
    image_label = tk.Label(wn, image=image)
    image_label.pack(fill='both', expand=True)

    headingFrame1 = tk.Frame(wn, bg='old lace', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.13)
    headingLabel = tk.Label(headingFrame1, text="Add Product", fg='black', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)

    labelFrame = tk.Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)

    prod_name_label = tk.Label(labelFrame, text="Product Name : ", bg='black', fg='white', font=('calibri', 11, 'bold'))
    prod_name_label.place(relx=0.05, rely=0.2)
    prod_name_entry = tk.Entry(labelFrame, font=('calibri', 11))
    prod_name_entry.place(relx=0.3, rely=0.2, relwidth=0.62)

    prod_price_label = tk.Label(labelFrame, text="Product Price : ", bg='black', fg='white', font=('calibri', 11, 'bold'))
    prod_price_label.place(relx=0.05, rely=0.4)
    prod_price_entry = tk.Entry(labelFrame, font=('calibri', 11))
    prod_price_entry.place(relx=0.3, rely=0.4, relwidth=0.62)

    date_label = tk.Label(labelFrame, text="Date : ", bg='black', fg='white', font=('calibri', 11, 'bold'))
    date_label.place(relx=0.05, rely=0.6)
    date_entry = tk.Entry(labelFrame, font=('calibri', 11))
    date_entry.place(relx=0.3, rely=0.6, relwidth=0.62)

    add_product_button = tk.Button(wn, text="Add Product", bg='light goldenrod', fg='black', command=add_product)
    add_product_button.place(relx=0.3, rely=0.85, relwidth=0.18, relheight=0.08)

    wn.mainloop()

# Function to remove a product window
def remove_product_window():
    global product_name_entry
    wn = tk.Toplevel()
    wn.title("PythonGeeks Shop Management System")
    wn.configure(bg='linen')
    wn.minsize(width=500, height=500)
    wn.geometry("700x600")

    image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/blur-blurred-close-up-confection.png")

    # Get the image dimensions
    image_width = image.width()
    image_height = image.height()

    # Set the window size to match the image dimensions
    wn.geometry(f"{image_width}x{image_height}")

    # Create a label with the image and place it in the center of the window
    image_label = tk.Label(wn, image=image)
    image_label.pack(fill='both', expand=True)
    
    headingFrame1 = tk.Frame(wn, bg="linen", bd=5)
    headingFrame1.place(relx=0.2, rely=0.1, relwidth=0.6, relheight=0.16)
    headingLabel = tk.Label(headingFrame1, text="Remove Product", fg='grey19', font=('Courier', 15, 'bold'))
    headingLabel.place(relx=0, rely=0, relwidth=1, relheight=1)
    
    labelFrame = tk.Frame(wn)
    labelFrame.place(relx=0.1, rely=0.3, relwidth=0.8, relheight=0.5)
    
    product_name_label = tk.Label(labelFrame, text="Product Name : ", bg='black', fg='white', font=('calibri', 11, 'bold'))
    product_name_label.place(relx=0.05, rely=0.2)
    product_name_entry = tk.Entry(labelFrame, font=('calibri', 11))
    product_name_entry.place(relx=0.3, rely=0.2, relwidth=0.62)
    
    # Remove Product Button
    remove_product_button = tk.Button(wn, text="Remove Product", bg='snow', fg='black', command=remove_product)
    remove_product_button.place(relx=0.3, rely=0.85, relwidth=0.18, relheight=0.08)
    
    wn.mainloop()



def main_menu_window():
    wn = tk.Tk()
    wn.title("PythonGeeks Shop Management System")
    wn.configure(bg='grey19')
    wn.minsize(width=400, height=400)
    wn.geometry("700x600")

    # Load the image
    image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/nk.png")
    login_btn = tk.PhotoImage(file='C:/Users/nahaa/Desktop/click-me-button-flat (1).png')
    quit_but = tk.PhotoImage(file="C:/Users/nahaa/Desktop/bye.png")

    # Get the image dimensions
    image_width = image.width()
    image_height = image.height()

    # Set the window size to match the image dimensions
    wn.geometry(f"{image_width}x{image_height}")

    # Create a label with the image and place it in the center of the window
    image_label = tk.Label(wn, image=image)
    image_label.pack(fill='both', expand=True)

    headingFrame1 = tk.Frame(wn, bg='grey19', bd=5)
    headingFrame1.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.25)
    heading_image = tk.PhotoImage(file="C:/Users/nahaa/Desktop/—Pngtree—order now banner_6958783.png")
    heading_image_label = tk.Label(headingFrame1, image=heading_image)
    heading_image_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    view_items_button = tk.Button(wn, text="View Items", command=view_items, bg='#f7f1e3', fg='black')
    view_items_button.place(relx=0.36, rely=0.4, relwidth=0.30, relheight=0.1)

    manage_menu_button = tk.Button(wn, image=login_btn, command=manage_menu, bg='#f7f1e3', fg='black')
    manage_menu_button.place(relx=0.36, rely=0.4, relwidth=0.30, relheight=0.1)

    quit_button = tk.Button(wn,image=quit_but, command=wn.destroy, bg='snow', fg='black')
    quit_button.place(relx=0.4, rely=0.9, relwidth=0.18, relheight=0.09)

    wn.mainloop()

main_menu_window()


# Create the main menu window
