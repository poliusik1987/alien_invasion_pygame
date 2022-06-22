import pygame

class Settings():

         def __init__(self):
                  self.screen_width = 897
                  self.screen_height = 640
                  self.bg_color = (255, 255, 255)
                  self.bg_fon = pygame.image.load('space.jpg')
                  self.gr_fon = pygame.image.load('sky_2.jpg')
                  self.win_fon = pygame.image.load('winner.jpg')
                  self.fon = pygame.image.load('sky.jpg')

                  self.ship_limit = 3

                  self.bullet_speed_factor = 3
                  self.bullet_width = 3
                  self.bullet_height = 15
                  self.bullet_color = (219, 2, 7)
                  self.bullets_allowed = 3
                  
                  self.pill_speed_factor = 1.5
                  self.pill_width = 5
                  self.pill_height = 15
                  self.pill_color = (119, 238, 0)
                  self.pills_allowed = 1
                  
                  self.ufo_speed_factor = 1
                  
                  self.fleet_drop_speed = 10
                  
                  self.speedup_scale = 1.1
                  
                  self.score_scale = 1.5
                  self.initialize_dynamic_settings()

         def initialize_dynamic_settings(self):
                  self.ship_speed_factor = 1.5
                  self.bullet_speed_factor = 3
                  self.alien_speed_factor = 1
                  self.fleet_direction = 1
                  self.alien_points = 50

         def increase_speed(self):
                  self.ship_speed_factor *= self.speedup_scale
                  self.bullet_speed_factor *= self.speedup_scale
                  self.alien_speed_factor *= self.speedup_scale
                  self.alien_points = int(self.alien_points * self.score_scale)

         
                  
                  
