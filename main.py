
import pygame
import os
import time
import random 
from GameObjects import Enemy, Player, WINDOW, WIDTH, HEIGHT, collide
from ScoreKeeper import Score_Keeper


#TODO write score to json  
#TODO Display top scores 
#TODO Add Missiles 

#initiating the font class for pygame
pygame.font.init()
pygame.display.set_caption("Space Shooter Game")

GAME_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))

def main(): 
    run = True
    FPS = 60
    level = 0
    lives = 5    
    top_score = 0
    
    main_font = pygame.font.SysFont("arial", 45)
    lost_font = pygame.font.SysFont("Helvetica", 50)

    enemies = []
    wave_length = 5
    enemy_velocity = 1

    play_velocity = 5
    player = Player(300, 650)

    laser_velocity = 8

    clock = pygame.time.Clock()
    lost = False 
    lost_count = 0

    def redraw_window():
        WINDOW.blit(GAME_BACKGROUND, (0,0))
        # draw text 
        # turn text into a surface and then put it on the screen. 
        lives_label = main_font.render(f"Lives: {lives }", 1, (255, 51, 204))
        levels_label = main_font.render(f"Level: {level}", 1, (0, 153, 255))
        player_score_label = main_font.render(f"Score: {player.score}", 1, (0, 153, 255))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))
        WINDOW.blit(player_score_label, (10, lives_label.get_height() + 10))
        
        for enemy in enemies: 
            enemy.draw(WINDOW)

        player.draw(WINDOW)
        pygame.display.update()
                        
        
    while run: 
        clock.tick(FPS)

        if lives <= 0 or player.health < 0: 
            lost = True 
            lost_count += 1
            
            score_recorded = False             
            if score_recorded == False :
                score_keeper = Score_Keeper()
                score_keeper.write_to_score_card(player.score)
                top_score = score_keeper.get_top_score()
                score_recorded = True

            lost_label = lost_font.render(f"You Lost!! Score: {player.score}.  Top Score: {top_score}", 1, (255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            pygame.display.update()
            

        if lost: 
            if lost_count > FPS * 3: 
                run = False 
            else: 
                continue
        
        # generate Enemies when all enemies are destroyed. 
        if(len(enemies) == 0): 
            level += 1
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        # check for events 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]  and player.x - play_velocity > 0: #left 
            player.x -= play_velocity
        if keys[pygame.K_d] and player.x + play_velocity + player.get_width() < WIDTH : #right
            player.x += play_velocity
        if keys[pygame.K_w] and player.y - play_velocity > 300: #up
            player.y -= play_velocity 
        if keys[pygame.K_s] and player.y + play_velocity  + player.get_height() + 15 < HEIGHT: #down
            player.y += play_velocity
        if keys[pygame.K_SPACE]: # shoot 
             player.shoot()


        for enemy in enemies[:]: 
            enemy.move(enemy_velocity)
            enemy.move_lasers(laser_velocity, player)

            if random.randrange(0, (5 / level) * 60) == 1:
                enemy.shoot()

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT: 
                lives -= 1
                enemies.remove(enemy)
                

        player.move_lasers(-laser_velocity, enemies)

        redraw_window()
        
        
def main_menu(): 
    title_font = pygame.font.SysFont("ariel", 70)
    run = True 
    while run: 
        WINDOW.blit(GAME_BACKGROUND, (0, 0))
        title_label = title_font.render("Press the Mouse to begin...", 1, (255, 255, 255))
        WINDOW.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 350))


        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN: 
                main()
    pygame.quit()


main_menu()