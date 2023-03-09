import random
import pygame

from dino_runner.components.power_ups.power_up import PowerUp
from dino_runner.components.power_ups.shield import Shield

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        #En que puntaje generaremos un power_up
        self.when_appears = 0

    def update(self, game_speed, score, player):
        if not self.power_ups and self.when_appears == score:
            self.when_appears += random.randint(500, 900)
            self.power_ups.append(Shield())

        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)

            if power_up.rect.colliderect(player.rect):
                power_up.start_time = pygame.time.get_ticks()
                player.on_pick_power_up(power_up)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset(self):
        self.power_ups.clear()
        self.when_appears = random.randint(100, 200)