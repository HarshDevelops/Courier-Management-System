from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from datetime import date,time
import mysql.connector
demo=mysql.connector.connect(
    user='root', #ENTER YOUR MYSQL USERNAME HERE    
    host='localhost', #ENTER YOUR MYSQL HOSTNAME HERE
    port=3308, #ENTER YOUR PORT NUMBER HERE. DEFAULT IS 3307(YOU CAN COMMENT THIS LINE TOO)
    password='tiger' #ENTER YOUR MYSQL PWD HERE
    )

mycursor=demo.cursor()

mycursor.execute("CREATE DATABASE IF NOT EXISTS SPEKTREN_COURIERS")
mycursor.execute("USE SPEKTREN_COURIERS")

mycursor.execute("""CREATE TABLE IF NOT EXISTS USERS(DATE_OF_REG DATE,
                 USERNAME VARCHAR(20),PASSWORD VARCHAR(20))""")
                

mycursor.execute("""CREATE TABLE IF NOT EXISTS PARCEL(SENDERS_NAME VARCHAR(100),                                     
                 SENDERS_CONTACT VARCHAR(20),
                 SENDERS_ADD VARCHAR(100),
                 RECEIVERS_NAME VARCHAR(100),
                 RECEIVERS_ADDRESS VARCHAR(120),
                 RECEIVERS_CONTACT VARCHAR(20),
                 WEIGHT VARCHAR(20),
                 AMOUNT VARCHAR(20))""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS MONEY_ORDER(RECEIVERS_NAME VARCHAR(100),
                 RECEIVERS_CITYORTOWN VARCHAR(30),
                 RECEIVERS_ADDRESS VARCHAR(120),
                 RECEIVERS_CONTACT VARCHAR(20),
                 AMOUNT VARCHAR(20))""")

mycursor.execute("""CREATE TABLE IF NOT EXISTS LETTER(SENDERS_NAME VARCHAR(100),
                 SENDERS_CONTACT VARCHAR(20),
                 SENDERS_ADD VARCHAR(100),
                 RECEIVERS_NAME VARCHAR(100),
                 RECEIVERS_ADDRESS VARCHAR(120),
                 RECEIVERS_CONTACT VARCHAR(20),
                 AMOUNT VARCHAR(20))""")

#p1= PrettyTable(['Type','Senders Name','Receivers Name','Total Price'])
#p2= PrettyTable(['Type','Receivers Name','Amount Sent','Our Comission','Total Price'])
#p3= PrettyTable(['Type','Receivers Name','Receivers Name','Weight','Total Price'])
                
 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Register")
    register_screen.geometry("300x250")
    register_screen.configure(background="deepskyblue")
 
    global username
    global password
    global username_entry
    global password_entry
    username = StringVar()
    password = StringVar()
 
    Label(register_screen, text="Please enter details below", bg="black",fg="white").pack()
    Label(register_screen, text="",bg='deepskyblue').pack()
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    Label(register_screen, text="",bg='deepskyblue').pack()
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()

    Label(register_screen, text="",bg='deepskyblue').pack()
    Button(register_screen, text="Register", width=10, height=1, bg="black", fg="white",command = register_check).pack()
 
 
# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    login_screen.configure(background="deepskyblue")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="",bg='deepskyblue').pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="",bg='deepskyblue').pack()
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="",bg='deepskyblue').pack()
    Label(login_screen,text=" ",bg='deepskyblue').pack(fill="both")
    Label(login_screen,text="* : Mandatory", fg="red",anchor="e",bg='deepskyblue').pack(fill="both")
    m=Button(login_screen, text="Login", width=10, height=1, command = login_verify).pack()


 
def register_user():
 
    global date
    username_info = username.get()
    password_info = password.get()
    date=(date.today())
    sql=("INSERT INTO USERS(DATE_OF_REG,USERNAME,PASSWORD) VALUES (%s,%s,%s)")
    val=(date,username_info,password_info)
    mycursor.execute(sql,val)
    demo.commit()
    Label(register_screen, text="Registration Success", fg="green", font=("calibri", 11)).pack()
    delete_registration_success()
    #courier()
    register_screen.mainloop()
 
def login_verify():
    username1 = username_verify.get()
    password1 = password_verify.get()
    sql="SELECT USERNAME,PASSWORD FROM USERS WHERE USERNAME='%s'"%username1
    mycursor.execute(sql)
    y=mycursor.fetchall()
    if(len(y)==0):
        user_not_found()
    for i in y:
        pfd=(i[-1]).lower()
        if(pfd == password1):
            delete_login_success()
        else:
            password_not_recognised()

def feed():
    global textcomment
    global frame_content
    global root
    global entry_name,entry_email
    root = Toplevel()
    root.configure(background='deepskyblue')
    root.title('Feedback')
    frame_header = ttk.Frame(root)
    frame_header.pack()

    img1 = Image.open("spektren.jpg")
    img2=img1.resize((150,100),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    panel=Label(frame_header,image=img3)
    panel.grid(row=0,column=0,rowspan=2)

    headerlabel = Label(frame_header, text='CUSTOMER FEEDBACK', foreground='orange',
                            font=('Arial', 24))
    headerlabel.grid(row=0, column=1)
    messagelabel = Label(frame_header,
                             text='PLEASE TELL US WHAT YOU THINK',
                             foreground='purple', font=('Arial', 10))
    messagelabel.grid(row=1, column=1)

    frame_content = Frame(root)
    frame_content.pack()
    global var
    global myvar
    myvar = StringVar()
    var = StringVar()

    namelabel =Label(frame_content, text='Name')
    namelabel.grid(row=0, column=0, padx=5, sticky='sw')
    entry_name = ttk.Entry(frame_content, width=18, font=('Arial', 14), textvariable=myvar)
    entry_name.grid(row=1, column=0)

    emaillabel = ttk.Label(frame_content, text='Email')
    emaillabel.grid(row=0, column=1, sticky='sw')
    entry_email = ttk.Entry(frame_content, width=18, font=('Arial', 14), textvariable=var)
    entry_email.grid(row=1, column=1)

    commentlabel = ttk.Label(frame_content, text='Comment', font=('Arial', 10))
    commentlabel.grid(row=2, column=0, sticky='sw')
    textcomment = Text(frame_content, width=55, height=10)
    textcomment.grid(row=3, column=0, columnspan=2)

    textcomment.config(wrap ='word')
    submitbutton = ttk.Button(frame_content, text='Submit', command=submit).grid(row=4, column=0, sticky='e')
    clearbutton = ttk.Button(frame_content, text='Clear', command=clear).grid(row=4, column=1, sticky='w')
    root.mainloop()

def clear():
    global entry_name
    global entry_email
    global textcomment
    messagebox.showinfo(title='clear', message='Do you want to clear?')
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    textcomment.delete(1.0, END)


def submit():
    file=open("feed2.txt",'a')
    global entry_name
    global entry_email
    global textcomment
    file.write('Name:{}'.format(myvar.get())+"  "+'Email:{}'.format(var.get())+"  "+'Comment:{}'.format(textcomment.get(1.0, END)))
    file.write('\n-----------------------------------------------------------------------------------------------------------------\n')
    file.close()
    messagebox.showinfo(title='Submit', message='Thank you for your Feedback, Your Comments Submited')
    entry_name.delete(0, END)
    entry_email.delete(0, END)
    textcomment.delete(1.0, END)

            
 
def courier():
    global courier_screen
    global v
    courier_screen=Tk()
    v=StringVar(courier_screen,"1")
    courier_screen.title("SPEKTREN COURIERS")
    courier_screen.geometry("300x300")
    courier_screen.configure(background="deepskyblue")
    v=StringVar(courier_screen,"1")
    courier_screen.title("Welcome To Spektren Courier ")

    Label(courier_screen,text="Select Your Choice",bg="black", fg="white", height="2", font=("Calibri", 13)).pack()
    Label(text="",bg="gold")

    options=["MONEY ORDER","LETTER","PARCEL"]
    
    v=StringVar(courier_screen)
    v.set("SELECT")
    w = OptionMenu(courier_screen, v, *options,command=fetch1)
    w.pack()
    courier_screen.mainloop()

    
def fetch1(x):
    x=v.get()
    if(x=="MONEY ORDER"):
        order_confirm()
    elif(x=="PARCEL"):
        parcel_confirm()
    elif(x=="LETTER"):
        letter_confirm()

def letter_confirm():
    response=messagebox.askokcancel(title="Confirmation Window",message="You have selected : letter")
    if(response==True):
        courier_screen.destroy()
        letter()
    elif(response==False):
        courier_screen.destroy()
        courier()
        

def order_confirm():
    response=messagebox.askokcancel(title="Confirmation Window",message="You have selected : MONEY ORDER")
    if(response==True):
        courier_screen.destroy()
        order()
    elif(response==False):
        courier_screen.destroy()
        courier()

def parcel_confirm():
    response=messagebox.askokcancel(title="Confirmation Window",message="You have selected : Parcel")
    if(response==True):
        courier_screen.destroy()
        parcel()
    elif(response==False):
        courier_screen.destroy()
        courier()


#-------------------------------------------------Designing window for letter----------------------------------------------------------------#

def letter():
    global letter_screen,lsname,lsno,lsadd,lrname,lrno,lradd
    letter_screen=Tk()
    letter_screen.title('letter')
    letter_screen.configure(background="deepskyblue")
    letter_screen.state('zoomed')
    Label(letter_screen,text="SPEKTREN COURIERS",bg="gold",fg="red",font=("Times", 30)).pack()
    Label(letter_screen,text="SENDER'S DETAILS",bg="dodgerblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack()
    Label(letter_screen,text='',bg='deepskyblue').pack()
    
    Label(letter_screen,text="Sender's Name:",font=("Times",10),bg='deepskyblue').pack()
    lsname=Entry(letter_screen,font=("Times",10))
    lsname.pack()
        
    Label(letter_screen,text='',bg='deepskyblue').pack()
    
    Label(letter_screen,text="Sender's Contact number:",font=("Times",10),bg='deepskyblue').pack()
    lsno=Entry(letter_screen,font=("Times",10))
    lsno.pack()
        
    Label(letter_screen,text='',bg='deepskyblue').pack()

    Label(letter_screen,text="Sender's Address:",font=("Times",10),bg='deepskyblue').pack()
    lsadd=Entry(letter_screen,font=("Times",10))
    lsadd.pack()
        
    Label(letter_screen,text='',bg='deepskyblue').pack()
    Label(letter_screen,text='',bg='deepskyblue').pack()
    Label(letter_screen,text='',bg='deepskyblue').pack()

    Label(letter_screen,text="RECEIVER'S DETAILS",bg="dodgerblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack()
    Label(letter_screen,text='',bg='deepskyblue').pack()

    Label(letter_screen,text="Receiver's Name:",font=("Times",10),bg='deepskyblue').pack()
    lrname=Entry(letter_screen,font=("Times",10))
    lrname.pack()
    
    Label(letter_screen,text='',bg='deepskyblue').pack()

    Label(letter_screen,text="Receiver's Contact number:",font=("Times",10),bg='deepskyblue').pack()
    lrno=Entry(letter_screen,font=("Times",10))
    lrno.pack()
    Label(letter_screen,text='',bg='deepskyblue').pack()

    Label(letter_screen,text="Receiver's Address:",font=("Times",10),bg='deepskyblue').pack()
    lradd=Entry(letter_screen,font=("Times",10))
    lradd.pack()
        
    Label(letter_screen,text='',bg='deepskyblue').pack()
    Label(letter_screen,text='',bg='deepskyblue').pack()

    img1 = Image.open("submit.png")
    img2=img1.resize((140,100),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    Button(letter_screen,text='',image=img3,command=letter_check).pack(side=TOP)
    letter_screen.mainloop()

def payletter():
    global payletter_screen
    global t,m2,csv2
    payletter_screen=Tk()
    payletter_screen.state('zoomed')
    payletter_screen.title('payment')
    payletter_screen.configure(background="deepskyblue")
    Label(payletter_screen,text="SPEKTREN COURIERS",bg="black",fg="white",font=("Times", 30)).pack()
    Label(payletter_screen,text='PAYMENT',bg="lightblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack(side=TOP)
    Label(payletter_screen,text='',bg='deepskyblue').pack()

    img1 = Image.open("cc.png")
    img2=img1.resize((380,380),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    Label(payletter_screen,text='',image=img3).pack()

    b1=Image.open("paypal logo.png")
    b2=b1.resize((140,21),Image.ANTIALIAS)
    b3=ImageTk.PhotoImage(b2)
    Button(payletter_screen,text='',command=paypalletter,image=b3).place(x=440,y=146)

    options=['Mastercard Debit Cards','Visa Debit Cards','RuPay Debit Cards','Maestro Debit Cards']
    t=StringVar(payletter_screen)
    t.set("    SELECT        ")
    w = OptionMenu(payletter_screen, t, *options)
    w.place(x=457,y=255.2)

    m2=Entry(payletter_screen,font=("Times",10),bd=5)
    m2.place(x=457,y=300)

    months=[' 01 ', ' 02 ',' 03 ',' 04 ',' 05 ',' 06 ',' 07 ',' 08 ',' 09 ', '10', '11', '12']
    mm=StringVar(payletter_screen)
    mm.set("mm")
    w1=OptionMenu(payletter_screen, mm, *months)
    w1.place(x=427,y=350)
    
    years=[2020,2021,2020,2023,2024,2025,2026,2027,2028,2029]
    yy=StringVar(payletter_screen)
    yy.set("yy")
    w2=OptionMenu(payletter_screen, yy, *years)
    w2.place(x=497.5,y=350)

    csv2=Entry(payletter_screen,font=("Times",10),bd=5)
    csv2.place(x=457,y=384)
    
    z1=Image.open("pay.png")
    z2=z1.resize((100,30),Image.ANTIALIAS)
    z3=ImageTk.PhotoImage(z2)
    Button(payletter_screen,text='',command=paymentlettercheck,image=z3).place(x=457,y=424)
    payletter_screen.mainloop()

def paypalletter():
    global email,pwd
    global firstclick
    global secondclick
    firstclick=True
    secondclick=True
    payletter_screen.destroy()
    paypal_screen=Tk()
    paypal_screen.configure(background="deepskyblue")
    paypal_screen.title('payment')
    paypal_screen.geometry('350x350')
    img1 = Image.open("paypal logo.png")
    img2=img1.resize((120,130),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    
    Label(paypal_screen,text='',image=img3).pack()
    email=Entry(paypal_screen,text='',font=('Times',13),bd=3,fg='royalblue')
    email.insert(0, 'Enter your email...')
    email.bind('<FocusIn>', on_entry_click)
    email.place(x=79,y=127.20)

    pwd=Entry(paypal_screen,text='',font=('Times',13),bd=3,fg='royalblue',show='*')
    pwd.insert(0, 'password ...')
    pwd.bind('<FocusIn>', on_entry_click_pass)
    pwd.place(x=79,y=167.20)

    img4 = Image.open("login2.png")
    img5=img1.resize((100,40),Image.ANTIALIAS)
    img6=ImageTk.PhotoImage(img4)
    Button(paypal_screen,text='',image=img6,command=paidletter).place(x=88,y=207)
    paypal_screen.mainloop()

    
def paymentlettercheck():
    if(len(m2.get())!=16 or len(csv2.get())!=3 ):
        response=messagebox.askokcancel(title='Error',message="""Error!
Please Ensure that no field is left empty!
Please Ensure that the CARD NUMBER is 16-digits and CSV is 3-digits
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if(response==True):
            print("",end="")

        if(response==False):
            payletter_screen.destroy()
            letter()
    else:
        paidletter()
    
def paidletter():
    sql="""INSERT INTO lETTER(SENDERS_NAME,
    SENDERS_CONTACT,
    SENDERS_ADD,
    RECEIVERS_NAME,
    RECEIVERS_ADDRESS,
    RECEIVERS_CONTACT,
    AMOUNT) VALUES(%s,%s,%s,%s,%s,%s,%s)"""

    val=(lsname1,lsno1,lsadd1,lrname1,lradd1,lno1,200)
    mycursor.execute(sql,val)
    demo.commit()
    response=messagebox.askokcancel(title='PAYMENT SUCCESFUL!!',message="""Payment Succesful
We are happy to serve you.
Press OK to use our service again
Press Cancel to Exit.
""")
    if(response==True):
        payletter_screen.destroy()
        courier()
    else:
        payletter_screen.destroy()

    

#-------------------------------------------------Designing window for order-----------------------------------------------------------------#


def order():
    global order_screen,nameo,placeo,addresso,numbero,amounto
    order_screen=Tk()
    order_screen.configure(background="deepskyblue")
    order_screen.state('zoomed')
    order_screen.title('Order')
    order_screen.configure(background='deepskyblue')
    name1=place1=address1=number1=StringVar()
    
    Label(order_screen,text="SPEKTREN COURIERS",bg="gold",fg="red",font=("Times", 30)).pack()
    Label(order_screen,text="RECIPIENT DETAILS",bg="lightblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack()
    Label(order_screen,text='',bg='deepskyblue').pack()
    
    Label(order_screen,text='Name:',font=("Times",8),bg='deepskyblue').pack()
    nameo=Entry(order_screen,font=("Times",8))
    nameo.pack()
    Label(order_screen,text='',bg='deepskyblue').pack()
    
    Label(order_screen,text='City/Town:',font=("Times",8),bg='deepskyblue').pack()
    placeo=Entry(order_screen,font=("Times",8))
    placeo.pack()
    Label(order_screen,text='',bg='deepskyblue').pack()
    
    Label(order_screen,text='Address:',font=("Times",8),bg='deepskyblue').pack()
    addresso=Entry(order_screen,font=("Times",8))
    addresso.pack()
    Label(order_screen,text='',bg='deepskyblue').pack()
    
    Label(order_screen,text='Contact Number:',font=("Times",8),bg='deepskyblue').pack()
    numbero=Entry(order_screen,font=("Times",8))
    numbero.pack()
    Label(order_screen,text='',bg='deepskyblue').pack()
    
    Label(order_screen,text='Amount:',font=("Times",8),bg='deepskyblue').pack()
    amounto=Entry(order_screen,font=("Times",8))
    amounto.pack()
    
    Label(order_screen,text='',bg='deepskyblue').pack()
    Label(order_screen,text='',bg='deepskyblue').pack()
    
    img1 = Image.open("submit.png")
    img2=img1.resize((140,100),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    Button(order_screen,text='',image=img3,command=order_check,relief=GROOVE).pack(side=TOP)
    order_screen.mainloop()
    
def payorder():
    global payo_screen
    global t,m1,csv1
    payo_screen=Tk()
    payo_screen.title('payment')
    payo_screen.state('zoomed')
    payo_screen.configure(background="deepskyblue")
    Label(payo_screen,text="SPEKTREN COURIERS",bg="black",fg="white",font=("Times", 30)).pack()
    Label(payo_screen,text='PAYMENT',bg="lightblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack(side=TOP)
    Label(payo_screen,text='',bd='deepskyblue').pack()

    img1 = Image.open("cc.png")
    img2=img1.resize((380,380),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    Label(payo_screen,text='',image=img3).pack()

    b1=Image.open("paypal logo.png")
    b2=b1.resize((140,21),Image.ANTIALIAS)
    b3=ImageTk.PhotoImage(b2)
    Button(payo_screen,text='',command=paypal,image=b3).place(x=440,y=146)

    options=['Mastercard Debit Cards','Visa Debit Cards','RuPay Debit Cards','Maestro Debit Cards']
    t=StringVar(payo_screen)
    t.set("    SELECT        ")
    w = OptionMenu(payo_screen, t, *options)
    w.place(x=457,y=255.2)

    m1=Entry(payo_screen,font=("Times",10),bd=5)
    m1.place(x=457,y=300)

    months=[' 01 ', ' 02 ',' 03 ',' 04 ',' 05 ',' 06 ',' 07 ',' 08 ',' 09 ', '10', '11', '12']
    mm=StringVar(payo_screen)
    mm.set("mm")
    w1=OptionMenu(payo_screen, mm, *months)
    w1.place(x=427,y=350)
    
    years=[2020,2021,2020,2023,2024,2025,2026,2027,2028,2029]
    yy=StringVar(payo_screen)
    yy.set("yy")
    w2=OptionMenu(payo_screen, yy, *years)
    w2.place(x=497.5,y=350)

    csv1=Entry(payo_screen,font=("Times",10),bd=5)
    csv1.place(x=457,y=384)
    
    z1=Image.open("pay.png")
    z2=z1.resize((100,30),Image.ANTIALIAS)
    z3=ImageTk.PhotoImage(z2)
    Button(payo_screen,text='',command=paymentordercheck,image=z3).place(x=457,y=424)
    payo_screen.mainloop()

def paymentordercheck():
    if(len(m1.get())!=16 or len(csv1.get())!=3 ):
        response=messagebox.askokcancel(title='Error',message="""Error!
Please Ensure that no field is left empty!
Please Ensure that the CARD NUMBER is 16-digits and CSV is 3-digits
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if(response==True):
            print("",end="")

        if(response==False):
            payo_screen.destroy()
            order()

    else:
        paidorder()

def paidorder():
    sql="INSERT INTO MONEY_ORDER(RECEIVERS_NAME,RECEIVERS_CITYORTOWN,RECEIVERS_ADDRESS,RECEIVERS_CONTACT,AMOUNT) VALUES(%s,%s,%s,%s,%s)"
    val=(rnameo,rplaceo,raddresso,rnumbero,ramounto)
    mycursor.execute(sql,val)
    demo.commit()
    response=messagebox.askokcancel(title='PAYMENT SUCCESFUL!!',message="""Payment Succesful
We are happy to serve you.
Press OK to use our service again
Press Cancel to Exit.
""")
    if(response==True):
        payo_screen.destroy()
        courier()
    if(response==False):
        payo_screen.destroy()
    
    

def paypal():
    global email,pwd
    global firstclick
    global secondclick
    firstclick=True
    secondclick=True
    payo_screen.destroy()
    paypal_screen=Tk()
    paypal_screen.configure(background="deepskyblue")
    paypal_screen.title('payment')
    paypal_screen.geometry('350x350')
    img1 = Image.open("paypal logo.png")
    img2=img1.resize((120,130),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    
    Label(paypal_screen,text='',image=img3,bg='deepskyblue').pack()
    email=Entry(paypal_screen,text='',font=('Times',13),bd=3,fg='royalblue')
    email.insert(0, 'Enter your email...')
    email.bind('<FocusIn>', on_entry_click)
    email.place(x=79,y=127.20)

    pwd=Entry(paypal_screen,text='',font=('Times',13),bd=3,fg='royalblue',show='*')
    pwd.insert(0, 'password ...')
    pwd.bind('<FocusIn>', on_entry_click_pass)
    pwd.place(x=79,y=167.20)

    img4 = Image.open("login2.png")
    img5=img1.resize((100,40),Image.ANTIALIAS)
    img6=ImageTk.PhotoImage(img4)
    Button(paypal_screen,text='',image=img6,command=paidorder).place(x=88,y=207)
    paypal_screen.mainloop()

def invoice_order():
    print()
    

#-------------------------------------------------Designing window for parcel-----------------------------------------------------------------#
 
def parcel():
    global parcel_screen,psname,psno,psadd,prname,pradd,prno,weight,p
    parcel_screen=Tk()
    parcel_screen.title('Parcel')
    parcel_screen.state('zoomed')
    parcel_screen.configure(background="deepskyblue")
    Label(parcel_screen,text="SPEKTREN COURIERS",bg="gold",fg="red",font=("Times", 30)).pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="SENDER'S DETAILS",bg="dodgerblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="Sender's Name:",font=("Times",10),bg='deepskyblue').pack()
    psname=Entry(parcel_screen,font=("Times",10))
    psname.pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="Sender's Contact number:",font=("Times",10),bg='deepskyblue').pack()
    psno=Entry(parcel_screen,font=("Times",10))
    psno.pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="Sender's Address:",font=("Times",10),bg='deepskyblue').pack()
    psadd=Entry(parcel_screen,font=("Times",10))
    psadd.pack()
    
    Label(parcel_screen,text='',bg='deepskyblue').pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()


    Label(parcel_screen,text="RECEIVER'S DETAILS",bg="dodgerblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="Receiver's Name:",font=("Times",10),bg='deepskyblue').pack()
    prname=Entry(parcel_screen,font=("Times",10))
    prname.pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="Receiver's Contact number:",font=("Times",10),bg='deepskyblue').pack()
    prno=Entry(parcel_screen,font=("Times",10))
    prno.pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="Receiver's Address:",font=("Times",10),bg='deepskyblue').pack()
    pradd=Entry(parcel_screen,font=("Times",10))
    pradd.pack()
    Label(parcel_screen,text='',bg='deepskyblue').pack()

    Label(parcel_screen,text="Enter the weight of the parcel in kg:",font=("Times",10),bg='deepskyblue').pack()
    weight=Entry(parcel_screen,font=("Times",10))
    weight.pack()

    def onclick(event=None):
        parcel_check()
    
    img1 = Image.open("submit.png")
    img2=img1.resize((140,100),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    parcel_screen.bind('<Return>', onclick)
    Button(parcel_screen,text='',image=img3,command=onclick).pack(side=TOP)
    
    parcel_screen.mainloop()

def payparcel():
    global payparcel_screen
    global j,m5,csv5
    payparcel_screen=Tk()
    payparcel_screen.title('Payment')
    payparcel_screen.state('zoomed')
    payparcel_screen.configure(background="deepskyblue")
    Label(payparcel_screen,text="SPEKTREN COURIERS",bg="black",fg="white",font=("Times", 30)).pack()
    Label(payparcel_screen,text='PAYMENT',bg="lightblue",relief="ridge",fg="white",font=("Times", 12),justify=LEFT).pack(side=TOP)
    Label(payparcel_screen,text='',bg='deepskyblue').pack()

    img1 = Image.open("cc.png")
    img2=img1.resize((380,380),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    Label(payparcel_screen,text='',image=img3).pack()

    b1=Image.open("paypal logo.png")
    b2=b1.resize((140,21),Image.ANTIALIAS)
    b3=ImageTk.PhotoImage(b2)
    Button(payparcel_screen,text='',command=paypalparcel,image=b3).place(x=440,y=146)

    options=['Mastercard Debit Cards','Visa Debit Cards','RuPay Debit Cards','Maestro Debit Cards']
    j=StringVar(payparcel_screen)
    j.set("    SELECT        ")
    w = OptionMenu(payparcel_screen, j, *options)
    w.place(x=457,y=255.2)

    m5=Entry(payparcel_screen,font=("Times",10),bd=5)
    m5.place(x=457,y=300)

    months=[' 01 ', ' 02 ',' 03 ',' 04 ',' 05 ',' 06 ',' 07 ',' 08 ',' 09 ', '10', '11', '12']
    mm=StringVar(payparcel_screen)
    mm.set("mm")
    w1=OptionMenu(payparcel_screen, mm, *months)
    w1.place(x=427,y=350)
    
    years=[2020,2021,2020,2023,2024,2025,2026,2027,2028,2029]
    yy=StringVar(payparcel_screen)
    yy.set("yy")
    w2=OptionMenu(payparcel_screen, yy, *years)
    w2.place(x=497.5,y=350)

    csv5=Entry(payparcel_screen,font=("Times",10),bd=5)
    csv5.place(x=457,y=384)
    
    z1=Image.open("pay.png")
    z2=z1.resize((100,30),Image.ANTIALIAS)
    z3=ImageTk.PhotoImage(z2)
    Button(payparcel_screen,text='',command=paymentparcelcheck,image=z3).place(x=457,y=424)
    payparcel_screen.mainloop()

def paymentparcelcheck():
    if(len(m5.get())!=16 or len(csv5.get())!=3 ):
        response=messagebox.askokcancel(title='Error',message="""Error!
Please Ensure that no field is left empty!
Please Ensure that the CARD NUMBER is 16-digits and CSV is 3-digits
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if(response==True):
            print("",end="")

        if(response==False):
            payparcel_screen.destroy()
            parcel()

    else:
        paidparcel()
    
    
def paypalparcel():
    global email,pwd
    global firstclick
    global secondclick
    firstclick=True
    secondclick=True
    payparcel_screen.destroy()
    paypalparcel_screen=Tk()
    paypalparcel_screen.geometry('350x350')
    payparcel_screen.configure(background="deepskyblue")
    paypalparcel_screen.title('Payment')
    img1 = Image.open("paypal logo.png")
    img2=img1.resize((120,130),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    
    Label(paypalparcel_screen,text='',image=img3).pack()
    email=Entry(paypalparcel_screen,text='',font=('Times',13),bd=3,fg='royalblue')
    email.insert(0, 'Enter your email...')
    email.bind('<FocusIn>', on_entry_click)
    email.place(x=79,y=127.20)

    pwd=Entry(paypalparcel_screen,text='',font=('Times',13),bd=3,fg='royalblue',show='*')
    pwd.insert(0, 'password ...')
    pwd.bind('<FocusIn>', on_entry_click_pass)
    pwd.place(x=79,y=167.20)

    img4 = Image.open("login2.png")
    img5=img1.resize((100,40),Image.ANTIALIAS)
    img6=ImageTk.PhotoImage(img4)
    Button(paypalparcel_screen,text='',image=img6,command=paidparcel).place(x=88,y=207)
    paypalparcel_screen.mainloop()

def paidparcel():
    
    sql="""INSERT INTO PARCEL(SENDERS_NAME,
    SENDERS_CONTACT,
    SENDERS_ADD,
    RECEIVERS_NAME,
    RECEIVERS_CONTACT,
    RECEIVERS_ADDRESS,
    WEIGHT,
    AMOUNT) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"""
    val=(psname1,psno1,psadd1,prname1,prno1,pradd1,x1,p)
    mycursor.execute(sql,val)
    demo.commit()
    response=messagebox.askokcancel(title='PAYMENT SUCCESFUL!!',message="""Payment Succesful
We are happy to serve you.
Press OK to use our service again
Press Cancel to Exit.
""")
    if(response==True):
        payparcel_screen.destroy()
        courier()
    if(response==False):
        payparcel_screen.destroy()

def on_entry_click_pass(event):
    global secondclick
    if secondclick: 
        secondclick = False
        pwd.delete(0, "end")

        
def on_entry_click(event):
    global firstclick

    if firstclick:
        firstclick = False
        email.delete(0, "end")

def invoice_parcel():
    print()

#-------------------------------------------------Designing window for error related issue---------------------------------------------------#
def password_not_recognised():
    response=messagebox.askretrycancel(title='Invalid password',message='Invalid password!Try again')
    if(response==True):
        login_screen.destroy()
        login()
    else:
        login_screen.destroy()
        main_screen.destroy()
 

 
def user_not_found():
    response=messagebox.askretrycancel(title='Invalid Username',message='Invalid username!Try again')
    if(response==True):
        login_screen.destroy()
        login()
    else:
        login_screen.destroy()
        main_screen.destroy()
    
def delete_paymentt_screen():
    payo_screen.destroy()
    paypal()
def delete_registration_success():
    register_screen.destroy()
    main_screen.destroy()
    courier()
 
def delete_login_success():
    login_screen.destroy()
    main_screen.destroy()
    courier()
def delete_parcel_data():
    global psname1,psno1,psadd1,prname1,pradd1,weight1,p,prno1,x1
    psname1=psname.get()
    psno1=psno.get()
    psadd1=psadd.get()
    prname1=prname.get()
    pradd1=pradd.get()
    weight1=weight.get()
    prno1=prno.get()
    x1=weight.get()
    y=int(x1)
    p=100
    if (y<5):
        p+=1000*y
    elif(y>5 and y<=10):
        p+=1500*y
    elif(y>10 and y<=30):
        p+=2000*y    
    parcel_screen.destroy()
    payparcel()

def delete_order_data():
    global rnameo,rplaceo,raddresso,rnumbero,ramounto
    rnameo=nameo.get()
    rplaceo=placeo.get()
    raddresso=addresso.get()
    rnumbero=numbero.get()
    ramounto=amounto.get()

    
    order_screen.destroy()
    payorder()
def delete_letter_data():
    global lsname1,lsno1,lsadd1,lrname1,lradd1,lno1
    lsname1=lsname.get()
    lsno1=lsno.get()
    lsadd1=lsadd.get()
    lrname1=lrname.get()
    lradd1=lradd.get()
    lno1=lrno.get()
    
    letter_screen.destroy()
    payletter()
def delete_password_not_recognised():
    password_not_recog_screen.destroy()
 
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()

def register_check():
    if(len(username_entry.get())==0):
        response=messagebox.askokcancel(title='Error',message='Username cannot be empty')
        if True:
            register_screen.destroy()
            register()
        elif response==False:
            register_screen.destroy()
            main_screen.destroy()

    elif(username_entry.get().isspace()==True):
        response=messagebox.askokcancel(title='Error',message='Invalid Username!')
        if True:
            register_screen.destroy()
            register()
        else:
            register_screen.destroy()
            main_screen.destroy()
    elif(len(password_entry.get())==0):
        response=messagebox.askokcancel(title='Error',message='Password cannot be empty')
        if True:
            register_screen.destroy()
            register()
        else:
            register_screen.destroy()
    elif(len(password_entry.get()) not in(8,9,10,11,12,13,14,15,16)):
        response=messagebox.askokcancel(title='Error',message="""Invalid!
MIN:8
MAX:16""")
        if True:
            register_screen.destroy()
            register()
        else:
            register_screen.destroy()
        
    else:
        register_user()

def letter_check():
    if(len(lsname.get())==0 or len(lsno.get())==0 or len(lsadd.get())==0 or len(lrname.get())==0 or len(lrno.get())==0 or len(lradd.get())==0):
        response=messagebox.askokcancel(title='Error',message="""Error!
Please Ensure that no field is left empty!
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if response==True:
            print('',end='')
        if response==False:
            letter_screen.destroy()
            courier()
    elif((lsno.get().isdigit()==False or lrno.get().isdigit()==False) and len(lsno.get())!=10 and len(lrno.get())!=10):
        response=messagebox.askokcancel(title='Error',message="""Error!
Invalid Phone number!
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if response==True:
            print('',end='')
        if response==False:
            letter_screen.destroy()
            courier()
    else:
        delete_letter_data()


def order_check():
    if(len(nameo.get())==0 or len(placeo.get())==0 or len(addresso.get())==0 or len(numbero.get())==0 or len(amounto.get())==0):
        response=messagebox.askokcancel(title='Error',message="""Error!
Please Ensure that no field is left empty!
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if response==True:
            print('',end='')
        if response==False:
            order_screen.destroy()
            courier()
    elif(numbero.get().isdigit()==False or amounto.get().isdigit()==False):
        response=messagebox.askokcancel(title='Error',message="""Error!
Invalid Phone number/Amount!
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if response==True:
            print('',end='')
        if response==False:
            order_screen.destroy()
            courier()
    else:
        delete_order_data()

def parcel_check():
    if(len(psname.get())==0 or len(psno.get())==0 or
       len(psadd.get())==0 or len(prname.get())==0 or len(pradd.get())==0 or len(prno.get())==0 or len(weight.get())==0):
        response=messagebox.askokcancel(title='Error',message="""Error!
Please Ensure that no field is left empty!
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if response==True:
            print('',end='')
        if response==False:
            parcel_screen.destroy()
            courier()
            
    elif(prno.get().isdigit()==False or weight.get().isdigit()==False or psno.get().isdigit()==False):
        response=messagebox.askokcancel(title='Error',message="""Error!
Invalid Phone number/Weight!
Press OK to correct the details
Press Cancel to go back to previous window.""")
        if response==True:
            print('',end='')
        if response==False:
            parcel_screen.destroy()
            courier()
    else:
        delete_parcel_data()

def courier_destroy_main():
    courier_screen.destroy()
    main_account_screen()
def delete_main():
    main_screen.destroy()
    
#-------------------------------------------------Designing main window----------------------------------------------------------------------#
   
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("400x400")
    main_screen.configure(background="deepskyblue")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", background="black", foreground="white",width="300", height="3", font=("Calibri", 15)).pack()
    Label(text="",background="deepskyblue").pack()
    
    img1 = Image.open("1111.png")
    img2=img1.resize((120,100),Image.ANTIALIAS)
    img3=ImageTk.PhotoImage(img2)
    panel=Label(main_screen,image=img3)
    panel.pack(side = "top")
    Label(text="",bg="deepskyblue").pack()
    
    
    b1=Button(text="Login", height="2", width="30", activebackground="red",command = login,bg='orange').pack()
    Label(text="",background="deepskyblue").pack()
    b2=Button(text="Register", height="2", width="30",activebackground="red",command=register,bg='orange').pack()
    Label(text="",background='deepskyblue').pack()
    b3=Button(text="GIVE FEEDBACK",height="2",width="30",activebackground="red",command=feed,bg='orange').pack()
    main_screen.mainloop()

main_account_screen()
#courier()
#order()
