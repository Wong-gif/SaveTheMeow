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