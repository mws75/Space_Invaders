
from asyncio.constants import ACCEPT_RETRY_DELAY
import pygame
import os
import time
import random 
from GameObjects import (PLAYER_SHIP, PLAYER_SHIP_ONE_MISSILE, 
                         PLAYER_SHIP_TWO_MISSILES, PLAYER_SHIP_LEFT, 
                         PLAYER_SHIP_RIGHT, Enemy, Player, WINDOW, 
                         WIDTH, HEIGHT, collide, Health_Pack, Rapid_Gun, 
                         Speed_Boost, Missile, Timer)

from ScoreKeeper import Score_Keeper
from Explosion.Explosion_GameObjects import Explosion
from PhysicsEngine import Movement
import math
from typing import List

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

def redraw_window(player, 
                  enemies, 
                  explosions, 
                  health_packs, 
                  rapid_guns, 
                  speed_boosts,
                  missiles, 
                  level,
                  lives,
                  main_font):
        WINDOW.blit(GAME_BACKGROUND, (0,0))
        # draw text 
        # turn text into a surface and then put it on the screen. 
        lives_label = main_font.render(f"Lives: {lives }", 1, (255, 51, 204))
        levels_label = main_font.render(f"Level: {level}", 1, (0, 153, 255))

        player_score_label = main_font.render(f"Score: {player.score}", 1, (0, 153, 255))
        player_health = main_font.render(f"Health: {player.health}", 1, (0, 153, 255))
        missile_label = main_font.render(f"Missiles: {player.missile_count}", 1, (0, 153, 255))


        WINDOW.blit(lives_label, (10, 10))
        WINDOW.blit(levels_label, (WIDTH - levels_label.get_width() - 10, 10))
        WINDOW.blit(player_score_label, (10, lives_label.get_height() + 10))
        WINDOW.blit(player_health, (10, lives_label.get_height() + player_score_label.get_height() + 10))
        WINDOW.blit(missile_label, (10, lives_label.get_height() + player_score_label.get_height() + player_health.get_height() + 10))

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

        for missile in missiles:
            missile.draw(WINDOW)

        player.draw(WINDOW)
        pygame.display.update()

def game_over(lives: int, player: Player, lost: bool, score_recorded: bool, lost_font: str) -> bool:
    if lives <= 0 or player.health < 0: 
        lost = True 
        if score_recorded == False :
            score_keeper = Score_Keeper()
            score_keeper.write_to_score_card(player.score)

        score_keeper = Score_Keeper()    
        top_score = score_keeper.get_top_score()
        lost_label = lost_font.render(f"You Lost!! Score: {player.score}.  Top Score: {top_score}", 1, (255,255,255))
        WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
        pygame.display.update()
    return lost
        
def generate_enemies(wave_length: int, enemies: List[Enemy]) -> List[Enemy]:
    
    for i in range(wave_length):
        enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["teal", "orange", "purple", "pink"]))
        enemies.append(enemy)
    
    return enemies
    
def generate_health_packs(health_packs: List[Health_Pack]) -> List[Health_Pack]:
    health_pack = Health_Pack((random.randint(WIDTH_MIN, WIDTH_MAX)), (random.randint(HEIGHT_MIN, HEIGHT_MAX)))
    health_packs.append(health_pack)
    return health_packs

def generate_health_pack(health_packs: List[Health_Pack], 
                                   health_refresh_timer: Timer, 
                                   health_pack_time_limit_timer: Timer, 
                                   FPS: int) -> List[Health_Pack]:
    if health_refresh_timer.time == 0:  # and Level == 2
        health_pack_time_limit_timer.time = FPS * 3
        health_refresh_timer.time = FPS * random.randint(5, 10)
        
        if len(health_packs) == 0:
            health_packs = generate_health_packs(health_packs)
    else:
        health_pack_time_limit_timer.time -= 1
        health_refresh_timer.time -= 1

    if health_pack_time_limit_timer.time == 0 and len(health_packs) > 0:
        health_packs.remove(health_packs[0])  # Assume health_pack is the first in the list

    return health_packs

def generate_rapid_gun(rapid_guns: List[Rapid_Gun]) -> List[Rapid_Gun]:
    rapid_gun = Rapid_Gun((random.randint(WIDTH_MIN, WIDTH_MAX)), (random.randint(HEIGHT_MIN, HEIGHT_MAX)))
    rapid_guns.append(rapid_gun)
    return rapid_guns

def main(): 
    run = True
    FPS = 60 
    level = 0
    lives = 5    
    score_recorded = False
    lost = False
    
    main_font = pygame.font.SysFont("arial", 45)
    lost_font = pygame.font.SysFont("Helvetica", 35)

    enemies = []
    explosions = []
    health_packs = []
    rapid_guns = []
    speed_boosts = [] 
    missiles = []

    wave_length = 5
    enemy_velocity = 1

    default_velocity = 5
    accel_x = 0
    accel_delta = 0.8
    player_velocity = 0
    player_max_velocity = default_velocity
    player = Player(300, 650)

    Player_ship = PLAYER_SHIP

    # Speed Boost Data
    speed_boost_velocity = 8
    speed_boost_on = False
    laser_velocity = 5
    
    clock = pygame.time.Clock()
    lost = False 
    lost_count = 0

    # Health Pack Data
    health_refresh_timer = Timer(FPS * random.randint(2, 5))
    health_pack_time_limit_timer = Timer(FPS * 3)
    
    # Rapid Gun Data
    rapid_gun_refresh_timer = Timer(FPS * random.randint(5, 10))
    rapid_gun_time_limit_timer = Timer(FPS * 3)
    
    # Speed  Boost Data 
    speed_boost_refresh_time =FPS * random.randint(5, 10)
    speed_boost_time_limit = FPS * 3

    # Missile Data 
    missile_refresh_time = FPS * random.randint(1, 2)
    missile_time_limit = FPS * 1

    # Special Weapon Data
    special_weapon_timer = Timer(FPS * 10)
    special_speed_time = FPS * 10 

    movement = Movement()
                              
    while run: 
        clock.tick(FPS)
        
        if player.missile_count == 0: 
            Player_ship = PLAYER_SHIP
            player.ship_img = Player_ship

        # game over section
        lost = game_over(lives, player, lost, score_recorded, lost_font)
        if lost: 
            score_recorded = True
            lost_count += 1
            if lost_count > FPS * 3: # sit for 3 seconds before quitting. 
                run = False 
            else: 
                continue # skip the rest of the game loop
        
        # generate Enemies when all enemies are destroyed. 
        if(len(enemies) == 0): 
            level += 1
            wave_length += 5
            enemies = generate_enemies(wave_length, enemies)

        # generate health pack       
        health_packs = generate_health_pack(health_packs, 
                                            health_refresh_timer, 
                                            health_pack_time_limit_timer, 
                                            FPS)
        for health_pack in health_packs:
            if collide(health_pack, player) and player.health < player.max_health:                
                player.health += 10    
                health_packs.remove(health_pack)
        

        # generate rapid gun 
        if rapid_gun_refresh_timer.time == 0: # and level == 2 
            rapid_gun_time_limit_timer.time = FPS * 3
            rapid_gun_refresh_timer.time = (FPS * random.randint(10, 20))

            if len(rapid_guns) == 0: 
                rapid_guns = generate_rapid_gun(rapid_guns)
                special_weapon_timer.time = FPS * 10
        else: 
            rapid_gun_time_limit_timer.time -= 1                
            rapid_gun_refresh_timer.time -= 1
        
        if rapid_gun_time_limit_timer.time == 0 and len(rapid_guns) > 0: 
            rapid_guns.remove(rapid_gun)
        
        if player.gun_type == "rapid_fire":
            special_weapon_timer.time -= 1
            if special_weapon_timer.time == 0: 
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

        if speed_boost_on == True:
            special_speed_time -= 1   
            if special_speed_time == 0:
                player_max_velocity = default_velocity
                speed_boost_on == False

        for speed_boost in speed_boosts:
            if collide(speed_boost, player):
                player_max_velocity = speed_boost_velocity
                speed_boost_on = True
                speed_boosts.remove(speed_boost)                 

        # generate missile 
        if missile_refresh_time == 0:
            missile_time_limit = FPS * 3
            missile_refresh_time = (FPS * random.randint(3,5))

            if len(missiles) == 0:
                missile = Missile((random.randint(WIDTH_MIN, WIDTH_MAX)), (random.randint(HEIGHT_MIN, HEIGHT_MAX)))
                missiles.append(missile)
        else:
            missile_refresh_time -= 1
            missile_time_limit -= 1
        
        if missile_time_limit == 0 and len(missiles) > 0:
            missiles.remove(missile)
        
        for missile in missiles:
            if collide(missile, player) and player.missile_count < 2:
                player.missile_count += 1
                missiles.remove(missile)
            if player.missile_count == 1: 
                Player_ship = PLAYER_SHIP_ONE_MISSILE
                player.ship_img = Player_ship
            if player.missile_count == 2: 
                Player_ship = PLAYER_SHIP_TWO_MISSILES
                player.ship_img = Player_ship

        # check for events 
        for event in pygame.event.get():
            # key up events
            if event.type == pygame.KEYUP:                
                player_velocity = 0 
                if event.key == pygame.K_a: 
                    player.ship_img =  Player_ship                    
                if event.key == pygame.K_d:
                    player.ship_img =  Player_ship
            # key down events 
            if event.type == pygame.KEYDOWN:                
                # Set acceleration value 
                if event.key == pygame.K_a or event.key == pygame.K_w:
                    accel_x = -accel_delta
                elif event.key == pygame.K_d or event.key == pygame.K_s:
                    accel_x = accel_delta

                elif event.key == pygame.K_r:
                    
                    if player.missile_count > 0:
                        player.shoot_missile()
                        player.missile_count -= 1

                        if player.missile_count == 1: 
                            Player_ship = PLAYER_SHIP_ONE_MISSILE
                            player.ship_img = Player_ship
                        elif player.missile_count == 0:
                            Player_ship = PLAYER_SHIP
                            player.ship_img = Player_ship
                        
            # quit events
            if event.type == pygame.QUIT: 
                run = False

            
    
        keys = pygame.key.get_pressed()
        # if any movement keys get pressed we need to calculate velocity
        if keys[pygame.K_a] or keys[pygame.K_d] or keys[pygame.K_w] or keys[pygame.K_s]:
            
            # update the velocity
            if abs(player_velocity + movement.ending_velocity(player_velocity, accel_x)) < player_max_velocity: 
                # update the player_velocity
                player_velocity = movement.ending_velocity(player_velocity, accel_x, 1)
            else: 
                if player_velocity + movement.ending_velocity(player_velocity, accel_x) < 0:
                    player_velocity = player_max_velocity * -1
                else: 
                    player_velocity = player_max_velocity

            # Right and Left Movement
            if keys[pygame.K_a]  and player.x + player_velocity > 0: #left 
                player.x += player_velocity
                player.ship_img = PLAYER_SHIP_LEFT
            if keys[pygame.K_d] and player.x + player_velocity + player.get_width() < WIDTH : #rights
                player.x += player_velocity
                player.ship_img = PLAYER_SHIP_RIGHT
            
            # Up and down Movement
            if keys[pygame.K_w] and player.y + player_velocity > 300: #up
                player.y += player_velocity 
                player.ship_img = Player_ship
            if keys[pygame.K_s] and player.y + player_velocity  + player.get_height() + 15 < HEIGHT: #down
                player.y += player_velocity
                player.ship_img = Player_ship
        
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
        missile_collision_cordinates = player.move_missiles(enemies)
        if len(collision_cordinates) > 0:
            explosion = Explosion(collision_cordinates[0], collision_cordinates[1], (255,255,255))
            explosions.append(explosion)

        if len(missile_collision_cordinates) > 0:
            explosion = Explosion(missile_collision_cordinates[0], missile_collision_cordinates[1], (255,255,255))
            explosions.append(explosion)    
        
        explosions_to_remove = []
        for explosion in explosions:
            explosion.move(WIDTH, HEIGHT)
            if explosion.exploded and len(explosion.projectiles) ==  0:
                explosions_to_remove.append(explosion)

        for explosion in explosions_to_remove:
            explosions.remove(explosion)

        redraw_window(player, enemies, explosions, health_packs,
                      rapid_guns, speed_boosts, missiles,
                      level, lives, main_font)
        
        print(player.missile_count)
        
        
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