import sys
from time import sleep
import pygame
from tkinter import *
from ufo import Ufo
from bullet import Bullet
from pill import Pill
from alien import Alien
from setting import Settings
import time

pygame.font.init()
pygame.init()
pygame.mixer.init()

fire = pygame.mixer.Sound('pew.wav')
fire.set_volume(0.3)

strike = pygame.mixer.Sound('strike.wav')
strike.set_volume(0.5)

fon_music = pygame.mixer.Sound('start.wav')
fon_music.set_volume(0.3)
             


pause = False
game_over = False

clock = pygame.time.Clock()
ai_settings = Settings()
screen = pygame.display.set_mode(
                  (ai_settings.screen_width, ai_settings.screen_height))


def create_alien(ai_settings, screen, aliens, alien_number, row_number, ufo):
         alien = Alien(ai_settings, screen)
         alien_width = alien.rect.width
         alien.x = alien_width + 2 * alien_width * alien_number
         alien.rect.x = alien.x
         alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number + 1.5 * ufo.rect.height
         aliens.add(alien)

def get_number_aliens_x(ai_settings, screen, alien_width):
         avaible_space_x = ai_settings.screen_width - 2 * alien_width
         number_aliens_x = int(avaible_space_x/(2 * alien_width))
         return number_aliens_x

def get_number_rows(ai_settings, screen, ship_height, alien_height):
         avaible_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
         number_rows = int(avaible_space_y/(2 * alien_height))
         return number_rows


def create_fleet(ai_settings, screen, ship, aliens, ufo):
         alien = Alien(ai_settings, screen)
         number_aliens_x = get_number_aliens_x(ai_settings, screen, alien.rect.width)
         number_rows = get_number_rows(ai_settings, screen, ship.rect.height, alien.rect.height)
         for row_number in range(number_rows):
                  for alien_number in range(number_aliens_x):
                           create_alien(ai_settings, screen, aliens, alien_number, row_number, ufo)


def change_fleet_direction(ai_settings, aliens):
         for alien in aliens.sprites():
                  alien.rect.y += ai_settings.fleet_drop_speed
         ai_settings.fleet_direction *= -1

def check_fleet_edges(ai_settings, aliens):
         for alien in aliens.sprites():
                  if alien.check_edges():
                           change_fleet_direction(ai_settings, aliens)
                           break


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills):
         screen_rect = screen.get_rect()
         for alien in aliens.sprites():
                  if alien.rect.bottom >= screen_rect.bottom:
                           ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills)
                           break


def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills):
         check_fleet_edges(ai_settings, aliens)
         aliens.update()
         if pygame.sprite.spritecollideany(ship, aliens):
                  ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills)
         check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills)


def create_ufo(ai_settings, screen, ufo):
         ufo = Ufo(ai_settings, screen)
         ufo.rect.y = ufo.rect.height + ufo.rect.height



def update_ufos(ai_settings, screen, ufo):
         create_ufo(ai_settings, screen, ufo)
         ufo.update()


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills):
         if stats.ships_left > 0:
                  stats.ships_left -= 1
                  sb.prep_ships()
         else:
                  screen.blit(ai_settings.gr_fon,(0,0))
                  text_game_over()
                  pygame.display.flip()

                  game_over = True

                  while game_over:
                           for event in pygame.event.get():
                                    if event.type == pygame.KEYDOWN:
                                             if event.key == pygame.K_q:
                                                      pygame.quit()
                                                      sys.exit()
                                             elif event.key == pygame.K_s:
                                                      game_over = False
                                                      check_keydown_events(event, ai_settings, screen, stats, sb, button_continuation, ship, aliens, bullets, ufo)
                                                      ship.center_ship()
                                                      pills.empty()
                                                      start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, ufo, pills)
                                    elif event.type == pygame.KEYUP:
                                             check_keyup_events(event, ship)

         aliens.empty()
         pills.empty()
         bullets.empty()
         create_fleet(ai_settings, screen, ship, aliens, ufo)
         ship.center_ship()
         sleep(0.5)

         
def fire_bullet(ai_settings, screen, ship, bullets):
         if len(bullets) < ai_settings.bullets_allowed:
                  new_bullet = Bullet(ai_settings, screen, ship)
                  bullets.add(new_bullet)
                  fire.play()


def update_bullets(ai_settings, screen, ship, aliens, bullets, stats, sb, ufo):
         bullets.update()
         for bullet in bullets.copy():
                  if bullet.rect.bottom <= 0:
                           bullets.remove(bullet)
         check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb, ufo)


def start_new_level(ai_settings, screen, ship, aliens, bullets, stats, sb, ufo):
         if len(aliens) == 0:
                  aliens.empty()
                  bullets.empty()
                  ai_settings.increase_speed()
                  stats.level += 1
                  sb.prep_level()
                  create_fleet(ai_settings, screen, ship, aliens, ufo)
                  ship.center_ship()
                  if stats.ships_left < 3:
                           stats.ships_left += 1
                           sb.prep_ships()

         elif stats.level == 16:
                  f1 = pygame.font.SysFont('mistral', 100)
                  text_1 = f1.render('You have win!', False, (240, 79, 23))
                  f2 = pygame.font.SysFont('mistral', 65)
                  text_2 = f2.render('Press Q to quit.', False, (240, 79, 23))

                  screen.blit(ai_settings.win_fon,(0,0))
                  screen.blit(text_1, (180, 240))
                  screen.blit(text_2, (220, 360))
                  pygame.display.flip()
                  fon_music.play()

                  game_over = True

                  while game_over:
                           for event in pygame.event.get():
                                    if event.type == pygame.QUIT:
                                             pygame.quit()
                                             sys.exit()
                                    elif event.type == pygame.KEYDOWN:
                                             if event.key == pygame.K_q:
                                                      pygame.quit()
                                                      sys.exit()
                  

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, stats, sb, ufo):
         collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
         if collisions:
                  strike.play()
                  for aliens in collisions.values():
                           stats.score += ai_settings.alien_points * len(aliens)
         sb.prep_score()
         start_new_level(ai_settings, screen, ship, aliens, bullets, stats, sb, ufo)


def fire_pill(ai_settings, screen, ufo, pills):
         if len(pills) < ai_settings.pills_allowed:
                  new_pill = Pill(ai_settings, screen, ufo)
                  pills.add(new_pill)
       
def check_pill_bottom(ai_settings, screen, ufo, pills):
         screen_rect = screen.get_rect()
         for pill in pills.sprites():
                  if pill.rect.top <= screen_rect.top:
                           pills.remove(pill)
                           fire_pill(ai_settings, screen, ufo, pills)    
         pills.update()

def update_pills(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills):
    fire_pill(ai_settings, screen, ufo, pills)
    check_pill_bottom(ai_settings, screen, ufo, pills)
    if pygame.sprite.spritecollideany(ship, pills):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, button_continuation, ufo, pills)
    for pill in pills.sprites():
        pill.draw_pill()



def write_score(stats):
         filename = 'score.txt'
         with open (filename, 'w') as file_object:
                  file_object.write(str(stats.score) + "\n")
                  file_object.write(str(stats.level) + "\n")


def check_exit_button(button_exit, mouse_x, mouse_y):
         if button_exit.rect.collidepoint(mouse_x, mouse_y):
                  pygame.quit()
                  sys.exit()


def check_start_button(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, ufo, pills, mouse_x, mouse_y):
         if button_start.rect.collidepoint(mouse_x, mouse_y):
                  start_menu()
                  start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, ufo, pills)


def start_menu():
    window = Tk()
    window.title("Name New Gamer")
    window.geometry('400x100')
    lbl = Label(window, text="Input your name")
    lbl.grid(column=0, row=0)
    txt = Entry(window, width=10)
    txt.grid(column=1, row=0)

    def exit_clicked():
         window.quit()
         window.destroy()

    def clicked():
        filename = 'name.txt'
        with open (filename, 'w') as file_object:
            file_object.write(txt.get())
            exit_clicked()

        
    btn = Button(window, text= "Enter", command=clicked)
    btn.grid(column=2, row=0)
    window.mainloop()



def start_game(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, ufo, pills):
       
         ai_settings.initialize_dynamic_settings()
         stats.reset_stats()
         
         stats.game_active = True
         stats.score = 0
         stats.level = 1
         
         sb.prep_images()
         pygame.mouse.set_visible(False)
         
         aliens.empty()
         bullets.empty()
         ai_settings.increase_speed()
         create_fleet(ai_settings, screen, ship, aliens, ufo)
         ship.center_ship()
         sleep(0.5)

         

def check_continuation_button(ai_settings, screen, stats, sb, button_continuation, ship, aliens, bullets, ufo, mouse_x, mouse_y):
         if button_continuation.rect.collidepoint(mouse_x, mouse_y):

                  ai_settings.initialize_dynamic_settings()
                  stats.dowhload_score()
                  stats.game_active = True
                  
                  sb.prep_images()
                  pygame.mouse.set_visible(False)

                  aliens.empty()
                  bullets.empty()

                  ai_settings.increase_speed()
                  create_fleet(ai_settings, screen, ship, aliens, ufo)
                  ship.center_ship()


def text_pause():
    f1 = pygame.font.SysFont('mistral', 100)
    text_1 = f1.render('Paused', True, (233, 18, 29))
    screen.blit(text_1, (320, 240))
    
    f2 = pygame.font.SysFont('mistral', 65)
    text_2 = f2.render('Press C to contininue.', True, (233, 18, 29))
    screen.blit(text_2, (200, 160))
    
    text_3 = f2.render('Press Q to quit.', True, (233, 18, 29))
    screen.blit(text_3, (220, 360))
    
    pygame.display.update()

def text_game_over():
    f1 = pygame.font.SysFont('mistral', 100)
    text_1 = f1.render('Game Over!', True, (44, 113, 214))
    screen.blit(text_1, (320, 240))
    
    f2 = pygame.font.SysFont('mistral', 65)
    text_2 = f2.render('Press S to new game.', True, (44, 113, 214))
    screen.blit(text_2, (200, 140))
    
    text_3 = f2.render('Press Q to quit.', True, (44, 113, 214))
    screen.blit(text_3, (220, 360))
    
    pygame.display.update()

      
def paused(event):
    pause = True
    text_pause()
    fon_music.play()
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_c:
                    pause = False
        clock.tick(15)



def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, button_exit, button_start, button_continuation, ufo, pills):
    screen.blit(ai_settings.fon,(0,0))
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ufo.blitme()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()

    for pill in pills.sprites():
        pill.draw_pill()


    if not stats.game_active:
        screen.blit(ai_settings.bg_fon,(0,0))
        button_exit.draw_button()
        button_start.draw_button()
        button_continuation.draw_button()
        fon_music.play()

    pygame.display.flip()



def check_keydown_events(event, ai_settings, screen, stats, sb, button_continuation, ship, aliens, bullets, ufo):
         if event.key == pygame.K_RIGHT:
                  ship.moving_right = True
                  
         elif event.key == pygame.K_LEFT:
                  ship.moving_left = True
                  
         elif event.key == pygame.K_SPACE:
                  fire_bullet(ai_settings, screen, ship, bullets)

         elif event.key == pygame.K_p:
                  paused(event)

         elif event.key == pygame.K_q:
                  write_score(stats)
                  pygame.quit()
                  sys.exit()


def check_keyup_events(event, ship):
         if event.key == pygame.K_RIGHT:
                  ship.moving_right = False
                  
         elif event.key == pygame.K_LEFT:
                  ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, button_continuation, button_exit, button_start, ship, aliens, bullets, pills, ufo):
         for event in pygame.event.get():
                  if event.type == pygame.MOUSEBUTTONDOWN:
                           mouse_x, mouse_y = pygame.mouse.get_pos()
                           check_exit_button(button_exit, mouse_x, mouse_y)

                  if event.type == pygame.MOUSEBUTTONDOWN:
                           mouse_x, mouse_y = pygame.mouse.get_pos()
                           check_start_button(ai_settings, screen, stats, sb, ship, aliens, bullets, button_start, ufo, pills, mouse_x, mouse_y)

                  if event.type == pygame.MOUSEBUTTONDOWN:
                           mouse_x, mouse_y = pygame.mouse.get_pos()
                           check_continuation_button(ai_settings, screen, stats, sb, button_continuation, ship, aliens, bullets, ufo, mouse_x, mouse_y)

                  if event.type == pygame.QUIT:
                           write_score(stats)
                           pygame.quit()
                           sys.exit()

                  elif event.type == pygame.KEYDOWN:
                           check_keydown_events(event, ai_settings, screen, stats, sb, button_continuation, ship, aliens, bullets, ufo)

                  elif event.type == pygame.KEYUP:
                           check_keyup_events(event, ship)

