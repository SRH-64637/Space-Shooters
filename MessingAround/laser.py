import pygame


class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y, SCREEN_WIDTH, SCREEN_HEIGHT, color):
        super().__init__()
        self.color = color
        self.SCREEN_HEIGHT, self.SCREEN_WIDTH = SCREEN_HEIGHT, SCREEN_WIDTH
        self.image = pygame.image.load(
            f"assets/pixel_laser_{color}.png"
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.center = (x + 50, y + 3)
        self.velocity = 4

    def update(self):
        if self.color == "yellow":
            self.rect.y -= self.velocity
        else:
            self.rect.y += self.velocity

        if self.rect.y > self.SCREEN_HEIGHT + 15 or self.rect.y < 0:
            self.kill()
