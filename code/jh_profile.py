import pygame
import os
'''import sys'''
import threading
import json
import tkinter as tk
from tkinter import messagebox

# Password strength detection
def is_password_strong(password):
    #this function is calculate the "password" got least than 8 alphabets or not
    if len(password) < 8:
        #this function is mean the computer giving your comment to correct your password.
        return "Password length must be at least 8 alphabets."
    #inside the () meaning is the password must got more than one uppercase letter in the password. 
    if not any(char.isupper() for char in password):
        return "Password must contain at least one capital letter." #this sentence is mean if the password inside didn't have more than one capital letter,it will print "password must contain at least one capital letter".  #inside the () meaning is the password must got more than one lowercase letter in the password. 
    if not any(char.islower() for char in password):
        return "Password must contain at least one small letter." #this sentence is mean if the password inside didn't have more than one small letter, it will print out "password must contain at least one  small letter". #inside the () meaning is the password must got more than one numbers in the password. 
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number." #this sentence is mean if the password inside didn't have more than one numbers, it will print "Password must contain at least one number.". #inside the () meaning is the password must got more than one numbers in the password.
    if not any(char in "@#$%&*" for char in password):
        return "Password must contain at least one special character (such as @, #, $, %)." #this sentence is mean if the password inside didn't have more than one symbol, it will print out "Password must contain at least one special character (such as @, #, $, %).". 
    return None

# Register function
def register(): #here is the register part
    username = username_entry.get() # this is the input to our user (username)
    password = password_entry.get() # this is the input to our user (password)

    if not username or not password: #if user input the username and password are wrong....
        messagebox.showwarning("Enter Error", "Please key in Username and Password!") #it will show out the warning using the tkinter function which is messagebox
        return

    # Password Strength Detection
    password_error = is_password_strong(password)
    if password_error: #if the password are not strong it will show out the error using the tkinter function which is message
        messagebox.showerror("Password not strong enough", password_error)
        return
    
        # Whether user exist or not
    if os.path.exists(f"{username}.txt"): # this whole thing is a function in python to help us to check whether got a file or not #os this is a module and path is a connection between code and file, however, you can say path like a road or highway between a plece to place.
        messagebox.showerror("Error", "User already exists. Please log in directly.") #if error it will print out "Error", "User already exists. Please log in directly." by using a function in tkinter which is messagebox.
        return #it meaning is finsh this knid of thing then can quit the function or stop the function.
    
    user_data = {
        "password": password,
        "game1": {
            "Coins": 0,
            "Diamonds": 0,
            "Time Taken": 0.0
        },
        "game2": {
            "Coins": 0,
            "Diamonds": 0,
            "Time Taken": 0.0
        }
    }

    # Store username and password into textfile
    with open(f"{username}.txt", "w") as file: #this is our file that store the username and password #however using txt is not safe, easy to hack our info, but now foundation only please forgive it.
        json.dump(user_data, file)

    messagebox.showinfo("Success", "Registration completed! You can proceed to log in.") #else you will get the info is "Success", "Registration completed! You can proceed to log in." with using the function in tkinter which is messagebox.
    clear_entries()

# Login function
def login(): # here is log in part
    global logged_in, username
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning("Error", "Please key in Username and Password!")
        return

    # Checking Username and Password
    if os.path.exists(f"{username}.txt"):
        with open(f"{username}.txt", "r") as file:
            user_data = json.load(file)  

        stored_password = user_data["password"]

        if password == stored_password:
            messagebox.showinfo("Success", "You have successfully logged in!")
            app.withdraw()  # Hide the login window

            def start_game():
                import qx_test_main
                qx_test_main.platform_map(username)
            
            threading.Thread(target=start_game).start()
           
        else:
            messagebox.showerror("Error", "Wrong Password, Please try again!")
            logged_in = False  # Log in failed, does not enter game
    else:
        messagebox.showerror("Error", "This user does not exist, Please register a new account.")
        logged_in = False  # Log in failed, does not enter game

    clear_entries()

# Empty input
def clear_entries():
    try: #try-except function is make sure our coding don't not have error 
        username_entry.delete(0, tk.END) #(username)this meaning when user are not input any thing  from 0 until tk.end
        password_entry.delete(0, tk.END) #for this is same function, but this sentence is for password.
    except Exception as e:
        print(f"Error clearing entries: {e}")

# Creating login page
def create_login_window():
    global app, username_entry, password_entry, logged_in

    app = tk.Tk() #create a tkinter window
    app.title("Registration and Log in") # the title for top of window 
    app.geometry("350x300") # the window size, width and height

    def on_close():
        global logged_in
        logged_in = False
        pygame.quit() #Closes the Pygame (if it's running), stopping any sounds and function. but our login are not added any BGM.
        exit()

    app.protocol("WM_DELETE_WINDOW", on_close) #"WM_DELETE_WINDOW" this sentence is represents the window close event #i use this is prevent accidental closure and ensures cleanup

    # Username label and input space
    username_label = tk.Label(app, text="Username:")
    username_label.pack(pady=5)
    username_entry = tk.Entry(app) #create a space to input the username and when the user input the username
    username_entry.pack(pady=5)

    # Password label and input space
    password_label = tk.Label(app, text="Password:") #text="Password:" the word inside text will show out on window, also inside the label
    password_label.pack(pady=5)
    password_entry = tk.Entry(app, show="*") #create a space to input the password and when the user input the password, it will genarate to * this symbol
    password_entry.pack(pady=5)

    # Password rules
    password_hint = tk.Label(
        app, #The parent window where the label is placed 
        text="Password requirements: At least 8 letters, including capital, small alphabets and special characters(@, #, $, %).", # display the text at the window
        fg="red", # color of the word is red
        font=("Time New roman", 9), # font and size
        wraplength=300,
        justify="left", # allign the text to the left
    )
    password_hint.pack(pady=5)

    # Register button
    register_button = tk.Button(app, text="Register", command=register)
    register_button.pack(pady=5)

    # Log in button
    login_button = tk.Button(app, text="Log in", command=login) # tk.button is generate a button to give user click it.
    login_button.pack(pady=5) #is a geometry manager in Tkinter, used to place the button inside the window.

    # Initialize login status
    logged_in = False

    # Run login interface
    app.mainloop()

create_login_window()
