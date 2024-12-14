from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
import random
import mysql.connector


class Owner_clas:

    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System")
        self.root.geometry("1295x580+230+220")

        # Variables
        self.var_ref = StringVar()
        x = random.randint(1000, 9999)
        self.var_ref.set(str(x))

        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_email = StringVar()
        self.var_phone = StringVar()
        self.var_idtype = StringVar()
        self.var_idnum = StringVar()
        self.var_nat = StringVar()
        self.var_search = StringVar()
        self.txt_search = StringVar()

        # Title
        lbl_title = Label(self.root, text="Add Owner Details", font=("times new roman", 32, "bold"),
                          bg="black", fg="silver", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=0, width=1295, height=70)

        # Logo
        img2 = Image.open("Images/icon.png")
        img2 = img2.resize((100, 70), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)
        lblimg = Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE)
        lblimg.place(x=0, y=0, width=100, height=70)

        # Owner Details Label Frame
        labelframe1eft = LabelFrame(self.root, text="Owner Details", font=("times new roman", 12, "bold"),
                                    padx=2, bd=2, relief=RIDGE)
        labelframe1eft.place(x=5, y=70, width=425, height=490)

        # Labels and Entries for Owner Details
        Label(labelframe1eft, text="Owner Ref", font=("times new roman", 12), padx=2, pady=6).grid(row=0, column=0,
                                                                                                   sticky=W)
        ttk.Entry(labelframe1eft, textvariable=self.var_ref, width=29, state='readonly',
                  font=("times new roman", 13, "bold")).grid(row=0, column=1)

        Label(labelframe1eft, text="First Name", font=("times new roman", 12), padx=2, pady=6).grid(row=1, column=0,
                                                                                                    sticky=W)
        ttk.Entry(labelframe1eft, textvariable=self.var_fname, width=29, font=("times new roman", 13, "bold")).grid(
            row=1, column=1)

        Label(labelframe1eft, text="Last name", font=("times new roman", 12), padx=2, pady=6).grid(row=2, column=0,
                                                                                                   sticky=W)
        ttk.Entry(labelframe1eft, textvariable=self.var_lname, width=29, font=("times new roman", 13, "bold")).grid(
            row=2, column=1)

        Label(labelframe1eft, text="Phone No.", font=("times new roman", 12), padx=2, pady=6).grid(row=3, column=0,
                                                                                                   sticky=W)
        ttk.Entry(labelframe1eft, textvariable=self.var_phone, width=29, font=("times new roman", 13, "bold")).grid(
            row=3, column=1)

        Label(labelframe1eft, text="Mail Id", font=("times new roman", 12), padx=2, pady=6).grid(row=4, column=0,
                                                                                                 sticky=W)
        ttk.Entry(labelframe1eft, textvariable=self.var_email, width=29, font=("times new roman", 13, "bold")).grid(
            row=4, column=1)

        Label(labelframe1eft, text="Nationality", font=("times new roman", 12), padx=2, pady=6).grid(row=5, column=0,
                                                                                                     sticky=W)
        combo_nat = ttk.Combobox(labelframe1eft, textvariable=self.var_nat, font=("times new roman", 12), width=29,
                                 state='readonly')
        combo_nat["value"] = ("", "Indian", "American", "British", "Other")
        combo_nat.current(0)
        combo_nat.grid(row=5, column=1)

        Label(labelframe1eft, text="ID Type", font=("times new roman", 12), padx=2, pady=6).grid(row=6, column=0,
                                                                                                 sticky=W)
        combo_id = ttk.Combobox(labelframe1eft, textvariable=self.var_idtype, font=("times new roman", 12), width=29,
                                state='readonly')
        combo_id["value"] = ("", "Aadhar_No", "Ration_ID", "Driving_license", "Passport", "Other")
        combo_id.current(0)
        combo_id.grid(row=6, column=1)

        Label(labelframe1eft, text="Id Number.", font=("times new roman", 12), padx=2, pady=6).grid(row=7, column=0,
                                                                                                    sticky=W)
        ttk.Entry(labelframe1eft, textvariable=self.var_idnum, width=29, font=("times new roman", 13, "bold")).grid(
            row=7, column=1)

        # Button Frame
        btn_frame = Frame(labelframe1eft, bd=2, relief=RIDGE)
        btn_frame.place(x=0, y=350, width=412, height=40)
        Button(btn_frame, text="Add", command=self.add_data, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=0, padx=1)
        Button(btn_frame, text="Update", command=self.update, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=1, padx=1)
        Button(btn_frame, text="Delete", command=self.delt, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=2, padx=1)
        Button(btn_frame, text="Reset", command=self.reset, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=3, padx=1)

        # Search and Table Frame
        Table_Frame = LabelFrame(self.root, text="View Details and Search System", font=("times new roman", 12, "bold"),
                                 padx=2, bd=2, relief=RIDGE)
        Table_Frame.place(x=435, y=70, width=860, height=490)
        Label(Table_Frame, text="Search By:", font=("times new roman", 20, "bold"), bg="black", fg="silver").grid(row=0,
                                                                                                                  column=0,
                                                                                                                  sticky=W,
                                                                                                                  padx=2)

        combo_Search = ttk.Combobox(Table_Frame, textvariable=self.var_search, font=("times new roman", 12), width=24,
                                    state='readonly')
        combo_Search["value"] = ("", "phone_number", "owner_id")
        combo_Search.current(0)
        combo_Search.grid(row=0, column=1, padx=2)

        txtsearch = ttk.Entry(Table_Frame, textvariable=self.txt_search, width=24, font=("times new roman", 13, "bold"))
        txtsearch.grid(row=0, column=2, padx=2)

        Button(Table_Frame, text="Search", command=self.search, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=3, padx=1)
        Button(Table_Frame, text="Show All", command=self.fetch_data, font=("times new roman", 12, "bold"), bg="black",
               fg="silver", width=10).grid(row=0, column=4, padx=1)

        # Table and Scrollbars
        details_table = Frame(Table_Frame, bd=2, relief=RIDGE)
        details_table.place(x=0, y=50, width=860, height=350)

        scroll_x = ttk.Scrollbar(details_table, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(details_table, orient=VERTICAL)

        self.Owner_Table = ttk.Treeview(details_table, columns=(
        "owner_id", "first_name", "last_name", "phone_number", "email", "idtype", "idnumber", "nationality"),
                                        xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.Owner_Table.xview)
        scroll_y.config(command=self.Owner_Table.yview)

        # Define Table Columns
        self.Owner_Table.heading("owner_id", text="Owner ID")
        self.Owner_Table.heading("first_name", text="First Name")
        self.Owner_Table.heading("last_name", text="Last Name")
        self.Owner_Table.heading("phone_number", text="Phone No.")
        self.Owner_Table.heading("email", text="Email")
        self.Owner_Table.heading("idtype", text="ID Type")
        self.Owner_Table.heading("idnumber", text="ID Number")
        self.Owner_Table.heading("nationality", text="Nationality")

        self.Owner_Table["show"] = "headings"

        for col in (
        "owner_id", "first_name", "last_name", "phone_number", "email", "idtype", "idnumber", "nationality"):
            self.Owner_Table.column(col, width=150)

        self.Owner_Table.pack(fill=BOTH, expand=1)
        self.Owner_Table.bind("<ButtonRelease-1>", self.get_cursor)
        self.fetch_data()
        self.reset()

    def add_data(self):
        if self.var_idnum.get() == "" or self.var_fname.get() == "" or self.var_idtype.get() == "" or self.var_email.get() == "" or self.var_lname.get() == "":
            messagebox.showerror("Error", "All fields required")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                               database="apartment_mang")
                my_cursor = conn.cursor()
                my_cursor.execute("INSERT INTO owner (owner_id, first_name, last_name, phone_number, email, idtype, idnumber, nationality) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (
                    self.var_ref.get(), self.var_fname.get(), self.var_lname.get(), self.var_phone.get(),
                    self.var_email.get(), self.var_idtype.get(), self.var_idnum.get(), self.var_nat.get()))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success", "Owner added", parent=self.root)
            except Exception as e:
                messagebox.showerror("Warning", f"Something went wrong: {str(e)}", parent=self.root)

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                       database="apartment_mang")
        my_cursor = conn.cursor()
        my_cursor.execute("SELECT owner_id, first_name, last_name, phone_number, email, idtype, idnumber, nationality FROM owner")
        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.Owner_Table.delete(*self.Owner_Table.get_children())
            for row in rows:
                self.Owner_Table.insert("", END, values=row)
        conn.close()

    def get_cursor(self, event=""):
        cursor_row = self.Owner_Table.focus()
        content = self.Owner_Table.item(cursor_row)
        row = content["values"]

        if row:
            self.var_ref.set(row[0])
            self.var_fname.set(row[1])
            self.var_lname.set(row[2])
            self.var_phone.set(row[3])
            self.var_email.set(row[4])
            self.var_idtype.set(row[5])
            self.var_idnum.set(row[6])
            self.var_nat.set(row[7])

    def update(self):
        if self.var_phone.get() == "":
            messagebox.showerror("Error", "Please enter phone number")
        else:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                               database="apartment_mang")
                my_cursor = conn.cursor()
                my_cursor.execute(
                    "UPDATE owner SET first_name=%s, last_name=%s, phone_number=%s, email=%s, idtype=%s, idnumber=%s, nationality=%s WHERE owner_id=%s",
                    (self.var_fname.get(), self.var_lname.get(), self.var_phone.get(),
                     self.var_email.get(), self.var_idtype.get(), self.var_idnum.get(),
                     self.var_nat.get(), self.var_ref.get()))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Updated", "Owner details updated successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error updating data: {str(e)}", parent=self.root)

    def delt(self):
        delete_confirm = messagebox.askyesno("Apartment Management System", "Do you want to delete this record?", parent=self.root)
        if delete_confirm:
            try:
                conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                               database="apartment_mang")
                my_cursor = conn.cursor()
                my_cursor.execute("DELETE FROM owner WHERE owner_id=%s", (self.var_ref.get(),))
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Deleted", "Owner deleted successfully", parent=self.root)
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting data: {str(e)}", parent=self.root)

    def reset(self):
        self.var_fname.set("")
        self.var_lname.set("")
        self.var_phone.set("")
        self.var_email.set("")
        self.var_nat.set("")
        self.var_idtype.set("")
        self.var_idnum.set("")

        x = random.randint(1000, 9999)
        self.var_ref.set(str(x))

    def search(self):
        conn = mysql.connector.connect(host="localhost", username="root", password="KSirushti@29",
                                       database="apartment_mang")
        my_cursor = conn.cursor()
        query = "SELECT * FROM owner WHERE " + str(self.var_search.get()) + " LIKE %s"
        value = ("%" + str(self.txt_search.get()) + "%",)
        my_cursor.execute(query, value)
        rows = my_cursor.fetchall()

        if len(rows) != 0:
            self.Owner_Table.delete(*self.Owner_Table.get_children())
            for i in rows:
                self.Owner_Table.insert("", END, values=i)
        conn.close()


if __name__ == "__main__":
    root = Tk()
    obj = Owner_clas(root)
    root.mainloop()
