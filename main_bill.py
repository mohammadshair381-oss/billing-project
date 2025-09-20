from tkinter import *
from tkinter import messagebox, simpledialog
import random
import os
import tempfile
import smtplib

def get_next_bill_number():
    if not os.path.exists("bills"):
        os.makedirs("bills")
    bills = [int(f.split('.')[0]) for f in os.listdir('bills') if f.endswith('.txt') and f.split('.')[0].isdigit()]
    return max(bills, default=500) + 1

billnumber = get_next_bill_number()

def more_options_window():
    more_win = Toplevel(root)
    more_win.title("More Options")
    more_win.geometry("500x400")
    more_win.config(bg="#313239")

    def return_bill():
        if textarea.get(1.0, END).strip():
            refunded_total = round(totalbill * 0.8)
            messagebox.showinfo("Return Processed", f"80% Refund Processed: ₹{refunded_total}")
        else:
            messagebox.showerror("Error", "No bill to refund.")

    def adjust_inventory():
        inv_win = Toplevel(more_win)
        inv_win.title("Adjust Inventory")
        inv_win.geometry("400x400")
        inv_win.config(bg="#313239")

        Label(inv_win, text="Select Category", bg="#313239", fg="white", font=("arial", 12)).pack()
        category = StringVar(inv_win)
        category.set("Cosmetics")
        OptionMenu(inv_win, category, "Cosmetics", "Grocery", "Cold Drinks").pack(pady=5)

        Label(inv_win, text="Product Name:", bg="#313239", fg="white").pack()
        pname = Entry(inv_win)
        pname.pack()

        Label(inv_win, text="New Quantity:", bg="#313239", fg="white").pack()
        pqty = Entry(inv_win)
        pqty.pack()

        Label(inv_win, text="New Price:", bg="#313239", fg="white").pack()
        pprice = Entry(inv_win)
        pprice.pack()

        def apply_changes():
            messagebox.showinfo("Updated", f"{pname.get()} updated with Qty: {pqty.get()}, Price: {pprice.get()} in {category.get()}")
            inv_win.destroy()

        Button(inv_win, text="Apply", command=apply_changes).pack(pady=10)

    def search_by_name_or_phone():
        term = simpledialog.askstring("Search Bill", "Enter customer name or phone number:")
        if not term:
            return
        for file in os.listdir('bills/'):
            with open(f'bills/{file}', 'r') as f:
                if term.lower() in f.read().lower():
                    textarea.delete(1.0, END)
                    f.seek(0)
                    textarea.insert(END, f.read())
                    return
        messagebox.showerror("Not Found", "No bill found for this customer.")

    Button(more_win, text="Return Bill (80%)", font=("arial", 14), width=25, command=return_bill).pack(pady=10)
    Button(more_win, text="Adjust Inventory", font=("arial", 14), width=25, command=adjust_inventory).pack(pady=10)
    Button(more_win, text="Search by Name/Phone", font=("arial", 14), width=25, command=search_by_name_or_phone).pack(pady=10)

def focus_next_widget(event):
    event.widget.tk_focusNext().focus()
    return "break"

# GUI Setup
root = Tk()
root.title("Retail Billing System")
root.geometry("1270x685")
root.config(bg="#313239")
root.bind_all("<Return>", focus_next_widget)
root.bind_all("<Down>", focus_next_widget)
root.bind_all("<Right>", focus_next_widget)

heading = Label(root, text="V.K.M. BILLING SYSTEM", font=("times new roman", 25, "bold"), bg="#313239", fg="#ffee08", bd=12, relief=GROOVE)
heading.pack(fill=X)
# Customer Details Frame
customer_frame = LabelFrame(root, text="Customer Details", font=("times new roman", 14, "bold"), fg="#ffee08", bd=8, relief=GROOVE, bg="#313239")
customer_frame.pack(fill=X)

Label(customer_frame, text="Name", font=("times new roman", 14, "bold"), bg="#313239", fg="white").grid(row=0, column=0, padx=20, pady=2)
nameEntry = Entry(customer_frame, font=("arial", 14), bd=7, width=18)
nameEntry.grid(row=0, column=1, padx=8)

Label(customer_frame, text="Phone", font=("times new roman", 14, "bold"), bg="#313239", fg="white").grid(row=0, column=2, padx=20)
phoneEntry = Entry(customer_frame, font=("arial", 14), bd=7, width=18)
phoneEntry.grid(row=0, column=3, padx=8)

Label(customer_frame, text="Bill No.", font=("times new roman", 14, "bold"), bg="#313239", fg="white").grid(row=0, column=4, padx=20)
billnumberEntry = Entry(customer_frame, font=("arial", 14), bd=7, width=18)
billnumberEntry.insert(0, str(billnumber))
billnumberEntry.grid(row=0, column=5, padx=8)

Button(customer_frame, text="SEARCH", font=("arial", 12, "bold"), bd=7, width=10, command=lambda: search_by_name_or_phone()).grid(row=0, column=6, padx=20, pady=8)

# Product Section Frame
productsFrame = Frame(root)
productsFrame.pack()

# Cosmetics
cosmeticsFrame = LabelFrame(productsFrame, text="Cosmetics", font=("times new roman", 14, "bold"), fg="#ffee08", bd=8, relief=GROOVE, bg="#313239")
cosmeticsFrame.grid(row=0, column=0, padx=10)
Label(cosmeticsFrame, text="Bath Soap", font=("times new roman", 14), bg="#313239", fg="white").grid(row=0, column=0, pady=5)
bathsoapEntry = Entry(cosmeticsFrame, font=("times new roman", 14), width=10, bd=5)
bathsoapEntry.grid(row=0, column=1, padx=10)
bathsoapEntry.insert(0, 0)

# Grocery
groceryFrame = LabelFrame(productsFrame, text="Grocery", font=("times new roman", 14, "bold"), fg="#ffee08", bd=8, relief=GROOVE, bg="#313239")
groceryFrame.grid(row=0, column=1, padx=10)
Label(groceryFrame, text="Rice", font=("times new roman", 14), bg="#313239", fg="white").grid(row=0, column=0, pady=5)
RiceEntry = Entry(groceryFrame, font=("times new roman", 14), width=10, bd=5)
RiceEntry.grid(row=0, column=1, padx=10)
RiceEntry.insert(0, 0)

# Cold Drinks
coldFrame = LabelFrame(productsFrame, text="Cold Drinks", font=("times new roman", 14, "bold"), fg="#ffee08", bd=8, relief=GROOVE, bg="#313239")
coldFrame.grid(row=0, column=2, padx=10)
Label(coldFrame, text="Maaza", font=("times new roman", 14), bg="#313239", fg="white").grid(row=0, column=0, pady=5)
MaazaEntry = Entry(coldFrame, font=("times new roman", 14), width=10, bd=5)
MaazaEntry.grid(row=0, column=1, padx=10)
MaazaEntry.insert(0, 0)

# Bill Area Frame
billframe = Frame(productsFrame, bd=8, relief=GROOVE)
billframe.grid(row=0, column=3, padx=10)
Label(billframe, text="Bill Area", font=("times new roman", 14, "bold"), bd=7, relief=GROOVE).pack(fill=X)

scrollbar = Scrollbar(billframe, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

textarea = Text(billframe, height=18, width=50, yscrollcommand=scrollbar.set)
textarea.pack()
scrollbar.config(command=textarea.yview)
# Bill Menu Frame
billmenuFrame = LabelFrame(root, text="Bill Menu", font=("times new roman", 14, "bold"), fg="#ffee08", bd=8, relief=GROOVE, bg="#313239")
billmenuFrame.pack(fill=X, pady=5)

# Button Frame inside Bill Menu
ButtonFrame = Frame(billmenuFrame, bd=8, relief=GROOVE)
ButtonFrame.grid(row=0, column=0)

# Example placeholders — connect to actual functions as needed
Button(ButtonFrame, text="Total", font=("arial", 16, "bold"), bg="#313239", fg="white", bd=5, width=8, pady=10).grid(row=0, column=0, padx=5)
Button(ButtonFrame, text="Bill", font=("arial", 16, "bold"), bg="#313239", fg="white", bd=5, width=8, pady=10).grid(row=0, column=1, padx=5)
Button(ButtonFrame, text="Email", font=("arial", 16, "bold"), bg="#313239", fg="white", bd=5, width=8, pady=10).grid(row=0, column=2, padx=5)
Button(ButtonFrame, text="Print", font=("arial", 16, "bold"), bg="#313239", fg="white", bd=5, width=8, pady=10).grid(row=0, column=3, padx=5)
Button(ButtonFrame, text="Clear", font=("arial", 16, "bold"), bg="#313239", fg="white", bd=5, width=8, pady=10).grid(row=0, column=4, padx=5)

# Return Button (80% Refund)
Button(ButtonFrame, text="Return", font=("arial", 16, "bold"), bg="#313239", fg="white", bd=5, width=8, pady=10,
       command=lambda: messagebox.showinfo("Return", f"80% Refund: ₹{round(totalbill * 0.8) if textarea.get(1.0, END).strip() else 0}")).grid(row=1, column=2, padx=5, pady=10)

# More Options Button (outside bill menu)
Button(root, text="More Options", font=("arial", 14, "bold"), bg="#ffee08", fg="black", bd=5, width=14, command=more_options_window).place(x=1100, y=20)

# Run the main GUI loop
root.mainloop()
