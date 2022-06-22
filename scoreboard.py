import pygame.font
from pygame.sprite import Group
from ship import Ship

class Scoreboard():

         def __init__(self, ai_settings, screen, stats):
                  self.screen = screen
                  self.screen_rect = screen.get_rect()
                  self.ai_settings = ai_settings
                  self.stats = stats
                  self.text_color = (252, 20, 1)
                  self.font = pygame.font.SysFont(None, 48)
                  self.prep_images()

         def prep_images(self):
                  self.prep_score()
                  self.gamer_name()
                  self.prep_level()
                  self.prep_ships()


         def prep_level(self):
                  self.level_image = self.font.render(str(self.stats.level), True,
                                                      self.text_color, 0)
                  self.level_rect = self.level_image.get_rect()
                  self.level_rect.right = self.score_rect.right
                  self.level_rect.top = self.score_rect.bottom + 10

                  
         def prep_score(self):
                  rounded_score = int(round(self.stats.score, -1))
                  score_str = "{:,}".format(rounded_score)
                  self.score_image = self.font.render(score_str, True, self.text_color, 0)
                  self.score_rect = self.score_image.get_rect()
                  self.score_rect.right = self.screen_rect.right - 20
                  self.score_rect.top = 20

         def gamer_name(self):
                  with open('name.txt', 'r') as file_object:
                           line = file_object.read()
                           self.name = line
                           self.name_image = self.font.render(self.name, True, self.text_color, 0)
                           self.name_image_rect = self.name_image.get_rect()
                           self.name_image_rect.centerx = self.screen_rect.centerx
                           self.name_image_rect.top = 20
                           

         def prep_ships(self):
                  self.ships = Group()
                  for ship_number in range(self.stats.ships_left):
                           ship = Ship(self.ai_settings, self.screen)
                           ship.rect.x = 10 + ship_number * ship.rect.width
                           ship.rect.y = 10
                           self.ships.add(ship)

         def show_score(self):
                  self.screen.blit(self.score_image, self.score_rect)
                  self.screen.blit(self.name_image, self.name_image_rect)
                  self.screen.blit(self.level_image, self.level_rect)
                  self.ships.draw(self.screen)
