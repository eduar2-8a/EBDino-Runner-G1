import random
import pygame

from dino_runner.components.power_ups.shield import Shield
from dino_runner.components.power_ups.hammer import Hammer

class PowerUpManager:
    def __init__(self):
        self.power_ups = []
        #En que puntaje generaremos un power_up
        self.when_appears = 0

    def update(self, game_speed, score, player):
        power_up_variation = random.randint(0,1)
        if not self.power_ups:
            if self.when_appears == score:
                if power_up_variation == 0:
                    self.when_appears += random.randint(400, 800)
                    self.power_ups.append(Shield())
                else:
                    self.when_appears += random.randint(500, 1000)
                    self.power_ups.append(Hammer())

        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)

            if power_up.rect.colliderect(player.rect) and power_up.type :
                power_up.start_time = pygame.time.get_ticks()
                player.on_pick_power_up(power_up)
                self.power_ups.remove(power_up)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

    def reset(self):
        self.power_ups.clear()
        self.when_appears = random.randint(100, 200)