import pygame

from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.bird import Bird

class ObstacleManager:
    def __init__(self):
        self.obstacles = []
        self.obstacles.append(Bird())

    def update(self, game):
        if not self.obstacles:
            self.obstacles.append(Cactus())

        for obstacle in self.obstacles:
            obstacle.update(game.game_speed, self.obstacles)
            if game.player.rect.colliderect(obstacle.rect):
                pygame.time.delay(500)
                game.playing = False
                
    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)