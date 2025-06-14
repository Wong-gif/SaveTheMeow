import pygame
import os
import threading
import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Register function
def register(): #here is the register part
    username = username_entry.get() # this is the input to our user (username)
    
    if not username:
        messagebox.showwarning("Enter Error", "Please key in Player Profile!") 
        return
    
        # Whether user exist or not
    if os.path.exists(f"{username}.txt"): # this whole thing is a function in python to help us to check whether got a file or not #os this is a module and path is a connection between code and file, however, you can say path like a road or highway between a plece to place.
        messagebox.showerror("Error", "User already exists. Please log in directly.") #if error it will print out "Error", "User already exists. Please log in directly." by using a function in tkinter which is messagebox.
        return #it meaning is finsh this knid of thing then can quit the function or stop the function.
      
    user_data = {
        "game1": {
            "Coins": 0,
            "Diamonds": 0,
            "Best Coins": 0,
            "Best Diamonds": 0
        },
        "game2": {
            "Coins": 0,
            "Diamonds": 0,
            "Best Coins": 0,
            "Best Diamonds": 0
        },
        "game3":{
            "Coins":0,
            "Diamonds":0
        },
        "inventory":{
            "Weapon for Boss": [],
            "Weapon for Farm": [],
            "Magic for Farm": []
        },
        "coins_spent": 0,
        "diamonds_spent": 0  # Track diamonds spent
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

    if not username:
        messagebox.showwarning("Error", "Please key in Player Profile!")
        return

    if os.path.exists(f"{username}.txt"):
        messagebox.showinfo("Success", "You have successfully logged in!")
        app.withdraw()  # Hide the login window

        def start_game_thread():
            try:
                import qx_test_main
                qx_test_main.open_game(username)
            finally:
                # When game exits, show login window again
                app.deiconify()
            
        threading.Thread(target=start_game_thread).start()
           
    else:
        messagebox.showerror("Error", "This user does not exist, Please register a new Player Profile.")
        logged_in = False  # Log in failed, does not enter game

    clear_entries() # when click the button the word will miss

# Empty input
def clear_entries():
    try: #try-except function is make sure our coding don't not have error 
        username_entry.delete(0, tk.END) #(username)this meaning when user are not input any thing  from 0 until tk.end
    except Exception as e:
        print(f"Error clearing entries: {e}")

# Creating login page
def create_login_window():
    global app, username_entry, logged_in

    app = tk.Tk() #create a tkinter window
    app.title("Save The Meow") # the title for top of window 
    app.geometry("1200x800") # the window size, width and height

    def on_close():
        global logged_in
        logged_in = False
        try:
            pygame.quit()
        except:
            pass  # In case pygame wasn't initialized
        app.destroy()  # Properly destroy the Tkinter window

    app.protocol("WM_DELETE_WINDOW", on_close) #"WM_DELETE_WINDOW" this sentence is represents the window close event #i use this is prevent accidental closure and ensures cleanup

    bg_image = Image.open("assets/images/123.png")
    bg_image = bg_image.resize((1200, 800), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(app, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Username label and input space
    username_label = tk.Label(app, text="Player Profile:", font=("Arial", 24))
    username_label.place(x=280, y=200) 
    username_entry = tk.Entry(app, font=("Arial", 24)) #create a space to input the username and when the user input the username
    username_entry.place(x=510, y=201) 

    # Register button
    register_button = tk.Button(app, text="Create Profile", command=register, font=("Arial", 23))
    register_button.place(x=150, y=550) 

    # Log in button
    login_button = tk.Button(app, text="Play This Profile", command=login, font=("Arial", 23))
    login_button.place(x=850, y=550)

    # Initialize login status
    logged_in = False

    # Run login interface
    app.mainloop()

create_login_window()
######
