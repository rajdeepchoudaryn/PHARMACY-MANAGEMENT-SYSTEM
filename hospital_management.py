import os
from tkinter import *
from tkinter import ttk, messagebox
from tkcalendar import Calendar, DateEntry
import random
import time
import tempfile
#import datetime
from datetime import date, datetime
import  tkinter.messagebox
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog, messagebox

import sqlite3
import os
cop = sqlite3.connect("pharmacy.db")
con = sqlite3.connect("recipt.db")
mycursor = con.cursor()

#--------------------------Functiondeclaration---------------------------------------------------
def Window3(win):
    ref_var = StringVar()
    win.configure(background='lightgreen')
    win.geometry("1300x750+0+0")
    win.title(" NURSERY MANAGEMENT SYSTEM")

    title_label = Label(win, text='*Database*', font=(
        'algerian', 35, 'bold'), bg="cyan", bd=8, relief=GROOVE)
    title_label.pack(side=TOP, fill=X)

    win.resizable(0, 0)

    #=====================ENTRY===========#

    entry_frame = LabelFrame(win, text="Enter Details", background="lightgreen", font=(
        'Arial', 30,'bold'), bd=7, relief=GROOVE)
    entry_frame.place(x=20, y=70, width=500, height=350)

    bill_no = Label(entry_frame, text="Enter to search",
                    font=('Arial', 16), bg="lightgreen")
    bill_no.grid(row=0, column=0, padx=2, pady=2)

    Label(entry_frame, text = "Search By", font = ('Areal', 16), bg = 'lightgreen').grid(row = 0, column = 1, padx = 2)
    search_ref = OptionMenu(entry_frame, ref_var,*['Ref. Id', 'Date', 'Name', 'Phone Number', 'Age'])
    ref_var.set('Ref. Id')
    search_ref.grid(row = 1, column = 1, padx = 2, pady = 4)
    bill_no_entry = Text(entry_frame, font=(
        'Arial', 20), height=1, width=20)
    bill_no_entry.grid(row=1, column=0, padx=2, pady=4)

    # =================Functions==============

    def reset_func():
        bill_txt.config(state = NORMAL)
        bill_txt.delete("1.0", END)
        bill_txt.config(state = DISABLED)
        tree.delete(*tree.get_children())
        bill_no_entry.delete(1.0, "end-1c")
        a = mycursor.execute(f"select * from data").fetchall()
        for data in a:
            tree.insert('', 'end', values=(data))

    def write_bill(bill, ref = 'ref'):
        a = mycursor.execute( f"select * from data where {ref} = '{bill}'").fetchone()
        if a:
            bill_txt.config(state = NORMAL)
            bill_txt.delete(1.0, END)
            bill_txt.insert(END, a[5])
            bill_txt.config(state = DISABLED)
        else:
            tkinter.messagebox.showerror("ERROR", "No bill found", parent = win)

    def search_func():
        ref_d = {"Ref. Id":"ref", "Name":"name", "Phone Number":"phone", "Date":"date", "Age":"age"}
        sbill = bill_no_entry.get(1.0, "end-1c")
        ref = ref_var.get()
        bill = sbill
        a = mycursor.execute(f"select ref, name, phone, date, age from data where {ref_d[ref]} like ('%{sbill}%') ").fetchall()
        tree.delete(*tree.get_children())
        for data in a:
            tree.insert('', 'end', values=(data))

    def display_all_func():
        bill_txt.config(state = NORMAL)
        bill_txt.delete(1.0, END)
        a = mycursor.execute("select slip from data").fetchall()
        for i in a:
            bill_txt.insert(END, i)
            bill_txt.insert(END, "\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        bill_txt.config(state = DISABLED)
 

    def delete_bill_func():
        ref_id = bill_no_entry.get(1.0, "end-1c").strip()  # Get the reference ID from the entry
        if not ref_id:
            messagebox.showerror("Error", "Please enter a reference ID to delete.", parent=win)
            return
        
        # Confirmation dialog
        if messagebox.askyesno("Confirmation", "Are you sure you want to delete this bill?"):
            # Execute the delete operation
            mycursor.execute("DELETE FROM data WHERE ref = ?", (ref_id,))
            con.commit()
            
            # Check if the deletion was successful
            if mycursor.rowcount > 0:
                messagebox.showinfo("Success", "Bill deleted successfully!")
            else:
                messagebox.showwarning("Warning", "No bill found with the given reference ID.")
            
            reset_func()  # Refresh the displayed bills
        else:
            messagebox.showinfo("Cancelled", "Deletion cancelled.")

    def print_bill():
        write = bill_txt.get('1.0', END)
        fname = tempfile.mktemp('.txt')
        open(fname, 'w').write(write)
        os.startfile(fname)
        
    def show_stock():
        xo=""
        mycursor=con.cursor()
        mycursor.execute("select* from food;")
        data=mycursor.fetchall()
        with open("stock_details.txt",'w') as frob:
            frob.writelines("{0:<15}{1:<10}{2:<5}".format("Plant","Price","Stock"))
            frob.writelines("\n"+("-"*54)+"\n")
            frob.writelines("\n")
            frob.flush()
            for i in data:
                xo=i
                frob.writelines("{0:<15}{1:<10}{2:<5}".format(i[0],str(i[1]),str(i[2]))+"\n")
                frob.flush()
            frob.writelines("\n"+("-"*54)+"\n")
            frob.flush()
        os.startfile("stock_details.txt")
    def OnSelected(event):
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        write_bill(selecteditem[0])

    def refresh():
        tree_1.delete(*tree_1.get_children())
        a = mycursor.execute("select * from food").fetchall()
        for data in a:
            tree_1.insert('', 'end', values=(data))


    def update_food(event):

        def update():
            mycursor.execute(f"update food set item = '{food.get()}', price = '{price.get()}', stock = '{stock.get()}' where item = '{food.get()}'")
            con.commit()
            refresh()
            messagebox.showinfo("done", "Data Updated", parent = box)
            box.destroy()

        def delete():
            mycursor.execute(f"delete from food where item = '{food.get()}'")
            con.commit()
            refresh()
            messagebox.showinfo('done', "Data Deleted", parent = box)
            box.destroy()

        f = "Areal 13 bold"
        b = "#cccccc"
        curItem = tree_1.focus()
        contents = (tree_1.item(curItem))
        selecteditem = contents['values']

        food = StringVar()
        price = StringVar()
        stock = StringVar()
        food.set(selecteditem[0])
        price.set(selecteditem[1])
        stock.set(selecteditem[2])

        box = Toplevel(win)
        box.title("Update mobile data")
        box.geometry('330x180')
        box.config(bg = b)
        
        Label(box, text = "plant name", font = f, bg = b).grid(row = 0, column = 0, padx = 10, pady = 10, sticky = W)
        food_inp = Entry(box, textvariable = food,font = f)
        food_inp.grid(row = 0, column = 1, padx = 4, pady = 10, sticky = W)

        Label(box, text = "Price", font = f, bg = b).grid(row = 1, column = 0, padx = 10, pady = 10, sticky = W)
        price_inp = Entry(box, textvariable = price, font = f)
        price_inp.grid(row = 1, column = 1, padx = 4, pady = 10, sticky = W)

        Label(box, text = "Stock", font = f, bg = b).grid(row = 2, column = 0, padx = 10, pady = 10, sticky = W)
        price_inp = Entry(box, textvariable = stock, font = f)
        price_inp.grid(row = 2, column = 1, padx = 4, pady = 10, sticky = W)

        Button(box, text = "Update", bg = 'green', font = f, bd = 4, command = update).grid(row = 3, column = 1, pady = 14, sticky = W)
        Button(box, text = "Delete", bg = 'red',font = f, bd = 4, command = delete).grid(row = 3, column = 1, pady = 14, sticky = E)

    def add_new():
        def add_item():
            if item_ent.get() == "" or price_ent.get() == "" or stock_ent.get() == "":
                messagebox.showerror("error", "Enter all the fields", parent= wd)
            elif not (price_ent.get().isdigit() or stock_ent.get().isdigit()):
                messagebox.showerror('error', "price should be a number", parent= wd)
            else:
                mycursor.execute(f"insert into food values('{item_ent.get()}', '{price_ent.get()}', '{stock_ent.get()}')")
                con.commit()
                messagebox.showinfo("done", "Item added", parent = wd)
                refresh()
                wd.destroy()

        if True:
            wd = Toplevel(win)
            wd.title("Add new item")
            wd.geometry('350x150')
            wd.resizable(0, 0)
            wd.config(bg = "#cccccc")
            item = Label(wd, text = "Enter plant name", font = "consolas 14 bold", bg = "#cccccc")
            item.grid(row = 0, column = 0, pady = 3, sticky = W)
            price = Label(wd, text = "Enter price", font = "consolas 14 bold", bg = "#cccccc") 
            price.grid(row = 1, column = 0, pady = 3, sticky = W)
            st = Label(wd, text = "Enter stock", font = "consolas 14 bold", bg = "#cccccc") 
            st.grid(row = 2, column = 0, pady = 3, sticky = W)
            item_ent = Entry(wd, font = 'consolas 12 bold')
            item_ent.grid(row = 0, column = 1, pady = 3)
            price_ent = Entry(wd, font = 'consolas 12 bold')
            price_ent.grid(row = 1, column = 1, pady = 3)
            stock_ent = Entry(wd, font = 'consolas 12 bold')
            stock_ent.grid(row = 2, column = 1, pady = 3)
            Button(wd, text = "Done", bd = 4, bg = "lightgreen", command = add_item, width = 10).grid(row = 3, column = 1, pady = 3)
    #=========================================#

    # ================Button=================

    button_frame = LabelFrame(entry_frame, bd=5, text="Options", bg="lightgreen", font=("Arial", 23,'bold'))
    button_frame.place(x=20, y=90, width=450, height=150)

    reset_btn = Button(button_frame, bd=6, text="Reset", font=('Arial', 16,'bold'),bg='red',fg='white' ,width=9, height=1, command=reset_func)
    reset_btn.grid(row=0, column=0, padx=4, pady=2)

    search_btn = Button(button_frame, bd=6, text="Search", font=('Arial', 16,'bold'),bg='red',fg='white' , width=9, height=1, command=lambda: search_func())
    search_btn.grid(row=0, column=1, padx=4, pady=2)

    add_btn = Button(button_frame,bd=6,text="Show all bill",font=('Arial',16,'bold'),bg='red',fg='white' ,width=9,height=1, command = display_all_func)
    add_btn.grid(row=0,column=2,padx=4,pady=2)

    print_btn = Button(button_frame,bd=6,text="Print Bill",font=('Arial',16,'bold'),bg='red',fg='white' ,width=9,height=1, command = print_bill)
    print_btn.grid(row=1,column=0,padx=4,pady=2)

    show_btn = Button(button_frame,bd=6,text="Show stock",font=('Arial',16,'bold'),bg='red',fg='white' ,width=9,height=1, command = show_stock)
    show_btn.grid(row=1,column=1,padx=4,pady=2)
    delete_btn = Button(button_frame, bd=6, text="Delete Bill", font=('Arial', 16, 'bold'), bg='red', fg='white', width=9, height=1, command=lambda: delete_bill_func())
    delete_btn.grid(row=1, column=2, padx=4, pady=2)


      #============== Calculater Frame =============#

    calc_frame = Frame(win, bd=8, relief=GROOVE, bg = 'lightgreen')
    calc_frame.place(x=585, y=90, width=650, height=295)

    scrollbarx = Scrollbar(calc_frame, orient = HORIZONTAL)
    scrollbary = Scrollbar(calc_frame, orient=VERTICAL)
    tree = ttk.Treeview(calc_frame, columns=("Ref. Id", "Name", "Phone", "Date", "Age"), selectmode="extended", yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set, height = 280)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Ref. Id', text="Ref. Id", anchor=W)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Phone', text="plant", anchor=W)
    tree.heading('Date', text="Date", anchor=W)
    tree.heading('Age', text="Age", anchor=W)
    tree.column('#0', stretch=YES, minwidth=0, width=0)
    tree.column('#1', stretch=YES, minwidth=0, width=80)
    tree.column('#2', stretch=YES, minwidth=0, width=180)
    tree.column('#3', stretch=YES, minwidth=0, width=120)
    tree.column('#4', stretch=YES, minwidth=0, width=150)
    tree.column('#5', stretch=YES, minwidth=0, width=80)
    tree.bind('<Double-Button-1>', OnSelected)
    tree.pack()

    a = mycursor.execute("select ref, name, phone, date, age from data").fetchall()
    for data in a:
            tree.insert('', 'end', values=(data))


    # =========================================

    # =====================Food Frame =======================

    food_frame = Frame(win, bd=8, relief=GROOVE, bg = 'lightgreen')
    food_frame.place(x=20, y=400, width=500, height=320)

    Button(food_frame, text= "Add New+", bd = 4, relief = FLAT, command = add_new).place(x = 40, y = 7, width = 100, height = 30)

    tree_box = Frame(food_frame, bg = 'lightgreen')
    tree_box.place(x= 0, y = 50, width = 480, height= 270)

    scrollbary_1 = Scrollbar(tree_box, orient=VERTICAL)
    tree_1 = ttk.Treeview(tree_box, columns=("Medicine", "Price", "Stock"), selectmode="extended", yscrollcommand=scrollbary_1.set)
    scrollbary_1.config(command=tree_1.yview)
    scrollbary_1.pack(side=RIGHT, fill=Y)
    tree_1.heading('Medicine', text = "Plant", anchor = W)
    tree_1.heading('Price', text = "Price", anchor = W)
    tree_1.heading('Stock', text = "Stock", anchor = W)
    tree_1.column('#0', minwidth = 0, width = 100)
    tree_1.column('#1', minwidth = 0, width = 100)
    tree_1.column('#2', minwidth = 0, width = 100)
    tree_1.bind('<Double-Button-1>', update_food)
    tree_1.pack()

    a = mycursor.execute("select * from food").fetchall()
    for data in a:
            tree_1.insert('', 'end', values=(data))
    

    # ========================================================

     # ===============Bill Frame ==============#

    bill_frame = LabelFrame(win, text="Bill Area", font=(
        "Arial", 18), background="lightgreen", bd=8, relief=GROOVE)
    bill_frame.place(x=550, y=400, width=700, height=320)

    y_scroll = Scrollbar(bill_frame, orient="vertical")
    bill_txt = Text(bill_frame, bg="white",fg='black', yscrollcommand=y_scroll.set)
    y_scroll.config(command=bill_txt.yview)
    y_scroll.pack(side=RIGHT, fill=Y)
    bill_txt.pack(fill=BOTH, expand=TRUE)
    bill_txt.config(state = DISABLED)



def main():
    
    def check_name(inp):
        if inp.isalpha() or inp.isspace():
            return True
        else:
            return False

    def check_phone(inp, var, action, l):
        l = int(l)
        if action == "0":
            if l == 3:
                icost(var[:-1])
            if l == 3 and (inp == var):
                addMedicine.config(state = DISABLED)
                cost.set("")
            elif l == 10 :
                go.config(state = DISABLED)
            return True
        elif action == "1" and inp.isdigit():
            if l == 3 and len(var) < l:
                icost(var+inp)
            if l == 10 and len(var) == 9:
                go.config(state = NORMAL)
            if len(var) >= l:
                if l == 10:
                    txtDob.focus_set()
                elif l == 2:
                    txtPatientAddress.focus_set()
                return False
            return True
        else:
            return False
 
    ADMIN_PASSWORD = "BLACK MONEY"
  

    def prompt_for_admin_password():
        # Prompt the user for the admin password
        password = simpledialog.askstring("Admin Access", "Enter admin password:", show='*')
        
        if password == ADMIN_PASSWORD:
            messagebox.showinfo("Access Granted", "Welcome, Admin!")
            return True  # Password is correct
        else:
            messagebox.showerror("Access Denied", "Incorrect password!")
            return False  # Password is incorrect






    def check_prescription(inp, var, action):
        nonlocal current_stock
        if action == '0':
            icost(var[:-1])
            no = current_stock
            if var[:-1] != '':
                no -= int(var[:-1])
                stock.set(str(no))
            if inp == var:
                stock.set(str(current_stock))
                addMedicine.config(state = DISABLED)
                cost.set("")
            if int(stock.get())>=0:
                txtstock.config(fg = 'black')
            return True
        elif action == '1' and len(var) < 3 and inp.isdigit():
            no = current_stock
            no -= int(var+inp)
            if no < 0:
                return False
            stock.set(str(no))
            icost(var+inp)
            return True
        else:
            return False

    def searching(pass2):
        name= int(pass2.get(1.0, "end-1c"))
        if name != "" :
            a = mycursor.execute(f"select * from data where ref = '{name}'").fetchone()
            if not a:
                tkinter.messagebox.showinfo("ERROR", "No data found.")
            else:
                txtFrameDetail=Text(font=('aerial',12,'bold'),width=141,height=4,padx=2,pady=4)
                txtFrameDetail.insert(END, a[1])
                q=txtFrameDetail.get('1.0','end-1c')
                filename=tempfile.mktemp('.txt')
                open(filename,'w').write(q)
                os.startfile(filename)
        else:
            tkinter.messagebox.showinfo("ERROR", "No data found")
    def search():
        rd=Tk()
        ans = IntVar()
        rd.geometry('350x350')
        rd.title("Plants Details")
        rd.configure(bg='Light Green')
       
        nam1=Label(rd,text='Reference Id: ',font=('arial 15 bold'),bg='Light Green')
        nam1.pack(pady = 15)
        pass2=Text(rd, width = 20, height = 1, font=(
        'Arial', 15) )
        pass2.pack(pady = 10)
        
        btn=Button(rd, text= "Search", font=('Forte', 15), width=18, bd=4, command=lambda : searching(pass2) ,bg='Red')
        btn.pack(pady = 15)


        rd.mainloop()
    def iExist():
        iExist=tkinter.messagebox.askyesno("nursey Management Systems","Confirm if you want to exit")
        if iExist >0:
            root.destroy()
            return

    def icost(no):
        addMedicine.config(state = NORMAL)
        if no == "":
            no = NumberTablets.get()
        c = price[cmbNameTablets.get()]
        total = int(no) * int(c)
        cost.set(str(total))

    def iPrescription():
        a, b, c, d = 20, 15, 13, 14
        txtPresciption.config(state = NORMAL)
        txtPresciption.delete("1.0",END)
        txtPresciption.insert(END, "                              NURSERY STORE MANAGEMENT \n                     GHATSHILA, JHARKHAND, PIN - 832303\n                        *****************************\n")
        txtPresciption.config(font = "consolas 12")
        txtPresciption.insert(END, f"Reference No.: {txtRef.get()}                                      Date - {txtIssuedDate.get()}\n")
        txtPresciption.insert(END, f"Name: {txtPatientName.get()}\nPhone: {txtPatientPhoneNo.get()}                   Age: {txtDob.get()}\nAddress: {txtPatientAddress.get()}\n----------------------------------------------------------------------------\n\n====================================BILL==================================\n")
        txtPresciption.insert(END, "+"+"-"*a+"+"+"-"*b+"+"+"-"*c+"+"+"-"*d+"+\n|  PLANT             |  pants guarantee  |  QUANTITY   |  PRICE       |\n+--------------------+---------------+-------------+--------------+\n")
        txtPresciption.config(state = DISABLED)

    def iPresciptionData():
        if int(stock.get()) < 0:
            messagebox.showerror("error", "Not enough stock")
            return
        nonlocal total_price
        addMedicine.config(state = DISABLED)
        btncost.config(state = NORMAL)
        txtPresciption.config(state = NORMAL)
        a, b, c, d = 19, 14, 12, 13
        name = cmbNameTablets.get()
        lname = len(name)
        no = NumberTablets.get()
        lno = len(no)
        exp = ExpDate.get()
        lexp = len(exp)
        total = cost.get()
        ltotal = len(total)
        txtPresciption.insert(END, "| "+name+" "*(a-lname) +"| "+exp+" "*(b-lexp) + "| "+no+" "*(c-lno) + "| "+total+" "*(d-ltotal)+"|\n")
        txtPresciption.insert(END, "+--------------------+---------------+-------------+--------------+\n")
        txtPresciption.config(state = DISABLED)
        total_price += int(total)
        st = int(no)
        mycursor.execute(f"update food set stock = stock - '{st}' where item = '{name}' ")
        con.commit()
        set_stock(name)
        

    def add_total():
        btnPrescription.config(state = NORMAL)
        btnPresciptionData.config(state = NORMAL)
        txtPresciption.config(state = NORMAL)
        l = len(str(total_price))
        txtPresciption.insert(END, f"| TOTAL:   =====     |      ====     |     ====    | {total_price}"+" "*(13 - l) +"|\n")
        txtPresciption.insert(END, "+--------------------+---------------+-------------+--------------+\n=================================THANK YOU=================================")
        txtPresciption.config(state = DISABLED)

    def print_slip():
        text = txtPresciption.get('1.0', END)
        with open("slip.txt", 'w') as f:
            f.write(text)
        os.startfile('slip.txt')

    def save_slip():
        mycursor.execute(f"insert into data values('{Ref.get()}', '{IssuedDate.get()}', '{PatientName.get()}', '{PatientPhoneNo.get()}', '{DateofBirth.get()}', '{txtPresciption.get('1.0', END)}' )")
        con.commit()
        tkinter.messagebox.showinfo("", "Records Saved")

    def iReset():
        nonlocal total_price
        total_price = 0
        root.destroy()
        main()

    def enable_disable(ev):
        txtPatientName.config(state = ev)
        txtPatientPhoneNo.config(state = ev)
        txtDob.config(state = ev)
        txtPatientAddress.config(state = ev)
        go.config(state = ev)

    def generate_prescription():
        msg = ""
        check = 0
        if PatientName.get() == "":
            msg = "Enter customer Name"
        else:
            check += 1

        if PatientPhoneNo.get() == "":
            msg = "Enter customer Phone number"
        else:
            check += 1
        
        if DateofBirth.get() == "":
            msg = "Enter the age"
        else:
            check += 1
        if PatientAddress.get() == "":
            msg = "Enter the address"
        else:
            check += 1
        if check == 4:
            enable_disable("disable")
            iPrescription()
            lblNameTablet.grid(row=7, column=0, sticky=W)
            cboNameTablet.grid(row=7, column=1, pady = 5)
            lblDose.grid(row=8, column=0, sticky=W)
            cboDose.grid(row=8, column=1, pady = 5)
            lblstock.grid(row = 9, column = 0, sticky = W)
            txtstock.grid(row=9, column=1, pady = 5)
            lblcost.grid(row=10, column=0, sticky=W)
            txtcost.grid(row=10, column=1, pady = 5)
            lblExpDate.grid(row=11, column=0, sticky=W)
            txtExpDate.grid(row=11, column=1, pady = 5)
            addMedicine.grid(row = 12, column = 0, columnspan = 2, pady = 10)

        else:
            tkinter.messagebox.showerror("error", msg)

    def set_stock(val):
        nonlocal current_stock, stock_dic, price
        mycursor.execute("select * from food")
        for i, j, k in mycursor:
            price[i] = j
            stock_dic[i] = k
        stock.set(stock_dic[val])
        current_stock = int(stock.get())
        # NumberTablets.set('')
        cost.set('')
        if NumberTablets.get() == '':
            addMedicine.config(state = DISABLED)
        else:
            addMedicine.config(state = NORMAL)
            st = int(stock_dic[val]) - int(NumberTablets.get())
            stock.set(st)
            icost(NumberTablets.get())
            if st < 0 :
                txtstock.config(fg = 'red')
            else:
                txtstock.config(fg = 'black')



    def update_medicine_image(event):
        selected_medicine = medicine_combobox.get()  # Get the selected medicine from the combobox
        print(f"Selected Medicine: {selected_medicine}")

        # Define the image path based on the selected medicine name
        image_path = os.path.join("E:\\REVATHY FINAL CS PROJECT (2)\\REVATHY FINAL CS PROJECT (2)\\HMS\\chaiti", f"{selected_medicine}.png")
        print(f"Image Path: {image_path}")

        # Check if the image file exists
        if os.path.exists(image_path):
            try:
                img = Image.open(image_path)
                img = img.resize((150, 150))  # Adjust size as needed
                img = ImageTk.PhotoImage(img)
                medicine_image_label.config(image=img)
                medicine_image_label.image = img  # Keep a reference to avoid garbage collection
            except Exception as e:
                print(f"Error opening image: {e}")
        else:
            print(f"No image found at: {image_path}")
            medicine_image_label.config(image='')  # Clear image if not found
            # Optionally, display a placeholder or default image if no image is found

    def open_image():
        medicine_name = medicine_combobox.get()
        image_path = f"{medicine_name}.png"  # Assuming image names match medicine names
    
        new_window = tk.Toplevel(root)  # Create a new window
        new_window.title(medicine_name)

        img = Image.open(image_path)
        img_tk = ImageTk.PhotoImage(img)
    
        label = tk.Label(new_window, image=img_tk)
        label.image = img_tk  # Keep a reference to avoid garbage collection
        label.pack()



    #--------------------------------------------------------------Frame----------------------------------------------------------------------------------------------------------------------------------
    root=Tk()
    root.title("NURSERY MANAGEMNET SYSTEM")
    root.geometry("1350x700+0+0")
    root.configure(background='Light Green')


    TitleFrame =Frame(root, bd=10, padx=20, relief=RIDGE,bg='maroon')
    TitleFrame.pack(side=TOP, fill = X)
    

    



    #------------------------------------VARIABLES-------------------------------------
    price = {}
    stock_dic = {}
    mycursor.execute("select * from food")
    for i, j, k in mycursor:
        price[i] = j
        stock_dic[i] = k
    cmbNameTablets=StringVar()
    Ref=StringVar()
    Dose=StringVar()
    NumberTablets=StringVar()
    IssuedDate=StringVar()
    ExpDate=StringVar()
    PatientPhoneNo=StringVar()
    PatientName=StringVar()
    PatientAddress=StringVar()
    Prescription=StringVar()
    stock = StringVar()
    DateofBirth = StringVar()
    Ref.set(random.randint(100000,9999999))
    IssuedDate.set(time.strftime("%d/%m/%y"))
    cost=StringVar()
    total_price = 0
    current_stock = 0
    # -----------------------------------------------------------------------------------------------

    lblTitle =Label(TitleFrame, font=("Algerian",40,"bold"), text="\tNURSERY MANAGEMENT \t", padx=2,bg='Misty Rose')
    lblTitle.pack(fill = X)

    # FrameDetail =Frame(MainFrame, bd=20, width=1350, height=400, padx=20, relief=RIDGE,bg='Misty Rose')
    # FrameDetail.pack(side=BOTTOM)

    ButtonFrame =Frame(root, bd=15, width=1350, padx=20, relief=RIDGE,bg='Misty Rose')
    ButtonFrame.pack(side=TOP)

    DataFrame =Frame(root, bd=20, padx=20, relief=RIDGE,bg='Misty Rose')
    DataFrame.pack(side=TOP, fill = BOTH)

    DataFrameLEFT=Frame(root, bd=10, padx=20, relief=RIDGE,bg='Misty Rose', width = 0.48 * root.winfo_width())
    DataFrameLEFT.pack(anchor = NW, side = LEFT, padx = 10, pady = 10)

    DataFrameRIGHT =Frame(root, bd=10, relief=RIDGE,bg='Misty Rose' )
    DataFrameRIGHT.pack(side = RIGHT, fill = Y, padx = 10, pady = 10)

    #------------------------------------------------------------DataFrameLEFT------------------------------------------------------------------------------------------------------------------------------------------------
    lblRef =Label(DataFrameLEFT, font=("arial",12,"bold"), text="Reference No. :", padx=2, pady=2,bg='Misty Rose')
    lblRef.grid(row=0, column=0, sticky=W)
    txtRef=Entry(DataFrameLEFT, font=("arial",12,"bold"), text="Reference No. :",  textvariable=Ref, width= 25,state=DISABLED)
    txtRef.grid(row=0, column=1, pady = 5)

    lblIssuedDate =Label(DataFrameLEFT, font=("arial",12,"bold"), text="Issued Date", padx=2, pady=2,bg='Misty Rose')
    lblIssuedDate.grid(row=1, column=0, sticky=W)
    txtIssuedDate=Entry(DataFrameLEFT, font=("arial",12,"bold"), text="Issued Date",  textvariable=IssuedDate, width= 25,state=DISABLED)
    txtIssuedDate.grid(row=1, column=1, pady = 5)
    
    lblPatientName =Label(DataFrameLEFT, font=("arial",12,"bold"), text="customer name", padx=2, pady=2,bg='Misty Rose')
    lblPatientName.grid(row=2, column=0, sticky=W)
    txtPatientName=Entry(DataFrameLEFT, font=("arial",12,"bold"), text="customer name",  textvariable=PatientName, width= 25)
    txtPatientName.grid(row=2, column=1, pady = 5)
    check_name_var = root.register(check_name)
    txtPatientName.config(validate = 'key', validatecommand = (check_name_var, "%S"))
    
    lblPatientPhoneNo =Label(DataFrameLEFT, font=("arial",12,"bold"), text="Phone No.", padx=2, pady=2,bg='Misty Rose')
    lblPatientPhoneNo.grid(row=3, column=0, sticky=W)
    txtPatientPhoneNo=Entry(DataFrameLEFT, font=("arial",12,"bold"), text="Phone No.", textvariable=PatientPhoneNo, width= 25)
    txtPatientPhoneNo.grid(row=3, column=1, pady = 5)
    check_phone_var = root.register(check_phone)
    txtPatientPhoneNo.config(validate = 'key', validatecommand = (check_phone_var, "%S", '%s', '%d', 10) )

    lblDob =Label(DataFrameLEFT, font=("arial",12,"bold"), text="Age", padx=2, pady=2,bg='Misty Rose')
    lblDob.grid(row=4, column=0, sticky=W)
    txtDob=Entry(DataFrameLEFT, textvariable=DateofBirth, font=("arial",12,"bold"), width= 25)
    txtDob.grid(row=4, column=1, pady = 5)
    txtDob.config(validate = 'key', validatecommand = (check_phone_var, "%S", '%s', '%d', 2))

    lblPatientAddress =Label(DataFrameLEFT, font=("arial",12,"bold"), text="customer Address", padx=2, pady=2,bg='Misty Rose')
    txtPatientAddress=Entry(DataFrameLEFT, font=("arial",12,"bold"), text="customer Address", textvariable=PatientAddress, width= 25)
    lblPatientAddress.grid(row=5, column=0, sticky=W)
    txtPatientAddress.grid(row=5, column=1, pady = 5)

    go = Button(DataFrameLEFT, text = "Generate bill", font = ("arial",12,"bold"), width = 40, command = generate_prescription, state = DISABLED)
    go.grid(row = 6, column = 0, columnspan = 2, pady = 10)

    lblNameTablet =Label(DataFrameLEFT, font=("arial",12,"bold"), text="Name of plant :", padx=2, pady=2,bg='Misty Rose')
    cboNameTablet=OptionMenu(DataFrameLEFT, cmbNameTablets, *price.keys(), command = set_stock)
    # cmbNameTablets.set(list(price.keys())[0])
    # stock.set(stock_dic[cmbNameTablets.get()])
        # Create a combobox for selecting medicine (updated to be labeled "Name of Tablets")
    medicines = ["Asian Ginseng", "American Ginseng", "Panax notoginseng",
                 "Himalayan ginseng", "Panax vietnamensis",
                 "mountain ginseng","Spider orchid", "Cattleyas", "Boat Orchid",
                 "Jewel orchids", "Dancing Lady Orchids",
                 "Pansy Orchids","Moth Orchid", "Swamp orchids ",
                 "Lady slipper orchid","Butterfly Orchid",
                 "Old Lady Cactus ", "Rainbow Hedgehog","Ric Rac Cactus",
                 "Lithops",
                 "Turks Cap Cactus","Cereus Cactus", "Thanksgiving Cactus",
                 "Tom Thumb",
                 "Mistletoe Cactus", "Moon Cactus", "Laceleaf",
                 "Philodendron",
                 "Arum Lilies", "Alocasia","Monstera",
                 "Pothos", "Zanzibar Gem",
                 "Caladium", "Peace lily", "Elephants ears",
                 "Queen of the Night",
                 "ghost orchid", "Lady of the night","velvet-leaved ",
                 "mistletoe cacti", "vanilla orchids","Bulbophyllum",
                 "air plants", "milkweeds","Anthurium clarinervium",
                 "Rosa Juliet"]  
    medicine_combobox = ttk.Combobox(root, values=medicines, textvariable=cmbNameTablets)
    medicine_combobox.pack(pady=10)

    # Update the medicine image when selection changes
    medicine_combobox.bind("<<ComboboxSelected>>", update_medicine_image)


    # Remove the extra box by not creating an additional Text or Entry widget in this area

    # Button to update the image directly below the combobox
    open_button = tk.Button(root, text="show image", command=open_image)
    open_button.pack(pady=10)

    # Rest of your layout and widget setup...

    
    # Label for medicine image
    
    lblDose =Label(DataFrameLEFT, font=("arial",12,"bold"), text="Quantity :", padx=2, pady=2,bg='Misty Rose')
    # values=("1","2","3","4","5","6","7","8","9","10","11","12","13","14","15")
    cboDose=Entry(DataFrameLEFT, textvariable=NumberTablets, font=("arial",12,"bold"), width= 25)
    cboDose.config(font=('arial',12,'bold')) 
    check_prescrip_var = root.register(check_prescription)
    cboDose.config(validate = 'key', validatecommand = (check_prescrip_var, "%S", '%s', '%d'))

    lblstock = Label(DataFrameLEFT, font=('arial',12,'bold'), text="Stock", padx=2, pady=2, bg='Misty Rose')
    txtstock=Entry(DataFrameLEFT, font=("arial",12,"bold"),textvariable=stock, state='readonly', bg = 'white')

    def p(event):
        global cal,dw
        dw=Toplevel()
        dw.grab_set()
        dw.title("calendar")
        dw.geometry('250x220+590+370')
        cal=Calendar(dw,selectmode='day',date_pattern='dd/mm/y')
        cal.place(x=0,y=0)
        sb=Button(dw,text="select",command=g)
        sb.place(x=90,y=190)
    def g():
        global wox
        today = date.today()
        y = today.year
        m = today.month
        d = today.day
        wox=f"{d}/{m}/{y}"
        d1=datetime.strptime(wox,"%d/%m/%Y")
        d2=datetime.strptime(cal.get_date(),"%d/%m/%Y")
        result=d2-d1
        if result.days<0:
            dw.destroy()
            messagebox.showerror("showerror","Please enter correct date!") 
        elif result.days>=0:
            txtExpDate.delete(0,END)
            txtExpDate.insert(0,cal.get_date())
            dw.destroy()
            
    lblExpDate =Label(DataFrameLEFT, font=("arial",12,"bold"), text="plant guarantee", padx=2, pady=2,bg='Misty Rose')
    txtExpDate=DateEntry(DataFrameLEFT, textvariable=ExpDate, width= 15)
    txtExpDate.bind("<1>",p)
    
    lblcost=Label(DataFrameLEFT, font=("arial",12,"bold"), text="Total Cost", padx=2, pady=2,bg='Misty Rose')
    txtcost=Entry(DataFrameLEFT, font=("arial",12,"bold"),textvariable=cost, state='readonly', bg = 'white')



    addMedicine = Button(DataFrameLEFT, text = "Add MOBILE ", font = ("arial",12,"bold"), width = 40, command = iPresciptionData, state = DISABLED)

    #--------------------------------------------------------------Data_Frame_Right------------------------------------------------------------
    scrx = Scrollbar(DataFrameRIGHT, orient = VERTICAL)
    scrx.pack(side = RIGHT, fill = Y)
    txtPresciption=Text(DataFrameRIGHT, font="monospace 14", padx = 5, pady = 5, width = 100, height = 100, yscrollcommand = scrx.set, fg = 'grey20', state = DISABLED)
    txtPresciption.pack(fill = BOTH)
    scrx.config(command = txtPresciption.yview)
    # txtPresciption.config(state = DISABLED)
    #---------------------------------------------------------------ButtonFrame----------------------------------------------------------------

    btncost=Button(ButtonFrame, text= "TOTAL", font=('Forte', 15), width=18, bd=4, command=add_total,bg='Purple', state = DISABLED)
    btncost.grid(row=0, column=0)
    btnPrescription=Button(ButtonFrame, text= "PRINT", font=('Forte', 15), width=18, bd=4, command=print_slip,bg='light blue', state = DISABLED)
    btnPrescription.grid(row=0, column=1)
    btnPresciptionData =Button(ButtonFrame, text= "SAVE", font=('Forte', 15), width=18, bd=4, command=save_slip,bg='Orange', state = DISABLED)
    btnPresciptionData.grid(row=0, column=2)
        # Example function to open the database window after checking credentials
    btnSea = Button(ButtonFrame, text="DATABASE", font=('Forte', 15), width=18, bd=4,
                    command=lambda: check_access_and_open_database())
    btnSea.grid(row=0, column=3)

    def check_access_and_open_database():
        if prompt_for_admin_password():  # Check if the password is correct
            Window3(Toplevel(root))  # Open the database window

   


   

    btnReset=Button(ButtonFrame, text= "RESET", font=('Forte', 15), width=18, bd=4, command=iReset,bg='Brown')
    btnReset.grid(row=0, column=4)
    btnExist=Button(ButtonFrame, text= "EXIT", font=('Forte', 17), width=18, bd=4, command=iExist,bg='Red')
    btnExist.grid(row=0, column=5)
    root.protocol("WM_DELETE_WINDOW", iExist)
   


    root.mainloop()
    #------------------------------------------------------------FrameDetail----------------------------------------------------------------------------------------------------------------------------------------------------------------
def login_page1():
     
    
     
     root=tkinter.Tk()
     root.title("LOGIN")
     root.geometry("900x440")
     root.resizable(0,0)
     image = Image.open("newscreen (1).png")
     img = ImageTk.PhotoImage(image)

     iml=Label(root,image=img)
     iml.place(x=0,y=0)
     def log():
          
          cursor=cop.cursor()
          user=name2.get()
          passw=pass2.get()
          w=False
          query="select username,password from register"
          cursor.execute(query)
          
          data=cursor.fetchall()
          for i in data:
               if user in i and passw in i:
                    
                    w=True
                    break
               else:
                     w=False
          if w==False:
               
              lable_nok=Label(root,text='Enter correct username or password !',font=("Microsoft YeHei UI Light",10),bg="grey",fg="white")
              lable_nok.place(x=100,y=190)   
              lable_nok.after(3000,lambda:lable_nok.destroy())
          else:
              root.destroy()
              main()

          #-----------------------------------

     l=Label(root,text="Username *",bg='black',font=('Arial', 14),fg='white')
     l.place(x=150,y=130)
     name2=Entry(root)
     name2.place( x = 150, y = 160)

     
     l=Label(root,text="Password*",bg='black',font=('Arial', 14),fg='white')
     l.place(x=150,y=200)
     pass2=Entry(root,show="*")
     pass2.place( x = 150, y = 235)
     l=Label(root,text="Don't Have An Account?*",bg='green',font=('Arial', 14),fg='white')
     l.place(x=100,y=380)

     def forget():
         def back2():
             forget.destroy()
             login_page1()
         def con_forget():
             
            mail=e1.get()
            p=e3.get()
            o=e4.get()
            recov=e2.get()
            w=False
            cursor=cop.cursor()
            query="select email ,rque from register"
            cursor.execute(query)
            data=cursor.fetchall()
            if mail=='' or p=='' or o=='' or recov=='':
                messagebox.showerror("error","Enter Details")
            elif p=='' or o=='':
                messagebox.showerror("error","Enter Password")
                
            else:
                
                for i in data:
                    if mail in i and recov in i:
                        w=True
                        break
                if w==False:
                    lable_nok=Label(fr,text='Enter correct email and Recovery Question !'
                                    ,font=("Microsoft YeHei UI Light",11),bg="white",fg="red")
                    lable_nok.place(x=150,y=130)
                    lable_nok.after(3000,lambda:lable_nok.destroy())
                else:
                    p=e3.get()
                    o=e4.get()
                    if p==o:
                        mycurso=cop.cursor()        
                        query="update register set password='{}' where email='{}'".format(p,mail)
                        mycurso.execute(query)
                        cop.commit()
                        forget.destroy()
                        login_page1()
                    else:
                        lable_nok=Label(fr,text='New password and confirm password not matched !',
                                        font=("Microsoft YeHei UI Light",10),bg="white",fg="red")
                        lable_nok.place(x=120,y=145)
                        lable_nok.after(3000,lambda:lable_nok.destroy())
 #--------------------------------------------------------------------            
         root.destroy()
         forget=Tk()
         forget.title("Forget")
         forget.geometry("720x400")
         forget.config(bg="white")

         fr=Frame(forget,bg='grey',width=500,height=200)
         fr.place(x=100,y=50)

         e1=Entry(fr,font=('arial', 12))
         e1.place( x = 250, y = 30)
         e2=Entry(fr,font=('arial', 12))
         e2.place( x = 250, y = 60)
         e3=Entry(fr,font=('arial', 12))
         e3.place( x = 250, y = 90)
         e3.config(show='*')
         e4=Entry(fr,font=('arial', 12))
         e4.place( x = 250, y = 120)
         e4.config(show='*')

         l=Label(fr,text="Email*",bg='grey',fg='white',font=('arial', 12))
         l.place(x=30,y=30)
         l=Label(fr,text="Recovery Keywords*",bg='grey',fg='white',font=('arial', 12))
         l.place(x=30,y=60)
         l=Label(fr,text=" Password*",bg='grey',fg='white',font=('arial', 12))
         l.place(x=27,y=90)
         l=Label(fr,text="Confirm Password*",bg='grey',fg='white',font=('arial', 12))
         l.place(x=30,y=120)

         o=Button(forget,text="<Back",bg="white",fg="Black",command=back2)
         o.place( x = 0, y = 0)
         o=Button(forget,text="confirm",bg="Black",fg="white",command=con_forget)
         o.place( x = 350, y = 250)


         
         forget.mainloop()
         
     
     

     def sign_up():
               def back1():
                    sign.destroy()
                    login_page1()
          
          
               root.destroy()
               sign=Tk()
               sign.title("Sign Up")
               sign.geometry("720x480")
               sign.config(bg="white")
               def validate_fullname(char):
                 return char.isalpha() or char == " "
               def validate_phone(char):
                    return char.isdigit()
               

               def signup():
                    n=e1.get()
                    un=e2.get()
                    em=e3.get()
                    gen=gend.get()
                    ad=e5.get()
                    ph=e6.get()
                    pa=e7.get()
                    cpa=e8.get()
                    reco=e9.get()
                    if not all([n, un, em, gen, ad, ph, pa, cpa, reco]):
                        messagebox.showerror("Fill","Please Enter Details")
                        return
                    elif n==" " or un==" " or em==" " or gen==' ' or ad==' ' or ph=='' or pa=='' or  cpa=='' or reco=='' :
                        messagebox.showerror("Fill","Incomplete Fields Enter All Fields")
                        return
                    
                    elif  n.isdigit():
                        messagebox.showerror("Error","Enter  A Valid Name")
                    elif "@" not in em or "." not in em:
                        messagebox.showerror("Error","Enter  A Valid Email")
                    elif not ph.isdigit() or len(ph)!=10:
                        messagebox.showerror("Error","Check Your Phone Number")
                        
                    elif pa!=cpa:
                        messagebox.showerror("Error","Check Your Password")
                    else:
                        cursor=cop.cursor()
                        query='''Insert into register values
                        ('{}','{}','{}','{}','{}','{}','{}','{}','{}')'''.format(n,un,em,gen,ad,ph,pa,cpa,reco)         
                        cop.execute(query)
                        cop.commit()
                        messagebox.showinfo("succesful","Sign Up succesfully")
                        sign.destroy()
                        login_page1()
                        

                    

               e1 = Entry(sign, font=('arial', 12), validate="key")
               e1['validatecommand'] = (e1.register(validate_fullname), '%S')
               e1.place( x = 300, y = 50)
               e2=Entry(sign,font=('arial', 12))
               e2.place( x = 300, y = 90)
               e3=Entry(sign,font=('arial', 12))
               e3.place( x = 300, y = 130)
               gend=ttk.Combobox(sign,font=('arial',12),width=20)
               gend["value"]=["Male","Female","Others"]
               gend.place( x = 300, y = 170)
               e5=Entry(sign,font=('arial', 12))
               e5.place( x = 300, y = 210)
               e6=Entry(sign,font=('arial', 12))
               e6['validatecommand'] = (e6.register(validate_phone), '%S')
               e6.place( x = 300, y = 250)
               e7=Entry(sign,font=('arial', 12))
               e7.place( x = 300, y = 290)
               e7.config(show='*')
               e8=Entry(sign,font=('arial', 12))
               e8.place( x = 300, y = 330)
               e8.config(show='*')
               e9=Entry(sign,font=('arial', 12))
               e9.place( x = 300, y = 370)
               



               l=Label(sign,text="Full Name*",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=50)
               l=Label(sign,text="Username *",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=90)
               l=Label(sign,text="Email *",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=130)
               l=Label(sign,text="Gender*",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=170)
               l=Label(sign,text="Address *",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=210)
               l=Label(sign,text="Phone No. *",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=250)
               l=Label(sign,text="Password*",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=290)
               
               
               l=Label(sign,text="Confirm Password*",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=330)
               l=Label(sign,text="Security Keyword *",bg='white',font=('arial', 12),fg='black')
               l.place(x=150,y=370)
               

               o=Button(sign,text="Sign Up",height="2",width="15",bg="orange",fg="Black",command=signup)
               o.place( x = 500, y = 300)
               o=Button(sign,text="<Back",bg="white",fg="Black",command=back1)
               o.place( x = 0, y = 0)

               sign.mainloop()


     o=Button(text="Login",bg="orange",fg="Black", command=log)
     o.place( x = 180, y = 260)
     o=Button(text="Sign Up",width="10",bg="blue",fg="white", command=sign_up)
     o.place( x = 350, y = 380)
     o=Button(text="Forget Password",width="15",bg="yellow",fg="black", command=forget)
     o.place( x = 250, y = 260)

     root.mainloop()
login_page1()


'''
def login_register():

    def change(user, pas, ans, inp, rs):
        if ans.get() == inp:
            mycursor.execute(f"update adm set password = '{pas.get()}' where username = '{user.get()}'")
            con.commit()
            tkinter.messagebox.showinfo("DONE", "Password changed!", parent = rs)
            rs.destroy()
        else:
            tkinter.messagebox.showerror("error", "Wrong answer to security question", parent = rs)

    def go_check(rs, name, email, ):
        answer = StringVar()
        password = StringVar()
        a = mycursor.execute(f"select * from adm where username = '{name.get()}' and email = '{email.get()}'").fetchone()
        if a:
            ques = a[3]
            ans = a[4]
            Label(rs,text=f"What is your {ques}").pack(pady = 10)
            pass2=Entry(rs,textvariable=answer).pack()
            
            Label(rs, text = "Enter new password *").pack()
            ent = Entry(rs, textvariable = password).pack(pady = 10)

            Button(rs,text="Change",bg="purple",fg="white",command= lambda : change(name, password, answer, ans, rs)).pack(pady = 10)
        else:
            tkinter.messagebox.showinfo("ERROR", "Wrong username or email! ", parent = rs)

    def forget():
        name=StringVar()
        email = StringVar()
        register_screen=Toplevel(main_screen)
        register_screen.title("Forgot Password Screen")
        register_screen.geometry("300x450")
        Label(register_screen,text="Forgot Password",height="2",width="300").pack()
        Label(text="").pack()

        Label(register_screen,text="User Name *").pack()
        name2=Entry(register_screen,textvariable=name)
        name2.pack(pady = 10)

        Label(register_screen,text="Email *").pack()
        pass2=Entry(register_screen,textvariable=email)
        pass2.pack(pady = 10)

        Button(register_screen,text="GO",bg="purple",fg="white",command= lambda : go_check(register_screen, name, email)).pack(pady = 10)

    def login_user(name, pas, n, p, wd):
        name=name.get()
        password=pas.get()
        n.delete(0,END)
        p.delete(0,END)
        if name != "" and password != "" :
            a = mycursor.execute(f"select * from adm where username = '{name}' and password = '{password}'").fetchone()
            if not a:
                tkinter.messagebox.showinfo("ERROR", "Wrong username or password.", parent = wd)
            else:
                main_screen.destroy()
                main()



    def login():
        login_screen=Toplevel(main_screen)
        login_screen.title("Login Screen")
        login_screen.geometry("300x300")
        Label(login_screen,text="Login Screen",height="2",width="300").pack()
        Label(text="").pack()
        Label(login_screen,text="Name *").pack(pady = 10)
        name3=StringVar()
        password3=StringVar()
        nam=Entry(login_screen,textvariable=name3)
        nam.pack(pady = 10)
        Label(login_screen,text="Password *").pack()
        pas=Entry(login_screen,textvariable=password3,show= '*')
        pas.pack(pady = 10)

        Button(login_screen,text="login",bg="purple",fg="white",command=lambda : login_user(name3, password3, nam, pas, login_screen)).pack(pady = 10)

        Button(login_screen,text="forgot password",bg="purple",fg="white", command = forget ).pack(pady = 10)

    def registration():
        # global register_screen, name, password, email, question, ans
        name=StringVar()
        password=StringVar()
        email = StringVar()
        question = StringVar()
        ans = StringVar()
        question.set("Favourite color")
        register_screen=Toplevel(main_screen)
        register_screen.title("Registration Screen")
        register_screen.geometry("300x450")
        Label(register_screen,text="Registration Screen",height="2",width="300").pack()
        Label(text="").pack()

        Label(register_screen,text="Name *").pack()
        name2=Entry(register_screen,textvariable=name)
        name2.pack(pady = 10)

        Label(register_screen,text="Password *").pack()
        pass2=Entry(register_screen,textvariable=password,show= '*')
        pass2.pack(pady = 10)

        Label(register_screen,text="Email *").pack()
        pass2=Entry(register_screen,textvariable=email)
        pass2.pack(pady = 10)

        Label(register_screen,text="Security queston *").pack()
        qlist = ['Favourite color', 'Favourite food', 'Faviourite person', 'Favourite fruit']
        drop = OptionMenu( register_screen , question , *qlist )
        drop.pack(pady = 10)

        Label(register_screen,text="Answer to question *").pack()
        pass2=Entry(register_screen,textvariable= ans )
        pass2.pack(pady = 10)

        Button(register_screen,text="Register",bg="purple",fg="white",command= lambda : register_user(name, password, email, question, ans)).pack(pady = 10)

    def register_user(name, password, email, question, ans):
        # error_msg = Label(rs,text="__",fg="red").pack(pady = 20)
        name1=name.get()
        pass1=password.get()
        email1 = email.get()
        ques1 = question.get()
        ans1 = ans.get()
        if name1 != "" and pass1 != "" and email1 != "" and ques1 != "" and ans1 != "":
            if "@" not in email1:
                tkinter.messagebox.showinfo("ERROR","Fill correct email")
                # error_msg.config(text = "Fill correct email!")
            else:
                names = mycursor.execute(f"select * from adm where username = '{name1}'").fetchall()
                if not names:
                    mycursor.execute(f"insert into adm values('{name1}', '{pass1}', '{email1}', '{ques1}', '{ans1}' )")
                    con.commit()
                    main_screen.destroy()
                    main()
                else:
                    tkinter.messagebox.showinfo("ERROR", "Username already exists!")
        else:
            tkinter.messagebox.showinfo("ERROR","Fill all the fields")
            # error_msg.config(text = "Fill all the fields!")
        


    main_screen=Tk()
    main_screen.geometry("300x250")
    main_screen.title("APOLO HOSPITAL")
    Label(text="SNSVM PHARMA STORE", bg="skyblue", fg="black",height="2",width="300").pack()
    Label(text="").pack()
    Button(text="Login",height="2",width="29",bg="pink",fg="white", command=login).pack()
    Label(text="").pack()
    Button(text="Registration",height="2",width="30",bg="pink",fg="white",command=registration).pack()
    main_screen.mainloop()


login_register()
'''
