import random  # Import random for generating payment_id
from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector

class AdminLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("400x300+600+250")

        # Variables
        self.username = StringVar()
        self.password = StringVar()

        # Login Frame
        login_frame = Frame(self.root, bd=4, relief=RIDGE, padx=10, pady=10)
        login_frame.place(x=50, y=50, width=300, height=200)

        # Title
        lbl_title = Label(login_frame, text="Admin Login", font=("Arial", 20, "bold"))
        lbl_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Username
        lbl_user = Label(login_frame, text="Username", font=("Arial", 12))
        lbl_user.grid(row=1, column=0, sticky=W, pady=5)
        entry_user = Entry(login_frame, textvariable=self.username, font=("Arial", 12))
        entry_user.grid(row=1, column=1, pady=5)

        # Password
        lbl_pass = Label(login_frame, text="Password", font=("Arial", 12))
        lbl_pass.grid(row=2, column=0, sticky=W, pady=5)
        entry_pass = Entry(login_frame, textvariable=self.password, font=("Arial", 12), show="*")
        entry_pass.grid(row=2, column=1, pady=5)

        # Login Button
        btn_login = Button(login_frame, text="Login", font=("Arial", 12, "bold"), command=self.verify_login)
        btn_login.grid(row=3, column=0, columnspan=2, pady=20)

    def verify_login(self):
        if self.username.get() == "admin" and self.password.get() == "passwd":
            self.root.destroy()
            root = Tk()
            ManagePay(root)
            root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")


class ManagePay:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Payments")
        self.root.geometry("1295x580+230+220")

        # Variables
        self.var_owner_id = StringVar()
        self.var_tenant_id = StringVar()
        self.var_bill_amount = StringVar()
        self.var_month = StringVar()
        self.var_year = StringVar()
        self.var_payment_status = StringVar(value="Pending")
        self.var_payment_date = StringVar()

        # Title
        lbl_title = Label(self.root, text="Manage Payments", font=("Arial", 32, "bold"),
                          bg="black", fg="silver", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=70)

        # Payment Details Label Frame
        labelframe_left = LabelFrame(self.root, text="Payment Details", font=("Arial", 12, "bold"),
                                     padx=2, bd=2, relief=RIDGE)
        labelframe_left.place(x=5, y=70, width=425, height=490)

        # Owner ID
        lbl_owner_id = Label(labelframe_left, text="Owner ID", font=("Arial", 12), padx=2, pady=6)
        lbl_owner_id.grid(row=1, column=0, sticky=W)
        self.combo_owner_id = ttk.Combobox(labelframe_left, textvariable=self.var_owner_id, font=("Arial", 12), width=27)
        self.combo_owner_id.grid(row=1, column=1)
        self.fetch_owners()

        # Tenant ID
        lbl_tenant_id = Label(labelframe_left, text="Tenant ID", font=("Arial", 12), padx=2, pady=6)
        lbl_tenant_id.grid(row=2, column=0, sticky=W)
        self.combo_tenant_id = ttk.Combobox(labelframe_left, textvariable=self.var_tenant_id, font=("Arial", 12), width=27)
        self.combo_tenant_id.grid(row=2, column=1)
        self.fetch_tenants()

        # Bill Amount
        lbl_bill_amount = Label(labelframe_left, text="Bill Amount", font=("Arial", 12), padx=2, pady=6)
        lbl_bill_amount.grid(row=3, column=0, sticky=W)
        entry_bill_amount = ttk.Entry(labelframe_left, textvariable=self.var_bill_amount, width=29, font=("Arial", 13, "bold"))
        entry_bill_amount.grid(row=3, column=1)

        # Month
        lbl_month = Label(labelframe_left, text="Month", font=("Arial", 12), padx=2, pady=6)
        lbl_month.grid(row=4, column=0, sticky=W)
        entry_month = ttk.Entry(labelframe_left, textvariable=self.var_month, width=29, font=("Arial", 13, "bold"))
        entry_month.grid(row=4, column=1)

        # Year
        lbl_year = Label(labelframe_left, text="Year", font=("Arial", 12), padx=2, pady=6)
        lbl_year.grid(row=5, column=0, sticky=W)
        entry_year = ttk.Entry(labelframe_left, textvariable=self.var_year, width=29, font=("Arial", 13, "bold"))
        entry_year.grid(row=5, column=1)

        # Payment Status
        lbl_payment_status = Label(labelframe_left, text="Payment Status", font=("Arial", 12), padx=2, pady=6)
        lbl_payment_status.grid(row=6, column=0, sticky=W)
        self.combo_payment_status = ttk.Combobox(labelframe_left, textvariable=self.var_payment_status, font=("Arial", 12), width=27, state='readonly')
        self.combo_payment_status["values"] = ("Pending", "Paid", "Overdue")
        self.combo_payment_status.grid(row=6, column=1)

        # Payment Date
        lbl_payment_date = Label(labelframe_left, text="Payment Date", font=("Arial", 12), padx=2, pady=6)
        lbl_payment_date.grid(row=7, column=0, sticky=W)
        entry_payment_date = ttk.Entry(labelframe_left, textvariable=self.var_payment_date, width=29, font=("Arial", 13, "bold"))
        entry_payment_date.grid(row=7, column=1)

        # Button Frame
        btn_frame = Frame(labelframe_left, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=400, width=412, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("Arial", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="Reset", command=self.reset, font=("Arial", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=1, padx=1)

        # Table Frame for Viewing Records
        Table_Frame = Frame(self.root, bd=4, relief=RIDGE)
        Table_Frame.place(x=435, y=70, width=860, height=490)

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.Payment_Table = ttk.Treeview(Table_Frame, columns=("payment_id", "owner_id", "tenant_id", "bill_amount", "month", "year", "payment_status", "payment_date"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Payment_Table.xview)
        scroll_y.config(command=self.Payment_Table.yview)

        self.Payment_Table.heading("payment_id", text="Payment ID")
        self.Payment_Table.heading("owner_id", text="Owner ID")
        self.Payment_Table.heading("tenant_id", text="Tenant ID")
        self.Payment_Table.heading("bill_amount", text="Bill Amount")
        self.Payment_Table.heading("month", text="Month")
        self.Payment_Table.heading("year", text="Year")
        self.Payment_Table.heading("payment_status", text="Status")
        self.Payment_Table.heading("payment_date", text="Payment Date")

        self.Payment_Table["show"] = "headings"
        for col in ("payment_id", "owner_id", "tenant_id", "bill_amount", "month", "year", "payment_status", "payment_date"):
            self.Payment_Table.column(col, width=100)

        self.Payment_Table.pack(fill=BOTH, expand=1)
        self.fetch_data()
        self.reset()

    def fetch_owners(self):
        """Fetch owner IDs for dropdown."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT owner_id FROM owner")
            rows = my_cursor.fetchall()
            conn.close()
            owner_options = [row[0] for row in rows]
            self.combo_owner_id["values"] = owner_options
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load owners: {str(e)}", parent=self.root)

    def fetch_tenants(self):
        """Fetch tenant IDs for dropdown."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT tenant_id FROM tenant")
            rows = my_cursor.fetchall()
            conn.close()
            tenant_options = [row[0] for row in rows]
            self.combo_tenant_id["values"] = tenant_options
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tenants: {str(e)}", parent=self.root)

    def generate_payment_id(self):
        """Generates a random payment ID."""
        return str(random.randint(1000, 9999))

    def add_data(self):
        """Adds a new payment record to the database."""
        payment_id = self.generate_payment_id()  # Generate random payment ID

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
            my_cursor = conn.cursor()
            query = """
                INSERT INTO manage_pay (payment_id, owner_id, tenant_id, bill_amount, month, year, payment_status, payment_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                payment_id,
                self.var_owner_id.get(),
                self.var_tenant_id.get(),
                self.var_bill_amount.get(),
                self.var_month.get(),
                self.var_year.get(),
                self.var_payment_status.get(),
                self.var_payment_date.get()
            )
            my_cursor.execute(query, values)
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Payment record added successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error adding payment record: {str(e)}", parent=self.root)

    def reset(self):
        """Resets all input fields."""
        self.var_owner_id.set("")
        self.var_tenant_id.set("")
        self.var_bill_amount.set("")
        self.var_month.set("")
        self.var_year.set("")
        self.var_payment_status.set("Pending")
        self.var_payment_date.set("")

    def fetch_data(self):
        """Fetches all payment records from the database and displays them in the Treeview."""
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM manage_pay")
        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.Payment_Table.delete(*self.Payment_Table.get_children())
            for row in rows:
                self.Payment_Table.insert("", END, values=row)
        conn.close()


if __name__ == "__main__":
    root = Tk()
    obj = AdminLogin(root)
    root.mainloop()
