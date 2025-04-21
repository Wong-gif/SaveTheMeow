import pygame, sys
from pygame.math import Vector2 as vector

window_width, window_height = 1280,720
tile_size = 64

Z_layers = {
    "bg" : 0,
    "clouds" : 1,
    "bg_tiles" : 2,
    "path" : 3,
    "bg_details" : 4,
    "main" : 5,
    "water" : 6,
    "fg" : 7
}