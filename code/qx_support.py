from qx_settings import *
from os.path import join

def import_image(*path, alpha = True, format = "png"):
    full_path = join(*path) + f".{format}"
    return pygame.image.load(full_path).convert if alpha else pygame.load.image(full_path).convert()