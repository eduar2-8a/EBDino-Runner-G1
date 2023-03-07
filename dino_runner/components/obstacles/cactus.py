from dino_runner.utils.constants import SMALL_CACTUS, LARGE_CACTUS
from dino_runner.components.obstacles.obstacle import Obstacle
import random

class Cactus(Obstacle):
    POSITION_Y_SMALL = 325
    POSITION_Y_LARGE = 300

    def __init__(self):
        cactus_type = random.randint(0,2)
        cactus_size = random.randint(0,1)
        if cactus_size == 1:
            image = LARGE_CACTUS[cactus_type]
            RECT_Y = self.POSITION_Y_LARGE
        else:
            image = SMALL_CACTUS[cactus_type]
            RECT_Y = self.POSITION_Y_SMALL
            
        super().__init__(image)
        self.rect.y = RECT_Y
