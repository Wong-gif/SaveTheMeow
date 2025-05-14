import pygame
from qx_settings import *
from pytmx.util_pygame import load_pygame
from os.path import join
from qx_overworld import Overworld
from qx_support import * 
from qx_data import Data

def platform_map(username):
    class Game: # main game class that runs the main loop to load the game, 
        def __init__(self): #calls this lines of code and initialize the game when an object is built
            pygame.init() #initialize pygame modules (eg. display, image, mixer ...)
            self.display_surface = pygame.display.set_mode((window_width,window_height)) #set the game window with specific dimension
            pygame.display.set_caption("Save The Meow") #set the title of the game
            self.clock = pygame.time.Clock() #creates a clock object to control the frame rate 
            self.import_assets() #call the method to import game assets

            self.data = Data() #creates an instance of the Data class to store game state or progress
            #generate the world map
            self.tmx_overworld = load_pygame(join("tiled_data_qianxian","tmx","overworld.tmx")) #load the Tiled overworld map, join from os adds either / or \ depending on your own device
            self.current_stage = Overworld(self.tmx_overworld,self.data,self.overworld_frames) #create the overworld stage with the map, data and graphics
        
        def import_assets(self):
            self.overworld_frames = { #dictionary to hold different types of animation frames for the overworld
                "palms" : import_folder("graphics_qx","overworld","palm"), #load palm tree animations
                "water" : import_folder("graphics_qx","overworld","water"), #load water animations
                "path" : import_folder_dict("graphics_qx","overworld","path"), #load path  tiles as a dictionary 
                "icon" : import_sub_folders("graphics_qx","overworld1","icon"), #load character icons from subfolders as different directions have differnt animations
                "characters" : all_character_import("graphics_qx","characters") #load all character sprites
            }

        def run(self): #main game loop
            while True: #infinite loop to keep the game always running 
                dt = self.clock.tick() / 1000 #limit the frame rate and get the delta time in seconds, this is to ensure obects move at the same speed regardless of the FPS
                for event in pygame.event.get(): #goes through all events in the event queue
                    if event.type == pygame.QUIT: #if the close button is clicked
                        pygame.quit() #quit all pygame modules
                        exit() #exit the program

                self.current_stage.run(dt) #run the current stage (overworld) logic and rendering, time is passed to the current scene so it can update accordingly
                pygame.display.update() #update the display with what has been drawn

    game = Game() #create an instance of the game class
    game.run() #start the game by running the main loop
 