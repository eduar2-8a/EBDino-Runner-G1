from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

import pygame
import random

class ObstacleManager:
    def __init__(self):
        self.obstacles = []

    def update(self, game, on_death):
        if not self.obstacles:
            rand_obstacle = random.randint(0,1)
            if rand_obstacle == 0:
                self.obstacles.append(Cactus())
            else:
                self.obstacles.append(Bird())

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.rect.colliderect(obstacle.rect):
                pygame.time.delay(100)
                on_death()

                
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)

    def reset(self):
        self.obstacles.clear()