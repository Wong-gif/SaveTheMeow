import pygame

class DeathPopup:
    def __init__(self, screen, width, height):
        self.screen = screen
        self.WIDTH = width
        self.HEIGHT = height
        self.active = False
        self.reason = ""
        self.restart_button = pygame.Rect(0, 0, 160, 50)
        self.font = pygame.font.SysFont("arial", 28)

    def show(self, reason_text):
        self.active = True
        self.reason = reason_text

    def hide(self):
        self.active = False

    def draw(self):
        if not self.active:
            return

        overlay = pygame.Surface((self.WIDTH, self.HEIGHT))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        popup_width, popup_height = 500, 300
        popup_x = self.WIDTH // 2 - popup_width // 2
        popup_y = self.HEIGHT // 2 - popup_height // 2
        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(self.screen, (255, 255, 255), popup_rect, border_radius=15)

        reason_text = self.font.render(self.reason, True, (0, 0, 0))
        self.screen.blit(reason_text, (
            popup_x + popup_width // 2 - reason_text.get_width() // 2,
            popup_y + 80
        ))

        self.restart_button = pygame.Rect(popup_x + popup_width // 2 - 80, popup_y + 180, 160, 50)
        pygame.draw.rect(self.screen, (200, 0, 0), self.restart_button, border_radius=8)

        restart_text = self.font.render("Restart", True, (255, 255, 255))
        self.screen.blit(restart_text, (
            self.restart_button.x + self.restart_button.width // 2 - restart_text.get_width() // 2,
            self.restart_button.y + 10
        ))

    def handle_event(self, event):
        if self.active and event.type == pygame.MOUSEBUTTONDOWN:
            if self.restart_button.collidepoint(event.pos):
                return True
        return False
    


#

import pygame
import random
import os
import json
from jh_death_popup import DeathPopup


def save_game1_data(username, coin, diamond):
    try:
        filename = f"{username}.txt"
        if os.path.exists(filename):
            with open(filename, "r") as file:
                user_data = json.load(file)
        else:
            user_data = {
                "game1": {},
                "game2": {}
            }
            
        user_data["game1"]["Coins"] = coin
        user_data["game1"]["Diamonds"] = diamond

        best_coin = user_data["game1"].get("Best Coins", 0)
        best_diamond = user_data["game1"].get("Best Diamonds", 0)

        user_data["game1"]["Best Coins"] = max(coin, best_coin)
        user_data["game1"]["Best Diamonds"] = max(diamond, best_diamond)

        with open(filename, "w") as file:
            json.dump(user_data, file, indent=4)

        print("Game 1 data saved successfully!")
    except Exception as e:
        print("Failed to save Game 1 data:", e)
