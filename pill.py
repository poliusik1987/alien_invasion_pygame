
import pygame
from pygame.sprite import Sprite


class Pill(Sprite):
    def __init__(self, ai_settings, screen, ufo):
        super(Pill, self).__init__()
        self.screen = screen
        self._ufo = ufo

        self.rect = pygame.Rect(self._ufo.rect.x + self._ufo.rect.width / 2,
                                self._ufo.rect.bottom,
                                ai_settings.pill_width,
                                ai_settings.pill_height)
        self.rect.top = self._ufo.rect.bottom

        self.y = float(self.rect.y)

        self.color = ai_settings.pill_color
        self.speed_factor = ai_settings.pill_speed_factor

    def update(self):
        self.y += self.speed_factor
        self.rect.y = self.y
        screen_rect = self.screen.get_rect()
        if self.rect.y > screen_rect.height:
            self.rect.x = self._ufo.rect.x + self._ufo.rect.width / 2
            self.y = float(self._ufo.rect.bottom)
            self.rect.y = self.y

    def draw_pill(self):
        pygame.draw.rect(self.screen, self.color, self.rect)
