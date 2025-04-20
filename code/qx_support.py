from qx_settings import *
from os.path import join
from os import walk

def import_image(*path, alpha = True, format = "png"):
    full_path = join(*path) + f".{format}"
    return pygame.image.load(full_path).convert if alpha else pygame.load.image(full_path).convert()

def import_folder(*path):
    frames = []
    for folder_path, sub_folders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key = lambda name : int(name.split(".")[0])):
            full_path = join(folder_path,image_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames