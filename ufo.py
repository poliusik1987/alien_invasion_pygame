import pygame
from pygame.sprite import Sprite

class Ufo(Sprite):

         def __init__(self, ai_settings, screen):
                  super(Ufo, self).__init__()
                  self.screen = screen
                  self.ai_settings = ai_settings

                  self.image = pygame.image.load('ufo.png')
                  self.rect = self.image.get_rect()
                  self.screen_rect = screen.get_rect()

                  self.rect.x = self.rect.width
                  self.rect.y = self.rect.height
                  self.x = float(self.rect.x)
       


         def update(self):
                  self.rect.x = self.x
                  if self.rect.right <= self.screen_rect.right:
                           self.x += self.ai_settings.ufo_speed_factor
                           return True
                  if self.rect.left >= self.screen_rect.left: 
                           self.x = 0
                           return True
              
                           


         def blitme(self):
                  self.screen.blit(self.image, self.rect)
                           
                  

         
                  
