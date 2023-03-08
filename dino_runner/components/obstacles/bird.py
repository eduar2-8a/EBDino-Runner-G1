from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle
import random

class Bird(Obstacle):
    POSITION_Y = 100

    def __init__(self):
        self.step = 0
        positional_variation = random.randint(0,200)
        self.image = BIRD[0]
        super().__init__(self.image)
        self.rect.y = self.POSITION_Y + positional_variation
    
    def update(self, game_speed, obstacle):
        self.image = BIRD[self.step //5]
        self.step += 1
        if self.step >= 10:
            self.step = 0
        super().update(game_speed, obstacle)
