from qx_settings import *
from os.path import join
from os import walk
from pytmx.util_pygame import load_pygame

def import_image(*path, alpha = True, format = "png"):
    full_path = join(*path) + f".{format}"
    surf = pygame.image.load(full_path).convert_alpha() if alpha else pygame.image.load(full_path).convert()
    return surf

def import_folder(*path):
    frames = []
    for folder_path, sub_folders, image_names in walk(join(*path)):
        for image_name in sorted(image_names, key = lambda name : int(name.split(".")[0])):
            full_path = join(folder_path,image_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames.append(surf)
    return frames

def import_folder_dict(*path):
    frames = {}
    for folder_path, sub_folder, image_names in walk(join(*path)):
        for image_name in image_names:
            full_path = join(folder_path,image_name)
            surf = pygame.image.load(full_path).convert_alpha()
            frames[image_name.split('.')[0]] = surf
    return frames

def import_sub_folders(*path):
    frames = {}
    for _,sub_folders,__ in walk(join(*path)):
        for sub_folder in sub_folders:
            frames[sub_folder] = import_folder(*path,sub_folder)
    return frames