from dino_runner.components.obstacles.cloud.cloud import Cloud

import random

class CloudManager:

    def __init__(self):
        self.clouds = []

    def update(self, game_speed, score):
        for cloud in self.clouds:
            cloud.update(game_speed, self.clouds)
        if score % 200 == 0:
            self.clouds.append(Cloud())
        if score % 350 == 0:
            self.clouds.append(Cloud())
    
    def draw(self, screen):
        for cloud in self.clouds:
            cloud.draw(screen)

    def reset(self):
        self.clouds.clear()
