import pygame.font

class Button_Exit():

    def __init__(self, ai_settings, screen, msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.width, self.height = 100, 64
        self.button_color = (102, 102, 255)
        self.text_color = (0, 0, 0)
        self.font = pygame.font.SysFont('mistral', 62)
        
        self.rect = pygame.Rect(0, 380, self.width, self.height)
        self.rect.centerx = self.screen_rect.centerx
       

        self.prep_msg(msg)


    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.y = 380
        self.msg_image_rect.centerx = self.rect.centerx


    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        

    


    

    
                  
                  

                  
