import pygame.font

class Button_Start():

         def __init__(self, ai_settings, screen, msg):
                  self.screen = screen
                  self.screen_rect = screen.get_rect()

                  self.width, self.height = 310, 64
                  self.button_color = (255, 141, 28)
                  self.text_color = (0, 0, 0)
                  self.font = pygame.font.SysFont('mistral', 62)
                  
                  self.rect = pygame.Rect(0, 200, self.width, self.height)
                  self.rect.centerx = self.screen_rect.centerx

                  self.prep_msg(msg)


         def prep_msg(self, msg):
                  self.msg_start = self.font.render(msg, True, self.text_color)
                  self.msg_start_rect = self.msg_start.get_rect()
                  self.msg_start_rect.y = 200
                  self.msg_start_rect.centerx = self.rect.centerx

         def draw_button(self):
                  self.screen.fill(self.button_color, self.rect)
                  self.screen.blit(self.msg_start, self.msg_start_rect)
                  
                  
                  
                  
                  

                  

                  

                  
