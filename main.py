
import pygame
import os
import time
import random 
from GameObjects import PLAYER_SHIP, PLAYER_SHIP_LEFT, PLAYER_SHIP_RIGHT, Enemy, Player, WINDOW, WIDTH, HEIGHT, collide, Health_Pack, Rapid_Gun, Speed_Boost
from ScoreKeeper import Score_Keeper
from Explosion.Explosion_GameObjects import Explosion


#TODO Add Missiles 
#TODO - Add acceration to speed boost so it isn't so jaring. 
#TODO collect new ships 

#TODO - Land on planet to create side scroller. 

#initiating the font class for pygame
pygame.font.init()
pygame.display.set_caption("Space Shooter Game")

GAME_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("assets/img", "background-black.png")), (WIDTH, HEIGHT))

HEIGHT_MAX = HEIGHT - 60
HEIGHT_MIN = HEIGHT - 400
WIDTH_MAX  = WIDTH - 50
WIDTH_MIN  = 50 

def main(): 
    run = True
    FPS = 60
    level = 0
    lives = 5    
    top_score = 0
    
    main_font = pygame.font.SysFont("arial", 45)
    lost_font = pygame.font.SysFont("Helvetica", 35)

    enemies = []
    explosions = []
    health_packs = []
    rapid_guns = []
    speed_boosts = [] 

    wave_length = 5
    enemy_velocity = 1

    default_velocity = 5
    speed_boost_velocity = 15
    play_velocity = default_velocity
    player = Player(300, 650)

    laser_velocity = 8

    clock = pygame.time.Clock()
    lost = False 
    lost_count = 0

    health_refresh_time = FPS * random.randint(2, 5)
    health_pack_time_limit = FPS * 3    
    
    rapid_gun_refresh_time = FPS * random.randint(5, 10)
    rapid_gun_time_limit = FPS * 3
    
    speed_boost_refresh_time =FPS * random.randint(5, 10)
    speed_boost_time_limit = FPS * 3

    special_weapon_time = FPS * 10
    special_speed_time = FPS * 10 

    def redraw_window():
        WINDOW.blit(GAME_BACKGROUND, (0,0))
        # draw text 
        # turn text into a surface and then put it on the screen. 
        lives_label = main_font.render(f"Lives: {lives }", 1, (255, 51, 204))
        levels_label = main_font.render(f"Level: {level}", 1, (0, 153, 255))
        player_score_label = main_font.render(f"Score: {player.score}", 1, (0, 153, 255))
        player_health = main_font.render(f"Health: {player.health}", 1, (0, 153, 255))

        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))
        WINDOW.blit(player_score_label, (10, lives_label.get_height() + 10))
        WINDOW.blit(player_health, (10, lives_label.get_height() + player_score_label.get_height() + 10))
        
        for enemy in enemies: 
            enemy.draw(WINDOW)

        for explosion in explosions:
            explosion.draw(WINDOW)
        
        for health_pack in health_packs:
            health_pack.draw(WINDOW)

        for rapid_gun in rapid_guns:
            rapid_gun.draw(WINDOW)
        
        for speed_boost in speed_boosts: 
            speed_boost.draw(WINDOW)

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
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["teal", "orange", "purple", "pink"]))
                enemies.append(enemy)
            
        # generate health pack         
        if health_refresh_time == 0: # and Level == 2
            health_pack_time_limit = FPS * 3         
            health_refresh_time = (FPS * random.randint(5, 10))
            
            if len(health_packs) == 0:       
                health_pack = Health_Pack((random.randint(WIDTH_MIN, WIDTH_MAX)), (random.randint(HEIGHT_MIN, HEIGHT_MAX)))
                health_packs.append(health_pack)            
        else:            
            health_pack_time_limit -= 1
            health_refresh_time -= 1

        if health_pack_time_limit == 0 and len(health_packs) > 0: 
            health_packs.remove(health_pack)

        for health_pack in health_packs:
            if collide(health_pack, player) and player.health < player.max_health:                
                player.health += 10    
                health_packs.remove(health_pack)
        

        # generate rapid gun 
        if rapid_gun_refresh_time == 0: # and level == 2 
            rapid_gun_time_limit = FPS * 3
            rapid_gun_refresh_time = (FPS * random.randint(10, 20))

            if len(rapid_guns) == 0: 
                rapid_gun = Rapid_Gun((random.randint(WIDTH_MIN, WIDTH_MAX)), (random.randint(HEIGHT_MIN, HEIGHT_MAX)))
                rapid_guns.append(rapid_gun)
                special_weapon_time = FPS * 10
        else: 
            rapid_gun_time_limit -= 1                
            rapid_gun_refresh_time -= 1
        
        if rapid_gun_time_limit == 0 and len(rapid_guns) > 0: 
            rapid_guns.remove(rapid_gun)
        
        if player.gun_type == "rapid_fire":
            special_weapon_time -= 1
            if special_weapon_time == 0: 
                player.gun_type, player.cool_down, player.laser_img = player.GUN_TYPE["default"] 
                               
        for rapid_gun in rapid_guns: 
            if collide(rapid_gun, player): 
                player.gun_type, player.cool_down, player.laser_img = player.GUN_TYPE["rapid_fire"]
                rapid_guns.remove(rapid_gun)


        # generate speed boost
        if speed_boost_refresh_time == 0: # and level = 3
            speed_boost_time_limit = FPS * 3
            speed_boost_refresh_time = (FPS * random.randint(10, 20))

            if len(speed_boosts) == 0: 
                speed_boost = Speed_Boost((random.randint(WIDTH_MIN, WIDTH_MAX)), (random.randint(HEIGHT_MIN, HEIGHT_MAX)))
                speed_boosts.append(speed_boost)
                special_speed_time = FPS * 10  
        else: 
            speed_boost_refresh_time -= 1
            speed_boost_time_limit -= 1

        if speed_boost_time_limit == 0 and len(speed_boosts) > 0: 
            speed_boosts.remove(speed_boost)

        if play_velocity == speed_boost_velocity:
            special_speed_time -= 1   
            if special_speed_time == 0:
                play_velocity = default_velocity

        for speed_boost in speed_boosts:
            if collide(speed_boost, player):
                play_velocity = speed_boost_velocity
                speed_boosts.remove(speed_boost)                 

                                            

        # check for events 
        for event in pygame.event.get():
            # key up events
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a: 
                    player.ship_img =  PLAYER_SHIP
                if event.key == pygame.K_d:
                    player.ship_img =  PLAYER_SHIP
            # quit events
            if event.type == pygame.QUIT: 
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]  and player.x - play_velocity > 0: #left 
            player.x -= play_velocity
            player.ship_img = PLAYER_SHIP_LEFT
        if keys[pygame.K_d] and player.x + play_velocity + player.get_width() < WIDTH : #right
            player.x += play_velocity
            player.ship_img = PLAYER_SHIP_RIGHT
        if keys[pygame.K_w] and player.y - play_velocity > 300: #up
            player.y -= play_velocity 
            player.ship_img = PLAYER_SHIP
        if keys[pygame.K_s] and player.y + play_velocity  + player.get_height() + 15 < HEIGHT: #down
            player.y += play_velocity
            player.ship_img = PLAYER_SHIP
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
                

        # explosions
        collision_cordinates = player.move_lasers(-laser_velocity, enemies)
        if len(collision_cordinates) > 0:
            explosion = Explosion(collision_cordinates[0], collision_cordinates[1], (255,255,255))
            explosions.append(explosion)
        
        explosions_to_remove = []
        for explosion in explosions:
            explosion.move(WIDTH, HEIGHT)
            if explosion.exploded and len(explosion.projectiles) ==  0:
                explosions_to_remove.append(explosion)

        for explosion in explosions_to_remove:
            explosions.remove(explosion)

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