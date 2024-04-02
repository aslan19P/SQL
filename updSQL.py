import mysql.connector
import hashlib
from tkinter import *

win = Tk()
win.geometry("4000x200")

def create_database():
    mycursor = mydb.cursor()
    mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
    mycursor.execute("CREATE TABLE IF NOT EXISTS test(id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255))")


def settings():
    setting = Toplevel(win)
    setting.title("settings")
    setting.geometry("250x250")

    def close_window():
        setting.destroy()

    host_entry = Entry(setting)
    user_host_entry = Entry(setting)
    password_host_entry = Entry(setting)
    database_host_entry = Entry(setting)

    host_entry.grid(row=0, column=1, padx=5, pady=5)
    user_host_entry.grid(row=1, column=1, padx=5, pady=5)
    password_host_entry.grid(row=2, column=1, padx=5, pady=5)
    database_host_entry.grid(row=3, column=1, padx=5, pady=5)

    def host():
        host_val = host_entry.get()
        user = user_host_entry.get()
        password = password_host_entry.get()
        global database
        database = database_host_entry.get()

        try:
            global mydb
            mydb = mysql.connector.connect(
                host=host_val,
                user=user,
                password=password,
                database=database
            )
            create_database()
            print("Connected to the database successfully")
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print("Error:", err)

    apply = Button(setting, text="Применить", command=lambda: host())
    apply.grid(row=4, column=1, padx=5, pady=5)

    close = Button(setting, text="Закрыть", command=lambda: close_window())
    close.grid(row=4, column=3, padx=5, pady=5)

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password="",
  database="users"
)


def hide_label(user_name_label):
    user_name_label.config(text="")

def hide_label1(user_password_label):
    user_password_label.config(text="")

def hide_label2(user_name_label_login):
    user_name_label_login.config(text="")

def hide_label3(user_password_label_login):
    user_password_label_login.config(text="")

user_name_entry = Entry(win, width=25)
user_name_entry.grid(column=1, row=1, pady=5, padx=10)

user_password_entry = Entry(win, width=25)
user_password_entry.grid(column=1, row=2, pady=2, padx=5)

register_button = Button(win, text="зарегистрироваться", font=('Times', 12) ,command=lambda:register_user(user_name_entry.get(), user_password_entry.get()))
register_button.grid(column=1, row=3, pady=4)

login_button = Button(win, text="Вход", font=('Times', 12) ,command=lambda:login_user(user_name_entry.get(), user_password_entry.get()))
login_button.grid(column=1, row=4, pady=4)

setting = Button(win, text="settings", command=lambda:settings())
setting.grid(column=4, row=10)

def register_user(user_name, user_password):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM test WHERE username=%s", (user_name,))
    if mycursor.fetchone():
        
        user_name_label = Label(win, text="Пользователь существует", font=('fixed', 10))
        user_name_label.grid(column=1, row=5)
        win.after(2000, lambda: hide_label(user_name_label))

    else:
        user_password = hashlib.sha256(user_password.encode()).hexdigest()
        mycursor.execute("INSERT INTO test (username, password) VALUES (%s, %s)", (user_name, user_password))

        user_password_label = Label(win, text="вы зарегистрированы", font=('fixed', 10))
        user_password_label.grid(column=1, row=5)
        win.after(2000, lambda: hide_label1(user_password_label))
        mydb.commit()


def login_user(user_name, user_password):
    mycursor = mydb.cursor()
    user_password = hashlib.sha256(user_password.encode()).hexdigest()
    mycursor.execute("SELECT * FROM test WHERE username=%s AND password=%s", (user_name, user_password))
    user = mycursor.fetchone()
    if user:
        user_name_label_login = Label(win, text=f"Добро пожаловать, {user_name}!", font=('fixed', 10))
        user_name_label_login.grid(column=1, row=5)
        win.after(2000, lambda: hide_label2(user_name_label_login))
    else:
        user_password_label_login = Label(win, text="Неправильный логин или пароль", font=('fixed', 10))
        user_password_label_login.grid(column=1, row=5)
        win.after(2000, lambda: hide_label3(user_password_label_login))


win.grid_columnconfigure(0, minsize=60)
win.grid_columnconfigure(1, minsize=60)
win.grid_columnconfigure(2, minsize=60)
win.grid_columnconfigure(3, minsize=60)

win.grid_rowconfigure(1, minsize=30)
win.grid_rowconfigure(2, minsize=30)
win.grid_rowconfigure(3, minsize=30)
win.grid_rowconfigure(4, minsize=30)
win.grid_rowconfigure(5, minsize=30)

win.mainloop()