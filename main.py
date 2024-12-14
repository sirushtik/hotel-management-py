from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from Owner import Owner_clas
from Tenant import TenantClass
from Lease import LeaseClass
from Maitenance_req import MaintenanceRequestClass
from Payment_mang import AdminLogin
from apartmentinfo import ApartmentInfoClass


class ApartmentManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Apartment Management System")
        self.root.geometry("1550x800+0+0")

        # ===================================1st image=======================================================
        img1 = Image.open("Images/banner1")
        img1 = Image.open("Images/banner1")
        img1 = img1.resize((1550, 140), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        lblimg = Label(self.root, image=self.photoimg1, bd=4, relief=RIDGE)
        lblimg.place(x=0, y=0, width=1550, height=140)

        # ============================================logo==========================================================
        img2 = Image.open("Images/icon.png")
        img2 = img2.resize((230, 140), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        lblimg = Label(self.root, image=self.photoimg2, bd=4, relief=RIDGE)
        lblimg.place(x=0, y=0, width=230, height=140)

        # ============================================title==========================================================
        lbl_title = Label(self.root, text="APARTMENT MANAGEMENT SYSTEM", font=("times new roman", 40, "bold"),
                          bg="black", fg="silver", bd=4, relief=RIDGE)
        lbl_title.place(x=0, y=140, width=1550, height=50)

        # ============================================main frame==========================================================
        main_frame = Frame(self.root, bd=4, relief=RIDGE)
        main_frame.place(x=0, y=190, width=1550, height=620)

        # ============================================menu==========================================================
        lbl_menu = Label(main_frame, text="OPTIONS", font=("times new roman", 20, "bold"), bg="black", fg="silver",
                         bd=4, relief=RIDGE)
        lbl_menu.place(x=0, y=0, width=230)

        # ============================================menu buttons frame==========================================================
        btn_frame = Frame(main_frame, bd=4, relief=RIDGE)
        btn_frame.place(x=0, y=50, width=230, height=300)

        own_btn = Button(btn_frame, text="Owner", command=self.owner_det, width=22,
                         font=("times new roman", 14, "bold"), bg="black",
                         fg="silver", bd=4, relief=RIDGE, cursor="hand2")
        own_btn.grid(row=0, column=0)

        tent_btn = Button(btn_frame, text="Tenant", command=self.tenant_det, width=22,
                          font=("times new roman", 14, "bold"), bg="black", fg="silver", bd=4, relief=RIDGE,
                          cursor="hand2")
        tent_btn.grid(row=1, column=0)

        det_btn = Button(btn_frame, text="Manage Pay", command=self.payment, width=22,
                         font=("times new roman", 14, "bold"), bg="black", fg="silver", bd=4, relief=RIDGE,
                         cursor="hand2")
        det_btn.grid(row=2, column=0)

        maint_btn = Button(btn_frame, text="Maintenance Req", command=self.maint_req, width=22,
                           font=("times new roman", 14, "bold"), bg="black", fg="silver", bd=4, relief=RIDGE,
                           cursor="hand2")
        maint_btn.grid(row=3, column=0)

        apart_btn = Button(btn_frame, text="Apartment Info", command=self.aprtment, width=22,
                           font=("times new roman", 14, "bold"), bg="black",
                           fg="silver", bd=4, relief=RIDGE, cursor="hand2")
        apart_btn.grid(row=4, column=0)

        leas_btn = Button(btn_frame, text="Lease Info", command=self.Lease, width=22,
                          font=("times new roman", 14, "bold"), bg="black",
                          fg="silver", bd=4, relief=RIDGE, cursor="hand2")
        leas_btn.grid(row=5, column=0)

        logout_btn = Button(btn_frame, text="Logout", command=self.logout, width=22,
                            font=("times new roman", 14, "bold"), bg="black", fg="silver", bd=4, relief=RIDGE,
                            cursor="hand2")
        logout_btn.grid(row=6, column=0)

        # =====================================right side image===============================================
        img3 = Image.open("Images/Main_bg.jpeg")
        img3 = img3.resize((1310, 590), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        lblimg1 = Label(main_frame, image=self.photoimg3, bd=4, relief=RIDGE)
        lblimg1.place(x=225, y=0, width=1310, height=590)

        # ===================================down images=================================================
        img4 = Image.open("Images/right_side.jpeg")
        img4 = img4.resize((230, 210), Image.LANCZOS)
        img4 = img4.resize((230, 210), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        lblimg2 = Label(main_frame, image=self.photoimg4, bd=4, relief=RIDGE)
        lblimg2.place(x=0, y=360, width=230, height=210)

    def owner_det(self):
        self.new_window = Toplevel(self.root)
        self.app = Owner_clas(self.new_window)

    def tenant_det(self):
        self.new_window = Toplevel(self.root)
        self.app = TenantClass(self.new_window)

    def maint_req(self):
        self.new_window = Toplevel(self.root)
        self.app = MaintenanceRequestClass(self.new_window)

    def Lease(self):
        self.new_window = Toplevel(self.root)
        self.app = LeaseClass(self.new_window)

    def payment(self):
        self.new_window = Toplevel(self.root)
        self.app = AdminLogin(self.new_window)

    def aprtment(self):
        self.new_window = Toplevel(self.root)
        self.app = ApartmentInfoClass(self.new_window)

    def logout(self):
        answer = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=self.root)
        if answer:
            self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    obj = ApartmentManagementSystem(root)
    root.mainloop()
