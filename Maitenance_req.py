from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import random


class MaintenanceRequestClass:

    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System - Maintenance Requests")
        self.root.geometry("1295x580+230+220")

        # Variables
        self.var_request_id = StringVar()
        self.var_tenant_id = StringVar()
        self.var_description = StringVar()
        self.var_priority = StringVar()
        self.var_status = StringVar(value="Pending")
        self.var_request_date = StringVar()
        self.var_completion_date = StringVar()

        # Title
        lbl_title = Label(self.root, text="Maintenance Requests", font=("times new roman", 32, "bold"),
                          bg="black", fg="silver", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=70)

        # Maintenance Request Details Label Frame
        labelframe_left = LabelFrame(self.root, text="Request Details", font=("times new roman", 12, "bold"),
                                     padx=2, bd=2, relief=RIDGE)
        labelframe_left.place(x=5, y=70, width=425, height=490)

        # Request ID (Read-only)
        Label(labelframe_left, text="Request ID", font=("times new roman", 12), padx=2, pady=6).grid(row=0, column=0, sticky=W)
        self.entry_request_id = ttk.Entry(labelframe_left, textvariable=self.var_request_id, width=29, font=("times new roman", 13, "bold"), state='readonly')
        self.entry_request_id.grid(row=0, column=1)

        # Tenant ID
        Label(labelframe_left, text="Tenant ID", font=("times new roman", 12), padx=2, pady=6).grid(row=1, column=0, sticky=W)
        self.combo_tenant_id = ttk.Combobox(labelframe_left, textvariable=self.var_tenant_id, font=("times new roman", 12), width=27)
        self.combo_tenant_id.grid(row=1, column=1)
        self.fetch_tenants()

        # Description (Dropdown)
        Label(labelframe_left, text="Description", font=("times new roman", 12), padx=2, pady=6).grid(row=2, column=0, sticky=W)
        self.combo_description = ttk.Combobox(labelframe_left, textvariable=self.var_description, font=("times new roman", 12), width=27, state='readonly')
        self.combo_description["values"] = (
            "General Repairs", "Plumbing Issue", "Electrical Issue", "HVAC (Heating/Cooling Issue)",
            "Painting and Decorating", "Pest Control", "Landscaping and Groundskeeping", "Security Systems",
            "Common Area Maintenance", "Emergency Repairs", "Appliance Maintenance", "Roofing and Exteriors", "Other"
        )
        self.combo_description.grid(row=2, column=1)
        self.combo_description.bind("<<ComboboxSelected>>", self.update_priority)

        # Priority (Read-only after selecting description)
        Label(labelframe_left, text="Priority", font=("times new roman", 12), padx=2, pady=6).grid(row=3, column=0, sticky=W)
        self.combo_priority = ttk.Combobox(labelframe_left, textvariable=self.var_priority, font=("times new roman", 12), width=27, state='readonly')
        self.combo_priority["values"] = ("Low", "Medium", "High", "Urgent")
        self.combo_priority.grid(row=3, column=1)
        self.combo_priority.config(state='readonly')  # Set priority to read-only

        # Status
        Label(labelframe_left, text="Status", font=("times new roman", 12), padx=2, pady=6).grid(row=4, column=0, sticky=W)
        self.combo_status = ttk.Combobox(labelframe_left, textvariable=self.var_status, font=("times new roman", 12), width=27, state='readonly')
        self.combo_status["values"] = ("Pending", "In Progress", "Completed", "Cancelled")
        self.combo_status.grid(row=4, column=1)

        # Request Date
        Label(labelframe_left, text="Request Date", font=("times new roman", 12), padx=2, pady=6).grid(row=5, column=0, sticky=W)
        self.entry_request_date = ttk.Entry(labelframe_left, textvariable=self.var_request_date, width=29, font=("times new roman", 13, "bold"))
        self.entry_request_date.grid(row=5, column=1)

        # Completion Date
        Label(labelframe_left, text="Completion Date", font=("times new roman", 12), padx=2, pady=6).grid(row=6, column=0, sticky=W)
        self.entry_completion_date = ttk.Entry(labelframe_left, textvariable=self.var_completion_date, width=29, font=("times new roman", 13, "bold"))
        self.entry_completion_date.grid(row=6, column=1)

        # Button Frame
        btn_frame = Frame(labelframe_left, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=350, width=412, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="Update", command=self.update, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="Delete", command=self.delt, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="Reset", command=self.reset, font=("times new roman", 12, "bold"), bg="black", fg="silver", width=10).grid(row=0, column=3, padx=1)

        # Table Frame
        Table_Frame = LabelFrame(self.root, text="View Requests", font=("times new roman", 12, "bold"), padx=2, bd=2, relief=RIDGE)
        Table_Frame.place(x=435, y=70, width=860, height=490)

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.Request_Table = ttk.Treeview(Table_Frame, columns=("request_id", "tenant_id", "description", "priority", "status", "request_date", "completion_date"),
                                          xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Request_Table.xview)
        scroll_y.config(command=self.Request_Table.yview)

        self.Request_Table.heading("request_id", text="Request ID")
        self.Request_Table.heading("tenant_id", text="Tenant ID")
        self.Request_Table.heading("description", text="Description")
        self.Request_Table.heading("priority", text="Priority")
        self.Request_Table.heading("status", text="Status")
        self.Request_Table.heading("request_date", text="Request Date")
        self.Request_Table.heading("completion_date", text="Completion Date")

        self.Request_Table["show"] = "headings"

        # Set column widths
        for col in ("request_id", "tenant_id", "description", "priority", "status", "request_date", "completion_date"):
            self.Request_Table.column(col, width=100)

        self.Request_Table.pack(fill=BOTH, expand=1)
        self.Request_Table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()
        self.reset()  # Automatically generate a request ID when the form loads

    def update_priority(self, *args):
        """Automatically update priority based on description and set it to read-only."""
        description_to_priority = {
            "General Repairs": "Medium",
            "Plumbing Issue": "High",
            "Electrical Issue": "High",
            "HVAC (Heating/Cooling Issue)": "High",
            "Painting and Decorating": "Low",
            "Pest Control": "Medium",
            "Landscaping and Groundskeeping": "Low",
            "Security Systems": "High",
            "Common Area Maintenance": "Medium",
            "Emergency Repairs": "Urgent",
            "Appliance Maintenance": "Low",
            "Roofing and Exteriors": "Medium",
            "Other": "Medium"
        }
        selected_description = self.var_description.get()
        self.var_priority.set(description_to_priority.get(selected_description, "Medium"))
        self.combo_priority.config(state='readonly')  # Set priority to read-only

    def fetch_tenants(self):
        """Fetch tenant IDs and names for dropdown."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT tenant_id, first_name FROM tenant")
            rows = my_cursor.fetchall()
            conn.close()
            tenant_options = ["{} - {}".format(row[0], row[1]) for row in rows]
            self.combo_tenant_id["values"] = tenant_options
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tenants: {str(e)}", parent=self.root)

    def add_data(self):
        """Adds a new maintenance request to the database with a generated request ID."""
        if self.var_tenant_id.get() == "" or self.var_description.get() == "" or self.var_priority.get() == "" or self.var_request_date.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
                my_cursor = conn.cursor()

                # Auto-generate a request ID
                self.var_request_id.set(str(random.randint(1000, 9999)))

                # Insert data into the database
                query = """
                    INSERT INTO maintenance_req (request_id, tenant_id, description, priority, status, request_date, completion_date)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
                values = (
                    self.var_request_id.get(),
                    self.var_tenant_id.get().split(" - ")[0],  # Get tenant ID only
                    self.var_description.get(),
                    self.var_priority.get(),
                    self.var_status.get(),
                    self.var_request_date.get(),
                    self.var_completion_date.get()
                )
                my_cursor.execute(query, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Maintenance request added successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error adding request: {str(e)}", parent=self.root)

    def fetch_data(self):
        """Fetches all maintenance requests from the database and displays them in the Treeview."""
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT * FROM maintenance_req")
        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.Request_Table.delete(*self.Request_Table.get_children())
            for row in rows:
                self.Request_Table.insert("", END, values=row)
        conn.close()

    def get_cursor(self, event=""):
        """Gets data from the selected row in the Treeview and populates the input fields."""
        cursor_row = self.Request_Table.focus()
        content = self.Request_Table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_request_id.set(row[0])
            self.var_tenant_id.set(f"{row[1]} - {self.get_tenant_name(row[1])}")
            self.var_description.set(row[2])
            self.var_priority.set(row[3])
            self.var_status.set(row[4])
            self.var_request_date.set(row[5])
            self.var_completion_date.set(row[6])

    def get_tenant_name(self, tenant_id):
        """Fetch tenant's name for displaying in the tenant dropdown."""
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT first_name FROM tenant WHERE tenant_id = %s", (tenant_id,))
        result = my_cursor.fetchone()
        conn.close()
        return result[0] if result else ""

    def update(self):
        """Updates the selected maintenance request in the database."""
        if self.var_request_id.get() == "":
            messagebox.showerror("Error", "Please select a request to update", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
                my_cursor = conn.cursor()

                tenant_id = self.var_tenant_id.get().split(" - ")[0]  # Get only the tenant ID

                query = """
                    UPDATE maintenance_req
                    SET tenant_id=%s, description=%s, priority=%s, status=%s, request_date=%s, completion_date=%s
                    WHERE request_id=%s
                """
                values = (
                    tenant_id,
                    self.var_description.get(),
                    self.var_priority.get(),
                    self.var_status.get(),
                    self.var_request_date.get(),
                    self.var_completion_date.get(),
                    self.var_request_id.get()
                )
                my_cursor.execute(query, values)
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Updated", "Maintenance request updated successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error updating request: {str(e)}", parent=self.root)

    def delt(self):
        """Deletes the selected maintenance request from the database."""
        delete_confirm = messagebox.askyesno("Apartment Management System", "Do you want to delete this maintenance request?", parent=self.root)
        if delete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29", database="apartment_mang")
                my_cursor = conn.cursor()
                my_cursor.execute("DELETE FROM maintenance_req WHERE request_id=%s", (self.var_request_id.get(),))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Deleted", "Maintenance request deleted successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting request: {str(e)}", parent=self.root)

    def reset(self):
        """Resets all input fields and generates a new request ID."""
        self.var_request_id.set(str(random.randint(1000, 9999)))  # Auto-generate a new request ID
        self.var_tenant_id.set("")
        self.var_description.set("")
        self.var_priority.set("")
        self.var_status.set("Pending")
        self.var_request_date.set("")
        self.var_completion_date.set("")


if __name__ == "__main__":
    root = Tk()
    obj = MaintenanceRequestClass(root)
    root.mainloop()
