import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Function to validate login credentials
def validate_login(username, password):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python_quiz"
        )

        cursor = conn.cursor()

        # Execute SQL query to check if username and password match
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            return True, user[0]  # Return True and the user ID
        else:
            return False, None

    except mysql.connector.Error as e:
        print("Error:", e)
        return False, None

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Function to handle login button click
def login_clicked():
    username = username_entry.get()
    password = password_entry.get()

    login_status, user_id = validate_login(username, password)
    if login_status:
        messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
        login_window.destroy()
        # Save the score in the database
        save_score(username)
        import quiz_program  # Import the main quiz program module
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to save the score in the database
def save_score(username):
    try:
        # Connect to MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="python_quiz"
        )

        cursor = conn.cursor()

        # Insert the score into the scores table
        cursor.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (username, 0))  # Assuming initial score is 0

        # Commit the transaction
        conn.commit()

    except mysql.connector.Error as e:
        print("Error:", e)

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

# Create the login window
login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("400x400")

# Create labels and entries for username and password
username_label = tk.Label(login_window, text="Username:", bg="lightblue", fg="black")
username_label.pack(pady=5)
username_entry = tk.Entry(login_window)
username_entry.pack(pady=5)

password_label = tk.Label(login_window, text="Password:", bg="lightblue", fg="black")
password_label.pack(pady=5)
password_entry = tk.Entry(login_window, show="*")
password_entry.pack(pady=5)

# Create the login button
login_btn = tk.Button(login_window, text="Login", command=login_clicked, bg="lightblue", fg="red")
login_btn.pack(pady=10)

# Start the login event loop
login_window.mainloop()
