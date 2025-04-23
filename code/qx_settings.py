import pygame, sys
from pygame.math import Vector2 as vector

window_width, window_height = 1200,800
tile_size = 64

animation_speed = 6

Z_layers = {
    "bg" : 0,
    "bg tiles" : 1,
    "path" : 2,
    "bg details" : 3,
    "main" : 4,
    "water" : 5,
}