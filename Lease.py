from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from datetime import datetime
import random


class LeaseClass:

    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System - Lease Information")
        self.root.geometry("1295x580+230+220")

        # Variables
        self.var_lease_id = StringVar()
        self.var_tenant_id = StringVar()
        self.var_owner_id = StringVar()
        self.var_lease_start = StringVar()
        self.var_lease_end = StringVar()
        self.var_monthly_rent = StringVar()
        self.var_security_deposit = StringVar()
        self.var_search = StringVar()
        self.txt_search = StringVar()

        # Title
        lbl_title = Label(self.root, text="Lease Information", font=("times new roman", 32, "bold"),
                          bg="black", fg="silver", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=70)

        # Lease Details Label Frame
        labelframe_left = LabelFrame(self.root, text="Lease Details", font=("times new roman", 12, "bold"),
                                     padx=2, bd=2, relief=RIDGE)
        labelframe_left.place(x=5, y=70, width=425, height=490)

        # Lease ID Field (Read-Only with Auto-generated Value)
        Label(labelframe_left, text="Lease ID", font=("times new roman", 12), padx=2, pady=6).grid(row=0, column=0, sticky=W)
        self.entry_lease_id = ttk.Entry(labelframe_left, textvariable=self.var_lease_id, width=29, font=("times new roman", 13, "bold"), state='readonly')
        self.entry_lease_id.grid(row=0, column=1)

        # Tenant selection dropdown
        Label(labelframe_left, text="Select Tenant", font=("times new roman", 12), padx=2, pady=6).grid(row=1, column=0, sticky=W)
        self.combo_tenant = ttk.Combobox(labelframe_left, textvariable=self.var_tenant_id, font=("times new roman", 12), width=27, state='readonly')
        self.combo_tenant.grid(row=1, column=1)
        self.fetch_tenants()  # Populate the tenant combobox

        # Owner selection dropdown
        Label(labelframe_left, text="Select Owner", font=("times new roman", 12), padx=2, pady=6).grid(row=2, column=0, sticky=W)
        self.combo_owner = ttk.Combobox(labelframe_left, textvariable=self.var_owner_id, font=("times new roman", 12), width=27, state='readonly')
        self.combo_owner.grid(row=2, column=1)
        self.fetch_owners()  # Populate the owner combobox

        # Lease Dates and Financial Details
        Label(labelframe_left, text="Lease Start Date", font=("times new roman", 12), padx=2, pady=6).grid(row=3, column=0, sticky=W)
        ttk.Entry(labelframe_left, textvariable=self.var_lease_start, width=29, font=("times new roman", 13, "bold")).grid(row=3, column=1)

        Label(labelframe_left, text="Lease End Date", font=("times new roman", 12), padx=2, pady=6).grid(row=4, column=0, sticky=W)
        ttk.Entry(labelframe_left, textvariable=self.var_lease_end, width=29, font=("times new roman", 13, "bold")).grid(row=4, column=1)

        Label(labelframe_left, text="Monthly Rent", font=("times new roman", 12), padx=2, pady=6).grid(row=5, column=0, sticky=W)
        ttk.Entry(labelframe_left, textvariable=self.var_monthly_rent, width=29, font=("times new roman", 13, "bold")).grid(row=5, column=1)

        Label(labelframe_left, text="Security Deposit", font=("times new roman", 12), padx=2, pady=6).grid(row=6, column=0, sticky=W)
        ttk.Entry(labelframe_left, textvariable=self.var_security_deposit, width=29, font=("times new roman", 13, "bold")).grid(row=6, column=1)

        # Button Frame
        btn_frame = Frame(labelframe_left, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=400, width=412, height=40)
        Button(btn_frame, text="Add", command=self.add_data, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="Update", command=self.update, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="Delete", command=self.delt, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="Reset", command=self.reset, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=3, padx=1)

        # Search and Table Frame
        Table_Frame = LabelFrame(self.root, text="View Lease Details", font=("times new roman", 12, "bold"), padx=2, bd=2, relief=RIDGE)
        Table_Frame.place(x=435, y=70, width=860, height=490)

        Label(Table_Frame, text="Search By:", font=("times new roman", 20, "bold"), bg="black", fg="silver").grid(row=0, column=0, sticky=W, padx=2)
        combo_search = ttk.Combobox(Table_Frame, textvariable=self.var_search, font=("times new roman", 12), width=24, state='readonly')
        combo_search["value"] = ("", "tenant_id", "owner_id", "lease_id")
        combo_search.current(0)
        combo_search.grid(row=0, column=1, padx=2)

        txt_search = ttk.Entry(Table_Frame, textvariable=self.txt_search, width=24, font=("times new roman", 13, "bold"))
        txt_search.grid(row=0, column=2, padx=2)

        Button(Table_Frame, text="Search", command=self.search, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=3, padx=1)
        Button(Table_Frame, text="Show All", command=self.fetch_data, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=4, padx=1)

        # Table and Scrollbars
        details_table = Frame(Table_Frame, bd=2, relief=RIDGE)
        details_table.place(x=0, y=50, width=860, height=350)

        scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.Lease_Table = ttk.Treeview(details_table, columns=("lease_id", "tenant_id", "owner_id", "lease_start", "lease_end", "monthly_rent", "security_deposit"), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Lease_Table.xview)
        scroll_y.config(command=self.Lease_Table.yview)

        # Define Table Columns
        self.Lease_Table.heading("lease_id", text="Lease ID")
        self.Lease_Table.heading("tenant_id", text="Tenant ID")
        self.Lease_Table.heading("owner_id", text="Owner ID")
        self.Lease_Table.heading("lease_start", text="Start Date")
        self.Lease_Table.heading("lease_end", text="End Date")
        self.Lease_Table.heading("monthly_rent", text="Monthly Rent")
        self.Lease_Table.heading("security_deposit", text="Security Deposit")
        self.Lease_Table["show"] = "headings"

        # Set Column Widths
        for col in ("lease_id", "tenant_id", "owner_id", "lease_start", "lease_end", "monthly_rent", "security_deposit"):
            self.Lease_Table.column(col, width=100)

        self.Lease_Table.pack(fill=BOTH, expand=1)
        self.Lease_Table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()
        self.reset()  # Automatically generate a lease ID when the form loads

    def add_data(self):
        """Adds a new lease record to the database with date validation and auto-generated lease ID."""
        # Validate and format date inputs
        try:
            lease_start_date = datetime.strptime(self.var_lease_start.get(), "%Y-%m-%d").date()
            lease_end_date = datetime.strptime(self.var_lease_end.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.", parent=self.root)
            return

        if self.var_tenant_id.get() == "" or self.var_owner_id.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
                my_cursor = conn.cursor()

                # Auto-generate lease ID
                self.var_lease_id.set(str(random.randint(1000, 9999)))

                tenant_id = self.var_tenant_id.get().split(" - ")[0]
                owner_id = self.var_owner_id.get().split(" - ")[0]

                query = """
                    INSERT INTO lease (lease_id, tenant_id, owner_id, lease_start_date, lease_end_date, monthly_rent, security_deposit)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    self.var_lease_id.get(),
                    tenant_id,
                    owner_id,
                    lease_start_date,
                    lease_end_date,
                    self.var_monthly_rent.get(),
                    self.var_security_deposit.get()
                )
                my_cursor.execute(query, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Lease record added successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error adding record: {str(e)}", parent=self.root)

    def reset(self):
        """Resets all input fields to their default values and generates a new lease ID."""
        self.var_lease_id.set(str(random.randint(1000, 9999)))  # Auto-generate a new lease ID
        self.var_tenant_id.set("")
        self.var_owner_id.set("")
        self.var_lease_start.set("")
        self.var_lease_end.set("")
        self.var_monthly_rent.set("")
        self.var_security_deposit.set("")

    def fetch_data(self):
        """Fetches data from the lease table and displays it in the Treeview."""
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                       database="apartment_mang")
        my_cursor = conn.cursor()
        query = """
            SELECT lease.lease_id, lease.tenant_id, lease.owner_id, lease.lease_start_date, lease.lease_end_date,
                   lease.monthly_rent, lease.security_deposit
            FROM lease
            JOIN tenant ON lease.tenant_id = tenant.tenant_id
            JOIN owner ON lease.owner_id = owner.owner_id
        """
        my_cursor.execute(query)
        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.Lease_Table.delete(*self.Lease_Table.get_children())
            for row in rows:
                self.Lease_Table.insert("", END, values=row)
        conn.close()

    def get_cursor(self, event=""):
        """Gets the data from the selected row in the Treeview and populates the input fields."""
        cursor_row = self.Lease_Table.focus()
        content = self.Lease_Table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_lease_id.set(row[0])
            self.var_tenant_id.set(f"{row[1]} - {self.get_tenant_name(row[1])}")
            self.var_owner_id.set(f"{row[2]} - {self.get_owner_name(row[2])}")
            self.var_lease_start.set(row[3])
            self.var_lease_end.set(row[4])
            self.var_monthly_rent.set(row[5])
            self.var_security_deposit.set(row[6])

    def fetch_tenants(self):
        """Fetch tenant details to populate the tenant dropdown menu."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                           database="apartment_mang")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT tenant_id, first_name FROM tenant")
            rows = my_cursor.fetchall()
            conn.close()
            tenant_options = ["{} - {}".format(row[0], row[1]) for row in rows]
            self.combo_tenant["values"] = tenant_options
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tenants: {str(e)}", parent=self.root)

    def fetch_owners(self):
        """Fetch owner details to populate the owner dropdown menu."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                           database="apartment_mang")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT owner_id, first_name FROM owner")
            rows = my_cursor.fetchall()
            conn.close()
            owner_options = ["{} - {}".format(row[0], row[1]) for row in rows]
            self.combo_owner["values"] = owner_options
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load owners: {str(e)}", parent=self.root)

    def get_tenant_name(self, tenant_id):
        """Fetches the tenant's name based on the tenant_id, used for display in the dropdown."""
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                       database="apartment_mang")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT first_name FROM tenant WHERE tenant_id = %s", (tenant_id,))
        result = my_cursor.fetchone()
        conn.close()
        return result[0] if result else ""

    def get_owner_name(self, owner_id):
        """Fetches the owner's name based on the owner_id, used for display in the dropdown."""
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                       database="apartment_mang")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT first_name FROM owner WHERE owner_id = %s", (owner_id,))
        result = my_cursor.fetchone()
        conn.close()
        return result[0] if result else ""

    def update(self):
        """Updates the selected lease record in the database with date validation."""
        try:
            lease_start_date = datetime.strptime(self.var_lease_start.get(), "%Y-%m-%d").date()
            lease_end_date = datetime.strptime(self.var_lease_end.get(), "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Invalid date format! Use YYYY-MM-DD.", parent=self.root)
            return

        if self.var_lease_id.get() == "":
            messagebox.showerror("Error", "Please select a lease to update", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                               database="apartment_mang")
                my_cursor = conn.cursor()

                tenant_id = self.var_tenant_id.get().split(" - ")[0]
                owner_id = self.var_owner_id.get().split(" - ")[0]

                query = """
                    UPDATE lease
                    SET tenant_id=%s, owner_id=%s, lease_start_date=%s, lease_end_date=%s,
                        monthly_rent=%s, security_deposit=%s
                    WHERE lease_id=%s
                """
                values = (
                    tenant_id,
                    owner_id,
                    lease_start_date,
                    lease_end_date,
                    self.var_monthly_rent.get(),
                    self.var_security_deposit.get(),
                    self.var_lease_id.get()
                )
                my_cursor.execute(query, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Updated", "Lease record updated successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error updating record: {str(e)}", parent=self.root)

    def delt(self):
        """Deletes the selected lease record from the database."""
        delete_confirm = messagebox.askyesno("Apartment Management System", "Do you want to delete this lease record?",
                                             parent=self.root)
        if delete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                               database="apartment_mang")
                my_cursor = conn.cursor()
                my_cursor.execute("DELETE FROM lease WHERE lease_id=%s", (self.var_lease_id.get(),))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Deleted", "Lease record deleted successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting record: {str(e)}", parent=self.root)

    def search(self):
        """Searches for lease records based on the selected search criteria and displays results in the Treeview."""
        if self.var_search.get() == "" or self.txt_search.get() == "":
            messagebox.showerror("Error", "Select a search criteria and enter a search term", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                               database="apartment_mang")
                my_cursor = conn.cursor()
                query = f"""
                    SELECT lease.lease_id, lease.tenant_id, lease.owner_id, lease.lease_start_date, lease.lease_end_date,
                           lease.monthly_rent, lease.security_deposit
                    FROM lease
                    JOIN tenant ON lease.tenant_id = tenant.tenant_id
                    JOIN owner ON lease.owner_id = owner.owner_id
                    WHERE {self.var_search.get()} LIKE %s
                """
                value = ("%" + self.txt_search.get() + "%",)
                my_cursor.execute(query, value)
                rows = my_cursor.fetchall()

                if len(rows) != 0:
                    self.Lease_Table.delete(*self.Lease_Table.get_children())
                    for row in rows:
                        self.Lease_Table.insert("", END, values=row)
                else:
                    messagebox.showinfo("No Results", "No records found matching the criteria", parent=self.root)

                conn.close()
            except Exception as e:
                messagebox.showerror("Error", f"Error searching records: {str(e)}", parent=self.root)


if __name__=="__main__":
    root = Tk()
    obj = LeaseClass(root)
    root.mainloop()
