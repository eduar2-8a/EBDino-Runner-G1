from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS
from dino_runner.components.obstacles.obstacle import Obstacle
import random

class Cactus(Obstacle):
    def __init__(self):
        cactus_type = random.randint(0,2)
        image = SMALL_CACTUS[cactus_type]
        super().__init__(image)
        self.rect.y = 325
