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
        messagebox.showwarning("Enter Error", "Please key in Username!") 
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
        "inventory":{
            "Weapon for Boss": [],
            "Weapon for Farm": []
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

    if not username:
        messagebox.showwarning("Error", "Please key in Username!")
        return

    if os.path.exists(f"{username}.txt"):
        messagebox.showinfo("Success", "You have successfully logged in!")
        app.withdraw()  # Hide the login window

        def start_game_thread():
            import qx_test_main
            qx_test_main.open_game(username)
            
        threading.Thread(target=start_game_thread).start()
           
    else:
        messagebox.showerror("Error", "This user does not exist, Please register a new account.")
        logged_in = False  # Log in failed, does not enter game

    clear_entries()

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
        pygame.quit() #Closes the Pygame (if it's running), stopping any sounds and function. but our login are not added any BGM.
        exit()

    app.protocol("WM_DELETE_WINDOW", on_close) #"WM_DELETE_WINDOW" this sentence is represents the window close event #i use this is prevent accidental closure and ensures cleanup

    bg_image = Image.open("assets/images/123.png")
    bg_image = bg_image.resize((1200, 800), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(app, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Username label and input space
    username_label = tk.Label(app, text="Username:", font=("Arial", 24))
    username_label.place(x=300, y=200) 
    username_entry = tk.Entry(app, font=("Arial", 24)) #create a space to input the username and when the user input the username
    username_entry.place(x=510, y=201) 

    # Register button
    register_button = tk.Button(app, text="Register", command=register, font=("Arial", 23))
    register_button.place(x=150, y=550) 

    # Log in button
    login_button = tk.Button(app, text="Log in", command=login, font=("Arial", 23))
    login_button.place(x=900, y=550)

    # Initialize login status
    logged_in = False

    # Run login interface
    app.mainloop()

create_login_window()



#  

import pygame

# 初始化pygame
pygame.init()

# 设定屏幕尺寸
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Super Mario Cover")

# 加载并调整背景图片
background = pygame.image.load("background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

# 加载马里奥角色
mario = pygame.image.load("mario.png")
mario = pygame.transform.scale(mario, (100, 100))

# Mario 位置
mario_x = 350
mario_y = 400
mario_speed = 2  # 降低速度
jump = False
jump_height = 10
gravity = jump_height

# 设定字体
font = pygame.font.Font(None, 80)
title_text = font.render("Super Mario", True, (255, 215, 0))

# 剧情文本
story_font = pygame.font.Font(None, 40)
story_text = [
    "once a lot a time ......",
    "help! me ",
    "HAlo！",
    "press ENTER to start the game"
]

# 游戏状态
show_story = True
running = True

while running:
    screen.fill((0, 0, 0))  # 黑色背景
    
    if show_story:
        # 显示剧情文本
        for i, line in enumerate(story_text):
            text_surface = story_font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (100, 150 + i * 50))
    else:
        # 游戏主界面
        screen.fill((135, 206, 250))  # 天空蓝色背景
        screen.blit(background, (0, 0))  # 显示背景
        screen.blit(mario, (mario_x, mario_y))  # 显示马里奥角色
        screen.blit(title_text, (250, 50))  # 显示标题

        # 获取按键状态
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # 左移
            mario_x -= mario_speed
        if keys[pygame.K_RIGHT]:  # 右移
            mario_x += mario_speed
        if keys[pygame.K_SPACE] and not jump:  # 跳跃
            jump = True

        # 处理跳跃逻辑
        if jump:
            mario_y -= gravity  # 向上跳
            gravity -= 1
            if gravity < -jump_height:
                jump = False
                gravity = jump_height
    
    # 监听事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            show_story = False  # 按 Enter 进入游戏

    pygame.display.flip()

pygame.quit()

