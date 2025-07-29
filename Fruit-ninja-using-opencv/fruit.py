# fruit.py

import pygame
import random

HEIGHT = 1000  # Screen height

class Fruit:
    def __init__(self, image, x, y, speed, is_bomb=False, name=None):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.is_bomb = is_bomb
        self.active = True
        self.name = name # added name here

    def update(self):
        if self.active:
            self.rect.y += self.speed
            if self.rect.y > 800:
                self.active = False

    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect)

    def check_collision(self, finger_point):
        if self.active and self.rect.collidepoint(finger_point):
            self.active = False
            if self.is_bomb:
                return 'bomb'
            else:
                self.sliced = True
                return 'fruit'
                    
class FruitHalf:
    def __init__(self, image, x, y, vx, vy, angle_speed):
        self.image = pygame.transform.scale(image, (60, 60))
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.angle = 0
        self.angle_speed = angle_speed
        self.active = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.5  # gravity
        self.angle += self.angle_speed
        if self.y > HEIGHT:
            self.active = False

    def draw(self, screen):
        rotated = pygame.transform.rotate(self.image, self.angle)
        rect = rotated.get_rect(center=(self.x, self.y))
        screen.blit(rotated, rect.topleft)



