from dino_runner.utils.constants import CLOUD, SCREEN_WIDTH
from pygame.sprite import Sprite
import random

class Cloud(Sprite):

    def __init__(self):
        self.image = CLOUD
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(45, 150)
        self.speed_variation = random.randint(10, 15)

    def update(self, game_speed, clouds):
        self.rect.x -= game_speed - self.speed_variation
        if self.rect.x < -self.rect.width:
            clouds.remove(self)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

