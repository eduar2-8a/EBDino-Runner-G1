import pygame
from dino_runner.utils.constants import FONT_STYLE, SCREEN_HEIGHT, SCREEN_WIDTH

# color parameter is a tuple of 3 elements. You can enter a value on pos_y when is_centered = True
def draw_text(screen, text, is_centered, size, pos_x, pos_y, color):
    font = pygame.font.Font(FONT_STYLE, size)
    text = font.render(text, True, color)
    text_rect = text.get_rect()

    if is_centered:
        text_rect.center = (SCREEN_WIDTH // 2, pos_y)
    else:
        text_rect.center = (pos_x, pos_y)
    screen.blit(text, text_rect)