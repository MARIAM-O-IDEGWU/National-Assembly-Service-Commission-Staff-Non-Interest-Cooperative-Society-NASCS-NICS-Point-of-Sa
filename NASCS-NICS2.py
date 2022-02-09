#==================imports===================
import sqlite3
import re
import os
from subprocess import call
import random
import tempfile
import string
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from time import strftime
from datetime import date
from tkinter import scrolledtext as tkst
import win32print
import win32api
import tkinter as tk
import pyscreenshot
from tkinter import filedialog
import csv
import datetime
#============================================



root = Tk()

root.geometry("1366x768")
root.title("Retail Manager")
root.config(bg="green")


user = StringVar()
passwd = StringVar()
fname = StringVar()
lname = StringVar()
new_user = StringVar()
new_passwd = StringVar()


cust_name = StringVar()
cust_num = StringVar()
cust_new_bill = StringVar()
cust_search_bill = StringVar()
bill_date = StringVar()
pdno=StringVar()
cstpd=StringVar()
prqty=StringVar()
icnmp=StringVar()
srchbll=StringVar()
fnobll=StringVar()
nambll=StringVar()
dtt=StringVar()

bno=StringVar()
bamt=StringVar()
bfn=StringVar()
bdbyr=StringVar()
sumup=StringVar()
ttsum=StringVar()
bdmnyr=StringVar()
entSTDT1=StringVar()
entEDDT1=StringVar()
sumsp=StringVar()
sumcp=StringVar()
sumprt=StringVar()
icnmr=StringVar()
icbil=StringVar()
icnmy=StringVar()


with sqlite3.connect("./Database/store.db") as db:
    cur = db.cursor()

def random_bill_number(stringLength):
    lettersAndDigits = string.ascii_letters.upper() + string.digits
    strr=''.join(random.choice(lettersAndDigits) for i in range(stringLength-2))
    return ('BB'+strr)


def valid_phone(phn):
    if phn:
        return True
    return False

def adm():
    #call(["python", "admin.py"])
    os.system("admin.py")


def login(Event=None):
    global username
    username = user.get()
    password = passwd.get()

    with sqlite3.connect("./Database/store.db") as db:
        cur = db.cursor()
    find_user = "SELECT * FROM employee WHERE emp_id = ? and password = ?"
    cur.execute(find_user, [username, password])
    results = cur.fetchall()
    if results:
        messagebox.showinfo("Login Page", "The login is successful")
        messagebox.showinfo("NOTICE", "Ensure you add Customers Name and File_No on the form before proceding")
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)
        root.withdraw()
        global biller
        global page2
        biller = Toplevel()
        page2 = bill_window(biller)
        page2.time()
        biller.protocol("WM_DELETE_WINDOW", exitt)
        biller.mainloop()

    else:
        messagebox.showerror("Error", "Incorrect username or password.")
        page1.entry2.delete(0, END)



def logout():
    sure = messagebox.askyesno("Logout", "Are you sure you want to logout?", parent=biller)
    if sure == True:
        biller.destroy()
        root.deiconify()
        page1.entry1.delete(0, END)
        page1.entry2.delete(0, END)

def profitnas():
    global prf
    global pageprf
    prf = Toplevel()
    pageprf = Profitnas(prf)
    prf.protocol("WM_DELETE_WINDOW", exitt)
    prf.mainloop()

global F5
global treep



class Profitnas:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("(NASCS-NICS)Profit")
        global lcmt

        self.labelp = Label(prf)
        self.labelp.place(relx=0, rely=0, width=1366, height=768)
        self.imgp = PhotoImage(file="./images/profit.png")
        self.labelp.configure(image=self.imgp)

        def nabill():
            cur = db.cursor()
            snrb = "select * from  bill"
            cur.execute(snrb, )
            trcrb.delete(*trcrb.get_children())
            fbtam = cur.fetchall()
            for dbm in fbtam:
                trcrb.insert('', 'end', values=(
                    dbm[0], dbm[1], dbm[2], dbm[3],dbm[4]))
                trcrb.pack(side='left', padx=0, pady=0)
                db.commit()

        def cmd_bill():
            global vrb
            global r2rb
            global rrb
            global lcmtb

            cur = db.cursor()
            vrb = icbil.get()
            srb= "select * from bill where CUSTOMER_NO=?"
            Lrb = (vrb,)
            rrb = cur.execute(srb, Lrb)
            rrb = cur.fetchall()
            trcrb.delete(*trcrb.get_children())
            if rrb:
              for r2rb in rrb:
                trcrb.insert(parent='', index='end', text='',values=(r2rb[0],r2rb[1],r2rb[2],r2rb[3],r2rb[4]))
                trcrb.heading("1st", text="BILL_NO")
                trcrb.heading("2nd", text="DATE")
                trcrb.heading("3rd", text="CUSTOMER_NAME")
                trcrb.heading("4th", text="CUSTOMER_NO")
                trcrb.heading("5th", text="BILL_DETAILS")
                trcrb.pack(side='left', padx=0, pady=0)
                db.commit()

        def delbil():
            cur = db.cursor()
            for selected_item in trcrb.selection():
               print(selected_item)
               cur.execute("DELETE from bill where customer_no=?",(trcrb.set(selected_item,"4th"),))
               db.commit()
               trcrb.delete(selected_item)

        def buyft():
            global Fdlb
            global trcrb
            def Clole():
                Fdlb.destroy()
            Fdlb = Frame(top, bg="green", relief=GROOVE, bd=10)
            Fdlb.place(x=730, y=230, width=600, height=250)
            lndrb = Label(Fdlb, text='BILLS', font='arial 15 bold', relief=GROOVE, bd=7).pack(fill=X)
            lndrqb = Label(Fdlb, text='SEARCH', font='arial 9').place(x=4, y=6)
            lnsr1b = tk.Entry(Fdlb,textvar=icbil, font=('bold', 12), width=7)
            lnsr1b.place(x=60, y=6)
            element_fdlb = ['1st', '2nd', '3rd', '4th', '5th']
            treeScrolb = tk.Scrollbar(Fdlb)
            treeScrolb.pack(side='right', fill='y')
            style = ttk.Style()
            style.configure("trcrb", highlightbackground="red")
            trcrb = ttk.Treeview(Fdlb, columns=element_fdlb, height=20, show="headings")
            trcrb.configure(yscrollcommand=treeScrolb.set)
            trcrb.column('1st', width=70, minwidth=50, stretch=tk.NO)
            trcrb.column('2nd', width=70, minwidth=50, stretch=tk.NO)
            trcrb.column('3rd', width=70, minwidth=50, stretch=tk.NO)
            trcrb.column('4th', width=70, minwidth=50, stretch=tk.NO)
            trcrb.column('5th', width=500, minwidth=500, stretch=tk.NO)
            sqlchb = "SELECT * FROM  bill"
            cur.execute(sqlchb, )
            trcrb.delete(*trcrb.get_children())
            fetchb = cur.fetchall()
            for datb in fetchb:
                trcrb.insert(parent='', index='end', text='', values=(datb[0],datb[1],datb[2],datb[3],datb[4]))
                trcrb.heading("1st", text="BILL_NO")
                trcrb.heading("2nd", text="DATE")
                trcrb.heading("3rd", text="CUSTOMER_NAME")
                trcrb.heading("4th", text="CUSTOMER_NO")
                trcrb.heading("5th", text="BILL_DETAILS")
                trcrb.pack(side='left', padx=0, pady=0)
                treeScrolb.config(command=trcrb.yview)
                bln = Button(Fdlb, bg="green", fg="white", width=7, text="Close", command=Clole).place(x=493, y=4)
                hadel1 = tk.Button(Fdlb, text='OK', bg='green', fg='white',command=cmd_bill).place(x=129, y=4)
                hbl1 = tk.Button(Fdlb, text='DELETE', bg='green', fg='white', command=delbil).place(x=159, y=4)
                harel1 = tk.Button(Fdlb, text="RESET", anchor="w", bg='green', fg='white',command=nabill).place(x=400, y=4)
                cnel1 = tk.Button(Fdlb, text="PRINT", anchor="w", bg='green', fg='white', command=cpro).place(x=443,y=4)


        def cpro():
            def Closecm():
                f9p.destroy()
            global usr
            f9p = Frame(relief=GROOVE, bd=10, bg='green')
            f9p.place(x=700, y=180, width=600, height=300)
            b9bi = Label(f9p, text='BILL REPORT', font='arial 15 bold', bg='white', bd=7, relief=GROOVE).pack(fill=X)
            sc_y = Scrollbar(f9p, orient=VERTICAL)
            ttrns = tk.Text(f9p, yscrollcommand=sc_y)
            sc_y.pack(side=RIGHT, fill=Y)
            sc_y.config(command=ttrns.yview)
            ttrns.pack()
            ttrns.tag_add("whole", "2.0", "end-1c")
            ttrns.tag_configure("whole", spacing3=10)
            user_in = ttrns.get(1.0, "end-1c")
            ttrns.delete(1.0, END)

            with open("pro.csv", "w", newline='',encoding="utf-8") as mcmtr:
                csvwriter = csv.writer(mcmtr, delimiter='|')
                hder = ['(NASCS-NICS)BILL REPORT']
                lne = ['--------------------------------------------------------']
                dta = ['BILL_NO       DATE  CUSTOMER_NAME  CUSTOMER_NO  BILL_DETAILS']
                csvwriter.writerow(hder)
                csvwriter.writerow(lne)
                csvwriter.writerow(dta)
                csvwriter.writerow(lne)

                for row_cm in trcrb.get_children():
                    row = trcrb.item(row_cm)['values']
                    if row_cm[0].isdigit():
                        csvwriter.writerow(row_cm)
                    csvwriter.writerow(lne)
                    csvwriter.writerow(row)

            with open("pro.csv", "r") as c:
                dtrc = c.read()
            ttrns.insert("1.0", dtrc)
            q = ttrns.get("1.0", "end-1c")
            filename = tempfile.mktemp(".txt")
            open(filename, "w").write(q)
            win32api.ShellExecute(0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
            clton = Button(f9p, bg="green", fg="white", width=9, text="CLOSE", command=Closecm).place(x=2, y=4)

        def refunin():
            global trcrr
            def rfecm():
                frp.destroy()
            global usr
            frp = Frame(relief=GROOVE, bd=10, bg='green')
            frp.place(x=700, y=180, width=600, height=300)
            b9bi = Label(frp, text='REFUND REPORT', font='arial 15 bold', bg='white', bd=7, relief=GROOVE).pack(fill=X)
            sc_y = Scrollbar(frp, orient=VERTICAL)
            trcrr1 = tk.Text(frp, yscrollcommand=sc_y)
            sc_y.pack(side=RIGHT, fill=Y)
            sc_y.config(command=trcrr1.yview)
            trcrr1.pack()
            trcrr1.tag_add("whole", "2.0", "end-1c")
            trcrr1.tag_configure("whole", spacing3=10)
            user_in = trcrr1.get(1.0, "end-1c")
            trcrr1.delete(1.0, END)

            with open("refun.csv", "w", newline='',encoding="utf-8") as mcmtr:
                csvwriter = csv.writer(mcmtr, delimiter='|')
                hder = ['(NASCS-NICS)REFUND REPORT']
                lne = ['--------------------------------------------------------']
                dta = ['BILL_NO       AMOUNT  FNO  DATE']
                csvwriter.writerow(hder)
                csvwriter.writerow(lne)
                csvwriter.writerow(dta)
                csvwriter.writerow(lne)

                for row_rf in trcrr.get_children():
                    row = trcrr.item(row_rf)['values']
                    if row_rf[0].isdigit():
                        csvwriter.writerow(row_rf)
                    csvwriter.writerow(lne)
                    csvwriter.writerow(row)

            with open("refun.csv", "r") as c:
                dtrc = c.read()
            trcrr1.insert("1.0", dtrc)
            q = trcrr1.get("1.0", "end-1c")
            filename = tempfile.mktemp(".txt")
            open(filename, "w").write(q)
            win32api.ShellExecute(0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
            rfton = Button(frp, bg="green", fg="white", width=9, text="CLOSE", command=rfecm).place(x=2, y=4)

        def nasrfnd():
            cur = db.cursor()
            snrf = "select * from  REFUND"
            cur.execute(snrf, )
            trcrr.delete(*trcrr.get_children())
            fetam = cur.fetchall()
            for dam in fetam:
                trcrr.insert('', 'end', values=(
                    dam[0], dam[1], dam[2], dam[3]))
                trcrr.pack(side='left', padx=0, pady=0)
                db.commit()

        def cmd_rend():
            global vr
            global r2r
            global rr
            global lcmt
            cur = db.cursor()
            vr = icnmr.get()
            sr= "select * from REFUND where BILLNO=?"
            Lr = (vr,)
            rr = cur.execute(sr, Lr)
            rr = cur.fetchall()
            trcrr.delete(*trcrr.get_children())
            if rr:
             for r2r in rr:
                trcrr.insert(parent='', index='end', text='', values=(r2r[0], r2r[1], r2r[2], r2r[3]))
                trcrr.heading("1st", text="BILLNO")
                trcrr.heading("2nd", text="AMOUNT")
                trcrr.heading("3rd", text="FNO")
                trcrr.heading("4th", text="DATE")
                trcrr.pack(side='left', padx=0, pady=0)
                db.commit()

        def dslril():
            cur = db.cursor()
            for selected_item in trcrr.selection():
               print(selected_item)
               cur.execute("DELETE from REFUND where billno=?",(trcrr.set(selected_item,"1st"),))
               db.commit()
               trcrr.delete(selected_item)

        def reft():
            global Fdlr
            global trcrr
            def Close():
                Fdlr.destroy()
            Fdlr = Frame(top, bg="green", relief=GROOVE, bd=10)
            Fdlr.place(x=730, y=230, width=600, height=250)
            lndrr = Label(Fdlr, text='SALES REFUND', font='arial 15 bold', relief=GROOVE, bd=7).pack(fill=X)
            lndrqr = Label(Fdlr, text='SEARCH', font='arial 9').place(x=4, y=6)
            lnsr1r = tk.Entry(Fdlr,textvar=icnmr, font=('bold', 12), width=7)
            lnsr1r.place(x=60, y=6)
            element_fdlr = ['1st', '2nd', '3rd', '4th']
            treeScrolr = tk.Scrollbar(Fdlr)
            treeScrolr.pack(side='right', fill='y')
            trcrr = ttk.Treeview(Fdlr, columns=element_fdlr, height=20, show="headings")
            trcrr.configure(yscrollcommand=treeScrolr.set)
            trcrr.column('1st', width=120, minwidth=70, stretch=tk.NO)
            trcrr.column('2nd', width=120, minwidth=70, stretch=tk.NO)
            trcrr.column('3rd', width=120, minwidth=70, stretch=tk.NO)
            trcrr.column('4th', width=300, minwidth=70, stretch=tk.NO)
            sqlchr = "SELECT * FROM  REFUND"
            cur.execute(sqlchr, )
            trcrr.delete(*trcrr.get_children())
            fetchr = cur.fetchall()
            for datr in fetchr:
                trcrr.insert(parent='', index='end', text='', values=(datr[0], datr[1], datr[2], datr[3]))
                trcrr.heading("1st", text="BILLNO")
                trcrr.heading("2nd", text="AMOUNT")
                trcrr.heading("3rd", text="FNO")
                trcrr.heading("4th", text="DATE")
                trcrr.pack(side='left', padx=0, pady=0)
                treeScrolr.config(command=trcrr.yview)
            bon = Button(Fdlr, bg="green", fg="white", width=7, text="Close", command=Close).place(x=493, y=4)
            hadelsrch = tk.Button(Fdlr, text='OK', bg='green', fg='white',command=cmd_rend).place(x=129, y=4)
            hbrf = tk.Button(Fdlr, text='DELETE', bg='green', fg='white', command=dslril).place(x=159, y=4)
            hareln = tk.Button(Fdlr, text="RESET", anchor="w", bg='green', fg='white',command=nasrfnd).place(x=400, y=4)
            cneln = tk.Button(Fdlr, text="PRINT", anchor="w", bg='green', fg='white',command=refunin).place(x=443, y=4)

        def rettbl():
            global blty
            def rfey():
                fry.destroy()
            global usr
            fry = Frame(relief=GROOVE, bd=10, bg='green')
            fry.place(x=700, y=180, width=600, height=300)
            b9by = Label(fry, text='INDIVIDUAL TOTAL BILL REPORT', font='arial 15 bold', bg='white', bd=7, relief=GROOVE).pack(fill=X)
            sc_y = Scrollbar(fry, orient=VERTICAL)
            blty = tk.Text(fry, yscrollcommand=sc_y)
            sc_y.pack(side=RIGHT, fill=Y)
            sc_y.config(command=blty.yview)
            blty.pack()
            blty.tag_add("whole", "2.0", "end-1c")
            blty.tag_configure("whole", spacing3=10)
            user_in = blty.get(1.0, "end-1c")
            blty.delete(1.0, END)

            with open("tbil.csv", "w", newline='',encoding="utf-8") as mcmty:
                csvwriter = csv.writer(mcmty, delimiter='|')
                hdey = ['(NASCS-NICS)TOTAL BILL REPORT']
                lny = ['--------------------------------------------------------']
                dty = ['BILL_NO       DATE  NAME  CUSTOMERS_NO TOTAL_BILL']
                csvwriter.writerow(hdey)
                csvwriter.writerow(lny)
                csvwriter.writerow(dty)
                csvwriter.writerow(lny)

                for row_y in trcry.get_children():
                    row = trcry.item(row_y)['values']
                    if row_y[0].isdigit():
                        csvwriter.writerow(row_y)
                    csvwriter.writerow(lny)
                    csvwriter.writerow(row)

            with open("tbil.csv", "r") as c:
                dtrc = c.read()
            blty.insert("1.0", dtrc)
            q = blty.get("1.0", "end-1c")
            filename = tempfile.mktemp(".txt")
            open(filename, "w").write(q)
            win32api.ShellExecute(0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
            rfton = Button(fry, bg="green", fg="white", width=9, text="CLOSE", command=rfey).place(x=2, y=4)

        def nasy():
            cur = db.cursor()
            snry = "select * from TOTAL"
            cur.execute(snry, )
            trcry.delete(*trcry.get_children())
            fetay = cur.fetchall()
            for damy in fetay:
                trcry.insert('', 'end', values=(
                    damy[0], damy[1], damy[2], damy[3],damy[4]))
                trcry.pack(side='left', padx=0, pady=0)
                db.commit()

        def cmttb():
            global vy
            global r2y
            global ry
            global lcmt
            cur = db.cursor()
            vy = icnmy.get()
            sy= "select * from TOTAL where BILLNO=?"
            Ly = (vy,)
            ry = cur.execute(sy, Ly)
            ry = cur.fetchall()
            trcry.delete(*trcry.get_children())
            if ry:
             for r2y in ry:
                trcry.insert(parent='', index='end', text='', values=(r2y[0], r2y[1], r2y[2], r2y[3], r2y[4]))
                trcry.heading("1st", text="BILLNO")
                trcry.heading("2nd", text="DATE")
                trcry.heading("3rd", text="NAME")
                trcry.heading("4th", text="CUSTOMERS_NO")
                trcry.heading("5th", text="TOTAL_BILL")
                trcry.pack(side='left', padx=0, pady=0)
                db.commit()

        def delttb():
            cur = db.cursor()
            for selected_itey in trcry.selection():
               print(selected_itey)
               cur.execute("DELETE from TOTAL where billno=?",(trcry.set(selected_itey,"1st"),))
               db.commit()
               trcry.delete(selected_itey)

        def ttbill():
            global Fdly
            global trcry
            def Cltt():
                Fdly.destroy()
            Fdly = Frame(top, bg="green", relief=GROOVE, bd=10)
            Fdly.place(x=730, y=230, width=600, height=250)
            lndry = Label(Fdly, text='TOTAL AMOUNT', font='arial 15 bold', relief=GROOVE, bd=7).pack(fill=X)
            lndrqy = Label(Fdly, text='SEARCH', font='arial 9').place(x=4, y=6)
            lnsr1y = tk.Entry(Fdly,textvar=icnmy, font=('bold', 12), width=7)
            lnsr1y.place(x=60, y=6)
            element_fdly = ['1st', '2nd', '3rd', '4th','5th']
            treeScroly = tk.Scrollbar(Fdly)
            treeScroly.pack(side='right', fill='y')
            trcry = ttk.Treeview(Fdly, columns=element_fdly, height=20, show="headings")
            trcry.configure(yscrollcommand=treeScroly.set)
            trcry.column('1st', width=120, minwidth=70, stretch=tk.NO)
            trcry.column('2nd', width=120, minwidth=70, stretch=tk.NO)
            trcry.column('3rd', width=120, minwidth=70, stretch=tk.NO)
            trcry.column('4th', width=120, minwidth=70, stretch=tk.NO)
            trcry.column('5th', width=120, minwidth=70, stretch=tk.NO)
            sqlchy = "SELECT * FROM  TOTAL"
            cur.execute(sqlchy, )
            trcry.delete(*trcry.get_children())
            fetchy = cur.fetchall()
            for daty in fetchy:
                trcry.insert(parent='', index='end', text='', values=(daty[0], daty[1], daty[2], daty[3], daty[4]))
                trcry.heading("1st", text="BILLNO")
                trcry.heading("2nd", text="DATE")
                trcry.heading("3rd", text="NAME")
                trcry.heading("4th", text="CUSTOMERS_NO")
                trcry.heading("5th", text="TOTAL_BILL")
                trcry.pack(side='left', padx=0, pady=0)
                treeScroly.config(command=trcry.yview)
            boy = Button(Fdly, bg="green", fg="white", width=7, text="Close", command=Cltt).place(x=493, y=4)
            hadelsrcy = tk.Button(Fdly, text='OK', bg='green', fg='white',command=cmttb).place(x=129, y=4)
            hbly = tk.Button(Fdly, text='DELETE', bg='green', fg='white', command=delttb).place(x=159, y=4)
            harely = tk.Button(Fdly, text="RESET", anchor="w", bg='green', fg='white',command=nasy).place(x=400, y=4)
            cnely = tk.Button(Fdly, text="PRINT", anchor="w", bg='green', fg='white',command=rettbl).place(x=443, y=4)

        fmnu = tk.Label(top, text="TOTAL BASE ON DATE RANGE:",bg='green', font=("century", 9)).place(x=50, y=180)
        fm1p = tk.Label(top, text="TOTAL SELLING:",bg='green', font=("century", 9)).place(x=50, y=230)
        sm1m = tk.Entry(top, font=('bold', 10),textvar=sumsp, width=13).place(x=170, y=230)
        fm2p = tk.Label(top, text="TOTAL COST:",bg='green', font=("century", 9)).place(x=50, y=260)
        s2m = tk.Entry(top, font=('bold', 10),textvar=sumcp, width=13).place(x=170, y=260)
        fm3p = tk.Label(top, text="TOTAL PROFIT:",bg='green', font=("century", 9)).place(x=50, y=290)
        s3m = tk.Entry(top, font=('bold', 10),textvar=sumprt, width=13).place(x=170, y=290)
        d4p = Button(top, text="CLICK TO VIEW REFUNDS", anchor="w", bg='green', command=reft).place(x=50, y=340)
        p4t=Button(top, text="CLICK TO VIEW ALL BILLS", anchor="w", bg='green',command=buyft).place(x=50, y=370)
        intt = Button(top, text="CLICK TO VIEW INDIVIDUAL TOTAL BILL", anchor="w", bg='green',command=ttbill).place(x=50, y=400)



        def nas_rep():
            cur = db.cursor()
            snsr = "select * from  buyers"
            cur.execute(snsr, )
            treep.delete(*treep.get_children())
            fetchtr = cur.fetchall()
            for dat2 in fetchtr:
                treep.insert('', 'end', values=(
                    dat2[0], dat2[1], dat2[2], dat2[3], dat2[4], dat2[5], dat2[6], dat2[7], dat2[8]))
                treep.pack(side='left', padx=0, pady=0)
                db.commit()

        def cmd_mt():
            global vcmds
            global r2
            global rcmd3
            global lcmt

            cur = db.cursor()
            vals1 = icnmp.get()
            scmd1 = "select * from buyers where PID=?"
            Lenme1 = (vals1,)
            rcmd3 = cur.execute(scmd1, Lenme1)
            rcmd3 = cur.fetchall()
            treep.delete(*treep.get_children())
            if rcmd3:
                for r2 in rcmd3:
                    treep.insert('', 'end', values=(r2[0], r2[1], r2[2], r2[3], r2[4], r2[5], r2[6], r2[7], r2[8]))
                    treep.heading("1st", text="FNO")
                    treep.heading("2nd", text="PID")
                    treep.heading("3rd", text="NAME")
                    treep.heading("4th", text="DATE")
                    treep.heading("5th", text="PNAME")
                    treep.heading("6th", text="PQty")
                    treep.heading("7th", text="SP")
                    treep.heading("8th", text="COSTP")
                    treep.heading("9th", text="PROFIT")
                    treep.pack(side='left', padx=0, pady=0)
                    db.commit()
        def removeitem():
            cur = db.cursor()
            for selected_item in treep.selection():
               print(selected_item)
               cur.execute("DELETE from buyers where PID=?",(treep.set(selected_item,"2nd"),))
               db.commit()
               treep.delete(selected_item)


        def reprtdate():
            global rxsult
            global Lxmem
            srtdpypd = entSTDT1.get()
            endpypd = entEDDT1.get()

            cur = db.cursor()
            sxl = "select * from buyers where DATE(date) between ? and ?"
            Lxmem = (srtdpypd, endpypd)
            rxsult = cur.execute(sxl, Lxmem)
            rxsult = cur.fetchall()
            treep.delete(*treep.get_children())
            if rxsult:
                for rxw1 in rxsult:
                    treep.insert(parent='', index='end', values=(
                        rxw1[0], rxw1[1], rxw1[2], rxw1[3], rxw1[4], rxw1[5], rxw1[6], rxw1[7], rxw1[8]))
                    treep.heading("1st", text="File_ID")
                    treep.heading("2nd", text="Product_id")
                    treep.heading("3rd", text="Name")
                    treep.heading("4th", text="Date")
                    treep.heading("5th", text="Product_Name")
                    treep.heading("6th", text="Qty")
                    treep.heading("7th", text="Selling_Price")
                    treep.heading("8th", text="Cost_Price")
                    treep.heading("9th", text="Profit")
                    treep.pack(side='left', padx=0, pady=0)
                    treeSpenp.config(command=treep.yview)
            sxl1="select SUM(sp) from buyers WHERE  DATE(date) between ? and ?"
            rxsult1 = cur.execute(sxl1, Lxmem)
            rxsult1 = cur.fetchone()[0]
            sumsp.set(rxsult1)
            sxl2 ="SELECT SUM(costp) FROM buyers WHERE DATE(date) between ? and ?"
            rxsult2 = cur.execute(sxl2, (Lxmem))
            rxsult2 = cur.fetchone()
            sumcp.set(rxsult2)
            sxl3 = "SELECT SUM(profit) FROM buyers WHERE DATE(date) between ? and ?"
            rxsult3 = cur.execute(sxl3, Lxmem)
            rxsult3 = cur.fetchone()
            sumprt.set(rxsult3)

        def cmtpro():
            def Closecm():
                f4p.destroy()

            global usr
            f4p = Frame(relief=GROOVE, bd=10, bg='green')
            f4p.place(x=700, y=180, width=600, height=300)
            bibi = Label(f4p, text='SALES REPORT', font='arial 15 bold', bg='white', bd=7, relief=GROOVE).pack(fill=X)
            sc_y = Scrollbar(f4p, orient=VERTICAL)
            ttrns = tk.Text(f4p, yscrollcommand=sc_y)
            sc_y.pack(side=RIGHT, fill=Y)
            sc_y.config(command=ttrns.yview)
            ttrns.pack()
            ttrns.tag_add("whole", "2.0", "end-1c")
            ttrns.tag_configure("whole", spacing3=10)
            user_in = ttrns.get(1.0, "end-1c")
            ttrns.delete(1.0, END)

            with open("profit.csv", "w", newline='') as mycmtr:
                csvwriter = csv.writer(mycmtr, delimiter='|')
                hder = ['(NASCS-NICS)SALES REPORT']
                lne = ['--------------------------------------------------------']
                dta = ['File_ID       Product_id   Name  Date Product_Name Qty  Selling_Price Cost_Price Profit']
                csvwriter.writerow(hder)
                csvwriter.writerow(lne)
                csvwriter.writerow(dta)
                csvwriter.writerow(lne)

                for row_cm in treep.get_children():
                    row = treep.item(row_cm)['values']
                    if row_cm[0].isdigit():
                        csvwriter.writerow(row_cm)
                    csvwriter.writerow(lne)
                    csvwriter.writerow(row)

            with open("profit.csv", "r") as c:
                dtrc = c.read()
            ttrns.insert("1.0", dtrc)
            q = ttrns.get("1.0", "end-1c")
            filename = tempfile.mktemp(".txt")
            open(filename, "w").write(q)
            win32api.ShellExecute(0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
            close_button = Button(f4p, bg="green", fg="white", width=9, text="CLOSE", command=Closecm)
            close_button.place(x=2, y=4)

        def dtpro():
            def Clpro():
                fpro.destroy()
            global usr
            fpro = Frame(relief=GROOVE, bd=10, bg='green')
            fpro.place(x=700, y=180, width=600, height=300)
            b9bi = Label(fpro, text='BILL REPORT', font='arial 15 bold', bg='white', bd=7, relief=GROOVE).pack(fill=X)
            sc_y = Scrollbar(fpro, orient=VERTICAL)
            ttrns = tk.Text(fpro, yscrollcommand=sc_y)
            sc_y.pack(side=RIGHT, fill=Y)
            sc_y.config(command=ttrns.yview)
            ttrns.pack()
            ttrns.tag_add("whole", "2.0", "end-1c")
            ttrns.tag_configure("whole", spacing3=10)
            user_in = ttrns.get(1.0, "end-1c")
            ttrns.delete(1.0, END)
            ttrns.insert(END, f"\nTOTAL SELLING:----\t\t{sumsp.get()}")
            ttrns.insert(END, f"\nTOTAL-COST:----\t\t{sumcp.get()}")
            ttrns.insert(END, f"\nTOTAL PROFIT:----\t{sumprt.get()}")
            ttrns.insert(END, f"\n======================================\n\n")

            with open("prodate.csv", "w", newline='') as mycmtr:
                csvwriter = csv.writer(mycmtr, delimiter='|')
                hder = ['(NASCS-NICS)SALES REPORT ON SPECIFIC DATE RANGE']
                lne = ['--------------------------------------------------------']
                dta = ['File_ID       Product_id   Name  Date Product_Name Qty  Selling_Price Cost_Price Profit']
                csvwriter.writerow(hder)
                csvwriter.writerow(lne)
                csvwriter.writerow(dta)
                csvwriter.writerow(lne)

                for row_cm in treep.get_children():
                    row = treep.item(row_cm)['values']
                    if row_cm[0].isdigit():
                        csvwriter.writerow(row_cm)
                    csvwriter.writerow(lne)
                    csvwriter.writerow(row)

            with open("prodate.csv", "r") as c:
                dtrc = c.read()
            ttrns.insert("1.0", dtrc)
            q = ttrns.get("1.0", "end-1c")
            filename = tempfile.mktemp(".txt")
            open(filename, "w").write(q)
            win32api.ShellExecute(0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
            clton = Button(fpro, bg="green", fg="white", width=9, text="CLOSE", command=Clpro).place(x=2, y=4)

        F5 = Frame(prf, relief=GROOVE, bg='green', bd=10)
        F5.place(relx=0.307, rely=0.203, width=880, height=300)
        element_headerp = ['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th']
        treep = ttk.Treeview(F5, columns=element_headerp, height=20, show="headings")
        bill_p = Label(F5, text='SALES REPORT',font='arial 15 bold', bd=7, relief=GROOVE)
        bill_p.pack(fill=X)
        lcmp = Label(F5, text='SEARCH',bg='green', font='arial 9')
        lcmp.place(x=4, y=6)
        lyp = Label(F5, text='DATE RANGE',bg='green', font='arial 6').place(x=510, y=6)
        treeSpenp = tk.Scrollbar(F5)
        treeSpenp.pack(side='right', fill='y')
        treep.configure(yscrollcommand=treeSpenp.set)
        treep.column('1st', width=60, minwidth=60, stretch=tk.NO)
        treep.column('2nd', width=60, minwidth=60, stretch=tk.NO)
        treep.column('3rd', width=150, minwidth=150, stretch=tk.NO)
        treep.column('4th', width=92, minwidth=90, stretch=tk.NO)
        treep.column('5th', width=200, minwidth=200, stretch=tk.NO)
        treep.column('6th', width=30, minwidth=30, stretch=tk.NO)
        treep.column('7th', width=90, minwidth=90, stretch=tk.NO)
        treep.column('8th', width=90, minwidth=90, stretch=tk.NO)
        treep.column('9th', width=90, minwidth=90, stretch=tk.NO)
        lcmt = tk.Entry(F5,textvar=icnmp,font=('bold', 12), width=7)
        lcmt.place(x=60, y=6)
        strtd = tk.Entry(F5, textvar=entSTDT1,font=('bold', 8), width=10).place(x=570, y=6)
        endtd = tk.Entry(F5, textvar=entEDDT1,font=('bold', 8), width=10).place(x=650, y=6)
        mndp =Button(F5, text='OK', bg='green',command=cmd_mt, fg='white').place(x=130, y=4)
        cmdp =Button(F5, text="RESET", anchor="w", bg='green',command=nas_rep, fg='white').place(x=180, y=4)
        cmnp =Button(F5, text="PRINT", anchor="w", bg='green',command=cmtpro,fg='white').place(x=230, y=4)
        dlnp = Button(F5, text="DELETE", anchor="w", bg='green', command=removeitem, fg='white').place(x=280, y=4)
        ddtp = Button(F5, text="OK", anchor="w", bg='green', fg='white',command=reprtdate).place(x=720, y=6)
        prrdt=Button(F5, text="PRINT", anchor="w", bg='green', fg='white',command=dtpro).place(x=760, y=6)

        sqlchp = "select * from  buyers"
        cur.execute(sqlchp, )
        treep.delete(*treep.get_children())
        fetchp = cur.fetchall()
        for data in fetchp:
            treep.insert('', 'end', values=(
                data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]))
            treep.heading("1st", text="File_ID")
            treep.heading("2nd", text="Product_id")
            treep.heading("3rd", text="Name")
            treep.heading("4th", text="Date")
            treep.heading("5th", text="Product_Name")
            treep.heading("6th", text="Qty")
            treep.heading("7th", text="Selling_Price")
            treep.heading("8th", text="Cost_Price")
            treep.heading("9th", text="Profit")
            treep.pack(side='left', padx=0, pady=0)
            treeSpenp.config(command=treep.yview)


        def sedbll():
            global row
            global rlt
            global vip
            global cap
            cap=search_fam.get()
            vhs = srchbll.get()
            shl = "SELECT bill_no,customer_name,bill_details FROM bill WHERE bill_no=?"
            shd="SELECT SUM(AMOUNT) from REFUND WHERE BILLNO=?"
            sh2 ="SELECT totalbill FROM TOTAL WHERE billno=?"
            cur = db.cursor()
            Lm = (vhs,)
            prt = cur.execute(sh2, Lm)
            prt = cur.fetchone()[0]
            vip = cur.execute(shd, Lm)
            vip = cur.fetchone()[0]
            rlt = cur.execute(shl, Lm)
            rlt = cur.fetchall()
            if rlt:
                for row in rlt:
                    fnobll.set(rlt[0][0])
                    nambll.set(rlt[0][1])
                    msg = ""
                    msg = msg + (rlt[0][2])
                    dtt.insert("end", msg)
                    sumup.set(vip)
                    ttsum.set(prt)
            cpt = prt
            spt = vip
            if cap:
                rept = cpt - spt
                bdmnyr.set(rept)


        def billreport():
            global user_in1, bld
            F5I = Frame(relief=GROOVE, bd=10)
            F5I.place(x=700, y=180, width=500, height=500)
            bill_title1 = Label(F5I, text='LOAN REFUND REPORT', font='arial 15 bold', bd=7, relief=GROOVE).pack(fill=X)
            scrol_y1 = Scrollbar(F5I, orient=VERTICAL)
            bld = tk.Text(F5I, yscrollcommand=scrol_y1)
            scrol_y1.pack(side=RIGHT, fill=Y)
            scrol_y1.config(command=bld.yview)
            bld.pack()
            user_in1 = bld.get(1.0, "end-1c")
            bld.delete(1.0, END)
            bld.insert(END, "\t  (NASCS-NICS) BILL REPORT ")
            bld.insert(END, f"\n\nBILL NO:------\t\t{fnobll.get()}")
            bld.insert(END, f"\nNAME:----\t\t{nambll.get()}")
            bld.insert(END, f"\nREFUND:----\t\t{sumup.get()}")
            bld.insert(END, f"\nTOTAL-BILL:----\t\t{ttsum.get()}")
            bld.insert(END, f"\nDEBT BALANCE:----\t{bdmnyr.get()}")
            bld.insert(END, f"\n======================================\n\n")
            bld.insert(END,  dtt.get("1.0", "end-1c"))
            #bld.insert(INSERT, dtt.get("1.0", tk.END))                                                                                                                                                               f"\n\n======================================")
            bld.configure(font='arial 9 bold')
            q = bld.get("1.0", "end-1c")
            filerfd = tempfile.mktemp(".txt")
            open(filerfd, "w",encoding="utf-8").write(q)
            win32api.ShellExecute(0, "print", filerfd, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)

        F5P = Frame(prf, relief=GROOVE, bg='green', bd=10)
        F5P.place(relx=0.307, rely=0.606, width=880, height=270)
        frfp = tk.Label(F5P, text="SEARCH INDIVIDUAL DETAILS:", font=("century", 9))
        frfp.place(x=9, y=10)
        fimp = tk.Label(F5P, text="ENTER BILL NUMBER:", font=("century", 9))
        fimp.place(x=9, y=40)
        search_fam = tk.Entry(F5P, textvar=srchbll, font=('bold', 10), width=13)
        search_fam.place(x=180, y=40)
        mokp =Button(F5P, text='OK', bg='green',command=sedbll,fg='white').place(x=277, y=40)
        l15 = tk.Label(F5P, text="BILL NUMBER:", anchor="w", width=20, font=("century", 9))
        l15.place(x=9, y=65)
        e15 = tk.Entry(F5P, textvar=fnobll,font=('bold', 10), width=20)
        e15.place(x=180, y=65)
        l1 = tk.Label(F5P, text="NAME:", width=20, anchor="w", font=("century", 9))
        l1.place(x=9, y=90)
        enan = tk.Entry(F5P,textvar=nambll, font=('bold', 10), width=20)
        enan.place(x=180, y=90)
        l1W = tk.Label(F5P, text="AMOUNT-REFUNDED:", width=20, anchor="w", font=("century", 9))
        l1W.place(x=9, y=115)
        amenn = tk.Entry(F5P,textvar=sumup, font=('bold', 10), width=20)
        amenn.place(x=180, y=115)
        itemr = tk.Label(F5P, text="ITEMS:", anchor="w", width=20, font=("century", 9))
        itemr.place(x=9, y=140)
        trep = tk.Scrollbar(F5P)
        trep.pack(side='right', fill='y')
        dtt = tk.Text(F5P, width=40, height=3,wrap=NONE,yscrollcommand=trep.set)
        dtt.place(x=180, y=140)
        trep.config(command=dtt.yview)
        lbd = tk.Label(F5P, text="BALANCE DEBT:", width=20, anchor="w", font=("century", 9))
        lbd.place(x=9, y=200)
        albd = tk.Entry(F5P,textvar=bdmnyr, font=('bold', 10), width=20)
        albd.place(x=180, y=200)
        ltl = tk.Label(F5P, text="ITEM TOTAL:", width=20, anchor="w", font=("century", 9))
        ltl.place(x=9, y=225)
        atd = tk.Entry(F5P, textvar=ttsum,font=('bold', 10), width=20)
        atd.place(x=180, y=225)
        mrcp = Button(F5P, text='GENERATE RECIEPT', bg='green', fg='white', command=billreport).place(x=330, y=225)

        def refund2():

            a1r2 = bno.get()
            e5r2 = bamt.get()
            jr2 = bfn.get()
            dbtl = bdbyr.get()

            sqlr3 = "INSERT INTO REFUND(BILLNO,AMOUNT,FNO,DATE) VALUES (?,?,?,?)"
            valr3 = (a1r2, e5r2, jr2, dbtl)
            cur = db.cursor()
            cur.execute(sqlr3, valr3)
            db.commit()
            messagebox.showinfo("Database", "Record Added to Database")

        def billrefund():
            global usr, bldr
            F5r = Frame(relief=GROOVE, bd=10)
            F5r.place(x=700, y=180, width=500, height=500)
            billr = Label(F5r, text='LOAN REFUND REPORT', font='arial 15 bold', bd=7, relief=GROOVE).pack(fill=X)
            scrr = Scrollbar(F5r, orient=VERTICAL)
            bldr = tk.Text(F5r, yscrollcommand=scrr)
            scrr.pack(side=RIGHT, fill=Y)
            scrr.config(command=bldr.yview)
            bldr.pack()
            usr = bldr.get(1.0, "end-1c")
            bldr.delete(1.0, END)
            bldr.insert(END, "\t  (NASCS-NICS) BILL REPORT ")
            bldr.insert(END, f"\n\nBILL NO:------\t\t\t{bno.get()}")
            bldr.insert(END, f"\nAMOUNT:----\t\t{bamt.get()}")
            bldr.insert(END, f"\nFNO:----\t\t{bfn.get()}")
            bldr.insert(END, f"\nDATE:----\t\t{bdbyr.get()}")
            #bldr.insert(END, f"\n======================================\n")                                                                                                                                                              f"\n\n======================================")
            bldr.configure(font='arial 9 bold')
            q = bldr.get("1.0", "end-1c")
            filerfd = tempfile.mktemp(".txt")
            open(filerfd, "w",encoding="utf-8").write(q)
            win32api.ShellExecute(0, "print", filerfd, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)

        #SECOND PHASE
        seperator = tk.Frame(F5P, height=250, width=10, bg='white')
        seperator.place(x=520, y=0)
        f2p = tk.Label(F5P, text="REFUND DETAILS:", font=("century", 9))
        f2p.place(x=530, y=10)
        f2mp = tk.Label(F5P, text="BILL NUMBER:", font=("century", 9))
        f2mp.place(x=530, y=40)
        search_f2 = tk.Entry(F5P, textvar=bno ,font=('bold', 10), width=13)
        search_f2.place(x=637, y=40)
        famn = tk.Label(F5P, text="AMOUNT:", width=12, anchor="w", font=("century", 9))
        famn.place(x=530, y=65)
        samn = tk.Entry(F5P,textvar=bamt, font=('bold', 10), width=13)
        samn.place(x=637, y=65)
        ffno = tk.Label(F5P, text="FNO:", width=12, anchor="w", font=("century", 9))
        ffno.place(x=530, y=90)
        sfno = tk.Entry(F5P, textvar= bfn,font=('bold', 10), width=13)
        sfno.place(x=637, y=90)
        fdt = tk.Label(F5P, text="DATE:", width=12, anchor="w", font=("century", 9))
        fdt.place(x=530, y=115)
        sdt = tk.Entry(F5P,textvar=bdbyr, font=('bold', 10), width=13)
        sdt.place(x=637, y=115)
        msmb = Button(F5P, text='SUBMIT', bg='green', fg='white',command=refund2).place(x=530, y=225)
        grcp = Button(F5P, text='GENERATE RECIEPT', bg='green', fg='white',command= billrefund).place(x=590, y=225)


def inventory():
    global inv
    global page3
    inv = Toplevel()
    page3 = Inventory(inv)
    page3.time()
    inv.protocol("WM_DELETE_WINDOW", exitt)
    inv.mainloop()


class Inventory:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Inventory")

        self.label1 = Label(inv)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/inventory.png")
        self.label1.configure(image=self.img)

        self.message = Label(inv)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="white")
        self.message.configure(background="#0ed145")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(inv)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="white")
        self.clock.configure(background="#0ed145")

        self.entry1 = Entry(inv)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(inv)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#CF1E14")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="white")
        self.button1.configure(background="#0ed145")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_product)

        self.button2 = Button(inv)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#0ed145")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="white")
        self.button2.configure(background="#0ed145")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(inv)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#0ed145")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="white")
        self.button3.configure(background="#0ed145")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""ADD PRODUCT""")
        self.button3.configure(command=self.add_product)

        self.button4 = Button(inv)
        self.button4.place(relx=0.052, rely=0.5, width=306, height=28)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#0ed145")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="white")
        self.button4.configure(background="#0ed145")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""UPDATE PRODUCT""")
        self.button4.configure(command=self.update_product)

        self.button5 = Button(inv)
        self.button5.place(relx=0.052, rely=0.57, width=306, height=28)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#0ed145")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="white")
        self.button5.configure(background="#0ed145")
        self.button5.configure(font="-family {Poppins SemiBold} -size 12")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""DELETE PRODUCT""")
        self.button5.configure(command=self.delete_product)

        self.button6 = Button(inv)
        self.button6.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#0ed145")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="white")
        self.button6.configure(background="#0ed145")
        self.button6.configure(font="-family {Poppins SemiBold} -size 12")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""EXIT""")
        self.button6.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(inv, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(inv, orient=VERTICAL)
        self.tree = ttk.Treeview(inv)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Product ID",
                "Name",
                "Category",
                "Sub-Category",
                "In Stock",
                "MRP",
                "Cost Price",
                "Vendor No.",
            )
        )

        self.tree.heading("Product ID", text="Product ID", anchor=W)
        self.tree.heading("Name", text="Name", anchor=W)
        self.tree.heading("Category", text="Category", anchor=W)
        self.tree.heading("Sub-Category", text="Sub-Category", anchor=W)
        self.tree.heading("In Stock", text="In Stock", anchor=W)
        self.tree.heading("MRP", text="MRP", anchor=W)
        self.tree.heading("Cost Price", text="Cost Price", anchor=W)
        self.tree.heading("Vendor No.", text="Vendor No.", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=80)
        self.tree.column("#2", stretch=NO, minwidth=0, width=260)
        self.tree.column("#3", stretch=NO, minwidth=0, width=100)
        self.tree.column("#4", stretch=NO, minwidth=0, width=120)
        self.tree.column("#5", stretch=NO, minwidth=0, width=80)
        self.tree.column("#6", stretch=NO, minwidth=0, width=80)
        self.tree.column("#7", stretch=NO, minwidth=0, width=80)
        self.tree.column("#8", stretch=NO, minwidth=0, width=100)

        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM raw_inventory")
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))


    def search_product(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        try:
            to_search = int(self.entry1.get())
        except ValueError:
            messagebox.showerror("Oops!!", "Invalid Product Id.", parent=inv)
        else:
            for search in val:
                if search == to_search:
                    self.tree.selection_set(val[val.index(search) - 1])
                    self.tree.focus(val[val.index(search) - 1])
                    messagebox.showinfo("Success!!", "Product ID: {} found.".format(self.entry1.get()), parent=inv)
                    break
            else:
                messagebox.showerror("Oops!!", "Product ID: {} not found.".format(self.entry1.get()), parent=inv)

    sel = []

    def on_tree_select(self, Event):
        self.sel.clear()
        for i in self.tree.selection():
            if i not in self.sel:
                self.sel.append(i)

    def delete_product(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected products?", parent=inv)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j % 8 == 0:
                        to_delete.append(val[j])

                for k in to_delete:
                    delete = "DELETE FROM raw_inventory WHERE product_id = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Products deleted from database.", parent=inv)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select a product.", parent=inv)

    def update_product(self):
        if len(self.sel) == 1:
            global p_update
            p_update = Toplevel()
            page9 = Update_Product(p_update)
            page9.time()
            p_update.protocol("WM_DELETE_WINDOW", self.ex2)
            global valll
            valll = []
            for i in self.sel:
                for j in self.tree.item(i)["values"]:
                    valll.append(j)

            page9.entry1.insert(0, valll[1])
            page9.entry2.insert(0, valll[2])
            page9.entry3.insert(0, valll[4])
            page9.entry4.insert(0, valll[5])
            page9.entry6.insert(0, valll[3])
            page9.entry7.insert(0, valll[6])
            page9.entry8.insert(0, valll[7])


        elif len(self.sel) == 0:
            messagebox.showerror("Error", "Please choose a product to update.", parent=inv)
        else:
            messagebox.showerror("Error", "Can only update one product at a time.", parent=inv)

        p_update.mainloop()


    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=inv)
        if sure == True:
            inv.destroy()

    def ex2(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=p_update)
        if sure == True:
            p_update.destroy()
            inv.deiconify()

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

    def add_product(self):
        global p_add
        global page4
        p_add = Toplevel()
        page4 = add_product(p_add)
        page4.time()
        p_add.protocol("WM_DELETE_WINDOW", exitt)
        p_add.mainloop()


class add_product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Product")

        self.label1 = Label(p_add)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/add_product.png")
        self.label1.configure(image=self.img)

        self.clock = Label(p_add)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="white")
        self.clock.configure(background="#0ed145")

        self.entry1 = Entry(p_add)
        self.entry1.place(relx=0.132, rely=0.296, width=996, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(p_add)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = p_add.register(self.testint)

        self.entry3 = Entry(p_add)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(p_add)
        self.entry4.place(relx=0.132, rely=0.646, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")

        self.entry6 = Entry(p_add)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")

        self.entry7 = Entry(p_add)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")

        self.entry8 = Entry(p_add)
        self.entry8.place(relx=0.527, rely=0.646, width=374, height=30)
        self.entry8.configure(font="-family {Poppins} -size 12")
        self.entry8.configure(relief="flat")
        self.entry8.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.button1 = Button(p_add)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#0ed145")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="white")
        self.button1.configure(background="#0ed145")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""ADD""")
        self.button1.configure(command=self.add)

        self.button2 = Button(p_add)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#0ed145")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="white")
        self.button2.configure(background="#0ed145")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def add(self):
        pqty = self.entry3.get()
        pcat = self.entry2.get()
        pmrp = self.entry4.get()
        pname = self.entry1.get()
        psubcat = self.entry6.get()
        pcp = self.entry7.get()
        pvendor = self.entry8.get()

        if pname.strip():
            if pcat.strip():
                if psubcat.strip():
                    if pqty:
                        if pcp:
                            try:
                                float(pcp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_add)
                            else:
                                if pmrp:
                                    try:
                                        float(pmrp)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_add)
                                    else:
                                        if valid_phone(pvendor):
                                            with sqlite3.connect("./Database/store.db") as db:
                                                cur = db.cursor()
                                            insert = (
                                                "INSERT INTO raw_inventory(product_name, product_cat, product_subcat, stock, mrp, cost_price, vendor_phn) VALUES(?,?,?,?,?,?,?)"
                                            )
                                            cur.execute(insert,
                                                        [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp),
                                                         pvendor])
                                            db.commit()
                                            messagebox.showinfo("Success!!", "Product successfully added in inventory.",
                                                                parent=p_add)
                                            p_add.destroy()
                                            page3.tree.delete(*page3.tree.get_children())
                                            page3.DisplayData()
                                            p_add.destroy()
                                        else:
                                            messagebox.showerror("Oops!", "Invalid phone number.", parent=p_add)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=p_add)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_add)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_add)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_add)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=p_add)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=p_add)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)
        self.entry8.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


class Update_Product:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Add Product")

        self.label1 = Label(p_update)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/update_product.png")
        self.label1.configure(image=self.img)

        self.clock = Label(p_update)
        self.clock.place(relx=0.84, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="white")
        self.clock.configure(background="#0ed145")

        self.entry1 = Entry(p_update)
        self.entry1.place(relx=0.132, rely=0.296, width=996, height=30)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.entry2 = Entry(p_update)
        self.entry2.place(relx=0.132, rely=0.413, width=374, height=30)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")

        self.r2 = p_update.register(self.testint)

        self.entry3 = Entry(p_update)
        self.entry3.place(relx=0.132, rely=0.529, width=374, height=30)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(validate="key", validatecommand=(self.r2, "%P"))

        self.entry4 = Entry(p_update)
        self.entry4.place(relx=0.132, rely=0.646, width=374, height=30)
        self.entry4.configure(font="-family {Poppins} -size 12")
        self.entry4.configure(relief="flat")

        self.entry6 = Entry(p_update)
        self.entry6.place(relx=0.527, rely=0.413, width=374, height=30)
        self.entry6.configure(font="-family {Poppins} -size 12")
        self.entry6.configure(relief="flat")

        self.entry7 = Entry(p_update)
        self.entry7.place(relx=0.527, rely=0.529, width=374, height=30)
        self.entry7.configure(font="-family {Poppins} -size 12")
        self.entry7.configure(relief="flat")

        self.entry8 = Entry(p_update)
        self.entry8.place(relx=0.527, rely=0.646, width=374, height=30)
        self.entry8.configure(font="-family {Poppins} -size 12")
        self.entry8.configure(relief="flat")

        self.button1 = Button(p_update)
        self.button1.place(relx=0.408, rely=0.836, width=96, height=34)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#0ed145")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="white")
        self.button1.configure(background="#0ed145")
        self.button1.configure(font="-family {Poppins SemiBold} -size 14")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""UPDATE""")
        self.button1.configure(command=self.update)

        self.button2 = Button(p_update)
        self.button2.place(relx=0.526, rely=0.836, width=86, height=34)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#0ed145")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="white")
        self.button2.configure(background="#0ed145")
        self.button2.configure(font="-family {Poppins SemiBold} -size 14")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""CLEAR""")
        self.button2.configure(command=self.clearr)

    def update(self):
        pqty = self.entry3.get()
        pcat = self.entry2.get()
        pmrp = self.entry4.get()
        pname = self.entry1.get()
        psubcat = self.entry6.get()
        pcp = self.entry7.get()
        pvendor = self.entry8.get()

        if pname.strip():
            if pcat.strip():
                if psubcat.strip():
                    if pqty:
                        if pcp:
                            try:
                                float(pcp)
                            except ValueError:
                                messagebox.showerror("Oops!", "Invalid cost price.", parent=p_update)
                            else:
                                if pmrp:
                                    try:
                                        float(pmrp)
                                    except ValueError:
                                        messagebox.showerror("Oops!", "Invalid MRP.", parent=p_update)
                                    else:
                                        if valid_phone(pvendor):
                                            product_id = valll[0]
                                            with sqlite3.connect("./Database/store.db") as db:
                                                cur = db.cursor()
                                            update = (
                                                "UPDATE raw_inventory SET product_name = ?, product_cat = ?, product_subcat = ?, stock = ?, mrp = ?, cost_price = ?, vendor_phn = ? WHERE product_id = ?"
                                            )
                                            cur.execute(update,
                                                        [pname, pcat, psubcat, int(pqty), float(pmrp), float(pcp),
                                                         pvendor, product_id])
                                            db.commit()
                                            messagebox.showinfo("Success!!",
                                                                "Product successfully updated in inventory.",
                                                                parent=p_update)
                                            valll.clear()
                                            Inventory.sel.clear()
                                            page3.tree.delete(*page3.tree.get_children())
                                            page3.DisplayData()
                                            p_update.destroy()
                                        else:
                                            messagebox.showerror("Oops!", "Invalid phone number.", parent=p_update)
                                else:
                                    messagebox.showerror("Oops!", "Please enter MRP.", parent=p_update)
                        else:
                            messagebox.showerror("Oops!", "Please enter product cost price.", parent=p_update)
                    else:
                        messagebox.showerror("Oops!", "Please enter product quantity.", parent=p_update)
                else:
                    messagebox.showerror("Oops!", "Please enter product sub-category.", parent=p_update)
            else:
                messagebox.showerror("Oops!", "Please enter product category.", parent=p_update)
        else:
            messagebox.showerror("Oops!", "Please enter product name", parent=p_update)

    def clearr(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.entry4.delete(0, END)
        self.entry6.delete(0, END)
        self.entry7.delete(0, END)
        self.entry8.delete(0, END)

    def testint(self, val):
        if val.isdigit():
            return True
        elif val == "":
            return True
        return False

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


def invoices():
    global invoice
    invoice = Toplevel()
    page7 = Invoice(invoice)
    page7.time()
    invoice.protocol("WM_DELETE_WINDOW", exitt)
    invoice.mainloop()

class Invoice:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Invoices")

        self.label1 = Label(invoice)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/invoices.png")
        self.label1.configure(image=self.img)

        self.message = Label(invoice)
        self.message.place(relx=0.046, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="white")
        self.message.configure(background="#0ed145")
        self.message.configure(text="""ADMIN""")
        self.message.configure(anchor="w")

        self.clock = Label(invoice)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="white")
        self.clock.configure(background="#0ed145")

        self.entry1 = Entry(invoice)
        self.entry1.place(relx=0.040, rely=0.286, width=240, height=28)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")

        self.button1 = Button(invoice)
        self.button1.place(relx=0.229, rely=0.289, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#0ed145")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="white")
        self.button1.configure(background="#0ed145")
        self.button1.configure(font="-family {Poppins SemiBold} -size 10")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Search""")
        self.button1.configure(command=self.search_inv)

        self.button2 = Button(invoice)
        self.button2.place(relx=0.035, rely=0.106, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#0ed145")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="white")
        self.button2.configure(background="#0ed145")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Logout""")
        self.button2.configure(command=self.Logout)

        self.button3 = Button(invoice)
        self.button3.place(relx=0.052, rely=0.432, width=306, height=28)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#0ed145")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="white")
        self.button3.configure(background="#0ed145")
        self.button3.configure(font="-family {Poppins SemiBold} -size 12")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""DELETE INVOICE""")
        self.button3.configure(command=self.on_tree_select)

        self.button4 = Button(invoice)
        self.button4.place(relx=0.135, rely=0.885, width=76, height=23)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#0ed145")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="white")
        self.button4.configure(background="#0ed145")
        self.button4.configure(font="-family {Poppins SemiBold} -size 12")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""EXIT""")
        self.button4.configure(command=self.Exit)

        self.scrollbarx = Scrollbar(invoice, orient=HORIZONTAL)
        self.scrollbary = Scrollbar(invoice, orient=VERTICAL)
        self.tree = ttk.Treeview(invoice)
        self.tree.place(relx=0.307, rely=0.203, width=880, height=550)
        self.tree.configure(
            yscrollcommand=self.scrollbary.set, xscrollcommand=self.scrollbarx.set
        )
        self.tree.configure(selectmode="extended")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.double_tap)

        self.scrollbary.configure(command=self.tree.yview)
        self.scrollbarx.configure(command=self.tree.xview)

        self.scrollbary.place(relx=0.954, rely=0.203, width=22, height=548)
        self.scrollbarx.place(relx=0.307, rely=0.924, width=884, height=22)

        self.tree.configure(
            columns=(
                "Bill Number",
                "Date",
                "Customer Name",
                "Customer Phone No.",
            )
        )

        self.tree.heading("#1", text="Bill Number", anchor=W)
        self.tree.heading("#2", text="Date", anchor=W)
        self.tree.heading("#3", text="Customer Name", anchor=W)
        self.tree.heading("#4", text="Customer Phone No.", anchor=W)

        self.tree.column("#0", stretch=NO, minwidth=0, width=0)
        self.tree.column("#1", stretch=NO, minwidth=0, width=219)
        self.tree.column("#2", stretch=NO, minwidth=0, width=219)
        self.tree.column("#3", stretch=NO, minwidth=0, width=219)
        self.tree.column("#4", stretch=NO, minwidth=0, width=219)
        self.DisplayData()

    def DisplayData(self):
        cur.execute("SELECT * FROM bill")
        fetch = cur.fetchall()
        for data in fetch:
            self.tree.insert("", "end", values=(data))
            sel = []

    def on_tree_select(self):
            cur = db.cursor()
            for selected_item in self.tree.selection():
               print(selected_item)
               cur.execute("DELETE from bill where bill_no=?",(self.tree.set(selected_item,"#1"),))
               db.commit()
               self.tree.delete(selected_item)
        #self.sel.clear()
        #for i in self.tree.selection():
            #if i not in self.sel:
                #self.sel.append(i)

    def double_tap(self, Event):
        item = self.tree.identify('item', Event.x, Event.y)
        global bill_num
        global textarea
        global user_in, win
        bill_num = self.tree.item(item)['values'][0]
        global F3
        global bill
        bill = Toplevel()
        F3 = Toplevel()
        pg = open_bill(bill)
        # bill.protocol("WM_DELETE_WINDOW", exitt)
        bill.mainloop()
        F3.mainloop()

    def delete_invoice(self):
        val = []
        to_delete = []

        if len(self.sel) != 0:
            sure = messagebox.askyesno("Confirm", "Are you sure you want to delete selected invoice(s)?",
                                       parent=invoice)
            if sure == True:
                for i in self.sel:
                    for j in self.tree.item(i)["values"]:
                        val.append(j)

                for j in range(len(val)):
                    if j % 5 == 0:
                        to_delete.append(val[j])

                for k in to_delete:
                    delete = "DELETE FROM bill WHERE bill_no = ?"
                    cur.execute(delete, [k])
                    db.commit()

                messagebox.showinfo("Success!!", "Invoice(s) deleted from database.", parent=invoice)
                self.sel.clear()
                self.tree.delete(*self.tree.get_children())

                self.DisplayData()
        else:
            messagebox.showerror("Error!!", "Please select an invoice", parent=invoice)

    def search_inv(self):
        val = []
        for i in self.tree.get_children():
            val.append(i)
            for j in self.tree.item(i)["values"]:
                val.append(j)

        to_search = self.entry1.get()
        for search in val:
            if search == to_search:
                self.tree.selection_set(val[val.index(search) - 1])
                self.tree.focus(val[val.index(search) - 1])
                messagebox.showinfo("Success!!", "Bill Number: {} found.".format(self.entry1.get()), parent=invoice)
                break
        else:
            messagebox.showerror("Oops!!", "Bill NUmber: {} not found.".format(self.entry1.get()), parent=invoice)

    def Logout(self):
        sure = messagebox.askyesno("Logout", "Are you sure you want to logout?")
        if sure == True:
            invoice.destroy()
            root.deiconify()
            page1.entry1.delete(0, END)
            page1.entry2.delete(0, END)

    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)

    def Exit(self):
        sure = messagebox.askyesno("Exit", "Are you sure you want to exit?", parent=invoice)
        if sure == True:
            invoice.destroy()



class open_bill:

  def __init__(self, top=None):

        top.geometry("765x488")
        top.resizable(0, 0)
        top.title("Bill")

        self.label1 = Label(bill)
        self.label1.place(relx=0, rely=0, width=765, height=488)
        self.img = PhotoImage(file="./images/bill.png")
        self.label1.configure(image=self.img)

        self.name_message = Text(bill)
        self.name_message.place(relx=0.178, rely=0.205, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(bill)
        self.num_message.place(relx=0.854, rely=0.205, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(bill)
        self.bill_message.place(relx=0.150, rely=0.243, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(bill)
        self.bill_date_message.place(relx=0.780, rely=0.243, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")

        self.Scrolledtext1 = tkst.ScrolledText(top)
        self.Scrolledtext1.place(relx=0.044, rely=0.41, width=695, height=284)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [bill_num])
        results = cur.fetchall()
        if results:
            self.name_message.insert(END, results[0][2])
            self.name_message.configure(state="disabled")

            self.num_message.insert(END, results[0][3])
            self.num_message.configure(state="disabled")

            self.bill_message.insert(END, results[0][0])
            self.bill_message.configure(state="disabled")

            self.bill_date_message.insert(END, results[0][1])
            self.bill_date_message.configure(state="disabled")

            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")

            abc = self.name_message.get("1.0", tk.END)

            curinp=self.Scrolledtext1.get("1.0",tk.END)
            f1=open("ojmimi.txt","w",encoding="utf-8")
            f1.write(curinp)
            f1.write(abc)

            bill_title = Label(F3, text='Contribution', font='arial 15 bold', bd=7, relief=GROOVE).pack(fill=X)
            scrol_y = Scrollbar(F3, orient=VERTICAL)
            textarea = tk.Text(F3, bg="light cyan", yscrollcommand=scrol_y)
            scrol_y.pack(side=RIGHT, fill=Y)
            scrol_y.config(command=textarea.yview)
            textarea.pack()
            user_in = textarea.get(1.0, "end-1c")
            textarea.delete(1.0, END)
            textarea.insert(END, "\t  WELCOME TO (NASCS-NICS) BILL REPORT")
            textarea.insert(INSERT, "\n\n Name:-----\t\t" + self.name_message.get("1.0", "end-1c"))
            textarea.insert(INSERT, "\n\n Number:-----\t\t" + self.num_message.get("1.0", "end-1c"))
            textarea.insert(INSERT, "\n\n MESSAGE:-----\t\t" + self.bill_message.get("1.0", "end-1c"))
            textarea.insert(INSERT, "\n\n DATE:-----\t\t" + self.bill_date_message.get("1.0", "end-1c"))
            textarea.insert(END, f"\n==============================================================================")
            textarea.insert(END, f" PRODUCT                 QTY                          COST")
            textarea.insert(END, f"\n============================================================================\n")
            #textarea.insert(INSERT, self.Scrolledtext1.get("1.0", "end-1c"))
            textarea.insert(INSERT, self.Scrolledtext1.get("1.0",tk.END))
            textarea.configure(font='arial 8 bold')
            textarea.configure(width=700)
            q = textarea.get("1.0", "end-1c")
            filename = tempfile.mktemp(".txt")
            #open(filename, "w", encoding="utf-8")
            file = open(filename, "w", encoding="utf-8")
            file.write(q)
            win32api.ShellExecute(0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)



class login_page:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("NASCS NICS")

        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/employee_login.png")
        self.label1.configure(image=self.img)

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.373, rely=0.273, width=374, height=24)
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=user)

        self.entry2 = Entry(root)
        self.entry2.place(relx=0.373, rely=0.384, width=374, height=24)
        self.entry2.configure(font="-family {Poppins} -size 10")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")
        self.entry2.configure(textvariable=passwd)

        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#0ed145")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="white")
        self.button1.configure(background="#0ed145")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""LOGIN""")
        self.button1.configure(command=login)


class Item:
    def __init__(self, name, price, qty):
        self.product_name = name
        self.price = price
        self.qty = qty
        #self.idpr=idpr

class Cart:
    def __init__(self):
        self.items = []
        self.dictionary = {}

    def add_item(self, item):
        self.items.append(item)

    def remove_item(self):
        self.items.pop()

    def remove_items(self):
        self.items.clear()

    def total(self):
        total = 0.0
        for i in self.items:
            total += i.price * i.qty
        return total

    def isEmpty(self):
        if len(self.items)==0:
            return True
        
    def allCart(self):
        for i in self.items:
            if (i.product_name in self.dictionary):
                self.dictionary[i.product_name] += i.qty
            else:
                self.dictionary.update({i.product_name:i.qty})
    

def exitt():
    sure = messagebox.askyesno("Exit","Are you sure you want to exit?", parent=biller)
    if sure == True:
        biller.destroy()
        root.destroy()


class bill_window:
    def __init__(self, top=None):
        top.geometry("1366x768")
        top.resizable(0, 0)
        top.title("Billing System")

        self.label = Label(biller)
        self.label.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file="./images/bill_window.png")
        self.label.configure(image=self.img)

        self.message = Label(biller)
        self.message.place(relx=0.038, rely=0.055, width=136, height=30)
        self.message.configure(font="-family {Poppins} -size 10")
        self.message.configure(foreground="white")
        self.message.configure(background="#0ed145")
        self.message.configure(text=username)
        self.message.configure(anchor="w")

        self.clock = Label(biller)
        self.clock.place(relx=0.9, rely=0.065, width=102, height=36)
        self.clock.configure(font="-family {Poppins Light} -size 12")
        self.clock.configure(foreground="white")
        self.clock.configure(background="#0ed145")

        self.entry1 = Entry(biller)
        self.entry1.place(relx=0.509, rely=0.23, width=240, height=24)
        self.entry1.configure(font="-family {Poppins} -size 12")
        self.entry1.configure(relief="flat")
        self.entry1.configure(textvariable=cust_name)

        self.entry2 = Entry(biller)
        self.entry2.place(relx=0.791, rely=0.23, width=240, height=24)
        self.entry2.configure(font="-family {Poppins} -size 12")
        self.entry2.configure(relief="flat")
        self.entry2.configure(textvariable=cust_num)

        self.entry3 = Entry(biller)
        self.entry3.place(relx=0.102, rely=0.23, width=240, height=24)
        self.entry3.configure(font="-family {Poppins} -size 12")
        self.entry3.configure(relief="flat")
        self.entry3.configure(textvariable=cust_search_bill)

        self.button1 = Button(biller)
        self.button1.place(relx=0.031, rely=0.104, width=76, height=23)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#0ed145")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="white")
        self.button1.configure(background="#0ed145")
        self.button1.configure(font="-family {Poppins SemiBold} -size 12")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Logout""")
        self.button1.configure(command=logout)


        self.button2 = Button(biller)
        self.button2.place(relx=0.315, rely=0.234, width=76, height=23)
        self.button2.configure(relief="flat")
        self.button2.configure(overrelief="flat")
        self.button2.configure(activebackground="#0ed145")
        self.button2.configure(cursor="hand2")
        self.button2.configure(foreground="white")
        self.button2.configure(background="#0ed145")
        self.button2.configure(font="-family {Poppins SemiBold} -size 12")
        self.button2.configure(borderwidth="0")
        self.button2.configure(text="""Search""")
        self.button2.configure(command=self.search_bill)


        self.button22 = Button(biller)
        self.button22.place(relx=0.9, rely=0.125, width=100, height=15)
        self.button22.configure(relief="flat")
        self.button22.configure(overrelief="flat")
        self.button22.configure(activebackground="#0ed145")
        self.button22.configure(cursor="hand2")
        self.button22.configure(foreground="#ffffff")
        self.button22.configure(background="#0ed145")
        self.button22.configure(font="-family {Poppins SemiBold} -size 10")
        self.button22.configure(borderwidth="0")
        self.button22.configure(text="""INVOICE""")
        self.button22.configure(command=invoices)


        self.button23 = Button(biller)
        self.button23.place(relx=0.9, rely=0.150, width=100, height=15)
        self.button23.configure(relief="flat")
        self.button23.configure(overrelief="flat")
        self.button23.configure(activebackground="#0ed145")
        self.button23.configure(cursor="hand2")
        self.button23.configure(foreground="#ffffff")
        self.button23.configure(background="#0ed145")
        self.button23.configure(font="-family {Poppins SemiBold} -size 10")
        self.button23.configure(borderwidth="0")
        self.button23.configure(text="""ADD PRODUCT""")
        self.button23.configure(command=inventory)

        self.buttonpr = Button(biller)
        self.buttonpr.place(relx=0.9, rely=0.175, width=100, height=15)
        self.buttonpr.configure(relief="flat")
        self.buttonpr.configure(overrelief="flat")
        self.buttonpr.configure(activebackground="#0ed145")
        self.buttonpr.configure(cursor="hand2")
        self.buttonpr.configure(foreground="#ffffff")
        self.buttonpr.configure(background="#0ed145")
        self.buttonpr.configure(font="-family {Poppins SemiBold} -size 10")
        self.buttonpr.configure(borderwidth="0")
        self.buttonpr.configure(text="""PROFIT""")
        self.buttonpr.configure(command=profitnas)

        self.button3 = Button(biller)
        self.button3.place(relx=0.048, rely=0.885, width=86, height=25)
        self.button3.configure(relief="flat")
        self.button3.configure(overrelief="flat")
        self.button3.configure(activebackground="#0ed145")
        self.button3.configure(cursor="hand2")
        self.button3.configure(foreground="white")
        self.button3.configure(background="#0ed145")
        self.button3.configure(font="-family {Poppins SemiBold} -size 10")
        self.button3.configure(borderwidth="0")
        self.button3.configure(text="""Total""")
        self.button3.configure(command=self.total_bill)

        self.button4 = Button(biller)
        self.button4.place(relx=0.141, rely=0.885, width=84, height=25)
        self.button4.configure(relief="flat")
        self.button4.configure(overrelief="flat")
        self.button4.configure(activebackground="#0ed145")
        self.button4.configure(cursor="hand2")
        self.button4.configure(foreground="white")
        self.button4.configure(background="#0ed145")
        self.button4.configure(font="-family {Poppins SemiBold} -size 10")
        self.button4.configure(borderwidth="0")
        self.button4.configure(text="""Generate""")
        self.button4.configure(command=self.gen_bill)

        self.button5 = Button(biller)
        self.button5.place(relx=0.230, rely=0.885, width=86, height=25)
        self.button5.configure(relief="flat")
        self.button5.configure(overrelief="flat")
        self.button5.configure(activebackground="#0ed145")
        self.button5.configure(cursor="hand2")
        self.button5.configure(foreground="white")
        self.button5.configure(background="#0ed145")
        self.button5.configure(font="-family {Poppins SemiBold} -size 10")
        self.button5.configure(borderwidth="0")
        self.button5.configure(text="""Clear""")
        self.button5.configure(command=self.clear_bill)

        self.button6 = Button(biller)
        self.button6.place(relx=0.322, rely=0.885, width=86, height=25)
        self.button6.configure(relief="flat")
        self.button6.configure(overrelief="flat")
        self.button6.configure(activebackground="#0ed145")
        self.button6.configure(cursor="hand2")
        self.button6.configure(foreground="white")
        self.button6.configure(background="#0ed145")
        self.button6.configure(font="-family {Poppins SemiBold} -size 10")
        self.button6.configure(borderwidth="0")
        self.button6.configure(text="""Exit""")
        self.button6.configure(command=exitt)

        self.button7 = Button(biller)
        self.button7.place(relx=0.098, rely=0.734, width=86, height=26)
        self.button7.configure(relief="flat")
        self.button7.configure(overrelief="flat")
        self.button7.configure(activebackground="#0ed145")
        self.button7.configure(cursor="hand2")
        self.button7.configure(foreground="white")
        self.button7.configure(background="#0ed145")
        self.button7.configure(font="-family {Poppins SemiBold} -size 10")
        self.button7.configure(borderwidth="0")
        self.button7.configure(text="""Add To Cart""")
        self.button7.configure(command=self.add_to_cart)

        self.button8 = Button(biller)
        self.button8.place(relx=0.274, rely=0.734, width=84, height=26)
        self.button8.configure(relief="flat")
        self.button8.configure(overrelief="flat")
        self.button8.configure(activebackground="#0ed145")
        self.button8.configure(cursor="hand2")
        self.button8.configure(foreground="white")
        self.button8.configure(background="#0ed145")
        self.button8.configure(font="-family {Poppins SemiBold} -size 10")
        self.button8.configure(borderwidth="0")
        self.button8.configure(text="""Clear""")
        self.button8.configure(command=self.clear_selection)

        self.button9 = Button(biller)
        self.button9.place(relx=0.194, rely=0.734, width=68, height=26)
        self.button9.configure(relief="flat")
        self.button9.configure(overrelief="flat")
        self.button9.configure(activebackground="#0ed145")
        self.button9.configure(cursor="hand2")
        self.button9.configure(foreground="white")
        self.button9.configure(background="#0ed145")
        self.button9.configure(font="-family {Poppins SemiBold} -size 10")
        self.button9.configure(borderwidth="0")
        self.button9.configure(text="""Remove""")
        self.button9.configure(command=self.remove_product)

        text_font = ("Poppins", "8")
        self.combo1 = ttk.Combobox(biller)
        self.combo1.place(relx=0.035, rely=0.408, width=477, height=26)

        find_category = "SELECT product_cat FROM raw_inventory"
        cur.execute(find_category)
        result1 = cur.fetchall()
        cat = []
        for i in range(len(result1)):
            if(result1[i][0] not in cat):
                cat.append(result1[i][0])


        self.combo1.configure(values=cat)
        self.combo1.configure(state="readonly")
        self.combo1.configure(font="-family {Poppins} -size 8")
        self.combo1.option_add("*TCombobox*Listbox.font", text_font)
        self.combo1.option_add("*TCombobox*Listbox.selectBackground", "#D2463E")


        self.combo2 = ttk.Combobox(biller)
        self.combo2.place(relx=0.035, rely=0.479, width=477, height=26)
        self.combo2.configure(font="-family {Poppins} -size 8")
        self.combo2.option_add("*TCombobox*Listbox.font", text_font) 
        self.combo2.configure(state="disabled")


        self.combo3 = ttk.Combobox(biller)
        self.combo3.place(relx=0.035, rely=0.551, width=477, height=26)
        self.combo3.configure(state="disabled")
        self.combo3.configure(font="-family {Poppins} -size 8")
        self.combo3.option_add("*TCombobox*Listbox.font", text_font)

        self.entry4 = ttk.Entry(biller,textvar=prqty)
        self.entry4.place(relx=0.035, rely=0.629, width=477, height=26)
        self.entry4.configure(font="-family {Poppins} -size 8")
        self.entry4.configure(foreground="#000000")
        self.entry4.configure(state="disabled")


        self.entrypid = ttk.Entry(biller,textvar=pdno)
        self.entrypid.place(relx=0.035, rely=0.695, width=100, height=15)
        self.entrypid.configure(font="-family {Poppins} -size 8")
        self.entrypid.configure(foreground="#000000")
        self.entrypid.configure(state="disabled")

        self.entrycstp = ttk.Entry(biller,textvar=cstpd)
        self.entrycstp.place(relx=0.120, rely=0.695, width=100, height=15)
        self.entrycstp.configure(font="-family {Poppins} -size 8")
        self.entrycstp.configure(foreground="#000000")
        self.entrycstp.configure(state="disabled")

        self.Scrolledtext1 = tkst.ScrolledText(top)
        self.Scrolledtext1.place(relx=0.439, rely=0.586, width=695, height=275)
        self.Scrolledtext1.configure(borderwidth=0)
        self.Scrolledtext1.configure(font="-family {Podkova} -size 8")
        self.Scrolledtext1.configure(state="disabled")

        self.combo1.bind("<<ComboboxSelected>>", self.get_category)

        self.Scrolledtext2 = tkst.ScrolledText()
        textsip = tk.Text()

        
    def get_category(self, Event):
        self.combo2.configure(state="readonly")
        self.combo2.set('')
        self.combo3.set('')
        find_subcat = "SELECT product_subcat FROM raw_inventory WHERE product_cat = ?"
        cur.execute(find_subcat, [self.combo1.get()])
        result2 = cur.fetchall()
        subcat = []
        for j in range(len(result2)):
            if(result2[j][0] not in subcat):
                subcat.append(result2[j][0])
        
        self.combo2.configure(values=subcat)
        self.combo2.bind("<<ComboboxSelected>>", self.get_subcat)
        self.combo3.configure(state="disabled")

    def get_subcat(self, Event):
        self.combo3.configure(state="readonly")
        self.combo3.set('')
        find_product = "SELECT product_name FROM raw_inventory WHERE product_cat = ? and product_subcat = ?"
        cur.execute(find_product, [self.combo1.get(), self.combo2.get()])
        result3 = cur.fetchall()
        pro = []
        for k in range(len(result3)):
            pro.append(result3[k][0])

        self.combo3.configure(values=pro)
        self.combo3.bind("<<ComboboxSelected>>",self.proID)
        self.entry4.configure(state="disabled")


    def show_qty(self, Event):
        self.entry4.configure(state="normal")
        self.qty_label = Label(biller)
        self.qty_label.place(relx=0.028, rely=0.664, width=82, height=26)
        self.qty_label.configure(font="-family {Poppins} -size 8")
        self.qty_label.configure(anchor="w")

        product_name = self.combo3.get()
        find_qty = "SELECT stock FROM raw_inventory WHERE product_name = ?"
        cur.execute(find_qty, [product_name])
        results = cur.fetchone()
        self.qty_label.configure(text="In Stock: {}".format(results[0]))
        self.qty_label.configure(background="#ffffff")
        self.qty_label.configure(foreground="#333333")

    def proID(self, Event):
        global row
        a = pdno.get()
        self.entry4.configure(state="normal")
        product_name = self.combo3.get()
        find_qtye = "SELECT product_id FROM raw_inventory WHERE product_name = ?"
        cur.execute(find_qtye,[product_name])
        results=cur.fetchone()
        if results:
            for row in results:
                pdno.set(results)
    def cstPro(self, Event):
        global row1
        b = cstpd.get()
        self.entry4.configure(state="normal")
        productcost = self.entrycstp
        find_cst= "SELECT cost_price FROM raw_inventory WHERE product_name = ?"
        cur.execute(find_cst,[productcost])
        resultc=cur.fetchone()
        if resultc:
            for row1 in resultc:
                b.set(resultc)

    cart = Cart()
    def add_to_cart(self):
        global sp
        global pidpro
        global bill_text
        global bilt
        global profit1
        global product_name
        self.Scrolledtext1.configure(state="normal")
        strr = self.Scrolledtext1.get('1.0', END)
        pidpro=self.entrypid.get()
        mem=self.entry1.get()
        mam=self.entry2.get().upper()
        prdcstn=self.entrycstp.get()
        today = datetime.date.today()
        if strr.find('Total')==-1:
             messagebox.showinfo("NOTICE","Please remove and renter items from Cart if  Customers_Name and File_No was empty before clicking this button")
             product_name = self.combo3.get()
             if(product_name!=""):
                product_qty = self.entry4.get()
                find_mrp = "SELECT mrp, stock FROM raw_inventory WHERE product_name = ?"
                cur.execute(find_mrp, [product_name])
                results = cur.fetchall()
                stock = results[0][1]
                mrp = results[0][0]
                if product_qty.isdigit()==True:
                   if (stock-int(product_qty))>=0:
                       sp = mrp*int(product_qty)
                       item = Item(product_name, mrp,int(product_qty))
                       self.cart.add_item(item)
                       self.Scrolledtext1.configure(state="normal")
                       bill_text = "{}\t\t\t\t\t\t{}\t\t\t\t\t   {}\n".format(product_name, product_qty, sp)
                       bilt = "{}\t{}\t{}\t{}\n".format(pidpro,product_name, product_qty, sp)
                       self.Scrolledtext1.insert('insert', bill_text)
                       self.Scrolledtext1.configure(state="disabled")
                   if (product_name==self.combo3.get()and pidpro==self.entrypid.get()):
                       finpr = "SELECT cost_price FROM raw_inventory WHERE product_name = ? and product_id=?"
                       cur.execute(finpr, (product_name,pidpro))
                       res = cur.fetchone()[0]
                       cstpd.set(res)
                       wen = res
                       cp = int(product_qty)
                       prof = wen * cp
                       outc=sp-prof
                       insert = (
                            "INSERT INTO buyers(FNO,PID,NAME,DATE,PNAME,PQTY,SP,COSTP,PROFIT) VALUES(?,?,?,?,?,?,?,?,?)"
                            )
                       cur.execute(insert, [self.entry2.get(), self.entrypid.get(), self.entry1.get(), str(date.today()),self.combo3.get(), self.entry4.get(),sp,self.entrycstp.get(),outc])
                       db.commit()
                   else:
                    messagebox.showerror("Oops!", "Out of stock. Check quantity.", parent=biller)
                else:
                 messagebox.showerror("Oops!", "Invalid quantity.", parent=biller)
             else:
                messagebox.showerror("Oops!", "Choose a product.", parent=biller)
        else:
                self.Scrolledtext1.delete('1.0', END)
                new_li = []
                li = strr.split("\n")
                for i in range(len(li)):
                    if len(li[i])!=0:
                        if li[i].find('Total')==-1:
                            new_li.append(li[i])
                    else:
                        break
                for j in range(len(new_li)-1):
                        self.Scrolledtext1.insert('insert', new_li[j])
                        self.Scrolledtext1.insert('insert','\n')
                        product_name = self.combo3.get()
                        pidpro = self.entrypid.get()

    def remove_product(self):
        if(self.cart.isEmpty()!=True):
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.Scrolledtext1.configure(state="normal")
                    get_all_bill = (self.Scrolledtext1.get('1.0', END).split("\n"))
                    new_string = get_all_bill[:len(get_all_bill)-3]
                    self.Scrolledtext1.delete('1.0', END)
                    for i in range(len(new_string)):
                        self.Scrolledtext1.insert('insert', new_string[i])
                        self.Scrolledtext1.insert('insert','\n')
                    
                    self.Scrolledtext1.configure(state="disabled")
            else:
                try:
                    self.cart.remove_item()
                except IndexError:
                    messagebox.showerror("Oops!", "Cart is empty", parent=biller)
                else:
                    self.Scrolledtext1.delete('1.0', END)
                    new_li = []
                    li = strr.split("\n")
                    for i in range(len(li)):
                        if len(li[i])!=0:
                            if li[i].find('Total')==-1:
                                new_li.append(li[i])
                            else:
                                break
                    new_li.pop()
                    for j in range(len(new_li)-1):
                        self.Scrolledtext1.insert('insert', new_li[j])
                        self.Scrolledtext1.insert('insert','\n')
                    self.Scrolledtext1.configure(state="disabled")

        else:
            messagebox.showerror("Oops!", "Add a product.", parent=biller)

    def wel_bill(self):
        self.name_message = Text(biller)
        self.name_message.place(relx=0.514, rely=0.452, width=176, height=30)
        self.name_message.configure(font="-family {Podkova} -size 10")
        self.name_message.configure(borderwidth=0)
        self.name_message.configure(background="#ffffff")

        self.num_message = Text(biller)
        self.num_message.place(relx=0.894, rely=0.452, width=90, height=30)
        self.num_message.configure(font="-family {Podkova} -size 10")
        self.num_message.configure(borderwidth=0)
        self.num_message.configure(background="#ffffff")

        self.bill_message = Text(biller)
        self.bill_message.place(relx=0.499, rely=0.477, width=176, height=26)
        self.bill_message.configure(font="-family {Podkova} -size 10")
        self.bill_message.configure(borderwidth=0)
        self.bill_message.configure(background="#ffffff")

        self.bill_date_message = Text(biller)
        self.bill_date_message.place(relx=0.852, rely=0.477, width=90, height=26)
        self.bill_date_message.configure(font="-family {Podkova} -size 10")
        self.bill_date_message.configure(borderwidth=0)
        self.bill_date_message.configure(background="#ffffff")
    
    def total_bill(self):
        global total2
        if self.cart.isEmpty():
            messagebox.showerror("Oops!", "Add a product.", parent=biller)
        else:
            self.Scrolledtext1.configure(state="normal")
            strr = self.Scrolledtext1.get('1.0', END)
            if strr.find('Total')==-1:
                self.Scrolledtext1.configure(state="normal")
                divider = "\n\n\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider)
                total = "\nTotal\t\t\t\t\t\t\t\t\t\t\tNGN. {}".format(self.cart.total())
                total2= "\n {}".format(self.cart.total())
                self.Scrolledtext1.insert('insert', total)
                divider2 = "\n"+("─"*61)
                self.Scrolledtext1.insert('insert', divider2)
                self.Scrolledtext1.configure(state="disabled")
            else:
                return

    state = 1
    def gen_bill(self):
        global der
        global bilt
        global divider
        product_name = self.combo3.get()
        product_qty = self.entry4.get()
        lin=self.combo1.get()
        pidpro = self.entrypid.get()
        mem=self.entry1.get()
        mam=self.entry2.get().upper()
        der="─"
        self.Scrolledtext1.insert('insert', bill_text)

        if self.state == 1:
            strr = self.Scrolledtext1.get('1.0', END)
            self.wel_bill()
            if(cust_name.get()==""):
                messagebox.showerror("Oops!", "Please enter a name.", parent=biller)
            elif(cust_num.get()==""):
                messagebox.showerror("Oops!", "Please enter a number.", parent=biller)
            elif valid_phone(cust_num.get())==False:
                messagebox.showerror("Oops!", "Please enter a valid number.", parent=biller)
            elif(self.cart.isEmpty()):
                messagebox.showerror("Oops!", "Cart is empty.", parent=biller)
            else:

                if strr.find('Total')==-1:
                    self.total_bill()
                    self.gen_bill()
                else:
                    bilt= "{}\t{}\t{}\t{}\t{}\t{}\n".format(pidpro,mem,mam, product_name, product_qty, sp)
                    f1 = open("roler.txt", "a", encoding="utf-8")
                    f1.write(bilt)
                    f1.close()

                    self.name_message.insert(END, cust_name.get())
                    self.name_message.configure(state="disabled")

                    self.num_message.insert(END, cust_num.get())
                    self.num_message.configure(state="disabled")
            
                    cust_new_bill.set(random_bill_number(8))

                    self.bill_message.insert(END, cust_new_bill.get())
                    self.bill_message.configure(state="disabled")
                
                    bill_date.set(str(date.today()))

                    self.bill_date_message.insert(END, bill_date.get())
                    self.bill_date_message.configure(state="disabled")
                    var=StringVar()
                    var.set(str(date.today()))


                    with sqlite3.connect("./Database/store.db") as db:
                        cur = db.cursor()
                    insert = (
                        "INSERT INTO bill(bill_no, date, customer_name, customer_no, bill_details) VALUES(?,?,?,?,?)"
                    )
                    cur.execute(insert, [cust_new_bill.get(), bill_date.get(), cust_name.get(), cust_num.get(), self.Scrolledtext1.get('1.0', END)])
                    insert2 = (
                        "INSERT INTO TOTAL(billno, date, name, CustNo, totalbill) VALUES(?,?,?,?,?)"
                    )
                    cur.execute(insert2, [cust_new_bill.get(), bill_date.get(), cust_name.get(), cust_num.get(),total2])
                    db.commit()
                    print(self.cart.allCart())                    #nap = self.name_message.get("1.0", tk.END)

                    messagebox.showinfo("Success!!", "Bill Generated", parent=biller)
                    self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
                    self.state = 0
        else:
            return
                    
    def clear_bill(self):
        self.wel_bill()
        self.entry1.configure(state="normal")
        self.entry2.configure(state="normal")
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)
        self.name_message.configure(state="normal")
        self.num_message.configure(state="normal")
        self.bill_message.configure(state="normal")
        self.bill_date_message.configure(state="normal")
        self.Scrolledtext1.configure(state="normal")
        self.name_message.delete(1.0, END)
        self.num_message.delete(1.0, END)
        self.bill_message.delete(1.0, END)
        self.bill_date_message.delete(1.0, END)
        self.Scrolledtext1.delete(1.0, END)
        self.name_message.configure(state="disabled")
        self.num_message.configure(state="disabled")
        self.bill_message.configure(state="disabled")
        self.bill_date_message.configure(state="disabled")
        self.Scrolledtext1.configure(state="disabled")
        self.cart.remove_items()
        self.state = 1

    def clear_selection(self):
        self.entry4.delete(0, END)
        self.combo1.configure(state="normal")
        self.combo2.configure(state="normal")
        self.combo3.configure(state="normal")
        self.combo1.delete(0, END)
        self.combo2.delete(0, END)
        self.combo3.delete(0, END)
        self.combo2.configure(state="disabled")
        self.combo3.configure(state="disabled")
        self.entry4.configure(state="disabled")
        try:
            self.qty_label.configure(foreground="#ffffff")
        except AttributeError:
            pass
             
    def search_bill(self):
        find_bill = "SELECT * FROM bill WHERE bill_no = ?"
        cur.execute(find_bill, [cust_search_bill.get().rstrip()])
        results = cur.fetchall()
        if results:
            self.clear_bill()
            self.wel_bill()
            self.name_message.insert(END, results[0][2])
            self.name_message.configure(state="disabled")
    
            self.num_message.insert(END, results[0][3])
            self.num_message.configure(state="disabled")
    
            self.bill_message.insert(END, results[0][0])
            self.bill_message.configure(state="disabled")

            self.bill_date_message.insert(END, results[0][1])
            self.bill_date_message.configure(state="disabled")

            self.Scrolledtext1.configure(state="normal")
            self.Scrolledtext1.insert(END, results[0][4])
            self.Scrolledtext1.configure(state="disabled")

            self.entry1.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")
            self.entry2.configure(state="disabled", disabledbackground="#ffffff", disabledforeground="#000000")

            self.textarea = tk.Text(bill)
            q = self.textarea.get("1.0", "end-1c")
            filename = tempfile.mktemp(".txt")
            open(filename, "w").write(q)
            win32api.ShellExecute(0, "print", filename, '/d:"%s"' % win32print.GetDefaultPrinter(), ".", 0)
            user_in = self.textarea.get(1.0, "end-1c")
            self.textarea.delete(1.0, END)
            self.textarea.insert(END, "\t  WELCOME TO (NASCS-NICS) CONTRIBUTION SCHEME")
            self.textarea.insert(END, f"\n\nFile No:-----\t\t{self.bill_message.get()}")
            self.textarea.insert(INSERT, self.bill_message.get("1.0", "end-1c"))
            self.textarea.insert(INSERT, self.num_message.get("1.0", "end-1c"))
            self.state = 0

        else:
            messagebox.showerror("Error!!", "Bill not found.", parent=biller)
            self.entry3.delete(0, END)
            
    def time(self):
        string = strftime("%H:%M:%S %p")
        self.clock.config(text=string)
        self.clock.after(1000, self.time)


page1 = login_page(root)
root.bind("<Return>", login)
root.mainloop()

