class GameStats():

         def __init__(self, ai_settings):
                  self.ai_settings = ai_settings
                  self.reset_stats()
                  self.game_active = False
                  

         def reset_stats(self):
                  self.ships_left = self.ai_settings.ship_limit
                  self.score = 0
                  self.level = 1
                  
         def dowhload_score(self):
                  self.ships_left = self.ai_settings.ship_limit
                  with open('score.txt', 'r') as file_object:
                           line = file_object.readlines()
                           self.score = int(line[0])
                           self.level = int(line[1])

                  with open('name.txt', 'r') as file_object:
                           line = file_object.read()
                           
