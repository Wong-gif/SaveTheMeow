import pygame
from qx_farm_settings import *

class UI:
    def __init__(self,available_weapons,available_magic):

        #general
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

        #bar setup
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
        self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)

        #convert weapon dictionary
        self.weapon_graphics = []
        for weapon_name in available_weapons:
            if weapon_name in weapons_data:
                path = weapons_data[weapon_name]["graphic"]
                weapon = pygame.image.load(path).convert_alpha()
                self.weapon_graphics.append(weapon)

        #convert magic dictionary
        self.magic_graphics = []
        for magic_name in available_magic:
            if magic_name in magic_data:
                path = magic_data[magic_name]["graphic"]
                magic = pygame.image.load(path).convert_alpha()
                self.magic_graphics.append(magic)

    def show_bar(self,current,max_amount,bg_rect,colour):
        #draw bg
        pygame.draw.rect(self.display_surface,UI_BG_COLOUR,bg_rect)

        #convert stat into pixel
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        #draw the bar
        pygame.draw.rect(self.display_surface,colour,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR,bg_rect,3)

    def show_coins(self,coins):
        text_surf = self.font.render(f"Coins: {int(coins)}",False,TEXT_COLOUR)
        x = self.display_surface.get_size()[0] - 1020
        y = self.display_surface.get_size()[1] - 700
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface,UI_BG_COLOUR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR,text_rect.inflate(20,20),3)

    def show_diamonds(self,diamonds):
        text_surf = self.font.render(f"Diamonds: {int(diamonds)}",False,TEXT_COLOUR)
        x = self.display_surface.get_size()[0] - 978
        y = self.display_surface.get_size()[1] - 650
        text_rect = text_surf.get_rect(bottomright = (x,y))

        pygame.draw.rect(self.display_surface,UI_BG_COLOUR,text_rect.inflate(20,20))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR,text_rect.inflate(20,20),3)

    def selection_box(self,left,top,has_switched):
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE)
        pygame.draw.rect(self.display_surface,UI_BG_COLOUR,bg_rect)
        if has_switched:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR_ACTIVE,bg_rect,3)
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER_COLOUR,bg_rect,3)
        return bg_rect

    def weapon_overlay(self,weapon_index,has_switched):
        bg_rect = self.selection_box(10, 700, has_switched)
    
    # Only show weapon if there are weapons available and the index is valid
        if len(self.weapon_graphics) > 0 and 0 <= weapon_index < len(self.weapon_graphics):
            weapon_surf = self.weapon_graphics[weapon_index]
            weapon_rect = weapon_surf.get_rect(center=bg_rect.center)
            self.display_surface.blit(weapon_surf, weapon_rect)

    def magic_overlay(self,magic_index,has_switched):
        bg_rect = self.selection_box(110, 700, has_switched)
    
    # Only show weapon if there are weapons available and the index is valid
        if len(self.magic_graphics) > 0 and 0 <= magic_index < len(self.magic_graphics):
            magic_surf = self.magic_graphics[magic_index]
            magic_rect = magic_surf.get_rect(center=bg_rect.center)
            self.display_surface.blit(magic_surf, magic_rect)


    def display(self,player):
        self.show_bar(player.health,player.stats["health"],self.health_bar_rect,HEALTH_COLOUR)
        self.show_coins(player.coins)
        self.show_diamonds(player.diamonds)
        self.weapon_overlay(player.weapons_index,not player.can_switch_weapon)
        self.magic_overlay(player.magic_index, not player.can_switch_magic)