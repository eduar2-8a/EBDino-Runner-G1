import pygame

from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DINO_START, FONT_STYLE
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.score import Score


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
        self.score = Score()
        self.death_count = 0
        self.max_score = 0
        self.final_score = 0

    def run(self):
        self.executing = True
        while self.executing:
            if not self.playing:
                self.show_menu()
        pygame.quit()

    def start_game(self):
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

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manager.update(self, self.on_death)
        self.score.update(self)

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255, 255, 255))
        self.draw_background()
        self.obstacle_manager.draw(self.screen)
        self.player.draw(self.screen)
        self.score.draw(self.screen)
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
        self.death_count += 1
        self.playing = False
        self.final_score = self.score.score
        if self.final_score > self.max_score:
            self.max_score = self.final_score 

    def show_menu(self):
        # Rellenar de color blanco la pantalla
        self.screen.fill((255, 255, 255))
        # Mensaje de bienvenida centrada
        if not self.death_count:
            self.draw_text("Welcome, press any key to start!", True, 32, 0, 0)
        else:
            self.draw_text(f"Your score: {self.final_score}, Deathcount: {self.death_count}, Max Score: {self.max_score}", True, 32, 0, 0)
            self.reset()
            #tarea aqui: añadir un mensaje de reinicio del juego y del numero de muertes,
            #y otro de cuantos puntos obtuve en una run
        # Poner una imagen a modo de icono en el centro
        self.screen.blit(DINO_START, (SCREEN_WIDTH // 2 - 40, 
                                      SCREEN_HEIGHT // 2 -140))
        # Plasmar los cambios
        pygame.display.flip()
        # Manejar eventos
        self.handle_menu_events()

    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.executing = False

            if event.type == pygame.KEYDOWN:
                self.start_game()

    def reset(self):
        self.obstacle_manager.reset()
        self.player.reset()
        self.score.reset(self)

    #if the text needs to be centered, just enter True as 2nd parameter and left the last two parameters (pos y and x) as 0 
    def draw_text(self, text, is_centered, size, pos_x, pos_y):
        font = pygame.font.Font(FONT_STYLE, size)
        text = font.render(text, True, (0, 0, 0))
        text_rect = text.get_rect()

        if is_centered:
            text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        else:
            text_rect.center = (pos_x, pos_y)
        self.screen.blit(text, text_rect)
        