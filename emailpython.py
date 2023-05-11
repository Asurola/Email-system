# imports
import sqlite3
import sys
import re
from tkinter import *
from tkinter import messagebox
from tkinter import scrolledtext as st

# define SQL connection function
def connect():
    # Database conncetion with try and except to catch errors
    try:
        sqlite3.connect("email2.db")
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False
    return True

# Define login function
def login_func():
    global email
    # Email and password entries 
    email = email_entry.get()
    password = password_entry.get()
    # if loop to validate email and password
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter an email address in a valid format. \nAn example of a valid format is: 6Days@Gmail.com") 
        return 
    # Check if the email and password are valid by referring to the database
    try:
        with sqlite3.connect("email2.db") as db:
            cursor = db.cursor()
            # query variable to select email and password from database
            query = 'SELECT * FROM users WHERE email=? AND password=?'
            # combined email and password entries with query
            cursor.execute(query, (email, password))
            # fetchone() method to retrieve the first row of the query result
            result = cursor.fetchone()
            cursor.close()
            # if loop to validate email and password
            if result:
                messagebox.showinfo("Login Successful", "Welcome!")
                return True
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
                return False
    except sqlite3.Error as e:
        print("Database error: ", e)
        return False

# Define email validation function
def is_valid_email(email):  
    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return True
    else:
        return False

# Define finish button function for register window
def finish_button_func():
    global register
    # Assign entries to variables
    email = reg_email_entry.get()
    password = reg_password_entry.get()
    confirm_password = confirm_password_entry.get()
    # Check if the email is valid
    if not is_valid_email(email):
        messagebox.showerror("Invalid Email", "Please enter an email address in a valid format. \n An example of a valid format is: 6Days@Gmail.com") 
        return  
    # Check if the password and confirm password match
    if password == confirm_password:
        # Check if the email already exists in the table
        db = sqlite3.connect("email2.db")
        cursor = db.cursor()
        query = 'SELECT * FROM users WHERE email=?'
        cursor.execute(query, (email,))
        result = cursor.fetchone()

        # If the email already exists, show an error message
        if result:
            messagebox.showerror("Registration Failed", "Email address already exists.")
            register.focus()
            reg_email_entry.focus()
            cursor.close()
        # Insert the new user into the table
        else:
            query = 'INSERT INTO users (email, password) VALUES (?, ?)'
            cursor.execute(query, (email, password))
            db.commit()
            cursor.close()
            messagebox.showinfo("Registration Successful", "You can now login.")
            register.destroy()
    else:
        # If the passwords do not match, show an error message
        messagebox.showerror("Registration Failed", "Passwords do not match.")
        register.focus()
        confirm_password_entry.focus()

# Define register button function
def register_button():
    global reg_email_entry
    global reg_password_entry
    global confirm_password_entry
    global finish_button
    global check_email
    global register
    # Create the register window and configure the window
    register = Tk()
    register.title("Register")
    register.configure(background="orchid")
    register.resizable(height=False, width=False)
    # Create the email and password labels and entries and place them in the window
    reg_email_label = Label(register, text="Email:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="orchid")
    reg_email_label.grid(row=0, column=0, padx=5, pady=5)
    reg_email_entry = Entry(register, font=("Bahnschrift Semibold", 20), borderwidth=5, highlightthickness=1, highlightcolor="orchid", highlightbackground="orchid")
    reg_email_entry.grid(row=0, column=1, padx=5, pady=5)
    reg_password_label = Label(register, text="Password:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="orchid")
    reg_password_label.grid(row=1, column=0, padx=5, pady=5)
    reg_password_entry = Entry(register, font=("Bahnschrift Semibold", 20), show="*", borderwidth=5, highlightthickness=0.5, highlightcolor="orchid", highlightbackground="orchid")
    reg_password_entry.grid(row=1, column=1, padx=5, pady=5)
    confirm_password_label = Label(register, text="Confirm Password:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="orchid")
    confirm_password_label.grid(row=2, column=0, padx=5, pady=5)
    confirm_password_entry = Entry(register, font=("Bahnschrift Semibold", 20), show="*", borderwidth=5, highlightthickness=0.5, highlightcolor="orchid", highlightbackground="orchid")
    confirm_password_entry.grid(row=2, column=1, padx=5, pady=5)
    finish_button = Button(register, text="Finish", font=("Bahnschrift", 20), fg="green", command=finish_button_func)
    finish_button.grid(row=3, column=1, padx=40, pady=5)

    register.mainloop()

# Create the login window and configure the window
login = Tk()
login.title("Email Login")
login.configure(background='light blue')
login.resizable(height=False, width=False)

# Create the email and password labels and entries and place them in the window
email_label = Label(login, text="Email:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
email_label.grid(row=0, column=0, padx=5, pady=5)
email_entry = Entry(login, font=("Bahnschrift Semibold", 20), borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
email_entry.grid(row=0, column=1, padx=5, pady=5)
password_label = Label(login, text="Password:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = Entry(login, font=("Bahnschrift Semibold", 20), show="*", borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
password_entry.grid(row=1, column=1, padx=5, pady=5)


# Define a function that will insert email data into the database
def insert(sender_email, receiver_email, title, content):
    # Connect to the database
    db = sqlite3.connect('email2.db')
    cursor = db.cursor()
    # Check if the email address already exists in the table
    cursor.execute("SELECT * FROM emails WHERE sender_email=?", (sender_email,))
    existing_row = cursor.fetchone()
    if existing_row:
        # If the email already exists, update the existing row instead of inserting a new one
        cursor.execute("UPDATE emails SET receiver_email=?, title=?, content=? WHERE sender_email=?", (receiver_email, title, sender_email, content))
    else:
        # If the email doesn't exist, insert a new row
        cursor.execute("INSERT INTO emails (content, receiver_email, title, sender_email) VALUES (?, ?, ?, ?)", (sender_email, receiver_email, title, content))
    # Commit the changes to the database
    db.commit()
    print("Data inserted")
    # Close the connection to the database
    db.close()

# define a function that will view recieved emails
def view_inbox():
    global inbox
    def view_email(row):
        global email_view
        # Create a new window to display the email and configure the window
        email_view = Tk()
        email_view.title("Email")
        email_view.configure(background="light blue")
        email_view.resizable(height=False, width=False)
        # Create the labels and entries for the email and place them in the window
        sender_email_label = Label(email_view, text="Sender Email:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
        sender_email_label.grid(row=0, column=0, padx=5, pady=5)
        sender_email_entry = Entry(email_view, font=("Bahnschrift Semibold", 20), width=50, borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
        sender_email_entry.grid(row=0, column=1, padx=5, pady=5)
        # Insert the sender email into the entry and make it read only
        sender_email_entry.insert(0, row[1])
        sender_email_entry.config(state="readonly")
        receiver_email_label = Label(email_view, text="Receiver Email:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
        receiver_email_label.grid(row=1, column=0, padx=5, pady=5)
        receiver_email_entry = Entry(email_view, font=("Bahnschrift Semibold", 20), width=50, borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
        receiver_email_entry.grid(row=1, column=1, padx=5, pady=5)
        # Insert the receiver email into the entry and make it read only
        receiver_email_entry.insert(0, row[2])
        receiver_email_entry.config(state="readonly")
        title_label = Label(email_view, text="Title:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
        title_label.grid(row=2, column=0, padx=5, pady=5)
        title_entry = Entry(email_view, font=("Bahnschrift Semibold", 20), width=50, borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
        title_entry.grid(row=2, column=1, padx=5, pady=5)
        # Insert the title into the entry and make it read only
        title_entry.insert(0, row[3])
        title_entry.config(state="readonly")
        content_label = Label(email_view, text="Content:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
        content_label.grid(row=3, column=0, padx=5, pady=5)
        # Create a scrolled text box to display the content of the email
        content_entry = st.ScrolledText(email_view, font=("Bahnschrift Semibold", 20), width=49, height=15, borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
        content_entry.grid(row=3, column=1, padx=5, pady=5) 
        # Insert the content into the entry and make it read only
        content_entry.insert(INSERT, row[4])
        # Disable the entry so the user can't edit it
        content_entry.config(state="disabled")
        email_view.mainloop()

    # Connect to the database
    db=sqlite3.connect('email2.db')
    cursor = db.cursor()
    cursor.execute("Select * from emails where receiver_email=?", (email_entry.get(),))
    rows = cursor.fetchall()
    # GUI window for inbox display and configuration
    inbox = Tk()
    inbox.title("Inbox")
    inbox.configure(background="light blue")
    # Loop that assigns a button to each email present for respective logged in user 
    for row in rows:
        email_button = Button(inbox, text=row[1], font=("Bahnschrift", 20), width=50, fg="blue", command=lambda row=row: view_email(row))
        email_button.grid(row=rows.index(row), column=0, padx=5, pady=5)
    # If no emails are found, display a message 
    if not rows:
        no_emails = Label(inbox, text="Empty inbox :(", font=("Bahnschrift", 20), bg="light blue")
        no_emails.grid(row=0, column=0, padx=5, pady=5)
    inbox.mainloop()
    # Close the database connection
    db.close()


# define function that takes user entries for recipient address, title and content and stores it in email database
def send_email():
    global compose_email
    global recipient_entry
    global title_entry
    global content_entry
    global sender_email
    # Get the user entries
    receiver_email = recipient_entry.get()
    title = title_entry.get()
    # Get the content from the scrolled text box
    content = content_entry.get("1.0", END)
    sender_email = email_entry.get()
    # Check if the email entry is valid
    if not is_valid_email(receiver_email):
        compose_email.focus() 
        messagebox.showerror("Invalid Email", "Please enter an email address in a valid format in the recipient box. \nAn example of a valid format is: 6Days@Gmail.com") 
        return 
    # Insert the email into the database
    insert(content, receiver_email, title, sender_email)
    # Clear the entries
    recipient_entry.delete(0, END)
    title_entry.delete(0, END)
    content_entry.delete("1.0", END)
    print("Email sent")

# Gui buttons and entries for the compose email window 
def compose_email_func():
    global recipient_entry
    global title_entry
    global content_entry
    global send_button
    global compose_email
    global compose_email_func
    # Create the compose email window and configure the window
    compose_email = Tk()
    compose_email.title("Compose Email")
    compose_email.configure(background="light blue")
    compose_email.resizable(height=False, width=False)
    compose_email.columnconfigure(0, weight=1)
    compose_email.rowconfigure(0, weight=1)
    # Create the labels and entries and place them in the window
    recipient_label = Label(compose_email, text="Recipient:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
    recipient_label.grid(row=0, column=0, padx=5, pady=5)
    recipient_entry = Entry(compose_email, font=("Bahnschrift Semibold", 20), width=60, borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
    recipient_entry.grid(row=0, column=1, padx=5, pady=5)
    title_label = Label(compose_email, text="Subject:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
    title_label.grid(row=1, column=0, padx=5, pady=5)
    title_entry = Entry(compose_email, font=("Bahnschrift Semibold", 20), width=60, borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
    title_entry.grid(row=1, column=1, padx=5, pady=5)
    content_label = Label(compose_email, text="Content:", font=("Bahnschrift Semibold", 20, UNDERLINE), fg="blue", bg="light blue")
    content_label.grid(row=2, column=0, padx=5, pady=5)
    content_entry = st.ScrolledText(compose_email, font=("Bahnschrift Semibold", 20), height=15, width=59, borderwidth=5, highlightthickness=0.5, highlightcolor="light blue", highlightbackground="light blue")
    content_entry.grid(row=2, column=1, padx=5, pady=5)
    send_button = Button(compose_email, text="Send", font=("Bahnschrift", 20), fg="green", command=send_email)
    send_button.grid(row=3, column=1, padx=5, pady=5)
    compose_email.mainloop()


# create a combined function for the email window and login withdrawal
def login_funcs():
    if login_func():
        login.withdraw()
        email_window()
    else:
        # If login is unsuccessful, focus on the email entry field again for user input
        login.tk_focusNext().focus()

# create a logout function that closes the email windows and exits the program
def logout():
    sys.exit()
    
    
#create email home window 
def email_window():
    global compose_email_func
    global email
    # Create the email window and configure the window
    email = Tk()
    email.title("Email")
    email.geometry("300x150")
    email.configure(background="light blue")
    email.resizable(height=False, width=False)
    email.columnconfigure(0, weight=1)
    email.rowconfigure(0, weight=1)
    # Create the buttons and place them in the window
    compose_button = Button(email, text="Compose", font=("Bahnschrift", 20), fg="green", command=compose_email_func)
    compose_button.grid(row=0, column=0, padx=5, pady=5, sticky=W)
    inbox_button = Button(email, text="Inbox", font=("Bahnschrift", 20), fg="green", command=view_inbox)
    inbox_button.grid(row=0, column=1, padx=5, pady=5, sticky=W)
    logout_button = Button(email, text="Logout", font=("Bahnschrift", 20), fg="red", command=logout)
    logout_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=S)
    email.columnconfigure(0, weight=1)
    email.rowconfigure(0, weight=1)
    email.mainloop()

# Create login and register buttons and place them in the window
login_button = Button(login, text="Login", font=("Bahnschrift", 20), fg="green", command=login_funcs)
login_button.grid(row=2, column=1, padx=40, pady=5)
reg_button = Button(login, text="Register", font=("Bahnschrift", 20), fg="red", command=register_button)
reg_button.grid(row=3, column=1, padx=25, pady=5)
register_label = Label(login, text="Don't have an account?", font=("Bahnschrift", 16), fg="dark blue", bg="light blue")
register_label.grid(row=3, column=0, padx=50, pady=5, sticky=E)

login.mainloop()

connect()
