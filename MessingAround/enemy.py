import pygame
from player import Player
from laser import Laser


class Enemy(pygame.sprite.Sprite):
    def __init__(
        self, color, x, y, velocity, direction, width, height, laser_time, laser_group
    ):
        super().__init__()
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = width, height
        self.color = color
        self.image = pygame.image.load(f"assets/invador.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.enemy_laser_group = laser_group
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = velocity
        self.direction = direction
        self.shoot_interval = laser_time
        self.last_shot_time = pygame.time.get_ticks()

    def update(self):
        self.action()
        self.restrict_motion()
        self.enemy_laser_group.update()
        if self.direction == 1:
            self.rect.x += self.velocity
        else:
            self.rect.x -= self.velocity

    def restrict_motion(self):
        if self.rect.right >= self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
            self.x = self.rect.centerx
            self.direction = -1
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.centerx
            self.direction = 1

    def action(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot_time >= self.shoot_interval:
            lasers = Laser(
                self.rect.x,
                self.rect.y + 40,
                self.SCREEN_WIDTH,
                self.SCREEN_HEIGHT,
                self.color,
            )
            self.enemy_laser_group.add(lasers)
            self.last_shot_time = now
