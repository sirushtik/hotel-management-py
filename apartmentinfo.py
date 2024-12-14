from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
import random


class ApartmentInfoClass:
    # Initialize available apartment counts
    available_2_bedroom_count = 5
    available_3_bedroom_count = 10

    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System - Apartment Information")
        self.root.geometry("1295x580+230+220")

        # Variables
        self.var_apartment_id = StringVar()
        self.var_owner_id = StringVar()
        self.var_tenant_id = StringVar()
        self.var_num_rooms = StringVar(value="2")  # Default to 2-bedroom
        self.var_is_available = StringVar(value="TRUE")  # Fixed value
        self.var_is_for_lease = StringVar(value="FALSE")  # Fixed value
        self.var_monthly_rent = StringVar()  # Will set based on room type
        self.var_deposit_amount = StringVar()  # Will set based on room type
        self.var_parking_spaces = StringVar(value="1")  # Fixed value

        # Title
        lbl_title = Label(self.root, text="Apartment Information", font=("times new roman", 32, "bold"),
                          bg="black", fg="silver", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=70)

        # Apartment Details Label Frame
        labelframe_left = LabelFrame(self.root, text="Apartment Details", font=("times new roman", 12, "bold"),
                                     padx=2, bd=2, relief=RIDGE)
        labelframe_left.place(x=5, y=70, width=425, height=490)

        # Apartment ID (Read-only)
        Label(labelframe_left, text="Apartment ID", font=("times new roman", 12), padx=2, pady=6).grid(row=0, column=0,
                                                                                                       sticky=W)
        self.entry_apartment_id = ttk.Entry(labelframe_left, textvariable=self.var_apartment_id, width=29,
                                            font=("times new roman", 13, "bold"), state='readonly')
        self.entry_apartment_id.grid(row=0, column=1)

        # Owner ID
        Label(labelframe_left, text="Owner ID", font=("times new roman", 12), padx=2, pady=6).grid(row=1, column=0,
                                                                                                   sticky=W)
        self.combo_owner_id = ttk.Combobox(labelframe_left, textvariable=self.var_owner_id,
                                           font=("times new roman", 12), width=27)
        self.combo_owner_id.grid(row=1, column=1)
        self.fetch_owners()  # Populate the owner dropdown

        # Tenant ID
        Label(labelframe_left, text="Tenant ID", font=("times new roman", 12), padx=2, pady=6).grid(row=2, column=0,
                                                                                                    sticky=W)
        self.combo_tenant_id = ttk.Combobox(labelframe_left, textvariable=self.var_tenant_id,
                                            font=("times new roman", 12), width=27)
        self.combo_tenant_id.grid(row=2, column=1)
        self.fetch_tenants()  # Populate the tenant dropdown

        # Number of Rooms (Dropdown with 2 or 3 options)
        Label(labelframe_left, text="Number of Rooms", font=("times new roman", 12), padx=2, pady=6).grid(row=3,
                                                                                                          column=0,
                                                                                                          sticky=W)
        self.combo_num_rooms = ttk.Combobox(labelframe_left, textvariable=self.var_num_rooms,
                                            font=("times new roman", 12), width=27, state='readonly')
        self.combo_num_rooms["values"] = ("2", "3")
        self.combo_num_rooms.current(0)
        self.combo_num_rooms.grid(row=3, column=1)
        self.combo_num_rooms.bind("<<ComboboxSelected>>", self.set_rent_and_deposit)

        # Availability (Fixed)
        Label(labelframe_left, text="Availability", font=("times new roman", 12), padx=2, pady=6).grid(row=4, column=0,
                                                                                                       sticky=W)
        self.entry_is_available = ttk.Entry(labelframe_left, textvariable=self.var_is_available, width=29,
                                            font=("times new roman", 13, "bold"), state='readonly')
        self.entry_is_available.grid(row=4, column=1)

        # For Lease (Fixed)
        Label(labelframe_left, text="For Lease", font=("times new roman", 12), padx=2, pady=6).grid(row=5, column=0,
                                                                                                    sticky=W)
        self.entry_is_for_lease = ttk.Entry(labelframe_left, textvariable=self.var_is_for_lease, width=29,
                                            font=("times new roman", 13, "bold"), state='readonly')
        self.entry_is_for_lease.grid(row=5, column=1)

        # Monthly Rent (Dependent on Room Type)
        Label(labelframe_left, text="Monthly Rent", font=("times new roman", 12), padx=2, pady=6).grid(row=6, column=0,
                                                                                                       sticky=W)
        self.entry_monthly_rent = ttk.Entry(labelframe_left, textvariable=self.var_monthly_rent, width=29,
                                            font=("times new roman", 13, "bold"), state='readonly')
        self.entry_monthly_rent.grid(row=6, column=1)

        # Deposit Amount (Dependent on Room Type)
        Label(labelframe_left, text="Deposit Amount", font=("times new roman", 12), padx=2, pady=6).grid(row=7,
                                                                                                         column=0,
                                                                                                         sticky=W)
        self.entry_deposit_amount = ttk.Entry(labelframe_left, textvariable=self.var_deposit_amount, width=29,
                                              font=("times new roman", 13, "bold"), state='readonly')
        self.entry_deposit_amount.grid(row=7, column=1)

        # Parking Spaces (Fixed)
        Label(labelframe_left, text="Parking Spaces", font=("times new roman", 12), padx=2, pady=6).grid(row=8,
                                                                                                         column=0,
                                                                                                         sticky=W)
        self.entry_parking_spaces = ttk.Entry(labelframe_left, textvariable=self.var_parking_spaces, width=29,
                                              font=("times new roman", 13, "bold"), state='readonly')
        self.entry_parking_spaces.grid(row=8, column=1)

        # Button Frame
        btn_frame = Frame(labelframe_left, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=400, width=412, height=40)

        Button(btn_frame, text="Add", command=self.add_data, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="Update", command=self.update, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="Delete", command=self.delt, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="Reset", command=self.reset, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=3, padx=1)

        # Table Frame
        Table_Frame = LabelFrame(self.root, text="View Apartments", font=("times new roman", 12, "bold"), padx=2, bd=2,
                                 relief=RIDGE)
        Table_Frame.place(x=435, y=70, width=860, height=490)

        scroll_x = ttk.Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Table_Frame, orient=VERTICAL)

        self.Apartment_Table = ttk.Treeview(Table_Frame, columns=(
        "apartment_id", "owner_id", "tenant_id", "num_rooms", "is_available", "is_for_lease", "monthly_rent",
        "deposit_amount", "parking_spaces"),
                                            xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Apartment_Table.xview)
        scroll_y.config(command=self.Apartment_Table.yview)

        self.Apartment_Table.heading("apartment_id", text="Apartment ID")
        self.Apartment_Table.heading("owner_id", text="Owner ID")
        self.Apartment_Table.heading("tenant_id", text="Tenant ID")
        self.Apartment_Table.heading("num_rooms", text="Rooms")
        self.Apartment_Table.heading("is_available", text="Available")
        self.Apartment_Table.heading("is_for_lease", text="For Lease")
        self.Apartment_Table.heading("monthly_rent", text="Monthly Rent")
        self.Apartment_Table.heading("deposit_amount", text="Deposit")
        self.Apartment_Table.heading("parking_spaces", text="Parking")

        self.Apartment_Table["show"] = "headings"
        for col in (
        "apartment_id", "owner_id", "tenant_id", "num_rooms", "is_available", "is_for_lease", "monthly_rent",
        "deposit_amount", "parking_spaces"):
            self.Apartment_Table.column(col, width=100)

        self.Apartment_Table.pack(fill=BOTH, expand=1)
        self.Apartment_Table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()
        self.reset()

    def set_rent_and_deposit(self, event=None):
        """Set rent and deposit based on the number of rooms."""
        if self.var_num_rooms.get() == "2":
            self.var_monthly_rent.set("1500")
            self.var_deposit_amount.set("1500")
        elif self.var_num_rooms.get() == "3":
            self.var_monthly_rent.set("2000")
            self.var_deposit_amount.set("2000")

    def fetch_owners(self):
        """Fetch owner IDs for dropdown."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                           database="apartment_mang")
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
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                           database="apartment_mang")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT tenant_id FROM tenant")
            rows = my_cursor.fetchall()
            conn.close()
            tenant_options = [row[0] for row in rows]
            self.combo_tenant_id["values"] = tenant_options
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load tenants: {str(e)}", parent=self.root)

    def add_data(self):
        """Adds a new apartment record to the database with dynamic values and room type restrictions."""
        if self.var_owner_id.get() == "" or self.var_tenant_id.get() == "":
            messagebox.showerror("Error", "Owner ID and Tenant ID are required", parent=self.root)
            return

        # Check and decrement availability based on room type
        if self.var_num_rooms.get() == "2" and ApartmentInfoClass.available_2_bedroom_count <= 0:
            messagebox.showerror("Error", "No 2-bedroom apartments available", parent=self.root)
            return
        elif self.var_num_rooms.get() == "3" and ApartmentInfoClass.available_3_bedroom_count <= 0:
            messagebox.showerror("Error", "No 3-bedroom apartments available", parent=self.root)
            return

        # Generate apartment ID with prefix based on room type
        prefix = "A2-" if self.var_num_rooms.get() == "2" else "A3-"
        self.var_apartment_id.set(prefix + str(random.randint(1000, 9999)))

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                           database="apartment_mang")
            my_cursor = conn.cursor()

            query = """
                INSERT INTO apartment_info (apartment_id, owner_id, tenant_id, num_rooms, is_available, is_for_lease,
                                            monthly_rent, deposit_amount, parking_spaces)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = (
                self.var_apartment_id.get(),
                self.var_owner_id.get(),
                self.var_tenant_id.get(),
                self.var_num_rooms.get(),
                self.var_is_available.get(),
                self.var_is_for_lease.get(),
                self.var_monthly_rent.get(),
                self.var_deposit_amount.get(),
                self.var_parking_spaces.get()
            )
            my_cursor.execute(query, values)
            conn.commit()

            # Decrement the count after successful addition
            if self.var_num_rooms.get() == "2":
                ApartmentInfoClass.available_2_bedroom_count -= 1
            elif self.var_num_rooms.get() == "3":
                ApartmentInfoClass.available_3_bedroom_count -= 1

            self.fetch_data()
            conn.close()
            messagebox.showinfo("Success", "Apartment added successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error adding apartment: {str(e)}", parent=self.root)

    def fetch_data(self):
        """Fetches all apartments from the database and displays them in the Treeview."""
        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                           database="apartment_mang")
            my_cursor = conn.cursor()
            my_cursor.execute("SELECT * FROM apartment_info")
            rows = my_cursor.fetchall()

            if len(rows) != 0:
                self.Apartment_Table.delete(*self.Apartment_Table.get_children())
                for row in rows:
                    self.Apartment_Table.insert("", END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching apartments: {str(e)}", parent=self.root)

    def get_cursor(self, event=""):
        """Gets data from the selected row in the Treeview and populates the input fields."""
        cursor_row = self.Apartment_Table.focus()
        content = self.Apartment_Table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_apartment_id.set(row[0])
            self.var_owner_id.set(row[1])
            self.var_tenant_id.set(row[2])
            self.var_num_rooms.set(row[3])
            self.var_is_available.set(row[4])
            self.var_is_for_lease.set(row[5])
            self.var_monthly_rent.set(row[6])
            self.var_deposit_amount.set(row[7])
            self.var_parking_spaces.set(row[8])

    def update(self):
        """Updates the owner and tenant IDs of the selected apartment in the database."""
        if self.var_apartment_id.get() == "":
            messagebox.showerror("Error", "Please select an apartment to update", parent=self.root)
            return

        try:
            conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                           database="apartment_mang")
            my_cursor = conn.cursor()

            # Update only the owner_id and tenant_id fields
            query = """
                UPDATE apartment_info
                SET owner_id=%s, tenant_id=%s
                WHERE apartment_id=%s
            """
            values = (
                self.var_owner_id.get(),
                self.var_tenant_id.get(),
                self.var_apartment_id.get()
            )
            my_cursor.execute(query, values)
            conn.commit()
            self.fetch_data()
            conn.close()
            messagebox.showinfo("Updated", "Apartment owner and tenant updated successfully", parent=self.root)
        except Exception as e:
            messagebox.showerror("Error", f"Error updating apartment: {str(e)}", parent=self.root)

    def delt(self):
        """Deletes the selected apartment record from the database and increments availability count."""
        if self.var_apartment_id.get() == "":
            messagebox.showerror("Error", "Please select an apartment to delete", parent=self.root)
            return

        delete_confirm = messagebox.askyesno("Apartment Management System", "Do you want to delete this apartment?",
                                             parent=self.root)
        if delete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                               database="apartment_mang")
                my_cursor = conn.cursor()
                my_cursor.execute("DELETE FROM apartment_info WHERE apartment_id=%s", (self.var_apartment_id.get(),))
                conn.commit()
                conn.close()

                # Increment the count after deletion based on room type
                if self.var_num_rooms.get() == "2":
                    ApartmentInfoClass.available_2_bedroom_count += 1
                elif self.var_num_rooms.get() == "3":
                    ApartmentInfoClass.available_3_bedroom_count += 1

                self.fetch_data()
                messagebox.showinfo("Deleted", "Apartment deleted successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting apartment: {str(e)}", parent=self.root)

    def reset(self):
        """Resets input fields and generates a new apartment ID, while fixed values remain unchanged."""
        # Generate a new apartment ID with prefix based on selected room type
        if self.var_num_rooms.get() == "2":
            prefix = "A2-"
        elif self.var_num_rooms.get() == "3":
            prefix = "A3-"
        else:
            prefix = "A-"
        self.var_apartment_id.set(prefix + str(random.randint(1000, 9999)))

        self.var_owner_id.set("")
        self.var_tenant_id.set("")
        self.set_rent_and_deposit()  # Reset rent and deposit based on room type


if __name__ == "__main__":
    root = Tk()
    obj = ApartmentInfoClass(root)
    root.mainloop()
