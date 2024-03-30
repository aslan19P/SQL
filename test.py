import mysql.connector
import hashlib
from tkinter import *

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="users"
)

win = Tk()
win.geometry("300x600")

mycursor = mydb.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS user(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")

user_name_entry = Entry(win)
user_name_entry.pack()

user_password_entry = Entry(win)
user_password_entry.pack()

bt = Button(win, text="зарегистрироваться", command=lambda:register_user(user_name_entry.get(), user_password_entry.get()))
bt.pack()

def register_user(user_name, user_password):
    mycursor.execute("SELECT * FROM user WHERE username=%s", (user_name,))
    if mycursor.fetchone():
        Label(win, text="Такой пользователь существует").pack()
    else:
        user_password = hashlib.sha256(user_password.encode()).hexdigest()
        mycursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (user_name, user_password))
        Label(win, text="Вы зарегистрированы !").pack()
        mydb.commit()
        


win.mainloop()