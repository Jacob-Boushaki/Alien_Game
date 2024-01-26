import pygame
import time
import random
import sys



pygame.font.init()
FONT = pygame.font.SysFont("Consolas", 30)





#These few lines will set up our window constants
WIN_WIDTH, WIN_HEIGHT = 1150, 620
ARENA_LEFT, ARENA_RIGHT = 50, 850
WINDOW = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Jacob's Alien Game")

#This is a macro? that will load this specific image
BG = pygame.image.load("Alien game\space.jpg")                

#These are are player size constants
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_VEL = 10

BULLET_VEL = 5
BULLET_DELAY = 1000

ALIEN_WIDTH = 40
ALIEN_HEIGHT = 40
ALIEN_VEL = 1

ALIEN_WAVES = 5
WAVE_DEALAY = 2000






def draw(player, elapsed_time, aliens, bullets):
    WINDOW.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {(round(elapsed_time * 10) / 10)} s", 1, "white")
    WINDOW.blit(time_text, (900,25))
    
    for bullet in bullets:
        pygame.draw.rect(WINDOW, "white", bullet)

    
    pygame.draw.rect(WINDOW, (201,148,227), player)

    #these are arena brackets for development purposes
    pygame.draw.rect(WINDOW, "purple", pygame.Rect(ARENA_LEFT - 5, 10, 5, 700))
    pygame.draw.rect(WINDOW, "purple", pygame.Rect(ARENA_RIGHT, 10, 5, 700))

    for alien in aliens:
        pygame.draw.rect(WINDOW, (62,255,111), alien)

    pygame.display.update()


def main():
    run = True    
 
    player = pygame.Rect(200, WIN_HEIGHT - PLAYER_HEIGHT - 40,
                         PLAYER_WIDTH, PLAYER_HEIGHT)
    hit = False

    bullets = []
    bullet_fire_time = 0
    fire = True    

    #This is the clock for our game
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    aliens = []

    wave_bool = False
    waves = ALIEN_WAVES

    NEW_WAVE = pygame.USEREVENT + 1
    pygame.time.set_timer(NEW_WAVE, WAVE_DEALAY)
    MOVE_DOWN = pygame.USEREVENT + 2
    pygame.time.set_timer(MOVE_DOWN, WAVE_DEALAY)
  
    
    #This is the main code for our game
    while run:
         
        clock.tick(60)
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            elif event.type == MOVE_DOWN:
                for alien in aliens[:]:
                    alien.y += 44
                wave_bool = not wave_bool

            elif event.type == NEW_WAVE and waves > 0 and (wave_bool):
                for i in range(8):
                    alien_x = (88 * i) + ARENA_LEFT + 10
                    alien = pygame.Rect(alien_x, -ALIEN_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT)
                    aliens.append(alien)
                waves -= 1




        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= ARENA_LEFT:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= ARENA_RIGHT:
            player.x += PLAYER_VEL


        if (fire):
            if keys[pygame.K_SPACE]:
                bullet_x = player.x + (PLAYER_WIDTH / 2)
                bullet = pygame.Rect(bullet_x, WIN_HEIGHT - PLAYER_HEIGHT - 40, 10, 10)
                bullets.append(bullet)
                bullet_fire_time = time.time()
                fire = False
         
        elif time.time() - bullet_fire_time > 0.3:
            fire = True


        for alien in aliens[:]:
            if (wave_bool):
                alien.x += ALIEN_VEL
            else:
                alien.x -= ALIEN_VEL
            if alien.y > WIN_HEIGHT:
                aliens.remove(alien)
            elif alien.y + alien.height >= player.y:
                hit = True                        

#group collide
            if alien.collidelistall(bullets):
                aliens.remove(alien)
                bullets.remove(bullet)


        for bullet in bullets[:]:
            bullet.y -= BULLET_VEL
            if bullet.y < -20:
                bullets.remove(bullet)


        if (hit):
            lost_text = FONT.render(f"You lost!", 1, "white")
            WINDOW.blit(lost_text, (WIN_WIDTH/2 - lost_text.get_width()/2, 
                                    WIN_HEIGHT/2 - lost_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break


        draw(player, elapsed_time, aliens, bullets)

    pygame.quit()
if __name__ == "__main__":
    main()