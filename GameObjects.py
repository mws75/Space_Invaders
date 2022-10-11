from re import S
import pygame 
import os


RED_SPACE_SHIP = pygame.image.load(os.path.join("assets/img", "pixel_ship_red_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets/img", "pixel_ship_blue_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets/img", "pixel_ship_green_small.png"))
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets/img", "pixel_ship_yellow.png"))
PINK_SPACE_SHIP = pygame.image.load(os.path.join("assets/img", "pixel_ship_pink.png"))
PURPLE_SPACE_SHIP  = pygame.image.load(os.path.join("assets/img", "pixel_ship_purple.png"))
TEAL_SPACE_SHIP = pygame.image.load(os.path.join("assets/img", "pixel_ship_teal.png"))
ORANGE_SPACE_SHIP = pygame.image.load(os.path.join("assets/img", "pixel_ship_orange.png"))
PLAYER_SHIP = pygame.image.load(os.path.join("assets/img", "player_ship.png"))
PLAYER_SHIP_RIGHT = pygame.image.load(os.path.join("assets/img", "player_ship_right_turn.png"))
PLAYER_SHIP_LEFT = pygame.image.load(os.path.join("assets/img", "player_ship_left_turn.png"))


RED_LASER = pygame.image.load(os.path.join("assets/img", "pixel_laser_red.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets/img", "pixel_laser_blue.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets/img", "pixel_laser_green.png"))
YELLOW_LASER = pygame.image.load(os.path.join("assets/img", "pixel_laser_yellow.png"))

HEALTH_PACK = pygame.image.load(os.path.join("assets/img", "health_pack.png"))
RAPID_FIRE_GUN = pygame.image.load(os.path.join("assets/img", "rapid_fire_gun.png"))

WIDTH, HEIGHT = 750, 750
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))



class Ship:

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None 
        self.lasers = []
        self.cool_down_counter = 0
        self.cool_down = 30

    def draw(self, window): 
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers: 
            laser.draw(WINDOW)

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


    def move_lasers(self, velocity, obj):
        self.cooldown()
        for laser in self.lasers: 
            laser.move(velocity)
            if laser.off_screen(HEIGHT): 
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)


    def cooldown(self):
        if self.cool_down_counter >= self.cool_down: 
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0: 
            self.cool_down_counter += 1
    
    def shoot(self):
        if self.cool_down_counter == 0: 
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1



# Player inherits from ship
class Player(Ship):

    GUN_TYPE = {
        "default": (30, YELLOW_LASER),
        "rapid_fire": (10, RED_LASER)
    }

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = PLAYER_SHIP
        self.cool_down, self.laser_img = self.GUN_TYPE["default"]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = 0

    def move_lasers(self, velocity, objs):
        self.cooldown()
        collision_cordinates = []
        for laser in self.lasers: 
            laser.move(velocity)
            if laser.off_screen(HEIGHT) and len(self.lasers) > 0: 
                self.lasers.remove(laser)
            else: 
                for obj in objs: 
                    if laser.collision(obj) and len(self.lasers) > 0:
                        collision_cordinates = [obj.x, obj.y]
                        objs.remove(obj)
                        self.score += 10
                        self.lasers.remove(laser)   
                        collision = True
        return collision_cordinates
             

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health / self.max_health), 10))
            



class Enemy(Ship):
    COLOR_MAP = {
        "red" : (RED_SPACE_SHIP, RED_LASER, 50),
        "green" : (GREEN_SPACE_SHIP, GREEN_LASER, 100),
        "blue" : (BLUE_SPACE_SHIP, BLUE_LASER, 150),
        "pink" : (PINK_SPACE_SHIP, BLUE_LASER, 200),
        "purple" : (PURPLE_SPACE_SHIP, RED_LASER, 200),
        "orange" : (ORANGE_SPACE_SHIP, RED_LASER, 200),
        "teal" : (TEAL_SPACE_SHIP, BLUE_LASER, 200)
    }


    def __init__(self, x, y, color, health = 0):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img, self.heath = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, velocity): 
        self.y += velocity

    def shoot(self):
        if self.cool_down_counter == 0: 
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class Laser: 
    def __init__(self, x, y, img):
        self.x = x 
        self.y = y 
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def move(self, velocity): 
        self.y += velocity
    
    def off_screen(self, height): 
        return not(self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)


class Health_Pack:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = HEALTH_PACK
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))


             


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x 
    offset_y = obj2.y - obj1.y

    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


