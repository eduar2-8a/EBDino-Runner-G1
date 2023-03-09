import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DINO_START, SHIELD_TYPE, GAME_OVER
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.obstacles.cloud.cloud_manager import CloudManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager

from dino_runner.components.score import Score
from dino_runner.components.text import draw_text


class Game:
    GAME_SPEED = 20

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = self.GAME_SPEED
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.executing = False

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()
        self.power_up_manager = PowerUpManager()
        self.cloud_manager = CloudManager()
        self.score = Score()
        self.death_count = 0

    def run(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
        pygame.quit()

    def start_game(self):
        self.reset()
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.executing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self, self.on_death)
        self.power_up_manager.update(self.game_speed, self.score.score, self.player)
        self.cloud_manager.update(self.game_speed, self.score.score)
        self.score.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.obstacle_manager.draw(self.screen)
        self.cloud_manager.draw(self.screen)
        self.power_up_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.score.draw(self.screen)
        self.player.check_power_up(self.screen)
        #pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def on_death(self):
        is_invincible = self.player.type == SHIELD_TYPE
        if not is_invincible:
            self.player.on_death()
            self.death_count += 1
            self.game_speed = 0
            self.playing = False

    def show_menu(self):
        # Rellenar de color blanco la pantalla
        self.screen.fill((255, 255, 255))
        # Mensaje de bienvenida centrada
        if not self.death_count:
            draw_text(self.screen, "Welcome, press any key to start!",
                       True, 32, 0, SCREEN_HEIGHT // 2, (0,0,0))
            self.screen.blit(DINO_START, (SCREEN_WIDTH // 2 - 40, 
                            SCREEN_HEIGHT // 2 -140))
        else:
            draw_text(self.screen, f"Your score: {self.score.final_score}",
                       True, 32, 0, SCREEN_HEIGHT // 2, (0,0,0))
            draw_text(self.screen, f"Deaths: {self.death_count}",
                       True, 24, 0, SCREEN_HEIGHT // 2 + 30, (0,0,0))
            draw_text(self.screen, f"Hi-Score: {self.score.max_score}",
                       True, 24, 0, SCREEN_HEIGHT // 2 + 60, (0,0,0))
            self.screen.blit(GAME_OVER, (SCREEN_WIDTH // 2 -190, 
                            SCREEN_HEIGHT // 2 -140))
            self.reset()

        pygame.display.flip()
        self.handle_menu_events()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False

            if event.type == pygame.KEYDOWN:
                self.start_game()

    def reset(self):
        self.game_speed = self.GAME_SPEED
        self.player.reset()
        self.obstacle_manager.reset()
        self.power_up_manager.reset()
        self.cloud_manager.reset()
        self.score.reset(self)
        