import pygame
import os
from laser import Laser


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, SCREEN_WIDTH, SCREEN_HEIGHT):
        super().__init__()
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = SCREEN_HEIGHT, SCREEN_WIDTH
        self.image = pygame.image.load(
            os.path.join("MessingAround", "assets/pixel_ship_yellow.png")
        ).convert_alpha()
        self.player_laser_group = pygame.sprite.Group()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.mask = pygame.mask.from_surface(self.image)
        self.velocity = 8
        self.laser_ready = True
        self.laser_time = 0
        self.laser_delay = 200
        self.laser_sfx = pygame.mixer.Sound(
            os.path.join("MessingAround", "assets/laser.mp3")
        )

    def track_movements(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.velocity
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.velocity
        if keys[pygame.K_SPACE] and self.laser_ready:
            self.laser_ready = False
            lasers = Laser(
                self.rect.x,
                self.rect.y,
                self.SCREEN_WIDTH,
                self.SCREEN_HEIGHT,
                "yellow",
            )
            self.laser_sfx.play()
            self.laser_time = pygame.time.get_ticks()
            self.player_laser_group.add(lasers)

    def is_ready(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.laser_time >= self.laser_delay:
            self.laser_ready = True

    def restrict_motion(self):
        if self.rect.right >= self.SCREEN_WIDTH:
            self.rect.right = self.SCREEN_WIDTH
            self.x = self.rect.centerx
        if self.rect.left < 0:
            self.rect.left = 0
            self.x = self.rect.centerx

    def update(self):
        self.track_movements()
        self.restrict_motion()
        self.player_laser_group.update()
        self.is_ready()
