
import sys
import pygame
from pygame.sprite import Group
from setting import Settings
from scoreboard import Scoreboard
from game_stats import GameStats
from button_exit import Button_Exit
from button_start import Button_Start
from button_continuation import Button_Continuation
from ufo import Ufo
from ship import Ship
import function_game as fg


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    button_continuation = Button_Continuation(ai_settings, screen, 'Continuation the game')
    button_exit = Button_Exit(ai_settings, screen, 'Exit')
    button_start = Button_Start(ai_settings, screen, 'Start new game')
    pygame.display.set_caption("Alien Invasion")

    ufo = Ufo(ai_settings, screen)
    pills = Group()
    bullets = Group()
    aliens = Group()
    stats = GameStats(ai_settings)
    ship = Ship(ai_settings, screen)
    sb = Scoreboard(ai_settings, screen, stats)

    fg.create_fleet(ai_settings, screen, ship, aliens, ufo)
    

    while True:
        fg.check_events(ai_settings, screen, stats, sb, button_continuation, button_exit, button_start, ship, aliens, bullets, pills, ufo)
        if stats.game_active:
            ship.update()
            fg.fon_music.stop()
            fg.update_ufos(ai_settings, screen, ufo)
            fg.update_pills(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills)
            fg.update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, ufo)
            fg.update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills)

        fg.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, button_exit, button_start, button_continuation, ufo, pills)

                
run_game()
