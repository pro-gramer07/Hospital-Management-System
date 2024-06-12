from tkinter import *
import mysql
from mysql import connector
import bcrypt
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.messagebox import askyesno


def isfloat(n):
    try:
        float(n)
        return True
    except ValueError:
        return False



db = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='admin',
    port=3306,
    database='hospital'
)
cur = db.cursor()
global appid
#******************************************** LOGIN ***********************************************************************************

def login():
    def register_page():
        loginwindow.destroy()
        register()

    def admin_dash(username):
        loginwindow.destroy()
        admin(username)

    def doctor_dash(username):
        loginwindow.destroy()
        doctor(username)

    def patient_dash(username):
        loginwindow.destroy()
        patient(username)

    def reset_password():
        loginwindow.destroy()
        reset()

    def hide():
        closeeye.config(file = 'close.png')
        passwordEntry.config(show = '*')
        eyeButton.config(command = show)

    def show():
        closeeye.config(file = 'open.png')
        passwordEntry.config(show = '')
        eyeButton.config(command = hide)

    def finish():
        if(askyesno("exit", "are you sure you want to exit?")):
            loginwindow.destroy()

    def validate():
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )

        cur = db.cursor()
        entered_username = usernameEntry.get()
        entered_password = passwordEntry.get()

        # Execute SQL query to fetch the usernames from the database
        cur.execute("SELECT username FROM users")
        usernames = cur.fetchall()  # Fetch all usernames from the database


        # Check if the entered username exists in the database
        if (entered_username,) in usernames:
            cur.execute("SELECT password_hash FROM users WHERE username = %s", (entered_username,))
            password_hash = cur.fetchone()
            cur.execute("SELECT user_type FROM users WHERE username = %s", (entered_username,))
            user_type = cur.fetchone()
            password_hash = password_hash[0]
            entered_password_hashed = bcrypt.hashpw(entered_password.encode('utf-8'),
                                                    password_hash.encode('utf-8'))

            # Compare the hashes
            if entered_password_hashed == password_hash.encode('utf-8'):
                # messagebox.showinfo("Login successful")
                if (user_type[0]) == 'Admin':
                    admin_dash(entered_username)
                elif (user_type[0]) == 'Patient':
                    patient_dash(entered_username)
                elif (user_type[0]) == 'Doctor':
                    doctor_dash(entered_username)
                # elif (user_type[0]) == 'Nurse':
                #     messagebox.showinfo('Nurse', 'Nurse')
                # elif (user_type[0]) == 'Staff':
                #     messagebox.showinfo('Staff')
            else:
                messagebox.showerror("Error", "Incorrect password")
        else:
            messagebox.showerror("Error", "Invalid username")
        db.close()


    def user_enter(event):
        if usernameEntry.get() == "Username":
            usernameEntry.delete(0, END)

    def password_enter(event):
        if passwordEntry.get() == "Password":
            passwordEntry.delete(0, END)



    loginwindow = Tk()
    loginwindow.geometry('1280x650+0+0')
    # loginwindow.resizable(False)

    bgImage = ImageTk.PhotoImage(file='bg.jpg')
    bglbl = Label(loginwindow, image=bgImage).pack()
    frame = tk.Frame(loginwindow, bg="white", width=345, height=350)
    frame.place(relx=0.48, rely=0.64, anchor=tk.CENTER)  # Place at the center, adjust dimensions as needed

    heading = Label(loginwindow, text='LOGIN', font=('times new roman', 28, 'bold'), bg='white', fg='blue').place(x=550, y=168)
    heading = Label(loginwindow, text='Hospital Management System', font=('times new roman', 28, 'bold'), bg='white', fg='blue').place(x=480, y=18)

    usernameEntry = Entry(loginwindow, width=25, font=('times new roman', 18, 'bold'),bd=1, bg='white', fg='blue')
    usernameEntry.place(x=471,y=280)
    usernameEntry.insert(0, "Username")
    usernameEntry.bind('<FocusIn>', user_enter)

    # Frame(loginwindow, width=302, height=2, bg='blue').place(x=471, y=330)

    passwordEntry = Entry(loginwindow, width=25, font=('times new roman', 18, 'bold'),bd=1, bg='white', fg='blue')
    passwordEntry.place(x=471,y=350)
    passwordEntry.insert(0, "Password")
    passwordEntry.bind('<FocusIn>', password_enter)

    # Frame(loginwindow, width=302, height=2, bg='blue').place(x=471, y=430)

    closeeye = PhotoImage(file='close.png')
    openeye = PhotoImage(file='open.png')

    eyeButton = Button(loginwindow, image=closeeye, bd=0, bg='white', activebackground='white', cursor='hand2', command=hide)
    eyeButton.place(x=730, y=353)


    loginButton = Button(loginwindow, text='Login', font=('times new roman', 18, 'bold'), fg='white', bg='blue', width=21, command=validate).place(x=471, y=450)


    exitButton = Button(loginwindow, text='Exit', font=('times new roman', 12, 'bold'), fg='white', bg='blue', width=12, command=finish).place(x=1100, y=31)


    Label(text="Don't have an account?",font=('times new roman', 14, 'bold') ,bd= 0, fg='blue' , bg = 'white').place(x=471, y=505)
    # Button(text="Register")

    newAccountButton = Button(loginwindow, text='Register', font=('times new roman', 14, 'bold underline'), bd= 0, fg='blue' , bg = 'white',  activeforeground= "blue", activebackground= "white", cursor = 'hand2', command=register_page).place(x=680, y=500)

    #forg9ot password
    forgotButton = Button(loginwindow, text='Forgot Password?', font=('times new roman', 14, 'bold underline'), bd= 0, fg='blue' , bg = 'white',  activeforeground= "blue", activebackground= "white", cursor = 'hand2', command=reset_password)
    forgotButton.place(x=620, y=400)

    loginwindow.mainloop()



#******************************************** RESET ***********************************************************************************
def reset():
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )

    def cancel():
        resetwindow.destroy()
        login()
    def change_password():
        if usernameEntry.get() == "" or newpasswordEntry.get() == "" or confirmpasswordEntry.get() == "":
            messagebox.showerror("Error", "All fields are required", parent=resetwindow)
        elif newpasswordEntry.get() != confirmpasswordEntry.get():
            messagebox.showerror("Error", "Password and confirm password are not matching", parent=resetwindow)
        else:
            newpassword = newpasswordEntry.get()
            entered_username = usernameEntry.get()
            cur = db.cursor()
            cur.execute("SELECT username FROM users")
            usernames = cur.fetchall()  # Fetch all usernames from the database
            if (entered_username,) not in usernames:
                messagebox.showerror("Error", "Username does not exist", parent=resetwindow)
            else:
                cur.execute("SELECT password_hash FROM users WHERE username = %s", (entered_username,))
                password_hash = cur.fetchone()
                password_hash = password_hash[0]
                newpassword_hashed = bcrypt.hashpw(newpassword.encode('utf-8'),
                                                        password_hash.encode('utf-8'))

                # Compare the hashes
                if newpassword_hashed == password_hash.encode('utf-8'):
                    messagebox.showerror("Error", "new password and old password cannot be same", parent=resetwindow)
                else:
                    cur.execute("UPDATE users SET password_hash = %s WHERE username = %s",
                                (newpassword_hashed, usernameEntry.get()))
                    db.commit()
                    messagebox.showinfo("Success", "Password has been changed successfully", parent=resetwindow)
                    resetwindow.destroy()
                    login()


    resetwindow = Tk()
    resetwindow.geometry('1280x650+0+0')
    resetwindow.title("SignUp Page")
    resetwindow.resizable(False, False)

    # dummy bg.jpg
    bgImage = ImageTk.PhotoImage(file='bg.jpg')
    bglbl = Label(resetwindow, image=bgImage).pack()

    # creating a frame
    frame = tk.Frame(resetwindow, bg="white", width=345, height=350)
    frame.place(relx=0.48, rely=0.64, anchor=tk.CENTER)  # Place at the center, adjust dimensions as needed

    heading = Label(resetwindow, text='Reset Password', font=('times new roman', 20, 'bold'), bg='white',
                    fg='blue').place(x=550, y=175)

    # username label
    usernameLabel = Label(frame, text="Username", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    usernameLabel.grid(row=0, column=0, sticky='w', padx=25, pady=(10, 0))

    # #username entry
    usernameEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    usernameEntry.grid(row=1, column=0, sticky='w', padx=25)

    # passwordname label
    newpasswordLabel = Label(frame, text="Password", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                             fg='blue')
    newpasswordLabel.grid(row=2, column=0, sticky='w', padx=25, pady=(10, 0))

    # username entry
    newpasswordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    newpasswordEntry.grid(row=3, column=0, sticky='w', padx=25)

    # confirm password label
    confirmpasswordLabel = Label(frame, text="Confirm Password", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                 bg='white', fg='blue')
    confirmpasswordLabel.grid(row=4, column=0, sticky='w', padx=25, pady=(10, 0))

    # confirm password entry
    confirmpasswordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    confirmpasswordEntry.grid(row=5, column=0, sticky='w', padx=25)


    emptyLabel2 = Label(frame, text="", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    emptyLabel2.grid(row=6, column=0, sticky='w', padx=25, pady=(10, 0))

    # submit button
    submitButton = Button(frame, text="Submit", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                          activebackground="blue", activeforeground="white", command=change_password, width=23)
    submitButton.grid(row=7, column=0, sticky='w', padx=25, pady=10)

    # submit button
    cancelButton = Button(frame, text="Cancel", font=('Open Sans', 16, 'bold'), fg='blue', bg='lightgray', bd=0,
                          activebackground="blue", activeforeground="white", command=cancel, width=23)
    cancelButton.grid(row=8, column=0, sticky='w', padx=25, pady=10)

    # empty label
    emptyLabel2 = Label(frame, text="", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    emptyLabel2.grid(row=9, column=0, sticky='w', padx=25, pady=(10, 0))

    resetwindow.mainloop()



#******************************************** REGISTER ***********************************************************************************



def register():
    def login_page():
        registerwindow.destroy()
        login()


    def details_page():
        registerwindow.destroy()
        details()

    def regValidate():
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )

        cur = db.cursor()
        global entered_username
        entered_username = usernameEntry.get()
        global entered_password
        entered_password = passwordEntry.get()
        global entered_email
        entered_email = emailEntry.get()
        global confirmPassword
        confirmPassword = confirmPasswordEntry.get()
        cur.execute("SELECT username FROM users")
        usernames = cur.fetchall()  # Fetch all usernames from the database
        cur.execute("SELECT email FROM users")
        emails = cur.fetchall()  # Fetch all usernames from the database
        if not entered_username or not entered_password or not confirmPassword or not entered_email:
            messagebox.showerror("Error", "Please fill in all fields.")
        elif entered_email in [email[0] for email in emails]:
            messagebox.showerror("Error", "Email already exists.")
        elif entered_username in [user[0] for user in usernames]:
            messagebox.showerror("Error", "Username already exists.")
        elif "@" not in entered_email:
            messagebox.showerror("Error", "Please enter a valid email address.")
        elif len(entered_username)<6:
            messagebox.showerror("Error", "Password should not be less than 6 characters")
        elif entered_password != confirmPassword:
            messagebox.showerror("Error", "Passwords do not match.")
        elif len(entered_password)<6:
            messagebox.showerror("Error", "Password should not be less than 6 characters")
        else:
            messagebox.showinfo('Verified', 'Your information has been verified!')
            details_page()

    registerwindow = Tk()
    registerwindow.geometry('1280x650+0+0')
    registerwindow.title("SignUp Page")
    registerwindow.resizable(False, False)

    # dummy bg.jpg
    bgImage = ImageTk.PhotoImage(file='bg.jpg')
    bglbl = Label(registerwindow, image=bgImage).pack()

    #creating a frame
    frame = tk.Frame(registerwindow, bg="white", width=345, height=350)
    frame.place(relx=0.48, rely=0.64, anchor=tk.CENTER)# Place at the center, adjust dimensions as needed

    heading = Label(registerwindow, text='Register', font=('times new roman', 28, 'bold'), bg='white', fg='blue').place(x=550, y=168)

    #email label
    emailLabel = Label(frame, text="Email", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    emailLabel.grid(row=1, column=0, sticky= 'w',padx = 25, pady=(10,0))

    #email entry
    emailEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    emailEntry.grid(row=2, column=0, sticky='w', padx=25)

    #username label
    usernameLabel = Label(frame, text="Username", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    usernameLabel.grid(row=3, column=0, sticky= 'w',padx = 25, pady=(10,0))

    #username entry
    usernameEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    usernameEntry.grid(row=4, column=0, sticky='w', padx=25)

    #password label
    passwordLabel = Label(frame, text="Password", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    passwordLabel.grid(row=5, column=0, sticky= 'w',padx = 25, pady=(10,0))

    #password entry
    passwordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    passwordEntry.grid(row=6, column=0, sticky='w', padx=25)

    #confirm password label
    confirmPasswordLabel = Label(frame, text="Confirm Password", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    confirmPasswordLabel.grid(row=7, column=0, sticky= 'w',padx = 25, pady=(10,0))

    #confirm password entry
    confirmPasswordEntry = Entry(frame, width=30, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    confirmPasswordEntry.grid(row=8, column=0, sticky='w', padx=25)


    #signup button
    signupButton = Button(frame, text="Signup", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0, activebackground="blue", activeforeground="white", width = 23, command=regValidate)
    signupButton.grid(row=9, column=0, pady = 15)

    # don't have an account label
    alreadyaccount = Label(frame, text="Already have an account?", font=('Open Sans', 12, 'bold'), bg='white', fg='blue')
    alreadyaccount.grid(row=10, column=0, sticky= 'w',padx = 25)

    #login button
    loginButton = Button(frame, text="Login", font=('Open Sans', 12, 'bold underline'), bg='white', fg='blue', width=7, bd=0, activebackground="white", activeforeground="blue", cursor= 'hand2', command = login_page)
    loginButton.grid(row=10, column=0, sticky= 'e',padx = 25)

    registerwindow.mainloop()


def storeUser():
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
    cur = db.cursor()
    dob = f'{year}-{month}-{date}'

    password_hash = bcrypt.hashpw(entered_password.encode('utf-8'), bcrypt.gensalt())
    password_hashed = password_hash.decode('utf-8')

    cur.execute(f"""INSERT INTO users (username, password_hash, user_type, first_name, last_name, gender, contact, email, house_number, street, sector, city, date_of_birth)
                       VALUES ('{entered_username}', '{password_hashed}', 'Patient', '{first_name}', '{last_name}', '{gender}', '{phone}', '{entered_email}',
                 '{house}', '{street}', '{sector}', '{city}', '{dob}')
            """)
    db.commit()

    cur.execute(f"""INSERT INTO Patient (pusername, blood_group, height, weight, pstatus) 
                       VALUES ('{entered_username}','{bgroup}', '{height}', '{weight}', 'Registered')
            """)
    db.commit()





def details():
    def details_next_page():
        detailswindow.destroy()
        detailsNext()

    def login_page():
        detailswindow.destroy()
        login()

    def detailValidate():
        global first_name
        first_name = firstNameEntry.get()
        global last_name
        last_name = lastnameEntry.get()
        global gender
        gender = genderVar.get()
        global phone
        phone = phoneNumberEntry.get()
        global height
        height = heightEntry.get()
        global weight
        weight = weightEntry.get()
        global bgroup
        bgroup = bgroupVar.get()

        if(first_name and last_name):
            if (phone.isdigit() and len(phone)==10):
                if(isfloat(height)):
                    if(isfloat(weight)):
                        details_next_page()
                    else:
                        messagebox.showerror("Error", "Weight should be in digits")
                else:
                    messagebox.showerror("Error", "Height should be in digits")
            else:
                messagebox.showerror("Error", "invalid phone number")
        else:
            messagebox.showerror("Error", "All fields are mandatory")

    detailswindow = Tk()
    detailswindow.geometry('1280x650+0+0')
    detailswindow.title("Details Page")
    detailswindow.resizable(False, False)

    # dummy bg.jpg
    bgImage = ImageTk.PhotoImage(file='bg.jpg')
    bglbl = Label(detailswindow, image=bgImage).pack()

    #creating a frame
    frame = tk.Frame(detailswindow, bg="white", width=345, height=350)
    frame.place(relx=0.48, rely=0.64, anchor=tk.CENTER)# Place at the center, adjust dimensions as needed

    heading = Label(detailswindow, text='Details', font=('times new roman', 28, 'bold'), bg='white', fg='blue').place(x=550, y=168)

    #first name label
    firstNameLabel = Label(frame, text="First Name", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    firstNameLabel.grid(row=1, column=0, sticky= 'w',padx = 25, pady=(10,0))

    #first name entry
    firstNameEntry = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    firstNameEntry.grid(row=2, column=0, sticky='w', padx=25)

    #lastname label
    lastnameLabel = Label(frame, text="Last Name", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    lastnameLabel.grid(row=1, column=1, sticky= 'w',padx = 5, pady=(10,0))

    #lastname entry
    lastnameEntry = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    lastnameEntry.grid(row=2, column=1, sticky='w', padx=5)

    #gender label
    genderLabel = Label(frame, text="Gender", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    genderLabel.grid(row=3, column=0, sticky= 'w',padx = 25, pady=(10,0))

    #gender entry

    genderVar = tk.StringVar()
    genderVar.set("Male")
    genderEntry = tk.OptionMenu(
        frame, genderVar, "Male", "Female", "Other")

    genderEntry.config(width=14)
    genderEntry.config(bg="blue", fg="white",  activebackground="blue", activeforeground="white")
    genderEntry["menu"].config(bg="blue", fg="white")
    genderEntry.grid(row=4, column=0, sticky='w', padx=22)


    #lastname label
    bgroupLabel = Label(frame, text="Blood Group", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    bgroupLabel.grid(row=3, column=1, sticky= 'w',padx = 5, pady=(10,0))

    #gender entry
    bgroupVar = tk.StringVar()
    bgroupVar.set("B+")
    bgroupEntry = tk.OptionMenu(
        frame, bgroupVar, "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-")

    bgroupEntry.config(width=14)
    bgroupEntry.config(bg="blue", fg="white",  activebackground="blue", activeforeground="white")
    bgroupEntry["menu"].config(bg="blue", fg="white")
    bgroupEntry.grid(row=4, column=1, sticky='w', padx=5)

    #first name label
    heightLabel = Label(frame, text="Height (cm)", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    heightLabel.grid(row=5, column=0, sticky= 'w',padx = 25, pady=(10,0))

    #first name entry
    heightEntry = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    heightEntry.grid(row=6, column=0, sticky='w', padx=25)

    #lastname label
    weightLabel = Label(frame, text="Weight (kg)", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    weightLabel.grid(row=5, column=1, sticky= 'w',padx = 5, pady=(10,0))

    #lastname entry
    weightEntry = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    weightEntry.grid(row=6, column=1, sticky='w', padx=5)

    # confirm Number label
    phoneNumberLabel = Label(frame, text="Contact(+92):", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                             fg='blue')
    phoneNumberLabel.grid(row=7, column=0, sticky='w', padx=25, pady=(10, 0))

    # confirm phoneNumberentry
    phoneNumberEntry = Entry(frame, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    phoneNumberEntry.grid(row=8, column=0, sticky='w', padx=25)



    #signup button
    nextButton = Button(frame, text="Next", font=('Open Sans', 14, 'bold'), fg='white', bg='blue', bd=0, activebackground="blue", activeforeground="white", width = 6, command=detailValidate)
    nextButton.grid(row=9, column=1, sticky='e', pady = 15, padx=25)

    # don't have an account label
    alreadyaccount = Label(frame, text="Already have an account?", font=('Open Sans', 9, 'bold'), bg='white', fg='blue')
    alreadyaccount.grid(row=10, column=0, sticky= 'w',padx = 25)

    #login button
    loginButton = Button(frame, text="Login", font=('Open Sans', 12, 'bold underline'), bg='white', fg='blue', width=7, bd=0, activebackground="white", activeforeground="blue", cursor= 'hand2', command = login_page)
    loginButton.grid(row=10, column=1, sticky= 'e',padx = 25)

    detailswindow.mainloop()





def detailsNext():
    def login_page():
        nextwindow.destroy()
        login()

    def details_next():
        storeUser()
        messagebox.showinfo('Registered', 'Registered Successfully!')
        login_page()



    def addressdetails():
        global house
        house = houseEntry.get()
        global street
        street = streetEntry.get()
        global sector
        sector = sectorEntry.get()
        global city
        city = cityEntry.get()
        global month
        month = monthVar.get()
        global date
        date = dateVar.get()

        global year
        year = yearEntry.get()
        if(house and street and sector and city and year):
            if(year.isdigit()):
                if(int(year) >= 1900 and int(year) <= 2023):
                    details_next()
                else:
                    messagebox.showerror("Error", "invalid year")
            else:
                messagebox.showerror("Error", "year should be in digits")
        else:
            messagebox.showerror("Error", "all fields are mandatory")





    nextwindow = Tk()
    nextwindow.geometry('1280x650+0+0')
    nextwindow.title("Details Page")
    nextwindow.resizable(False, False)

    # dummy bg.jpg
    bgImage = ImageTk.PhotoImage(file='bg.jpg')
    bglbl = Label(nextwindow, image=bgImage).pack()

    # creating a frame
    frameleft = tk.Frame(nextwindow, bg="white", width=345, height=350)
    frameleft.place(relx=0.48, rely=0.63, anchor=tk.CENTER)  # Place at the center, adjust dimensions as needed

    heading = Label(nextwindow, text='Details', font=('times new roman', 28, 'bold'), bg='white', fg='blue').place(
        x=550, y=168)

    # address label
    addressLabel = Label(frameleft, text="Address", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                         fg='blue')
    addressLabel.grid(row=0, column=0, sticky='w', padx=25)

    # House label
    houseLabel = Label(frameleft, text="House No", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    houseLabel.grid(row=2, column=0, sticky='w', padx=25)

    # First name entry
    houseEntry = Entry(frameleft, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    houseEntry.grid(row=3, column=0, sticky='w', padx=25)

    # Street label
    streetLabel = Label(frameleft, text="Street", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    streetLabel.grid(row=2, column=1, sticky='w', padx=5)

    # Street entry
    streetEntry = Entry(frameleft, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    streetEntry.grid(row=3, column=1, sticky='w', padx=5)

    # sector label
    sectorLabel = Label(frameleft, text="Sector/Area", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                        fg='blue')
    sectorLabel.grid(row=4, column=0, sticky='w', padx=25)

    # First name entry
    sectorEntry = Entry(frameleft, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    sectorEntry.grid(row=5, column=0, sticky='w', padx=25)

    # city label
    cityLabel = Label(frameleft, text="City", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    cityLabel.grid(row=4, column=1, sticky='w', padx=5)

    # city entry
    cityEntry = Entry(frameleft, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    cityEntry.grid(row=5, column=1, sticky='w', padx=5)

    # address label
    dobLabel = Label(frameleft, text="Date of birth", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white',
                     fg='blue')
    dobLabel.grid(row=6, column=0, sticky='w', padx=25, pady=(10, 0))

    # House label
    dateLabel = Label(frameleft, text="Date", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    dateLabel.grid(row=7, column=0, sticky='w', padx=25)

    # First name entry
    dateVar = tk.StringVar()
    dateVar.set("01")
    dateEntry = tk.OptionMenu(
        frameleft, dateVar, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30")

    dateEntry.config(width=14)
    dateEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dateEntry["menu"].config(bg="blue", fg="white")
    dateEntry.grid(row=8, column=0, sticky='w', padx=25)
    # Street label
    monthLabel = Label(frameleft, text="Month", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    monthLabel.grid(row=7, column=1, sticky='w', padx=5)

    # Street entry
    monthVar = tk.StringVar()
    monthVar.set("01")
    monthEntry = tk.OptionMenu(
        frameleft, monthVar, "01", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12")

    monthEntry.config(width=14)
    monthEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    monthEntry["menu"].config(bg="blue", fg="white")
    monthEntry.grid(row=8, column=1, sticky='w', padx=5)

    # House label
    yearLabel = Label(frameleft, text="Year", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    yearLabel.grid(row=9, column=0, sticky='w', padx=25)

    # First name entry
    yearEntry = Entry(frameleft, width=12, font=('Microsoft Yahei UI Light', 12, 'bold'), fg='white', bg='blue')
    yearEntry.grid(row=10, column=0, sticky='w', padx=25)




    # signup button
    nextButton = Button(frameleft, text="Register", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                        activebackground="blue", activeforeground="white", width=7, command=addressdetails)
    nextButton.grid(row=11, column=1, sticky='e', pady=15, padx=5)

    # don't have an account label
    alreadyaccount = Label(frameleft, text="already have account", font=('Open Sans', 9, 'bold'), bg='white', fg='blue')
    alreadyaccount.config(width=19)
    alreadyaccount.grid(row=12, column=0, sticky='w', padx=25)

    # login button
    loginButton = Button(frameleft, text="Login", font=('Open Sans', 12, 'bold underline'), bg='white', fg='blue',
                         width=7, bd=0, activebackground="white", activeforeground="blue", cursor='hand2',
                         command=login_page)
    loginButton.grid(row=12, column=1, sticky='e', padx=5)
    nextwindow.mainloop()








#******************************************** ADMIN  ***********************************************************************************

def admin(username):
    adminDashboard= Tk()
    adminDashboard.geometry('1280x650+0+0')
    adminDashboard.title("Admin Dashboard")
    adminDashboard.resizable(False, False)

    def admin_page():
        adminDashboard.destroy()
        admin_info(username)


    # patient info window
    def patient_window():
        adminDashboard.destroy()
        adminPatientInfo(username)

    #doctor info window
    def doctor_window():
        adminDashboard.destroy()
        adminDoctorInfo(username)
    #
    def adminapp_page():
        adminDashboard.destroy()
        adminapp(username)

    def logout():
        if(askyesno("logout", "are you sure you want to logout?")):
            adminDashboard.destroy()
            login()

    # #nurse info window
    # def nurse_window():
    #     adminDashboard.destroy()
    #     import nurseinfoWindow
    #
    # #staff info window
    # def staff_window():
    #     adminDashboard.destroy()
    #     import staffinfoWindow
    #
    # #accomodation info window
    # def accomodation_window():
    #     adminDashboard.destroy()
    #     import accomodationinfoWindow




    bg = ImageTk.PhotoImage(file = "admin3.jpg")
    bgLabel = tk.Label(adminDashboard, image = bg)
    bgLabel.image_names = bg
    bgLabel.place(x = 175, y = -10, relwidth = 1, relheight = 1)
    frame = tk.Frame(adminDashboard,bg='white', width=345, height=650)
    frame.place(relx=0, rely=0)

    #making heading label
    heading = Label(adminDashboard, text='Admin Dashboard', font=('times new roman', 28, 'bold underline'), bg='white', fg='blue')
    heading.grid(row=0, column=0, sticky='w', padx=25, pady=25)


    #patient info button
    infobtn = Button(adminDashboard, text='Personal info', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=admin_page)
    infobtn.grid(row=1, column=0, sticky='w', padx=50 , pady = 15)

    #patient info button
    patientbtn = Button(adminDashboard, text='Patient info', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=patient_window)
    patientbtn.grid(row=2, column=0, sticky='w', padx=50 , pady = 15)

    #doctor info button
    doctorbtn = Button(adminDashboard, text='Doctor info', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=doctor_window)
    doctorbtn.grid(row=3, column=0, sticky='w', padx=50 , pady = 15)


    #nurse info button
    appbtn = Button(adminDashboard, text='Appointment info', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=adminapp_page)
    appbtn.grid(row=4, column= 0, sticky='w', padx=50 , pady = 15)

    # #nurse info button
    # nursebtn = Button(adminDashboard, text='Nurse info', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white")
    # nursebtn.grid(row=3, column= 0, sticky='w', padx=50 , pady = 15)
    #
    # #staff info button
    # staffbtn = Button(adminDashboard, text='Staff info', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white")
    # staffbtn.grid(row=4, column=0, sticky='w', padx=50 , pady = 15)

    #accomodation info button
    # accomodationbtn = Button(adminDashboard, text='Accomodation info', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white")
    # accomodationbtn.grid(row=5, column=0, sticky='w', padx=50 , pady = 15)

    #accomodation info button
    logoutbtn = Button(adminDashboard, text='Log out', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=logout)
    logoutbtn.grid(row=6, column=0, sticky='w', padx=50 , pady = 15)

    adminDashboard.mainloop()



#******************************************** ADMIN PERSONAL INFO ***********************************************************************************


def admin_info(username):
    def back():
        admin_info_window.destroy()
        # calling the doctor dashboard window
        admin(username)

    def saveInfo():
        newfirstname = (admin_first_name.get())
        newlastname = (admin_last_name.get())
        newgender = (genderVar.get())
        newcontact = (admin_contact.get())
        newemail = (admin_email.get())
        newhousenumber = (admin_house_no.get())
        newstreet = (admin_street.get())
        newsector = (admin_sector.get())
        newcity = (admin_city.get())
        # username = doctor_username.get()
        newdob = f"{yearVar.get()}-{monthVar.get()}-{dateVar.get()}"

        cur.execute(f"""UPDATE users SET first_name = '{newfirstname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET last_name = '{newlastname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET gender = '{newgender}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET contact = '{newcontact}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET email = '{newemail}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET house_number = '{newhousenumber}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET street = '{newstreet}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET sector = '{newsector}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET city = '{newcity}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET date_of_birth = '{newdob}' WHERE username = '{username}'""")
        db.commit()

        messagebox.showinfo("success", "Information has been updated")


    # doctor info window
    # global doctor_info_window
    # make new window for doctor info
    admin_info_window = Tk()
    admin_info_window.geometry('1280x650+0+0')
    admin_info_window.title("Admin Info")
    admin_info_window.resizable(False, False)

    # making the text variables for the entries to store the data
    doctor_username = StringVar()
    admin_first_name = StringVar()
    admin_last_name = StringVar()
    # doctor_salary = StringVar()
    admin_contact = StringVar()
    admin_email = StringVar()
    admin_house_no = StringVar()
    admin_street = StringVar()
    admin_sector = StringVar()
    admin_city = StringVar()
    yearVar = StringVar()


    frame = tk.Frame(admin_info_window, bg='white', width=1280, height=650)
    frame.place(relx=0, rely=0)

    # making heading label
    heading = Label(admin_info_window, text='Admin Info', font=('times new roman', 28, 'bold underline'), bg='white',
                    fg='blue')
    heading.place(x=450, y=25)

    # doctor username label
    doctor_username_label = Label(admin_info_window, text="Username:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                  bg='white', fg='blue')
    doctor_username_label.place(x=40, y=100)

    # doctor username entry
    doctor_username_entry = Entry(admin_info_window, textvariable=doctor_username, width=20,
                                  font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_username_entry.place(x=40, y=130)

    # doctor first name label
    doctor_first_name_label = Label(admin_info_window, text="First Name:",
                                    font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_first_name_label.place(x=40, y=180)

    # doctor first name entry
    doctor_first_name_entry = Entry(admin_info_window, width=20, textvariable=admin_first_name,
                                    font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_first_name_entry.place(x=40, y=210)

    # doctor last name label
    doctor_last_name_label = Label(admin_info_window, text="Last Name:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                   bg='white', fg='blue')
    doctor_last_name_label.place(x=40, y=260)

    # doctor last name entry
    admin_last_name_entry = Entry(admin_info_window, width=20, textvariable=admin_last_name,
                                  font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    admin_last_name_entry.place(x=40, y=290)



    # doctor email label
    doctor_email_label = Label(admin_info_window, text="Email:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                               bg='white', fg='blue')
    doctor_email_label.place(x=40, y=420)

    # doctor email entry
    doctor_email_entry = Entry(admin_info_window, width=20, textvariable=admin_email,
                               font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_email_entry.place(x=40, y=450)

    # doctor phone label
    doctor_contact_label = Label(admin_info_window, text="Contact(+92):", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                 bg='white', fg='blue')
    doctor_contact_label.place(x=40, y=500)

    # doctor phone entry
    doctor_contact_entry = Entry(admin_info_window, width=20, textvariable=admin_contact,
                                 font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_contact_entry.place(x=40, y=530)

    # doctor house number label
    doctor_house_no_label = Label(admin_info_window, text="House No:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                  bg='white', fg='blue')
    doctor_house_no_label.place(x=400, y=100)

    # doctor house number entry
    doctor_house_no_entry = Entry(admin_info_window, width=20, textvariable=admin_house_no,
                                  font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_house_no_entry.place(x=400, y=130)

    # doctor street label
    doctor_street_label = Label(admin_info_window, text="Street:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_street_label.place(x=400, y=180)

    # doctor street entry
    doctor_street_entry = Entry(admin_info_window, width=20, textvariable=admin_street,
                                font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_street_entry.place(x=400, y=210)

    # doctor sector label
    doctor_sector_label = Label(admin_info_window, text="Sector:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_sector_label.place(x=400, y=260)

    # doctor sector entry
    doctor_sector_entry = Entry(admin_info_window, width=20, textvariable=admin_sector,
                                font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_sector_entry.place(x=400, y=290)

    # doctor city label
    doctor_city_label = Label(admin_info_window, text="City:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                              bg='white', fg='blue')
    doctor_city_label.place(x=400, y=340)

    # doctor city entry
    doctor_city_entry = Entry(admin_info_window, width=20, textvariable=admin_city,
                              font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_city_entry.place(x=400, y=370)

    # doctor dob entry
    # day of birth label
    dateLabel = Label(admin_info_window, text='B.Date:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    dateLabel.place(x=400, y=430)

    # date of birth entry
    # making a drop down menu for date of birth
    # date of birth entry
    dateVar = tk.StringVar()
    dateVar.set("01")
    dateEntry = tk.OptionMenu(
        admin_info_window, dateVar, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
        "31")
    dateEntry.config(width=15)
    dateEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dateEntry["menu"].config(bg="blue", fg="white")
    dateEntry.place(x=470, y=430)

    # month of birth label
    monthLabel = Label(admin_info_window, text='B.Month:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    monthLabel.place(x=400, y=480)

    # month of birth entry
    # making a drop down menu for month of birth
    monthVar = tk.StringVar()
    monthVar.set("01")
    monthEntry = tk.OptionMenu(
        admin_info_window, monthVar, "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12")
    monthEntry.config(width=15)
    monthEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    monthEntry["menu"].config(bg="blue", fg="white")
    monthEntry.place(x=470, y=480)

    # year of birth label
    yearLabel = Label(admin_info_window, text='B.Year:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    yearLabel.place(x=400, y=540)

    # year of birth entry
    yearEntry = Entry(admin_info_window, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=yearVar)
    yearEntry.place(x=470, y=540, width=130)


    # doctor gender label
    doctor_gender_label = Label(admin_info_window, text="Gender: ", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_gender_label.place(x=40, y=340)

    # doctor gender entry
    genderVar = StringVar()
    genderVar.set("Male")
    doctor_gender_entry = tk.OptionMenu(
        admin_info_window, genderVar, "Male", "Female", "Other")
    doctor_gender_entry.config(width=25, bg="blue", fg="white", activebackground="blue", activeforeground="white")
    doctor_gender_entry["menu"].config(bg="blue", fg="white")
    doctor_gender_entry.place(x=40, y=370)

    # ********************FRAME FOR PICTURE*************************
    # adding a new frame
    picture_frame = tk.Frame(admin_info_window, bg="BLUE", width=289, height=290)
    picture_frame.pack()
    picture_frame.place(x=980, y=90)
    #
    # adding a label to the frame
    bg = ImageTk.PhotoImage(file="adm1.png")
    picture_label = tk.Label(picture_frame, image=bg)
    picture_label.pack()
    picture_label.place(x=5, y=5)
    # print(username)
    cur.execute(f"""select * from users_personal where username = '{username}'""")
    adm = cur.fetchone()
    doctor_username.set(adm[0])
    admin_first_name.set(adm[1])
    admin_last_name.set(adm[2])
    genderVar.set(adm[3])
    admin_contact.set(adm[4])
    admin_email.set(adm[5])
    admin_house_no.set(adm[6])
    admin_street.set(adm[7])
    admin_sector.set(adm[8])
    admin_city.set(adm[9])
    dateVar.set(adm[10])
    monthVar.set(adm[11])
    yearVar.set(adm[12])

    # doctor_contact.set(adm[9])

    # ******************* BUTTONS *******************
    # update button
    update_button = Button(admin_info_window, text="Update", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='blue',
                           fg='white', width=20, bd=1, height=2, activebackground="blue", activeforeground="white", command=saveInfo)
    update_button.place(x=750, y=400)

    # BACK BUTTON
    back_button = Button(admin_info_window, text="Back", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='blue',
                         fg='white', width=20, bd=1, height=2, activebackground="blue", activeforeground="white",
                         command=back)
    back_button.place(x=750, y=500)

    admin_info_window.mainloop()



#******************************************** ADMIN DOCTOR INFO ***********************************************************************************


def adminDoctorInfo(username):
    adminDoctorWindow = Tk()
    adminDoctorWindow.geometry('1280x650+0+0')
    adminDoctorWindow.title("Admin Dashboard")
    adminDoctorWindow.resizable(False, False)

    def admin_page():
        adminDoctorWindow.destroy()
        admin(username)

    def clear():
        usernamevar.set('')
        passwordvar.set('')
        emailvar.set('')
        firstNamevar.set('')
        lastNamevar.set('')
        contactvar.set('')
        salaryvar.set('')
        specvar.set('')
        houseNumbervar.set('')
        streetvar.set('')
        sectorvar.set('')
        cityvar.set('')
        yearvar.set('')
        doctorStatus.set('')


    def adddoctor():
        if (usernameEntry.get() == ""):
            print("no data")
        else:
            db = mysql.connector.connect(
                host='127.0.0.1',
                user='admin',
                password='admin',
                port=3306,
                database='hospital'
            )
            cur = db.cursor()
            dob = f"{yearvar.get()}-{monthVar.get()}-{dateVar.get()}"
            entered_password = passwordvar.get()
            password_hash = bcrypt.hashpw(entered_password.encode('utf-8'), bcrypt.gensalt())
            password_hashed = password_hash.decode('utf-8')
            cur.execute(f"""INSERT INTO users (username, password_hash, user_type, first_name, last_name, gender, contact, email, house_number, street, sector, city, date_of_birth)
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s)""",
                        (usernameEntry.get(), password_hashed, "Doctor", firstNameEntry.get(), lastNameEntry.get(),
                         genderVar.get(),
                         contactEntry.get(), emailEntry.get(), houseNumberEntry.get(),
                         streetEntry.get(), sectorEntry.get(), cityEntry.get(), dob)
                        )
            db.commit()
            cur.execute(f""" select deptid from dept where dname = '{deptidVar.get()}'""")
            dept = cur.fetchone()
            dept = dept[0]
            cur.execute(
                f"""INSERT INTO doctor (dusername, salary, specialization,  dstatus, deptid) VALUES (%s, %s, %s, %s, %s)"""
                , (usernameEntry.get(), salaryEntry.get(), specEntry.get(), doctorStatusEntry.get(), dept))
            db.commit()
            db.close()
            messagebox.showinfo("success", "Doctor inserted successfully")
            clear()
            refreshTable(dtable)

    def validateinfo():
        entered_username = usernamevar.get()
        entered_password = passwordvar.get()
        entered_email = emailEntry.get()
        first_name = firstNamevar.get()
        last_name = lastNamevar.get()
        phone = contactvar.get()
        salary = salaryvar.get()
        spec = specvar.get()
        house = houseNumbervar.get()
        street = streetvar.get()
        sector = sectorvar.get()
        city = cityvar.get()
        year = yearEntry.get()
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        cur.execute("SELECT username FROM users")
        usernames = cur.fetchall()  # Fetch all usernames from the database
        cur.execute("SELECT email FROM users")
        emails = cur.fetchall()  # Fetch all usernames from the database
        if (not entered_username or not entered_password or not entered_email or not first_name
                or not last_name or not house or not street or not sector or not city or not year or not spec):
            messagebox.showerror("Error", "Please fill in all fields.")
        elif entered_email in [email[0] for email in emails]:
            messagebox.showerror("Error", "Email already exists.")
        elif entered_username in [user[0] for user in usernames]:
            messagebox.showerror("Error", "Username already exists.")
        elif "@" not in entered_email:
            messagebox.showerror("Error", "Please enter a valid email address.")
        elif len(entered_username) < 6:
            messagebox.showerror("Error", "Username should not be less than 6 characters")
        elif len(entered_password) < 6:
            messagebox.showerror("Error", "Password should not be less than 6 characters")
        else:
            if (phone.isdigit() and len(phone) == 10):
                if (salary.isdigit()):
                    if (year.isdigit()):
                        if (int(year) >= 1900 and int(year) <= 2023):
                            adddoctor()
                        else:
                            messagebox.showerror("Error", "invalid year")
                    else:
                        messagebox.showerror("Error", "year should be in digits")
                else:
                    messagebox.showerror("Error", "Salary should be in digits")
            else:
                messagebox.showerror("Error", "invalid phone number")

    def fetchdata(dtable):
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        cur.execute(f"""select username, first_name,
                         last_name, gender, contact, email, house_number,
                         street, sector, city, salary, specialization, dstatus, created_at from users, doctor 
    where username=dusername""")
        rows = cur.fetchall()
        if (len(rows) != 0):
            dtable.delete(*dtable.get_children())
            for items in rows:
                dtable.insert('', END, values=items)
            db.commit()
        db.close()

    def getdata(event=''):
        currow = dtable.focus()
        data = dtable.item(currow)
        row = data['values']
        print(len(row))
        usernamevar.set(row[0])
        firstNamevar.set(row[1])
        lastNamevar.set(row[2])
        genderVar.set(row[3])
        contactvar.set(row[4])
        emailvar.set(row[5])
        houseNumbervar.set(row[6])
        streetvar.set(row[7])
        sectorvar.set(row[8])
        cityvar.set(row[9])
        salaryvar.set(row[10])
        specvar.set(row[11])
        doctorStatus.set(row[12])
        us = usernamevar.get()
        cur.execute(f"""select dname from doctor join dept using (deptid) where doctor.dusername = '{us}' """)
        dept = cur.fetchone()
        deptidVar.set(dept[0])

        cur.execute(f"""select extract(day from date_of_birth), extract(month from date_of_birth), extract(year from date_of_birth) 
        from users where username = '{us}'""")
        dob = cur.fetchone()
        dateVar.set(dob[0])
        monthVar.set(dob[1])
        yearvar.set(dob[2])

    # text variables
    usernamevar = tk.StringVar()
    passwordvar = tk.StringVar()
    firstNamevar = tk.StringVar()
    lastNamevar = tk.StringVar()
    contactvar = tk.StringVar()
    emailvar = tk.StringVar()
    houseNumbervar = tk.StringVar()
    streetvar = tk.StringVar()
    sectorvar = tk.StringVar()
    cityvar = tk.StringVar()
    # bgroupvar = tk.StringVar()
    salaryvar = tk.StringVar()
    specvar = tk.StringVar()
    yearvar = tk.StringVar()
    doctorStatus = tk.StringVar()

    # *************************************frame *************************************
    # making a new frame for showing table of patient details
    frame = tk.Frame(adminDoctorWindow, bg='white', highlightbackground="blue", highlightthickness=2, width=1260,
                     height=370)
    frame.place(x=10, y=5)

    # making tree view
    scroll_x = ttk.Scrollbar(frame, orient=HORIZONTAL)
    # scroll_x.pack(side='bottom', fill='x')
    scroll_y = Scrollbar(frame, orient=VERTICAL)
    # scroll_y.pack(side='right', fill='y')

    # setting the style for the heading of the tree view
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), bg='blue', fg='white')

    # setting the tree view
    # ,
    dtable = ttk.Treeview(frame, style="Treeview", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    dtable['columns'] = ("username", "first_name",
                         "last_name", "gender", "contact", "email", "house_number",
                         "street", "sector", "city", "salary", "spec",
                         "dstatus", "created_at"
                         )
    # scroll_x = ttk.Scrollbar(command=ptable.xview)
    # scroll_y = ttk.Scrollbar(command=ptable.yview)

    # tree.heading("user_id", text="User ID", anchor=CENTER)
    dtable.heading("username", text="Username", anchor=CENTER)
    # tree.heading("password_hash", text="Password Hash", anchor=CENTER)
    # tree.heading("user_type", text="User Type", anchor=CENTER)
    dtable.heading("first_name", text="F.Name", anchor=CENTER)
    dtable.heading("last_name", text="L.Name", anchor=CENTER)
    dtable.heading("gender", text="Gender", anchor=CENTER)
    dtable.heading("contact", text="Phone #", anchor=CENTER)
    dtable.heading("email", text="Email", anchor=CENTER)
    dtable.heading("house_number", text="House #", anchor=CENTER)
    dtable.heading("street", text="Street", anchor=CENTER)
    dtable.heading("sector", text="Sector", anchor=CENTER)
    dtable.heading("city", text="city", anchor=CENTER)
    # tree.heading("date_of_birth", text="DOB", anchor=CENTER)
    dtable.heading("salary", text="Salary", anchor=CENTER)
    dtable.heading("spec", text="Spec", anchor=CENTER)
    dtable.heading("dstatus", text="Status", anchor=CENTER)
    dtable.heading("created_at", text="Created At", anchor=CENTER)
    # tree.heading("pusername", text="PUsername", anchor=CENTER)
    # tree.heading("blood_group", text="Blood Group", anchor=CENTER)
    # tree.heading("height", text="Height", anchor=CENTER)
    # tree.heading("weight", text="Weight", anchor=CENTER)
    dtable['show'] = 'headings'

    dtable.pack(fill=BOTH, expand=1)

    dtable.place(x=5, y=2, width=1245, height=390)

    # ptable.column("#0", width=0, stretch=NO)
    # tree.column("user_id", anchor=CENTER, width=62)
    dtable.column("username", anchor=CENTER, width=60)
    # tree.column("password_hash", anchor=CENTER, width=62)
    # tree.column("user_type", anchor=CENTER, width=62)
    dtable.column("first_name", anchor=CENTER, width=60)
    dtable.column("last_name", anchor=CENTER, width=60)
    dtable.column("gender", anchor=CENTER, width=60)
    dtable.column("contact", anchor=CENTER, width=60)
    dtable.column("email", anchor=CENTER, width=60)
    dtable.column("house_number", anchor=CENTER, width=60)
    dtable.column("street", anchor=CENTER, width=60)
    dtable.column("sector", anchor=CENTER, width=60)
    dtable.column("city", anchor=CENTER, width=40)
    # tree.column("date_of_birth", anchor=CENTER, width=50)
    dtable.column("salary", anchor=CENTER, width=68)
    dtable.column("spec", anchor=CENTER, width=68)
    dtable.column("dstatus", anchor=CENTER, width=68)
    dtable.column("created_at", anchor=CENTER, width=60)
    # tree.column("pusername", anchor=CENTER, width=62)
    # tree.column("blood_group", anchor=CENTER, width=62)
    # tree.column("height", anchor=CENTER, width=62)
    # tree.column("weight", anchor=CENTER, width=62)

    dtable.bind('<ButtonRelease-1>', getdata)

    def refreshTable(table):
        for item in table.get_children():  # list of every row's id
            dtable.delete(item)
        fetchdata(table)

    def updatestatus():
        global selectedpusername
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        newusername = (usernamevar.get())
        newfirstname = (firstNamevar.get())
        newlastname = (lastNamevar.get())
        newgender = (genderVar.get())
        newcontact = (contactvar.get())
        newemail = (emailvar.get())
        newhousenumber = (houseNumbervar.get())
        newstreet = (streetvar.get())
        newsector = (sectorvar.get())
        newcity = (cityvar.get())
        newsalary = (salaryvar.get())
        newspec = (specvar.get())
        newstatus = (doctorStatusEntry.get())
        username = usernamevar.get()
        newdob = f"{yearvar.get()}-{monthVar.get()}-{dateVar.get()}"
        print(username)
        print(newstatus)

        cur.execute(f"""UPDATE users SET username = '{newusername}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET first_name = '{newfirstname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET last_name = '{newlastname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET gender = '{newgender}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET contact = '{newcontact}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET email = '{newemail}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET house_number = '{newhousenumber}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET street = '{newstreet}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET sector = '{newsector}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET city = '{newcity}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE doctor SET salary = '{newsalary}' WHERE dusername = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE doctor SET specialization = '{newspec}' WHERE dusername = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE doctor SET dstatus = '{newstatus}' WHERE dusername = '{username}'""")
        db.commit()
        messagebox.showinfo("success", "Information has been updated")
        refreshTable(dtable)

    # ******************** FRAME1 FOR THE DATA HOLDERS ***********************
    frame1 = tk.Frame(adminDoctorWindow, bg='white', highlightbackground="blue", highlightthickness=2, width=1260,
                      height=260)
    frame1.place(x=10, y=370)

    # username label
    usernameLabel = Label(adminDoctorWindow, text='Username:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    usernameLabel.place(x=20, y=380)

    # username entry
    usernameEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                          textvariable=usernamevar)
    usernameEntry.place(x=120, y=380)

    # first name label
    firstNameLabel = Label(adminDoctorWindow, text='First Name:', font=('times new roman', 12, 'bold'), bg='white',
                           fg='blue')
    firstNameLabel.place(x=20, y=420)

    # first name entry
    firstNameEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                           textvariable=firstNamevar)
    firstNameEntry.place(x=120, y=420)

    # last name label
    lastNameLabel = Label(adminDoctorWindow, text='Last Name:', font=('times new roman', 12, 'bold'), bg='white',
                          fg='blue')
    lastNameLabel.place(x=20, y=460)

    # last name entry
    lastNameEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                          textvariable=lastNamevar)
    lastNameEntry.place(x=120, y=460)

    # password label
    passwordLabel = Label(adminDoctorWindow, text='Password:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    passwordLabel.place(x=20, y=500)

    # password entry
    passwordEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                          textvariable=passwordvar)
    passwordEntry.place(x=120, y=500)

    # gender label
    genderLabel = Label(adminDoctorWindow, text="Gender: ", font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    genderLabel.place(x=580, y=380)
    # gender entry
    genderVar = StringVar()
    genderVar.set("Male")
    genderEntry = tk.OptionMenu(
        adminDoctorWindow, genderVar, "Male", "Female", "Other")
    genderEntry.config(width=20, bg="blue", fg="white", activebackground="blue", activeforeground="white")
    genderEntry["menu"].config(bg="blue", fg="white")
    genderEntry.place(x=680, y=380)

    # contact label
    contactLabel = Label(adminDoctorWindow, text='Contact(+92):', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    contactLabel.place(x=580, y=420)

    # contact entry
    contactEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                         textvariable=contactvar)
    contactEntry.place(x=680, y=420)

    # email label
    emailLabel = Label(adminDoctorWindow, text='Email:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    emailLabel.place(x=580, y=460)

    # email entry
    emailEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                       textvariable=emailvar)
    emailEntry.place(x=680, y=460)

    # house number label
    houseNumberLabel = Label(adminDoctorWindow, text='House #:', font=('times new roman', 12, 'bold'), bg='white',
                             fg='blue')
    houseNumberLabel.place(x=300, y=380)

    # house number entry
    houseNumberEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                             textvariable=houseNumbervar)
    houseNumberEntry.place(x=400, y=380)

    # street label
    streetLabel = Label(adminDoctorWindow, text='Street:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    streetLabel.place(x=300, y=420)

    # street entry
    streetEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                        textvariable=streetvar)
    streetEntry.place(x=400, y=420)

    # sector label
    sectorLabel = Label(adminDoctorWindow, text='Sector:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    sectorLabel.place(x=300, y=460)

    # sector entry
    sectorEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                        textvariable=sectorvar)
    sectorEntry.place(x=400, y=460)

    # date of birth label
    cityLabel = Label(adminDoctorWindow, text='City:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    cityLabel.place(x=300, y=500)

    # date of birth entry
    cityEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=cityvar)
    cityEntry.place(x=400, y=500)

    # weight label
    salaryLabel = Label(adminDoctorWindow, text='Salary:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    salaryLabel.place(x=20, y=540)

    # weight entry
    salaryEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                        textvariable=salaryvar)
    salaryEntry.place(x=120, y=540)

    # height label
    specLabel = Label(adminDoctorWindow, text='Specialization:', font=('times new roman', 12, 'bold'), bg='white',
                      fg='blue')
    specLabel.place(x=300, y=540)

    # height entry
    specEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=specvar)
    specEntry.place(x=400, y=540)

    # blood group label
    deptidLabel = Label(adminDoctorWindow, text='Dept:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    deptidLabel.place(x=580, y=500)

    db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
    cur = db.cursor()
    cur.execute("SELECT dname FROM Dept")
    depts = cur.fetchall()

    dept_ids = [dept[0] for dept in depts]  # Extracting department IDs from the fetched data

    deptidVar = tk.StringVar()
    deptd = dept_ids[0]
    deptidVar.set(deptd)  # Set the default value to the first department ID

    deptidEntry = tk.OptionMenu(adminDoctorWindow, deptidVar, *dept_ids)

    deptidEntry.config(width=20)
    deptidEntry.config(width=20)
    deptidEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    deptidEntry["menu"].config(bg="blue", fg="white")
    # bgroupEntry.grid(row=4, column=1, sticky='w', padx=5)
    deptidEntry.place(x=680, y=500)

    # day of birth label
    dateLabel = Label(adminDoctorWindow, text='Date:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    dateLabel.place(x=20, y=580)

    # date of birth entry
    # making a drop down menu for date of birth
    # date of birth entry
    dateVar = tk.StringVar()
    dateVar.set("01")
    dateEntry = tk.OptionMenu(
        adminDoctorWindow, dateVar, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
        "31")
    dateEntry.config(width=20)
    dateEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dateEntry["menu"].config(bg="blue", fg="white")
    dateEntry.place(x=120, y=580)

    # month of birth label
    monthLabel = Label(adminDoctorWindow, text='Month:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    monthLabel.place(x=300, y=580)

    # month of birth entry
    # making a drop down menu for month of birth
    monthVar = tk.StringVar()
    monthVar.set("01")
    monthEntry = tk.OptionMenu(
        adminDoctorWindow, monthVar, "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12")
    monthEntry.config(width=20)
    monthEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    monthEntry["menu"].config(bg="blue", fg="white")
    monthEntry.place(x=400, y=580)

    # year of birth label
    yearLabel = Label(adminDoctorWindow, text='Year:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    yearLabel.place(x=580, y=580)

    # year of birth entry
    yearEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=yearvar)
    yearEntry.place(x=680, y=580)

    # patient status label
    doctorStatusLabel = Label(adminDoctorWindow, text='Doctor Status:', font=('times new roman', 12, 'bold'), bg='white',
                              fg='blue')
    doctorStatusLabel.place(x=580, y=540)

    # patient status entry
    doctorStatusEntry = Entry(adminDoctorWindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                              textvariable=doctorStatus)
    doctorStatusEntry.place(x=680, y=540)

    # ************************************* BUTTONS *************************************
    # add button
    addButton = Button(adminDoctorWindow, text="Add Doctor", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                       activebackground="blue", activeforeground="white", width=10, command=validateinfo)
    addButton.place(x=1000, y=400)

    # update button
    updateButton = Button(adminDoctorWindow, text="Update", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                          activebackground="blue", activeforeground="white", width=8, command=updatestatus)
    updateButton.place(x=1000, y=480)


    # update button
    clrButton = Button(adminDoctorWindow, text="C", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                          activebackground="blue", activeforeground="white", width=4, command=clear)
    clrButton.place(x=1170, y=560)

    # save button
    backButton = Button(adminDoctorWindow, text="Dashboard", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                        activebackground="blue", activeforeground="white", width=10, command=admin_page)
    backButton.place(x=1000, y=560)

    fetchdata(dtable)
    adminDoctorWindow.mainloop()


#******************************************** ADMIN PATIENT INFO ***********************************************************************************


def adminPatientInfo(username):
    adminpatientwindow = Tk()
    adminpatientwindow.geometry('1280x650+0+0')
    adminpatientwindow.title("Admin Dashboard")
    adminpatientwindow.resizable(False, False)

    def admin_page():
        adminpatientwindow.destroy()
        admin(username)

    def clear():
        usernamevar.set('')
        passwordvar.set('')
        emailvar.set('')
        firstNamevar.set('')
        lastNamevar.set('')
        contactvar.set('')
        heightvar.set('')
        weightvar.set('')
        houseNumbervar.set('')
        streetvar.set('')
        sectorvar.set('')
        cityvar.set('')
        yearvar.set('')
        patientStatus.set('')



    def isfloat(n):
        try:
            float(n)
            return True
        except ValueError:
            return False


    def addpatient():
        if(usernameEntry.get()==""):
            print("no data")
        else:
            # db = mysql.connector.connect(
            #     host='127.0.0.1',
            #     user='admin',
            #     password='admin',
            #     port=3306,
            #     database='hospital'
            # )
            # cur = db.cursor()
            dob = f"{yearvar.get()}-{monthVar.get()}-{dateVar.get()}"
            entered_password = passwordvar.get()
            password_hash = bcrypt.hashpw(entered_password.encode('utf-8'), bcrypt.gensalt())
            password_hashed = password_hash.decode('utf-8')
            cur.execute(f"""INSERT INTO users (username, password_hash, user_type, first_name, last_name, gender, contact, email, house_number, street, sector, city, date_of_birth)
                           VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s)""",
                        (usernameEntry.get(), password_hashed, "Patient", firstNameEntry.get(), lastNameEntry.get(),genderVar.get(),
                           contactEntry.get(), emailEntry.get(), houseNumberEntry.get(),
                        streetEntry.get(), sectorEntry.get(), cityEntry.get(), dob)
            )
            db.commit()
            cur.execute(f"""INSERT INTO patient (pusername, blood_group, height, weight, pstatus) VALUES (%s, %s, %s, %s, %s)"""
                        , (usernameEntry.get(), bgroupVar.get(), heightEntry.get(), weightEntry.get(), patientStatusEntry.get()))
            db.commit()
            db.close()
            messagebox.showinfo("success", "Patient inserted successfully")
            clear()
            refreshTable(ptable)


    def validateinfo():
        entered_username = usernamevar.get()
        entered_password = passwordvar.get()
        entered_email = emailEntry.get()
        first_name = firstNamevar.get()
        last_name = lastNamevar.get()
        phone = contactvar.get()
        height = heightvar.get()
        weight = weightvar.get()
        house = houseNumbervar.get()
        street = streetvar.get()
        sector = sectorvar.get()
        city = cityvar.get()
        year = yearEntry.get()

        # db = mysql.connector.connect(
        #     host='127.0.0.1',
        #     user='admin',
        #     password='admin',
        #     port=3306,
        #     database='hospital'
        # )
        # cur = db.cursor()
        cur.execute("SELECT username FROM users")
        usernames = cur.fetchall()  # Fetch all usernames from the database
        cur.execute("SELECT email FROM users")
        emails = cur.fetchall()  # Fetch all usernames from the database
        if (not entered_username or not entered_password or not entered_email or not first_name
                or not last_name or not house or not street or not sector or not city or not year):
            messagebox.showerror("Error", "Please fill in all fields.")
        elif entered_email in [email[0] for email in emails]:
            messagebox.showerror("Error", "Email already exists.")
        elif entered_username in [user[0] for user in usernames]:
            messagebox.showerror("Error", "Username already exists.")
        elif "@" not in entered_email:
            messagebox.showerror("Error", "Please enter a valid email address.")
        elif len(entered_username) < 6:
            messagebox.showerror("Error", "Username should not be less than 6 characters")
        elif len(entered_password) < 6:
            messagebox.showerror("Error", "Password should not be less than 6 characters")
        else:
            if (phone.isdigit() and len(phone) == 10):
                if (isfloat(height)):
                    if (isfloat(weight)):
                        if (year.isdigit()):
                            if (int(year) >= 1900 and int(year) <= 2023):
                                addpatient()
                            else:
                                messagebox.showerror("Error", "invalid year")
                        else:
                            messagebox.showerror("Error", "year should be in digits")
                    else:
                        messagebox.showerror("Error", "Weight should be in digits")
                else:
                    messagebox.showerror("Error", "Height should be in digits")
            else:
                messagebox.showerror("Error", "invalid phone number")




    def fetchdata(ptable):
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        cur.execute(f"""select username, first_name,
                         last_name, gender, contact, email, house_number,
                         street, sector, city, height, weight,  pstatus, created_at from users, patient 
    where username=pusername""")
        rows = cur.fetchall()
        # cur.execute(f"""select pstatus from patient""")
        # pstatus = cur.fetchall()
        if(len(rows)!=0):
            ptable.delete(* ptable.get_children())
            for items in rows:
                ptable.insert('', END, values=items)
            db.commit()
        db.close()

    def getdata(event=''):
        currow = ptable.focus()
        data = ptable.item(currow)
        row = data['values']
        print(len(row))
        usernamevar.set(row[0])
        firstNamevar.set(row[1])
        lastNamevar.set(row[2])
        genderVar.set(row[3])
        contactvar.set(row[4])
        emailvar.set(row[5])
        houseNumbervar.set(row[6])
        streetvar.set(row[7])
        sectorvar.set(row[8])
        cityvar.set(row[9])
        heightvar.set(row[10])
        weightvar.set(row[11])
        patientStatus.set(row[12])
        us = usernamevar.get()
        cur.execute(f"""select extract(day from date_of_birth), extract(month from date_of_birth), extract(year from date_of_birth) 
        from users where username = '{us}'""")
        dob = cur.fetchone()
        dateVar.set(dob[0])
        monthVar.set(dob[1])
        yearvar.set(dob[2])


    # text variables
    usernamevar = tk.StringVar()
    passwordvar = tk.StringVar()
    firstNamevar = tk.StringVar()
    lastNamevar = tk.StringVar()
    contactvar = tk.StringVar()
    emailvar = tk.StringVar()
    houseNumbervar = tk.StringVar()
    streetvar = tk.StringVar()
    sectorvar = tk.StringVar()
    cityvar = tk.StringVar()
    # bgroupvar = tk.StringVar()
    heightvar = tk.StringVar()
    weightvar = tk.StringVar()
    yearvar = tk.StringVar()
    patientStatus = tk.StringVar()



    # *************************************frame *************************************
    # making a new frame for showing table of patient details
    frame = tk.Frame(adminpatientwindow, bg='white', width=1260, height=370)
    frame.place(x=10, y=5)

    # making tree view
    scroll_x = ttk.Scrollbar(frame, orient=HORIZONTAL)
    # scroll_x.pack(side='bottom', fill='x')
    scroll_y = Scrollbar(frame, orient=VERTICAL)
    # scroll_y.pack(side='right', fill='y')


    # setting the style for the heading of the tree view
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), bg='blue', fg='white')

    # setting the tree view
    # ,
    ptable = ttk.Treeview(frame, style="Treeview", xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
    ptable['columns'] = ("username", "first_name",
                         "last_name", "gender", "contact", "email", "house_number",
                         "street", "sector", "city", "height", "weight",
                         "pstatus", "created_at"
                         )

    ptable.heading("username", text="Username", anchor=CENTER)
    ptable.heading("first_name", text="F.Name", anchor=CENTER)
    ptable.heading("last_name", text="L.Name", anchor=CENTER)
    ptable.heading("gender", text="Gender", anchor=CENTER)
    ptable.heading("contact", text="Phone #", anchor=CENTER)
    ptable.heading("email", text="Email", anchor=CENTER)
    ptable.heading("house_number", text="House #", anchor=CENTER)
    ptable.heading("street", text="Street", anchor=CENTER)
    ptable.heading("sector", text="Sector", anchor=CENTER)
    ptable.heading("city", text="city", anchor=CENTER)
    ptable.heading("height", text="Height", anchor=CENTER)
    ptable.heading("weight", text="Weight", anchor=CENTER)
    ptable.heading("pstatus", text="Status", anchor=CENTER)
    ptable.heading("created_at", text="Created At", anchor=CENTER)

    ptable['show'] = 'headings'

    ptable.pack(fill=BOTH, expand=1)

    ptable.place(x=5, y=2, width=1245, height=390)


    ptable.column("username", anchor=CENTER, width=60)
    ptable.column("first_name", anchor=CENTER, width=60)
    ptable.column("last_name", anchor=CENTER, width=60)
    ptable.column("gender", anchor=CENTER, width=60)
    ptable.column("contact", anchor=CENTER, width=60)
    ptable.column("email", anchor=CENTER, width=60)
    ptable.column("house_number", anchor=CENTER, width=60)
    ptable.column("street", anchor=CENTER, width=60)
    ptable.column("sector", anchor=CENTER, width=60)
    ptable.column("city", anchor=CENTER, width=40)
    ptable.column("height", anchor=CENTER, width=68)
    ptable.column("weight", anchor=CENTER, width=68)
    ptable.column("pstatus", anchor=CENTER, width=68)
    ptable.column("created_at", anchor=CENTER, width=60)


    ptable.bind('<ButtonRelease-1>', getdata)


    def refreshTable(table):
        for item in table.get_children():  # list of every row's id
            ptable.delete(item)
        fetchdata(table)



    def updatestatus():

        global selectedpusername
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        newusername = (usernamevar.get())
        newfirstname = (firstNamevar.get())
        newlastname = (lastNamevar.get())
        newgender = (genderVar.get())
        newcontact = (contactvar.get())
        newemail = (emailvar.get())
        newhousenumber = (houseNumbervar.get())
        newstreet = (streetvar.get())
        newsector = (sectorvar.get())
        newcity = (cityvar.get())
        newheight = (heightvar.get())
        newweight = (weightvar.get())
        newstatus = (patientStatusEntry.get())
        username = usernamevar.get()
        newdob = f"{yearvar.get()}-{monthVar.get()}-{dateVar.get()}"
        year = yearvar.get()

        if (newcontact.isdigit() and len(newcontact) == 10):
            if (isfloat(newheight)):
                if (isfloat(newweight)):
                    if (year.isdigit()):
                        if (int(year) >= 1900 and int(year) <= 2023):
                            cur.execute(
                                f"""UPDATE users SET first_name = '{newfirstname}', last_name = '{newlastname}', 
                                 gender = '{newgender}', contact = '{newcontact}', email = '{newemail}', house_number = '{newhousenumber}', 
                                 street = '{newstreet}', sector = '{newsector}', 
                                 city = '{newcity}' WHERE username = '{username}'""")
                            db.commit()
                            cur.execute(f"""UPDATE patient SET height = '{newheight}',  weight = '{newweight}', 
                             pstatus = '{newstatus}' WHERE pusername = '{username}'""")
                            db.commit()
                            messagebox.showinfo("success", "Information has been updated")
                            refreshTable(ptable)
                        else:
                            messagebox.showerror("Error", "invalid year")
                    else:
                        messagebox.showerror("Error", "year should be in digits")
                else:
                    messagebox.showerror("Error", "Weight should be in digits")
            else:
                messagebox.showerror("Error", "Height should be in digits")
        else:
            messagebox.showerror("Error", "invalid phone number")

        # cur.execute(f"""UPDATE users SET username = '{newusername}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET first_name = '{newfirstname}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET last_name = '{newlastname}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET gender = '{newgender}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET contact = '{newcontact}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET email = '{newemail}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET house_number = '{newhousenumber}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET street = '{newstreet}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET sector = '{newsector}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET date_of_birth = '{newdob}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE users SET city = '{newcity}' WHERE username = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE patient SET height = '{newheight}' WHERE pusername = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE patient SET weight = '{newweight}' WHERE pusername = '{username}'""")
        # db.commit()
        # cur.execute(f"""UPDATE patient SET pstatus = '{newstatus}' WHERE pusername = '{username}'""")
        # db.commit()





    # ******************** FRAME1 FOR THE DATA HOLDERS ***********************
    frame1 = tk.Frame(adminpatientwindow, bg='white', highlightbackground="blue", highlightthickness=2, width=1260, height=260)
    frame1.place(x=10, y=370)

    # username label
    usernameLabel = Label(adminpatientwindow, text='Username:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    usernameLabel.place(x=20, y=380)

    # username entry
    usernameEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                          textvariable=usernamevar)
    usernameEntry.place(x=120, y=380)

    # first name label
    firstNameLabel = Label(adminpatientwindow, text='First Name:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    firstNameLabel.place(x=20, y=420)

    # first name entry
    firstNameEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                           textvariable=firstNamevar)
    firstNameEntry.place(x=120, y=420)

    # last name label
    lastNameLabel = Label(adminpatientwindow, text='Last Name:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    lastNameLabel.place(x=20, y=460)

    # last name entry
    lastNameEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                          textvariable=lastNamevar)
    lastNameEntry.place(x=120, y=460)

    # password label
    passwordLabel = Label(adminpatientwindow, text='Password:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    passwordLabel.place(x=20, y=500)

    # password entry
    passwordEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=passwordvar)
    passwordEntry.place(x=120, y=500)

    # gender label
    genderLabel = Label(adminpatientwindow, text="Gender: ", font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    genderLabel.place(x=580, y=380)
    # gender entry
    genderVar = StringVar()
    genderVar.set("Male")
    genderEntry = tk.OptionMenu(
        adminpatientwindow, genderVar, "Male", "Female", "Other")
    genderEntry.config(width=20, bg="blue", fg="white", activebackground="blue", activeforeground="white")
    genderEntry["menu"].config(bg="blue", fg="white")
    genderEntry.place(x=680, y=380)

    # contact label
    contactLabel = Label(adminpatientwindow, text='Contact(+92):', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    contactLabel.place(x= 580, y=420)

    # contact entry
    contactEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                         textvariable=contactvar)
    contactEntry.place(x=680, y=420)

    # email label
    emailLabel = Label(adminpatientwindow, text='Email:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    emailLabel.place(x=580, y=460)

    # email entry
    emailEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=emailvar)
    emailEntry.place(x=680, y=460)

    # house number label
    houseNumberLabel = Label(adminpatientwindow, text='House #:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    houseNumberLabel.place(x= 300, y=380)

    # house number entry
    houseNumberEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                             textvariable=houseNumbervar)
    houseNumberEntry.place(x=400, y=380)

    # street label
    streetLabel = Label(adminpatientwindow, text='Street:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    streetLabel.place(x=300, y=420)

    # street entry
    streetEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=streetvar)
    streetEntry.place(x=400, y=420)

    # sector label
    sectorLabel = Label(adminpatientwindow, text='Sector:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    sectorLabel.place(x=300, y=460)

    # sector entry
    sectorEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=sectorvar)
    sectorEntry.place(x=400, y=460)

    # date of birth label
    cityLabel = Label(adminpatientwindow, text='City:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    cityLabel.place(x=300, y=500)

    # date of birth entry
    cityEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=cityvar)
    cityEntry.place(x=400, y=500)

    # weight label
    weightLabel = Label(adminpatientwindow, text='Weight:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    weightLabel.place(x=20, y=540)

    # weight entry
    weightEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=weightvar)
    weightEntry.place(x=120, y=540)

    # height label
    heightLabel = Label(adminpatientwindow, text='Height:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    heightLabel.place(x=300, y=540)

    # height entry
    heightEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=heightvar)
    heightEntry.place(x=400, y=540)

    # blood group label
    bgroupLabel = Label(adminpatientwindow, text='Blood Group:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    bgroupLabel.place(x=580, y=500)

    # blood group entry
    bgroupVar = tk.StringVar()
    bgroupVar.set("B+")
    bgroupEntry = tk.OptionMenu(
        adminpatientwindow, bgroupVar, "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-")

    bgroupEntry.config(width=20)
    bgroupEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    bgroupEntry["menu"].config(bg="blue", fg="white")
    # bgroupEntry.grid(row=4, column=1, sticky='w', padx=5)
    bgroupEntry.place(x=680, y=500)

    # day of birth label
    dateLabel = Label(adminpatientwindow, text='Date:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    dateLabel.place(x=20, y=580)

    # date of birth entry
    # making a drop down menu for date of birth
    # date of birth entry
    dateVar = tk.StringVar()
    dateVar.set("01")
    dateEntry = tk.OptionMenu(
        adminpatientwindow, dateVar, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
        "31")
    dateEntry.config(width=20)
    dateEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dateEntry["menu"].config(bg="blue", fg="white")
    dateEntry.place(x=120, y=580)

    # month of birth label
    monthLabel = Label(adminpatientwindow, text='Month:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    monthLabel.place(x=300, y=580)

    # month of birth entry
    # making a drop down menu for month of birth
    monthVar = tk.StringVar()
    monthVar.set("01")
    monthEntry = tk.OptionMenu(
        adminpatientwindow, monthVar, "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12")
    monthEntry.config(width=20)
    monthEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    monthEntry["menu"].config(bg="blue", fg="white")
    monthEntry.place(x=400, y=580)

    # year of birth label
    yobLabel = Label(adminpatientwindow, text='Year:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    yobLabel.place(x=580, y=580)

    # year of birth entry
    yearEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=yearvar)
    yearEntry.place(x=680, y=580)



    # patient status label
    patientStatusLabel = Label(adminpatientwindow, text='Patient Status:', font=('times new roman', 12, 'bold'), bg='white',
                               fg='blue')
    patientStatusLabel.place(x=580, y=540)

    # patient status entry
    patientStatusEntry = Entry(adminpatientwindow, font=('times new roman', 12, 'bold'), bg='white', fg='blue',
                               textvariable=patientStatus)
    patientStatusEntry.place(x= 680, y=540)

    # ************************************* BUTTONS *************************************
    # add button
    addButton = Button(adminpatientwindow, text="Add Patient", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                       activebackground="blue", activeforeground="white", width=10, command=validateinfo)
    addButton.place(x=1000, y=400)

    # update button
    updateButton = Button(adminpatientwindow, text="Update", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                          activebackground="blue", activeforeground="white", width=8, command=updatestatus)
    updateButton.place(x=1000, y=480)

    # update button
    clrButton = Button(adminpatientwindow, text="C", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                          activebackground="blue", activeforeground="white", width=4, command=clear)
    clrButton.place(x=1170, y=560)

    # save button
    backButton = Button(adminpatientwindow, text="Dashboard", font=('Open Sans', 16, 'bold'), fg='white', bg='blue', bd=0,
                        activebackground="blue", activeforeground="white", width=10, command=admin_page)
    backButton.place(x=1000, y=560)


    fetchdata(ptable)
    adminpatientwindow.mainloop()


#******************************************** ADMIN APPOINTMENT INFO ***********************************************************************************

def adminapp(username):
    adminAppointmentInfoWindow = Tk()
    adminAppointmentInfoWindow.geometry('1280x650+0+0')
    adminAppointmentInfoWindow.title("Admin Appointment Info")
    adminAppointmentInfoWindow.resizable(False, False)

    def refreshTable(table):
        for item in table.get_children():  # list of every row's id
            table.delete(item)
        fetchdata(table)

    def clear():
        appdatevar.set("")
        appstatusvar.set("")
        app_timestampvar.set("")
        pusernamevar.set("")
        symptomsvar.set("")
        dusernamevar.set("")

    def admin_page():
        adminAppointmentInfoWindow.destroy()
        admin(username)

    def isfloat(n):
        try:
            float(n)
            return True
        except ValueError:
            return False

    def validateinfo():
        # entered_appid = appidEntry.get()
        entered_appstatus = appstatusEntry.get()
        entered_pusername = pusernameVar.get()
        entered_symptoms = symptomsEntry.get()
        entered_dusername = dusernameVar.get()
        entered_date = dateVar.get()
        entered_month = monthVar.get()

        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        # cur.execute(f"""select appid from appointment where appid = '{entered_appid}'""")
        # appid_fetched = cur.fetchall()
        cur.execute(f"""select pusername from patient where pusername = '{entered_pusername}'""")
        pusername_fetched = cur.fetchall()
        cur.execute(f"""select dusername from doctor where dusername = '{entered_dusername}'""")
        dusername_fetched = cur.fetchall()
        # if (len(appid_fetched) != 0):
        #     messagebox.showerror("Error", "Appointment ID already exists!")
        if (len(pusername_fetched) == 0):
            messagebox.showerror("Error", "Patient Username does not exist!")
        elif (len(dusername_fetched) == 0):
            messagebox.showerror("Error", "Doctor Username does not exist!")
        elif (
                entered_appstatus == "" or entered_pusername == "" or entered_symptoms == "" or entered_dusername == "" or entered_date == "" or entered_month == ""):
            messagebox.showerror("Error", "Please fill all the fields!")
        elif (isfloat(entered_appstatus)):
            messagebox.showerror("Error", "Appointment Status cannot be a number!")
        elif (isfloat(entered_pusername)):
            messagebox.showerror("Error", "Patient Username cannot be a number!")
        elif (isfloat(entered_symptoms)):
            messagebox.showerror("Error", "Symptoms cannot be a number!")
        elif (isfloat(entered_dusername)):
            messagebox.showerror("Error", "Doctor Username cannot be a number!")
        else:
            appdate = f"2024-{monthVar.get()}-{dateVar.get()}"
            cur.execute(
                f"""insert into appointment(appstatus, pusername, symptoms, dusername, appdate) values('{entered_appstatus}', '{pusernameVar.get()}', '{entered_symptoms}', '{entered_dusername}', '{appdate}')""")
            db.commit()
            messagebox.showinfo("Success", "Appointment added successfully!")
            clear()
            fetchdata(apptable)

    def fetchdata(apptable):
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        cur.execute(f"""select appid, appdate, appstatus, app_timestamp, pusername, symptoms, dusername from appointment""")
        rows = cur.fetchall()
        # cur.execute(f"""select pstatus from patient""")
        # pstatus = cur.fetchall()
        if (len(rows) != 0):
            apptable.delete(*apptable.get_children())
            for items in rows:
                apptable.insert('', END, values=items)
            db.commit()
        cur.close()
        db.close()

    def getdata(event=''):
        currow = apptable.focus()
        data = apptable.item(currow)
        row = data['values']
        # print(len(row))
        appidvar.set(row[0])
        appdatevar.set(row[1])
        appstatusvar.set(row[2])
        app_timestampvar.set(row[3])
        pusernamevar.set(row[4])
        symptomsvar.set(row[5])
        dusernamevar.set(row[6])
        # cur.execute(f"""select appid from appointment where pusername = '{pusernameVar.get()}' and
        # dusername = '{dusernameVar.get()}' and symptoms = '{symptomsvar.get()}'""")
        # global appid
        # appid = cur.fetchone()
        # cur.close()
        # appid = appid[0]
        # print(appid)

    def updateInfo():
        # global appid
        # print(appid[0])
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()
        global appid
        cur.execute(f"""update appointment set symptoms = '{symptomsvar.get()}', appstatus = '{appstatusvar.get()}' where appid = '{appidvar.get()}'""")
        db.commit()
        messagebox.showinfo("Success", "information has been updated")
        refreshTable(apptable)

    # making the text variables for the admin appointment info window
    appidvar = StringVar()
    appdatevar = StringVar()
    appstatusvar = StringVar()
    app_timestampvar = StringVar()
    pusernamevar = StringVar()
    symptomsvar = StringVar()
    dusernamevar = StringVar()

    # making the frame for the admin appointment info window
    frame = tk.Frame(adminAppointmentInfoWindow, bg='white',
                     width=1260,
                     height=370)
    frame.place(x=10, y=5)

    # setting the style for the heading of the tree view
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), bg='blue', fg='white')

    apptable = ttk.Treeview(frame, style="Treeview")
    apptable['columns'] = ("appid","appdate", "appstatus", "app_timestamp", "pusername", "symptoms", "dusername")

    # setting the headings for the columns of the tree view
    apptable.heading("appid", text="ID")
    apptable.heading("appdate", text="Appointment date")
    apptable.heading("appstatus", text="Appointment Status")
    apptable.heading("app_timestamp", text="Appointment Timestamp")
    apptable.heading("pusername", text="Patient Username")
    apptable.heading("symptoms", text="Symptoms")
    apptable.heading("dusername", text="Doctor Username")
    apptable['show'] = 'headings'

    apptable.pack(fill=BOTH, expand=1)

    apptable.place(x=10, y=5, width=1240, height=350)

    # setting the width of the columns of the tree view
    apptable.column("appid", width=30)
    apptable.column("appdate", width=100)
    apptable.column("appstatus", width=100)
    apptable.column("app_timestamp", width=100)
    apptable.column("pusername", width=100)
    apptable.column("symptoms", width=100)
    apptable.column("dusername", width=100)

    apptable.bind("<ButtonRelease-1>", getdata)

    # ******* FRAME1 FOR THE DATA HOLDERS ********
    frame1 = tk.Frame(adminAppointmentInfoWindow, bg='white', highlightbackground="blue", highlightthickness=2,
                      width=1260,
                      height=200)
    frame1.place(x=10, y=420)

    # appstatus label
    appstatusLabel = Label(frame1, text='Appointment Status: ', font=('times new roman', 14, 'bold'), bg='white',
                           fg='blue')
    appstatusLabel.place(x=30, y=145)

    # appstatus entry
    appstatusEntry = Entry(frame1, font=('times new roman', 14), bg='white', textvariable=appstatusvar)
    appstatusEntry.place(x=220, y=145)

    # pusername label
    pusernameLabel = Label(frame1, text='Patient Username: ', font=('times new roman', 14, 'bold'), bg='white',
                           fg='blue')
    pusernameLabel.place(x=30, y=35)

    # pusername entry
    # pusernameEntry = Entry(frame1, font=('times new roman', 14), bg='white', textvariable=pusernamevar)
    # pusernameEntry.place(x=220, y=35)

    db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
    cur = db.cursor()
    cur.execute("SELECT username FROM users where user_type = 'Patient'")
    pusernames = cur.fetchall()

    pusernames = [pusername[0] for pusername in pusernames]  # Extracting department IDs from the fetched data

    pusernameVar = tk.StringVar()
    pusername = pusernames[0]
    # print(pusername)
    pusernameVar.set(pusername)  # Set the default value to the first department ID

    pusernameEntry = tk.OptionMenu(frame1, pusernameVar, *pusernames)

    pusernameEntry.config(width=20)
    pusernameEntry.config(width=20)
    pusernameEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    pusernameEntry["menu"].config(bg="blue", fg="white")
    # bgroupEntry.grid(row=4, column=1, sticky='w', padx=5)
    pusernameEntry.place(x=220, y=35)

    # symptoms label
    symptomsLabel = Label(frame1, text='Symptoms: ', font=('times new roman', 14, 'bold'), bg='white', fg='blue')
    symptomsLabel.place(x=30, y=95)

    # symptoms entry
    symptomsEntry = Entry(frame1, font=('times new roman', 14), bg='white', textvariable=symptomsvar)
    symptomsEntry.place(x=220, y=95)

    appidEntry = Entry(frame1, font=('times new roman', 1), bg='white', textvariable=appidvar)
    appidEntry.place(x=220, y=95)

    # dusername label
    dusernameLabel = Label(frame1, text='Doctor Username: ', font=('times new roman', 14, 'bold'), bg='white',
                           fg='blue')
    dusernameLabel.place(x=450, y=35)

    # dusername entry
    # dusernameEntry = Entry(frame1, font=('times new roman', 14), bg='white', textvariable=dusernamevar)
    # dusernameEntry.place(x=640, y=35)

    db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
    cur = db.cursor()
    cur.execute("SELECT username FROM users where user_type = 'Doctor'")
    dusernames = cur.fetchall()

    dusernames = [dusername[0] for dusername in dusernames]  # Extracting department IDs from the fetched data

    dusernameVar = tk.StringVar()
    dusername = dusernames[0]
    # print(pusername)
    dusernameVar.set(dusername)  # Set the default value to the first department ID

    dusernameEntry = tk.OptionMenu(frame1, dusernameVar, *dusernames)

    dusernameEntry.config(width=20)
    dusernameEntry.config(width=20)
    dusernameEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dusernameEntry["menu"].config(bg="blue", fg="white")
    # bgroupEntry.grid(row=4, column=1, sticky='w', padx=5)
    dusernameEntry.place(x=640, y=35)

    # date label
    dateLabel = Label(frame1, text='Date: ', font=('times new roman', 14, 'bold'), bg='white', fg='blue')
    dateLabel.place(x=450, y=95)

    # date entry dropdown
    # date of birth entry
    dateVar = tk.StringVar()
    dateVar.set("01")
    dateEntry = tk.OptionMenu(
        frame1, dateVar, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
        "31")
    dateEntry.config(width=20)
    dateEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dateEntry["menu"].config(bg="blue", fg="white")
    dateEntry.place(x=640, y=95)

    # month of birth label
    monthLabel = Label(frame1, text='Month:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    monthLabel.place(x=450, y=145)

    # month of birth entry
    # making a drop down menu for month of birth
    monthVar = tk.StringVar()
    monthVar.set("01")
    monthEntry = tk.OptionMenu(
        frame1, monthVar, "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12")
    monthEntry.config(width=20)
    monthEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    monthEntry["menu"].config(bg="blue", fg="white")
    monthEntry.place(x=640, y=145)

    # buttons for the admin appointment info window
    # add button
    addButton = Button(frame1, text='Add', font=('times new roman', 14, 'bold'), bg='blue', fg='white', width=20, bd=0,
                       activebackground="blue", activeforeground="white", command=validateinfo)
    addButton.place(x=930, y=30)

    updateButton = Button(frame1, text='Update', font=('times new roman', 14, 'bold'), bg='blue', fg='white', width=20,
                          bd=0,
                          activebackground="blue", activeforeground="white", command=updateInfo)
    updateButton.place(x=930, y=90)

    clrButton = Button(frame1, text='C', font=('times new roman', 14, 'bold'), bg='blue', fg='white', width=4,
                          bd=0,
                          activebackground="blue", activeforeground="white", command=clear)
    clrButton.place(x=1170, y=150)

    # back button
    backButton = Button(frame1, text='Back', font=('times new roman', 14, 'bold'), bg='blue', fg='white', width=20,
                        bd=0,
                        activebackground="blue", activeforeground="white", command=admin_page)
    backButton.place(x=930, y=150)

    fetchdata(apptable)

    adminAppointmentInfoWindow.mainloop()


#******************************************** DOCTOR ***********************************************************************************


def doctor(username):

    def logout():
        if(askyesno("logout", "are you sure you want to logout?")):
            doctorDashboard.destroy()
            login()

    def docpres_page():
        doctorDashboard.destroy()
        docpres(username)

    def docapp():
        doctorDashboard.destroy()
        doctorappointment(username)


    def doctor_info_page():
        doctorDashboard.destroy()
        doctor_info(username)

    # doctor dashboard window
    doctorDashboard = Tk()
    doctorDashboard.geometry('1280x650+0+0')
    doctorDashboard.title("Doctor Dashboard")
    doctorDashboard.resizable(False, False)

    # dummy bg.jpg
    bg = ImageTk.PhotoImage(file="doctor1.jpg")
    bgLabel = tk.Label(doctorDashboard, image=bg)
    bgLabel.image_names = bg
    bgLabel.place(x=175, y=-10, relwidth=1, relheight=1)
    frame = tk.Frame(doctorDashboard, bg='white', width=345, height=650)
    frame.place(relx=0, rely=0)

    # making heading label
    heading = Label(doctorDashboard, text='Doctor Dashboard', font=('times new roman', 28, 'bold underline'), bg='white',
                    fg='blue')
    heading.grid(row=0, column=0, sticky='w', padx=25, pady=25)

    # personal info button
    personalbtn = Button(doctorDashboard, text='Personal info', font=('times new roman', 20, 'bold'), bg='blue', fg='white',
                         width=15, bd=0, activebackground="blue", activeforeground="white", command=doctor_info_page)
    personalbtn.grid(row=1, column=0, sticky='w', padx=50, pady=25)

    # patient info button
    # patientbtn = Button(doctorDashboard, text='Patient info', font=('times new roman', 20, 'bold'), bg='blue', fg='white',
    #                     width=15, bd=0, activebackground="blue", activeforeground="white")
    # patientbtn.grid(row=2, column=0, sticky='w', padx=50, pady=25)

    # appointment info button
    appointmentbtn = Button(doctorDashboard, text='Appointment info', font=('times new roman', 20, 'bold'), bg='blue',
                            fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=docapp)
    appointmentbtn.grid(row=3, column=0, sticky='w', padx=50, pady=25)

    # prescription info button
    prescriptionbtn = Button(doctorDashboard, text='Prescription info', font=('times new roman', 20, 'bold'), bg='blue',
                             fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=docpres_page)
    prescriptionbtn.grid(row=4, column=0, sticky='w', padx=50, pady=25)

    #accomodation info button
    logoutbtn = Button(doctorDashboard, text='Log out', font=('times new roman', 20, 'bold'), bg='blue', fg='white', width=15, bd=0, activebackground="blue", activeforeground="white", command=logout)
    logoutbtn.grid(row=5, column=0, sticky='w', padx=50 , pady = 15)

    doctorDashboard.mainloop()


#******************************************** DOCTOR PERSONAL INFO ***********************************************************************************


def doctor_info(username):
    def back():
        doctor_info_window.destroy()
        # calling the doctor dashboard window
        doctor(username)

    def saveInfo():
        newfirstname = (doctor_first_name.get())
        newlastname = (doctor_last_name.get())
        newgender = (genderVar.get())
        newcontact = (doctor_contact.get())
        newemail = (doctor_email.get())
        newhousenumber = (doctor_house_no.get())
        newstreet = (doctor_street.get())
        newsector = (doctor_sector.get())
        newcity = (doctor_city.get())
        newspec = (doctor_spec.get())
        newdept = (departmentVar.get())
        username = doctor_username.get()
        newdob = f"{yearVar.get()}-{monthVar.get()}-{dateVar.get()}"

        cur.execute(f"""UPDATE users SET first_name = '{newfirstname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET last_name = '{newlastname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET gender = '{newgender}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET contact = '{newcontact}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET email = '{newemail}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET house_number = '{newhousenumber}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET street = '{newstreet}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET sector = '{newsector}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET city = '{newcity}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET date_of_birth = '{newdob}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""select deptid from dept where dname = '{newdept}'""")
        newdeptid = cur.fetchone()
        cur.execute(f"""UPDATE doctor SET deptid = '{newdeptid[0]}' WHERE dusername = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE doctor SET specialization = '{newspec}' WHERE dusername = '{username}'""")
        db.commit()
        messagebox.showinfo("success", "Information has been updated")


    # doctor info window
    # global doctor_info_window
    # make new window for doctor info
    doctor_info_window = Tk()
    doctor_info_window.geometry('1280x650+0+0')
    doctor_info_window.title("Doctor Info")
    doctor_info_window.resizable(False, False)

    # making the text variables for the entries to store the data
    doctor_username = StringVar()
    doctor_first_name = StringVar()
    doctor_last_name = StringVar()
    doctor_salary = StringVar()
    doctor_contact = StringVar()
    doctor_email = StringVar()
    doctor_house_no = StringVar()
    doctor_street = StringVar()
    doctor_sector = StringVar()
    doctor_city = StringVar()
    doctor_spec = StringVar()
    yearVar = StringVar()


    frame = tk.Frame(doctor_info_window, bg='white', width=1280, height=650)
    frame.place(relx=0, rely=0)

    # making heading label
    heading = Label(doctor_info_window, text='Doctor Info', font=('times new roman', 28, 'bold underline'), bg='white',
                    fg='blue')
    heading.place(x=450, y=25)

    # doctor username label
    doctor_username_label = Label(doctor_info_window, text="Username:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                  bg='white', fg='blue')
    doctor_username_label.place(x=40, y=100)

    # doctor username entry
    doctor_username_entry = Entry(doctor_info_window, textvariable=doctor_username, width=20,
                                  font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_username_entry.place(x=40, y=130)

    # doctor first name label
    doctor_first_name_label = Label(doctor_info_window, text="First Name:",
                                    font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_first_name_label.place(x=40, y=180)

    # doctor first name entry
    doctor_first_name_entry = Entry(doctor_info_window, width=20, textvariable=doctor_first_name,
                                    font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_first_name_entry.place(x=40, y=210)

    # doctor last name label
    doctor_last_name_label = Label(doctor_info_window, text="Last Name:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                   bg='white', fg='blue')
    doctor_last_name_label.place(x=40, y=260)

    # doctor last name entry
    doctor_last_name_entry = Entry(doctor_info_window, width=20, textvariable=doctor_last_name,
                                   font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_last_name_entry.place(x=40, y=290)

    # #doctor password label
    # doctor_password_label = Label(doctor_info_window, text="Password:", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    # doctor_password_label.place(x=40, y=340)

    # #doctor password entry
    # doctor_password_entry = Entry(doctor_info_window, width=20, font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    # doctor_password_entry.place(x=40, y=370)

    # doctor salary label
    doctor_salary_label = Label(doctor_info_window, text="Salary:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_salary_label.place(x=40, y=340)


    # doctor salary entry
    doctor_salary_entry = Entry(doctor_info_window, width=20, textvariable=doctor_salary,
                                font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_salary_entry.place(x=40, y=370)

    # doctor email label
    doctor_email_label = Label(doctor_info_window, text="Email:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                               bg='white', fg='blue')
    doctor_email_label.place(x=40, y=420)

    # doctor email entry
    doctor_email_entry = Entry(doctor_info_window, width=20, textvariable=doctor_email,
                               font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_email_entry.place(x=40, y=450)

    # doctor phone label
    doctor_contact_label = Label(doctor_info_window, text="Contact(+92):", font=('Microsoft Yahei UI Light', 12, 'bold'),
                           bg='white', fg='blue')
    doctor_contact_label.place(x=40, y=500)

    # doctor phone entry
    doctor_contact_entry = Entry(doctor_info_window, width=20, textvariable=doctor_contact,
                                 font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_contact_entry.place(x=40, y=530)

    # doctor house number label
    doctor_house_no_label = Label(doctor_info_window, text="House No:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                  bg='white', fg='blue')
    doctor_house_no_label.place(x=400, y=100)

    # doctor house number entry
    doctor_house_no_entry = Entry(doctor_info_window, width=20, textvariable=doctor_house_no,
                                  font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_house_no_entry.place(x=400, y=130)

    # doctor street label
    doctor_street_label = Label(doctor_info_window, text="Street:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_street_label.place(x=400, y=180)

    # doctor street entry
    doctor_street_entry = Entry(doctor_info_window, width=20, textvariable=doctor_street,
                                font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_street_entry.place(x=400, y=210)

    # doctor sector label
    doctor_sector_label = Label(doctor_info_window, text="Sector:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_sector_label.place(x=400, y=260)

    # doctor sector entry
    doctor_sector_entry = Entry(doctor_info_window, width=20, textvariable=doctor_sector,
                                font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_sector_entry.place(x=400, y=290)

    # doctor city label
    doctor_city_label = Label(doctor_info_window, text="City:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                              bg='white', fg='blue')
    doctor_city_label.place(x=400, y=340)

    # doctor city entry
    doctor_city_entry = Entry(doctor_info_window, width=20, textvariable=doctor_city,
                              font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_city_entry.place(x=400, y=370)

    # doctor dob entry
    # day of birth label
    dateLabel = Label(doctor_info_window, text='B.Date:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    dateLabel.place(x=400, y=430)

    # date of birth entry
    # making a drop down menu for date of birth
    # date of birth entry
    dateVar = tk.StringVar()
    dateVar.set("01")
    dateEntry = tk.OptionMenu(
        doctor_info_window, dateVar, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
        "31")
    dateEntry.config(width=15)
    dateEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dateEntry["menu"].config(bg="blue", fg="white")
    dateEntry.place(x=470, y=430)

    # month of birth label
    monthLabel = Label(doctor_info_window, text='B.Month:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    monthLabel.place(x=400, y=480)

    # month of birth entry
    # making a drop down menu for month of birth
    monthVar = tk.StringVar()
    monthVar.set("01")
    monthEntry = tk.OptionMenu(
        doctor_info_window, monthVar, "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12")
    monthEntry.config(width=15)
    monthEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    monthEntry["menu"].config(bg="blue", fg="white")
    monthEntry.place(x=470, y=480)

    # year of birth label
    yearLabel = Label(doctor_info_window, text='B.Year:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    yearLabel.place(x=400, y=540)

    # year of birth entry
    yearEntry = Entry(doctor_info_window, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=yearVar)
    yearEntry.place(x=470, y=540, width=130)

    # doctor speciality label
    doctor_spec_label = Label(doctor_info_window, text="Specialization:",
                              font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_spec_label.place(x=750, y=100)

    # doctor speciality entry
    doctor_spec_entry = Entry(doctor_info_window, textvariable=doctor_spec, width=20,
                              font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_spec_entry.place(x=750, y=130)

    # doctor department label
    doctor_department_label = Label(doctor_info_window, text="Department:",
                                    font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    doctor_department_label.place(x=750, y=180)

    # doctor department entry
    departmentVar = StringVar()
    departmentVar.set("Cardiology")
    doctor_department_entry = tk.OptionMenu(
        doctor_info_window, departmentVar, "Cardiology", "Neurology", "Orthopedics", "Gynecology", "Oncology",
        "Dermatology", "Pediatrics", "Psychiatry", "Urology", "Ophthalmology", "Gastroenterology", "Endocrinology",
        "Nephrology", "Pulmonology", "Rheumatology", "Anesthesiology", "Radiology", "Pathology", "General Surgery",
        "Plastic Surgery", "Thoracic Surgery", "Colon and Rectal Surgery", "Obstetrics and Gynecology",
        "Otolaryngology", "Oral and Maxillofacial Surgery", "Orofacial Pain", "Orthodontics", "Periodontics",
        "Prosthodontics", "Pediatric Dentistry", "Endodontics", "Public Health Dentistry",
        "Oral and Maxillofacial Pathology", "Oral and Maxillofacial Radiology", "Dental Anesthesiology",
        "Dental Public Health", "Oral Biology", "Oral Medicine", "Forensic Odontology", "Veterinary Dentistry")
    doctor_department_entry.config(width=25, bg="blue", fg="white", activebackground="blue", activeforeground="white")
    doctor_department_entry["menu"].config(bg="blue", fg="white")
    doctor_department_entry.place(x=750, y=210)

    # doctor gender label
    doctor_gender_label = Label(doctor_info_window, text="Gender: ", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_gender_label.place(x=750, y=260)

    # doctor gender entry
    genderVar = StringVar()
    genderVar.set("Male")
    doctor_gender_entry = tk.OptionMenu(
        doctor_info_window, genderVar, "Male", "Female", "Other")
    doctor_gender_entry.config(width=25, bg="blue", fg="white", activebackground="blue", activeforeground="white")
    doctor_gender_entry["menu"].config(bg="blue", fg="white")
    doctor_gender_entry.place(x=750, y=290)

    # ********************FRAME FOR PICTURE*************************
    # adding a new frame
    picture_frame = tk.Frame(doctor_info_window, bg="BLUE", width=240, height=290)
    picture_frame.pack()
    picture_frame.place(x=1020, y=200)
    #
    # adding a label to the frame
    bg = ImageTk.PhotoImage(file="doc1.png")
    picture_label = tk.Label(picture_frame, image=bg)
    picture_label.pack()
    picture_label.place(x=5, y=5)
    # print(username)
    cur.execute(f"""select * from doctor_personal where username = '{username}'""")
    doc = cur.fetchone()
    doctor_username.set(doc[0])
    doctor_username_entry.config(state="readonly")
    doctor_first_name.set(doc[1])
    doctor_last_name.set(doc[2])
    genderVar.set(doc[3])
    doctor_contact.set(doc[4])
    doctor_email.set(doc[5])
    doctor_house_no.set(doc[6])
    doctor_street.set(doc[7])
    doctor_sector.set(doc[8])
    doctor_city.set(doc[9])
    dateVar.set(doc[10])
    monthVar.set(doc[11])
    yearVar.set(doc[12])
    departmentVar.set(doc[13])
    doctor_spec.set(doc[14])
    doctor_salary.set(doc[15])
    doctor_salary_entry.config(state='readonly')
    # doctor_contact.set(doc[9])

    # ******************* BUTTONS *******************
    # update button
    update_button = Button(doctor_info_window, text="Update", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='blue',
                           fg='white', width=20, bd=1, height=2, activebackground="blue", activeforeground="white", command=saveInfo)
    update_button.place(x=750, y=400)

    # BACK BUTTON
    back_button = Button(doctor_info_window, text="Back", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='blue',
                         fg='white', width=20, bd=1, height=2, activebackground="blue", activeforeground="white",
                         command=back)
    back_button.place(x=750, y=500)

    doctor_info_window.mainloop()



#******************************************** DOCTOR APPOINTMENT INFO ***********************************************************************************


def doctorappointment(docusername):
    global persid
    appointmentWindow = Tk()
    appointmentWindow.title("Prescription")
    appointmentWindow.geometry("1280x650+0+0")
    appointmentWindow.config(bg="white")
    appointmentWindow.resizable(False, False)

    def doctor_page():
        appointmentWindow.destroy()
        doctor(docusername)


    #     #database connection and all data fetching function
    def fetch_data(prestable):
        db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
        cur = db.cursor()

        #printing the table form database

        cur.execute(f""" select pusername, first_name, last_name, symptoms, appstatus, appdate
        from appointment a join patient p using (pusername) join users u where u.username = p.pusername and
         dusername = '{docusername}'""")
        rows = cur.fetchall()
        # print(rows)
        if len(rows) != 0:
            prestable.delete(* prestable.get_children())
            for i in rows:
                prestable.insert('', END, values=i)
            db.commit()
        db.close()



    # adding upper frame for the table
    upperFrame = Frame(appointmentWindow, bg='white', width=1260,
                       height=350)
    upperFrame.place(x=5, y=0)

    # adding table tree view to the upper frame
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), bg='blue', fg='white')
    prestable = ttk.Treeview(upperFrame, style="Treeview")
    prestable['columns'] = ("Patient Username", "First Name", "Last Name", "Symptoms", "Appointment Status", "Appointment Date")
    prestable.place(x=15, y=10, width=1230, height=340)

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=340)




    prestable.heading("Patient Username", text="Patient Username", anchor=CENTER)

    prestable.heading("First Name", text="First Name", anchor=CENTER)
    prestable.heading("Last Name", text="Last Name", anchor=CENTER)
    prestable.heading("Symptoms", text="Symptoms", anchor=CENTER)
    prestable.heading("Appointment Status", text="Appointment Status", anchor=CENTER)
    prestable.heading("Appointment Date", text="Appointment Date", anchor=CENTER)


    prestable['show'] = 'headings'

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=390)

    # prestable.column("#0", width=0, stretch=NO)
    prestable.column("Patient Username", anchor=CENTER, width=80)

    prestable.column("First Name", anchor=CENTER, width=80)
    prestable.column("Last Name", anchor=CENTER, width=80)
    prestable.column("Symptoms", anchor=CENTER, width=80)
    prestable.column("Appointment Status", anchor=CENTER, width=80)
    prestable.column("Appointment Date", anchor=CENTER, width=80)





    # adding lower frame for the textfields or entries
    lowerFrame = Frame(appointmentWindow, bg="white",  width=1260,
                       height=225)
    lowerFrame.place(x=5, y=400)



    # back button to the lower frame
    backButton = Button(lowerFrame, text="Back", font=("Times New Roman Bold", 14), fg="white", bg="blue", command=doctor_page)
    backButton.place(x=990, y=150, width=200, height=45)

    fetch_data(prestable)

    appointmentWindow.mainloop()



#******************************************** DOCTOR PRESCRIPTION INFO ***********************************************************************************


def docpres(docusername):
    docpresWindow = Tk()
    docpresWindow.title("Prescription")
    docpresWindow.geometry("1280x650+0+0")
    docpresWindow.config(bg="white")
    docpresWindow.resizable(False, False)

    def doctor_page():
        docpresWindow.destroy()
        doctor(docusername)



    def clear():
        pusernameVar.set("")
        pstatusVar.set("")
        medicineVar.set("")
        diseaseVar.set("")
        dosageVar.set("")
        frequencyVar.set("")
        routeVar.set("")
        durationVar.set("")




    def addPres():
        if pusernameVar.get() == "" or medicineVar.get() == "" or diseaseVar.get() == "" or dosageVar.get() == "" or frequencyVar.get() == "" or routeVar.get() == "" or durationVar.get() == "":
            messagebox.showerror("Error", "All fields are required")

        else:
            db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
            my_cursor = db.cursor()
            my_cursor.execute("""INSERT INTO PRESCRIPTION(medicine, disease ,dosage ,frequency ,route ,duration ,pusername , dusername
            ) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)""", (medicineVar.get(), diseaseVar.get(), dosageVar.get(), frequencyVar.get(), routeVar.get(), durationVar.get(), pusernameVar.get(), docusername))
            db.commit()
            db.close()
            messagebox.showinfo("success", "Information has been updated")
            clear()
            refreshTable(prestable)



    #     #database connection and all data fetching function
    def fetch_data(prestable):
        db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
        cur = db.cursor()

        #printing the table form database

        cur.execute(f""" select * from doctor_pres where dusername = '{docusername}'""")
        rows = cur.fetchall()
        # print(rows)
        if len(rows) != 0:
            prestable.delete(* prestable.get_children())
            for i in rows:
                prestable.insert('', END, values=i)
            db.commit()
        db.close()


    def getdata(event=''):
        currow = prestable.focus()
        data = prestable.item(currow)
        row = data['values']


        pusernameVar.set(row[0])

        pstatusVar.set(row[4])

        medicineVar.set(row[7])
        diseaseVar.set(row[8])
        dosageVar.set(row[9])
        frequencyVar.set(row[10])
        routeVar.set(row[11])
        durationVar.set(row[12])

        global selectedpresid

        cur.execute(f""" select presid from prescription where pusername = '{pusernameVar.get()}' and dusername = '{docusername}'
        and medicine = '{medicineVar.get()}'""")
        selectedpresid = cur.fetchone()
        selectedpresid = selectedpresid[0]


    def refreshTable(table):
        for item in table.get_children():  # list of every row's id
            table.delete(item)
        fetch_data(table)


    # adding upper frame for the table
    upperFrame = Frame(docpresWindow, bg='white', width=1260,
                       height=350)
    upperFrame.place(x=5, y=0)

    # adding table tree view to the upper frame
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), bg='blue', fg='white')
    prestable = ttk.Treeview(upperFrame, style="Treeview")
    prestable['columns'] = (
    "Patient Username", "Blood Group", "Height", "Weight", "Patient Status", "First Name", "Last Name", "Medicine",
    "Disease", "Dosage", "Frequency", "Route", "Duration")
    prestable.place(x=15, y=10, width=1230, height=340)

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=340)



    prestable.heading("#0", text="", anchor=CENTER)
    prestable.heading("Patient Username", text="Patient Username", anchor=CENTER)
    prestable.heading("Blood Group", text="Blood Group", anchor=CENTER)
    prestable.heading("Height", text="Height", anchor=CENTER)
    prestable.heading("Weight", text="Weight", anchor=CENTER)
    prestable.heading("Patient Status", text="Patient Status", anchor=CENTER)
    prestable.heading("First Name", text="First Name", anchor=CENTER)
    prestable.heading("Last Name", text="Last Name", anchor=CENTER)
    prestable.heading("Medicine", text="Medicine", anchor=CENTER)
    prestable.heading("Disease", text="Disease", anchor=CENTER)
    prestable.heading("Dosage", text="Dosage", anchor=CENTER)
    prestable.heading("Frequency", text="Frequency", anchor=CENTER)
    prestable.heading("Route", text="Route", anchor=CENTER)
    prestable.heading("Duration", text="Duration", anchor=CENTER)

    prestable['show'] = 'headings'

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=390)

    prestable.column("#0", width=0, stretch=NO)
    prestable.column("Patient Username", anchor=CENTER, width=110)
    prestable.column("Blood Group", anchor=CENTER, width=80)
    prestable.column("Height", anchor=CENTER, width=50)
    prestable.column("Weight", anchor=CENTER, width=50)
    prestable.column("Patient Status", anchor=CENTER, width=80)
    prestable.column("First Name", anchor=CENTER, width=70)
    prestable.column("Last Name", anchor=CENTER, width=70)
    prestable.column("Medicine", anchor=CENTER, width=50)
    prestable.column("Disease", anchor=CENTER, width=50)
    prestable.column("Dosage", anchor=CENTER, width=50)
    prestable.column("Frequency", anchor=CENTER, width=70)
    prestable.column("Route", anchor=CENTER, width=40)
    prestable.column("Duration", anchor=CENTER, width=60)

    prestable.bind("<ButtonRelease-1>", getdata)

    def updateInfo():
        # global selectedpusername
        db = mysql.connector.connect(
            host='127.0.0.1',
            user='admin',
            password='admin',
            port=3306,
            database='hospital'
        )
        cur = db.cursor()



        print(pusernameVar.get())
        print(pusernameVar.get())
        print(pusernameVar.get())
        cur.execute("UPDATE PRESCRIPTION SET MEDICINE = %s, DISEASE = %s, DOSAGE = %s, FREQUENCY = %s, ROUTE = %s, DURATION = %s WHERE presid = %s", (medicineVar.get(), diseaseVar.get(), dosageVar.get(), frequencyVar.get(), routeVar.get(), durationVar.get(), selectedpresid))
        db.commit()
        cur.execute(f"UPDATE patient SET pstatus = '{pstatusVar.get()}' where pusername = '{pusernameVar.get()}'")
        db.commit()
        db.close()
        # clear()
        messagebox.showinfo("Success", "Prescription Updated")
        refreshTable(prestable)




    # adding lower frame for the textfields or entries
    lowerFrame = Frame(docpresWindow, bg="white", width=1260,
                       height=225)
    lowerFrame.place(x=5, y=400)


    # making the text variables for the entries
    pusernameVar = StringVar()

    pstatusVar = StringVar()
    firstnameVar = StringVar()
    lastnameVar = StringVar()
    medicineVar = StringVar()
    diseaseVar = StringVar()
    dosageVar = StringVar()
    frequencyVar = StringVar()
    routeVar = StringVar()
    durationVar = StringVar()



    # making the labels and entries for the lower frame
    pusernameLabel = Label(lowerFrame, text="Patient Username", font=("Times New Roman Bold", 12), bg="white",
                           fg="blue")
    pusernameLabel.place(x=10, y=30)



    db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
    cur = db.cursor()
    cur.execute("SELECT username FROM users where user_type = 'Patient'")
    pusernames = cur.fetchall()


    pusernames = [pusername[0] for pusername in pusernames]  # Extracting department IDs from the fetched data

    pusernameVar = tk.StringVar()
    pusername = pusernames[0]
    # print(pusername)
    pusernameVar.set(pusername)  # Set the default value to the first department ID

    pusernameEntry = tk.OptionMenu(lowerFrame, pusernameVar, *pusernames)

    pusernameEntry.config(width=20)
    pusernameEntry.config(width=20)
    pusernameEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    pusernameEntry["menu"].config(bg="blue", fg="white")
    # bgroupEntry.grid(row=4, column=1, sticky='w', padx=5)
    pusernameEntry.place(x=150, y=30)



    pstatusLabel = Label(lowerFrame, text="Patient Status", font=("Times New Roman Bold", 12), bg="white", fg="blue")
    pstatusLabel.place(x=10, y=80)

    pstatusEntry = Entry(lowerFrame, font=("Times New Roman Bold", 12), bg="white", fg="black", textvariable=pstatusVar)
    pstatusEntry.place(x=150, y=80)



    medicineLabel = Label(lowerFrame, text="Medicine", font=("Times New Roman Bold", 12), bg="white", fg="blue")
    medicineLabel.place(x=10, y=180)

    medicineEntry = Entry(lowerFrame, font=("Times New Roman Bold", 12), bg="white", fg="black", textvariable=medicineVar)
    medicineEntry.place(x=150, y=180)

    diseaseLabel = Label(lowerFrame, text="Disease", font=("Times New Roman Bold", 12), bg="white", fg="blue")
    diseaseLabel.place(x=10, y=130)

    diseaseEntry = Entry(lowerFrame, font=("Times New Roman Bold", 12), bg="white", fg="black", textvariable=diseaseVar)
    diseaseEntry.place(x=150, y=130)

    dosageLabel = Label(lowerFrame, text="Dosage", font=("Times New Roman Bold", 12), bg="white", fg="blue")
    dosageLabel.place(x=500, y=30)

    dosageEntry = Entry(lowerFrame, font=("Times New Roman Bold", 12), bg="white", fg="black", textvariable=dosageVar)
    dosageEntry.place(x=650, y=30)

    frequencyLabel = Label(lowerFrame, text="Frequency", font=("Times New Roman Bold", 12), bg="white", fg="blue")
    frequencyLabel.place(x=500, y=80)

    frequencyEntry = Entry(lowerFrame, font=("Times New Roman Bold", 12), bg="white", fg="black",
                           textvariable=frequencyVar)
    frequencyEntry.place(x=650, y=80)

    routeLabel = Label(lowerFrame, text="Route", font=("Times New Roman Bold", 12), bg="white", fg="blue")
    routeLabel.place(x=500, y=130)

    routeEntry = Entry(lowerFrame, font=("Times New Roman Bold", 12), bg="white", fg="black", textvariable=routeVar)
    routeEntry.place(x=650, y=130)

    durationLabel = Label(lowerFrame, text="Duration", font=("Times New Roman Bold", 12), bg="white", fg="blue")
    durationLabel.place(x=500, y=180)

    durationEntry = Entry(lowerFrame, font=("Times New Roman Bold", 12), bg="white", fg="black", textvariable=durationVar)
    durationEntry.place(x=650, y=180)

    # adding buttons to the lower frame
    addButton = Button(lowerFrame, text="Add", height=2, font=("Times New Roman Bold", 14), fg="white", bg="blue", command=addPres)
    addButton.place(x=990, y=30, width=200, height=45)

    # edit button to the lower frame
    editButton = Button(lowerFrame, text="Update", height=2, font=("Times New Roman Bold", 14), fg="white", bg="blue", command=updateInfo)
    editButton.place(x=990, y=90, width=200, height=45)

    # edit button to the lower frame
    clrButton = Button(lowerFrame, text="C", height=2, font=("Times New Roman Bold", 14), fg="white", bg="blue", command=clear)
    clrButton.place(x=1200, y=150, width=40, height=45)

    # back button to the lower frame
    backButton = Button(lowerFrame, text="Back", font=("Times New Roman Bold", 14), fg="white", bg="blue", command=doctor_page)
    backButton.place(x=990, y=150, width=200, height=45)

    fetch_data(prestable)

    docpresWindow.mainloop()


#******************************************** PATIENT ***********************************************************************************


    #view profile function
def patient(username):
    def patient_page():
        patient_dashboard.destroy()
        patient_info(username)

    def logout():
        if(askyesno("logout", "are you sure you want to logout?")):
            patient_dashboard.destroy()
            login()

    def patapp_page():
        patient_dashboard.destroy()
        patientapp(username)

    def patpres_page():
        patient_dashboard.destroy()
        patpres(username)


    #making the patient dashboard
    patient_dashboard = Tk()
    patient_dashboard.title("Patient Dashboard")
    patient_dashboard.geometry("1280x650+0+0")
    patient_dashboard.resizable(False, False)

    #making the frame for the patient dashboard
    bg = ImageTk.PhotoImage(file="patient1.jpg")
    bgLabel = tk.Label(patient_dashboard, image=bg)
    bgLabel.image_names = bg
    bgLabel.place(x=175, y=-10, relwidth=1, relheight=1)
    frame = tk.Frame(patient_dashboard, bg='white', width=345, height=650)
    frame.place(relx=0, rely=0)


    #making the heading for the patient dashboard
    heading = tk.Label(frame, text="Patient Dashboard", font=("times new roman", 20, "bold underline"), bg="white", fg="blue")
    heading.place(x=50, y=50)


    #making the buttons for the patient dashboard
    viewProfile = tk.Button(frame, text="View Profile", width=20, height=2, fg="white",  bg="blue", font=("times new roman", 20, "bold"), command=patient_page)
    viewProfile.place(x=50, y=150)

    viewAppointments = tk.Button(frame, text="View Appointments", width=20, height=2, fg="white", bg="blue", font=("times new roman", 20, "bold"), command=patapp_page)
    viewAppointments.place(x=50, y=250)

    viewPrescriptions = tk.Button(frame, text="View Prescriptions", width=20, height=2, fg="white", bg="blue", font=("times new roman", 20, "bold"), command=patpres_page)
    viewPrescriptions.place(x=50, y=350)

    logout = tk.Button(frame, text="Logout", width=20, height=2, fg="white", bg="blue", font=("times new roman", 20, "bold"), command=logout)
    logout.place(x=50, y=450)

    patient_dashboard.mainloop()



#******************************************** PATIENT PERSONAL INFO ***********************************************************************************

def patient_info(username):
    db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )

    cur = db.cursor()
    def back():
        patient_info_window.destroy()
        # calling the doctor dashboard window
        patient(username)

    def saveInfo():
        newfirstname = (patient_first_name.get())
        newlastname = (patient_last_name.get())
        newgender = (genderVar.get())
        newcontact = (patient_contact.get())
        newemail = (patient_email.get())
        newhousenumber = (patient_house_no.get())
        newstreet = (patient_street.get())
        newsector = (patient_sector.get())
        newcity = (patient_city.get())
        newweight = weightVar.get()
        newheight = heightVar.get()
        newbgroup = bgroupVar.get()
        # username = patient_username.get()
        newdob = f"{yearVar.get()}-{monthVar.get()}-{dateVar.get()}"

        cur.execute(f"""UPDATE users SET first_name = '{newfirstname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET last_name = '{newlastname}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET gender = '{newgender}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET contact = '{newcontact}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET email = '{newemail}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET house_number = '{newhousenumber}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET street = '{newstreet}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET sector = '{newsector}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET city = '{newcity}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE users SET date_of_birth = '{newdob}' WHERE username = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE patient SET height = '{newheight}' WHERE pusername = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE patient SET weight = '{newweight}' WHERE pusername = '{username}'""")
        db.commit()
        cur.execute(f"""UPDATE patient SET blood_group = '{newbgroup}' WHERE pusername = '{username}'""")
        db.commit()
        messagebox.showinfo("success", "Information has been updated")


    # doctor info window
    # global doctor_info_window
    # make new window for doctor info
    patient_info_window = Tk()
    patient_info_window.geometry('1280x650+0+0')
    patient_info_window.title("Patient Info")
    patient_info_window.resizable(False, False)

    # making the text variables for the entries to store the data
    patient_username = StringVar()
    patient_first_name = StringVar()
    patient_last_name = StringVar()
    # doctor_salary = StringVar()
    patient_contact = StringVar()
    patient_email = StringVar()
    patient_house_no = StringVar()
    patient_street = StringVar()
    patient_sector = StringVar()
    patient_city = StringVar()
    heightVar = StringVar()
    weightVar = StringVar()
    heightVar = StringVar()
    yearVar = StringVar()


    frame = tk.Frame(patient_info_window, bg='white', width=1280, height=650)
    frame.place(relx=0, rely=0)

    # making heading label
    heading = Label(patient_info_window, text='Patient Info', font=('times new roman', 28, 'bold underline'), bg='white',
                    fg='blue')
    heading.place(x=450, y=25)

    # doctor username label
    patient_username_label = Label(patient_info_window, text="Username:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                   bg='white', fg='blue')
    patient_username_label.place(x=40, y=100)

    # doctor username entry
    patient_username_entry = Entry(patient_info_window, textvariable=patient_username, width=20,
                                   font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_username_entry.place(x=40, y=130)

    # doctor first name label
    patient_first_name_label = Label(patient_info_window, text="First Name:",
                                     font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_first_name_label.place(x=40, y=180)

    # doctor first name entry
    patient_first_name_entry = Entry(patient_info_window, width=20, textvariable=patient_first_name,
                                     font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_first_name_entry.place(x=40, y=210)

    # doctor last name label
    patient_last_name_label = Label(patient_info_window, text="Last Name:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                    bg='white', fg='blue')
    patient_last_name_label.place(x=40, y=260)

    # doctor last name entry
    patient_last_name_entry = Entry(patient_info_window, width=20, textvariable=patient_last_name,
                                    font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_last_name_entry.place(x=40, y=290)




    # blood group label
    bgroupLabel = Label(patient_info_window, text='Blood Group:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    bgroupLabel.place(x=40, y=340)

    # blood group entry
    bgroupVar = tk.StringVar()
    bgroupVar.set("B+")
    bgroupEntry = tk.OptionMenu(
        patient_info_window, bgroupVar, "A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-")

    bgroupEntry.config(width=20)
    bgroupEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    bgroupEntry["menu"].config(bg="blue", fg="white")
    # bgroupEntry.grid(row=4, column=1, sticky='w', padx=5)
    bgroupEntry.place(x=40, y=370)

    # doctor email label
    patient_email_label = Label(patient_info_window, text="Email:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    patient_email_label.place(x=40, y=420)

    # doctor email entry
    patient_email_entry = Entry(patient_info_window, width=20, textvariable=patient_email,
                                font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_email_entry.place(x=40, y=450)

    # doctor phone label
    patient_contact_label = Label(patient_info_window, text="Contact(+92):", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                  bg='white', fg='blue')
    patient_contact_label.place(x=40, y=500)

    # doctor phone entry
    patient_contact_entry = Entry(patient_info_window, width=20, textvariable=patient_contact,
                                  font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_contact_entry.place(x=40, y=530)

    # doctor house number label
    patient_house_no_label = Label(patient_info_window, text="House No:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                   bg='white', fg='blue')
    patient_house_no_label.place(x=400, y=100)

    # doctor house number entry
    patient_house_no_entry = Entry(patient_info_window, width=20, textvariable=patient_house_no,
                                   font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_house_no_entry.place(x=400, y=130)

    # doctor street label
    patient_street_label = Label(patient_info_window, text="Street:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                 bg='white', fg='blue')
    patient_street_label.place(x=400, y=180)

    # doctor street entry
    patient_street_entry = Entry(patient_info_window, width=20, textvariable=patient_street,
                                 font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_street_entry.place(x=400, y=210)

    # doctor sector label
    patient_sector_label = Label(patient_info_window, text="Sector:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                 bg='white', fg='blue')
    patient_sector_label.place(x=400, y=260)

    # doctor sector entry
    patient_sector_entry = Entry(patient_info_window, width=20, textvariable=patient_sector,
                                 font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_sector_entry.place(x=400, y=290)

    # doctor city label
    patient_city_label = Label(patient_info_window, text="City:", font=('Microsoft Yahei UI Light', 12, 'bold'),
                               bg='white', fg='blue')
    patient_city_label.place(x=400, y=340)

    # doctor city entry
    patient_city_entry = Entry(patient_info_window, width=20, textvariable=patient_city,
                               font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    patient_city_entry.place(x=400, y=370)

    # doctor dob entry
    # day of birth label
    dateLabel = Label(patient_info_window, text='B.Date:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    dateLabel.place(x=400, y=430)

    # date of birth entry
    # making a drop down menu for date of birth
    # date of birth entry
    dateVar = tk.StringVar()
    dateVar.set("01")
    dateEntry = tk.OptionMenu(
        patient_info_window, dateVar, "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
        "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30",
        "31")
    dateEntry.config(width=15)
    dateEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    dateEntry["menu"].config(bg="blue", fg="white")
    dateEntry.place(x=470, y=430)

    # month of birth label
    monthLabel = Label(patient_info_window, text='B.Month:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    monthLabel.place(x=400, y=480)

    # month of birth entry
    # making a drop down menu for month of birth
    monthVar = tk.StringVar()
    monthVar.set("01")
    monthEntry = tk.OptionMenu(
        patient_info_window, monthVar, "01", "02", "03", "04", "05", "06", "07", "08", "09",
        "10", "11", "12")
    monthEntry.config(width=15)
    monthEntry.config(bg="blue", fg="white", activebackground="blue", activeforeground="white")
    monthEntry["menu"].config(bg="blue", fg="white")
    monthEntry.place(x=470, y=480)

    # year of birth label
    yearLabel = Label(patient_info_window, text='B.Year:', font=('times new roman', 12, 'bold'), bg='white', fg='blue')
    yearLabel.place(x=400, y=540)

    # year of birth entry
    yearEntry = Entry(patient_info_window, font=('times new roman', 12, 'bold'), bg='white', fg='blue', textvariable=yearVar)
    yearEntry.place(x=470, y=540, width=130)

    # doctor speciality label
    heightLabel = Label(patient_info_window, text="Height:",
                        font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    heightLabel.place(x=750, y=100)

    # doctor speciality entry
    heightEntry = Entry(patient_info_window, textvariable=heightVar, width=20,
                        font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    heightEntry.place(x=750, y=130)


    # doctor speciality label
    weightLabel = Label(patient_info_window, text="Weight:",
                        font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    weightLabel.place(x=750, y=180)

    # doctor speciality entry
    weightEntry = Entry(patient_info_window, textvariable=weightVar, width=20,
                        font=('Microsoft Yahei UI Light', 12, 'bold'), bg='white', fg='blue')
    weightEntry.place(x=750, y=210)


    # doctor gender label
    doctor_gender_label = Label(patient_info_window, text="Gender: ", font=('Microsoft Yahei UI Light', 12, 'bold'),
                                bg='white', fg='blue')
    doctor_gender_label.place(x=750, y=260)

    # doctor gender entry
    genderVar = StringVar()
    genderVar.set("Male")
    doctor_gender_entry = tk.OptionMenu(
        patient_info_window, genderVar, "Male", "Female", "Other")
    doctor_gender_entry.config(width=25, bg="blue", fg="white", activebackground="blue", activeforeground="white")
    doctor_gender_entry["menu"].config(bg="blue", fg="white")
    doctor_gender_entry.place(x=750, y=290)

    # ********************FRAME FOR PICTURE*************************
    # adding a new frame
    picture_frame = tk.Frame(patient_info_window, bg="BLUE", width=230, height=230)
    picture_frame.pack()
    picture_frame.place(x=1020, y=200)
    #
    # adding a label to the frame
    bg = ImageTk.PhotoImage(file="pat1.png")
    picture_label = tk.Label(picture_frame, image=bg)
    picture_label.pack()
    picture_label.place(x=5, y=5)
    # print(username)
    cur.execute(f"""select * from patient_personal where username = '{username}'""")
    doc = cur.fetchone()
    patient_username.set(doc[0])
    patient_first_name.set(doc[1])
    patient_last_name.set(doc[2])
    genderVar.set(doc[3])
    patient_contact.set(doc[4])
    patient_email.set(doc[5])
    patient_house_no.set(doc[6])
    patient_street.set(doc[7])
    patient_sector.set(doc[8])
    patient_city.set(doc[9])
    dateVar.set(doc[10])
    monthVar.set(doc[11])
    yearVar.set(doc[12])
    # departmentVar.set(doc[13])
    heightVar.set(doc[13])
    weightVar.set(doc[14])
    bgroupVar.set(doc[15])
    # doctor_contact.set(doc[9])

    # ******************* BUTTONS *******************
    # update button
    update_button = Button(patient_info_window, text="Update", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='blue',
                           fg='white', width=20, bd=1, height=2, activebackground="blue", activeforeground="white", command=saveInfo)
    update_button.place(x=750, y=400)

    # BACK BUTTON
    back_button = Button(patient_info_window, text="Back", font=('Microsoft Yahei UI Light', 12, 'bold'), bg='blue',
                         fg='white', width=20, bd=1, height=2, activebackground="blue", activeforeground="white",
                         command=back)
    back_button.place(x=750, y=500)

    patient_info_window.mainloop()


#******************************************** PATIENT APPOINTMENT INFO ***********************************************************************************


def patientapp(patusername):
    patappWindow = Tk()
    patappWindow.title("Prescription")
    patappWindow.geometry("1280x650+0+0")
    patappWindow.config(bg="white")
    patappWindow.resizable(False, False)

    def patient_page():
        patappWindow.destroy()
        patient(patusername)


    #     #database connection and all data fetching function
    def fetch_data(prestable):
        db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
        cur = db.cursor()

        #printing the table form database

        cur.execute(f""" select dusername, first_name, last_name, symptoms, appstatus, appdate
        from appointment a join doctor d using (dusername) join users u where u.username = d.dusername and
         pusername = '{patusername}'""")
        rows = cur.fetchall()
        # print(rows)
        if len(rows) != 0:
            prestable.delete(* prestable.get_children())
            for i in rows:
                prestable.insert('', END, values=i)
            db.commit()
        db.close()



    # adding upper frame for the table
    upperFrame = Frame(patappWindow, bg='white', width=1260,
                       height=350)
    upperFrame.place(x=5, y=0)

    # adding table tree view to the upper frame
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), bg='blue', fg='white')
    prestable = ttk.Treeview(upperFrame, style="Treeview")
    prestable['columns'] = ("Doctor Username", "First Name", "Last Name", "Symptoms", "Appointment Status", "Appointment Date")
    prestable.place(x=15, y=10, width=1230, height=340)

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=340)




    prestable.heading("Doctor Username", text="Doctor Username", anchor=CENTER)

    prestable.heading("First Name", text="First Name", anchor=CENTER)
    prestable.heading("Last Name", text="Last Name", anchor=CENTER)
    prestable.heading("Symptoms", text="Symptoms", anchor=CENTER)
    prestable.heading("Appointment Status", text="Appointment Status", anchor=CENTER)
    prestable.heading("Appointment Date", text="Appointment Date", anchor=CENTER)


    prestable['show'] = 'headings'

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=390)

    # prestable.column("#0", width=0, stretch=NO)
    prestable.column("Doctor Username", anchor=CENTER, width=80)

    prestable.column("First Name", anchor=CENTER, width=80)
    prestable.column("Last Name", anchor=CENTER, width=80)
    prestable.column("Symptoms", anchor=CENTER, width=80)
    prestable.column("Appointment Status", anchor=CENTER, width=80)
    prestable.column("Appointment Date", anchor=CENTER, width=80)





    # adding lower frame for the textfields or entries
    lowerFrame = Frame(patappWindow, bg="white", width=1260,
                       height=225)
    lowerFrame.place(x=5, y=400)



    # back button to the lower frame
    backButton = Button(lowerFrame, text="Back", font=("Times New Roman Bold", 14), fg="white", bg="blue", command=patient_page)
    backButton.place(x=990, y=150, width=200, height=45)

    fetch_data(prestable)

    patappWindow.mainloop()


#******************************************** PATIENT PRESCRIPTION INFO ***********************************************************************************


def patpres(patusername):
    global persid
    patpresWindow = Tk()
    patpresWindow.title("Prescription")
    patpresWindow.geometry("1280x650+0+0")
    patpresWindow.config(bg="white")
    patpresWindow.resizable(False, False)

    def patient_page():
        patpresWindow.destroy()
        patient(patusername)


    #     #database connection and all data fetching function
    def fetch_data(prestable):
        db = mysql.connector.connect(
        host='127.0.0.1',
        user='admin',
        password='admin',
        port=3306,
        database='hospital'
    )
        cur = db.cursor()

        #printing the table form database

        cur.execute(f""" select * from patient_pres where pusername = '{patusername}'""")
        rows = cur.fetchall()
        # print(rows)
        if len(rows) != 0:
            prestable.delete(* prestable.get_children())
            for i in rows:
                prestable.insert('', END, values=i)
            db.commit()
        db.close()
        db.close()




    # adding upper frame for the table
    upperFrame = Frame(patpresWindow, bg='white', width=1260,
                       height=350)
    upperFrame.place(x=5, y=0)

    # adding table tree view to the upper frame
    style = ttk.Style()
    style.configure("Treeview.Heading", font=('times new roman', 14), bg='blue', fg='white')
    prestable = ttk.Treeview(upperFrame, style="Treeview")
    prestable['columns'] = (
    "Doctor Username", "First Name", "Last Name", "Medicine",
    "Disease", "Dosage", "Frequency", "Route", "Duration")
    prestable.place(x=15, y=10, width=1230, height=340)

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=340)




    # prestable.heading("#0", text="", anchor=CENTER)
    prestable.heading("Doctor Username", text="Doctor Username", anchor=CENTER)
    prestable.heading("First Name", text="First Name", anchor=CENTER)
    prestable.heading("Last Name", text="Last Name", anchor=CENTER)
    prestable.heading("Medicine", text="Medicine", anchor=CENTER)
    prestable.heading("Disease", text="Disease", anchor=CENTER)
    prestable.heading("Dosage", text="Dosage", anchor=CENTER)
    prestable.heading("Frequency", text="Frequency", anchor=CENTER)
    prestable.heading("Route", text="Route", anchor=CENTER)
    prestable.heading("Duration", text="Duration", anchor=CENTER)

    prestable['show'] = 'headings'

    prestable.pack(fill=BOTH, expand=1)

    prestable.place(x=5, y=2, width=1245, height=390)

    # prestable.column("#0", width=0, stretch=NO)
    prestable.column("Doctor Username", anchor=CENTER, width=110)
    prestable.column("First Name", anchor=CENTER, width=70)
    prestable.column("Last Name", anchor=CENTER, width=70)
    prestable.column("Medicine", anchor=CENTER, width=50)
    prestable.column("Disease", anchor=CENTER, width=50)
    prestable.column("Dosage", anchor=CENTER, width=50)
    prestable.column("Frequency", anchor=CENTER, width=70)
    prestable.column("Route", anchor=CENTER, width=40)
    prestable.column("Duration", anchor=CENTER, width=60)



    # adding lower frame for the textfields or entries
    lowerFrame = Frame(patpresWindow, bg="white", width=1260,
                       height=225)
    lowerFrame.place(x=5, y=400)



    # back button to the lower frame
    backButton = Button(lowerFrame, text="Back", font=("Times New Roman Bold", 14), fg="white", bg="blue", command=patient_page)
    backButton.place(x=990, y=150, width=200, height=45)

    fetch_data(prestable)

    patpresWindow.mainloop()


login()


