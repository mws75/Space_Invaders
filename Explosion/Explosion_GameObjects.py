import pygame 
import time
import random
import math


COLORS = [
        (255, 0, 0),
        (0, 255, 0),
        (0, 0, 255),
        (0, 255, 255),
        (255, 165, 0),
        (230, 230, 250),
        (255, 192, 203)
    ]



class Projectile: 
    WIDTH = 5
    HEIGHT = 10
    ALPHA_DECREMENT = 6

    def __init__(self, x, y, x_velocity, y_velocity, color):
            self.x = x
            self.y = y
            self.x_velocity = x_velocity
            self.y_velocity = y_velocity
            self.color = color
            self.alpha = 255

    # What happens after this? 
    def move(self):
        self.x += self.x_velocity
        self.y += self.y_velocity 
        # can't have a negative alpha. So need to make it 0
        self.alpha = max(0, self.alpha - self.ALPHA_DECREMENT)

    def draw(self, window):
        self.draw_rect_alpha(window, self.color + (self.alpha,), (self.x, self.y, self.WIDTH, self.HEIGHT))


    # static method doesn't require properties from its class
    @staticmethod
    def draw_rect_alpha(surface, color, rectangle):
        shape_surface = pygame.Surface((pygame.Rect(rectangle).size), pygame.SRCALPHA)
        pygame.draw.rect(shape_surface, color, shape_surface.get_rect())
        # blit takes one surface and puts it on another surface
        surface.blit(shape_surface, rectangle)




class Explosion: 
    RADIUS = 10 
    MAX_PROJECTILES = 50
    MIN_PROJECTILES = 25
    PROJECTILE_VEL = 4


    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.projectiles = []
        self.exploded = False 
    
    def move(self, max_width, max_height):
        if not self.exploded:
            self.explode()

        projectile_to_remove = []
        for projectile in self.projectiles:
            projectile.move()
            # where is projectile.draw() called? 

            if projectile.x >= max_width or projectile.x < 0: 
                projectile_to_remove.append(projectile)

            elif projectile.y >= max_height or projectile.y < 0: 
                projectile_to_remove.append(projectile)     

        for projectile in projectile_to_remove:
            self.projectiles.remove(projectile) 



    def explode(self):
        self.exploded = True
        num_projectiles = random.randrange(self.MIN_PROJECTILES, self.MAX_PROJECTILES)
        
        if random.randint(0, 1) == 0:
            self.create_circular_pattern(num_projectiles)
        else:
            self.create_star_pattern()

        # TWO PATTERNS, CIRCULAR AND STAR

    def create_circular_pattern(self, num_projectiles):
        
        # how to make a circular
        # circular has 360 degrees = 2pi (the radian of the angle)
        # so instead of degrees, we are using radians. 
        # 180 degrees = pi
        # 90 degrees = pi / 2
        # pick angles from 0 to 2

        angle_difference = math.pi * 2 / num_projectiles # evenly move around the circle
        current_angle = 0
        velocity = random.randrange(self.PROJECTILE_VEL - 1, self.PROJECTILE_VEL + 1)
        for i in range(num_projectiles):
            x_velocity = math.sin(current_angle) * velocity
            y_velocity = math.cos(current_angle) * velocity
            color = random.choice(COLORS)
            self.projectiles.append(Projectile(self.x, self.y, x_velocity, y_velocity, color))
            current_angle += angle_difference

    def create_star_pattern(self):
        angle_difference = math.pi / 4
        current_angle = 0
        for i in range(1, 65): 
            velocity = self.PROJECTILE_VEL + (i % 8)
            x_velocity = math.sin(current_angle) * velocity
            y_velocity = math.cos(current_angle) * velocity
            color = random.choice(COLORS)
            self.projectiles.append(Projectile(self.x, self.y, x_velocity, y_velocity, color))
            if i % 8 == 0:
                current_angle += angle_difference 


    def draw(self, window):
        if not self.exploded:
            pygame.draw.circle(window, self.color, (self.x, self.y), self.RADIUS)

        for projectile in self.projectiles: 
            projectile.draw(window)


            





def main():
    pass 

if __name__ == '__main__':
    main()

            