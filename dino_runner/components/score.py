import pygame
from dino_runner.utils.constants import FONT_STYLE
from dino_runner.components.text import draw_text


class Score:
    def __init__(self):
        self.score = 0
        self.max_score = 0
        self.final_score = 0

    def update(self, game):
        self.score += 1
        if self.score % 100 == 0:
            game.game_speed += 2

    def draw(self, screen):
        draw_text(screen, f"Score: {self.score}", False, 24, 950, 30, (0,0,0))

    def reset(self, game):
        if self.score > 0:
            self.final_score = self.score
        if self.final_score > self.max_score:
            self.max_score = self.final_score
        self.score = 0
        game.game_speed = game.GAME_SPEED
        
