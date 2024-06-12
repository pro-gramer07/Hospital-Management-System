from tkinter import *
import mysql
from mysql import connector
import bcrypt
import tkinter as tk
from tkinter import ttk, messagebox

db = mysql.connector.connect(
    host='127.0.0.1',
    user='admin',
    password='admin',
    port=3306,
    database='hospital'
)

cur = db.cursor()
dob = f"1989-03-05"
entered_password = "admin"
password_hash = bcrypt.hashpw(entered_password.encode('utf-8'), bcrypt.gensalt())
password_hashed = password_hash.decode('utf-8')
cur.execute(f"""INSERT INTO users (username, password_hash, user_type, first_name, last_name, gender, contact, email, house_number, street, sector, city, date_of_birth)
               VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s , %s)""",
            ("admin", password_hashed, "Admin", "Admin", "User", "Male",
             "3147984326", "adminuser@gmail.com", "44b",
             "31E", "I-8/2", "Islamabad", dob))

db.commit()
