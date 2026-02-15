import pygame
from vector import Vector

class Object():
    def __init__(self, x, y, velocity, mass, r, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.velocity = velocity
        self.mass = mass
        self.r = r
        self.color = color
        self.acceleration = Vector(0, 0)

    def update(self, dt):
        self.velocity += self.acceleration
        self.x += self.velocity.x * dt #velocity is in pixels per second, so multiply by dt (s) to get the change in position
        self.y += self.velocity.y * dt
    
    def draw_object(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    def select(self):
        self.color = (0, 255, 0)

    def unselect(self):
        self.color = (255, 0, 0)
    
