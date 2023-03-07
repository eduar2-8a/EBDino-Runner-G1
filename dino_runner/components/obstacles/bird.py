from dino_runner.utils.constants import BIRD
from dino_runner.components.obstacles.obstacle import Obstacle
import random

class Bird(Obstacle):
    POSITION_Y = 100

    def __init__(self):
        positional_variation = random.randint(0,50)
        image = BIRD[0]
        super().__init__(image)
        self.rect.y = self.POSITION_Y + positional_variation
