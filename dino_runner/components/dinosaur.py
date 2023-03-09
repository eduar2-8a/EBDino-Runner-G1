from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD
from dino_runner.components.text import draw_text

import pygame


DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD}

class Dinosaur(Sprite):
    POSITION_X = 80
    POSITION_Y = 310
    POSITION_Y_DUCK = 342
    JUMP_VELOCITY = 8.5


    def __init__(self):
        self.image = RUNNING[0]
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y
        self.type = DEFAULT_TYPE
        # En que momento deberia acabar el power up
        self.power_up_time_up = 0

        self.step = 0
        self.action = DINO_RUNNING
        self.jump_velocity = self.JUMP_VELOCITY

    def update(self, user_input):

        if self.action != DINO_JUMPING:
            if user_input[pygame.K_UP]:
                self.action = DINO_JUMPING
            elif user_input[pygame.K_DOWN]:
                self.action = DINO_DUCKING
            else:
                self.action = DINO_RUNNING

        if self.action == DINO_RUNNING:
            self.run()
        elif self.action == DINO_JUMPING:
            self.jump()
        elif self.action == DINO_DUCKING:
            self.ducking()
        
        if self.step >= 10:
                self.step = 0            

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x , self.rect.y))

    def run(self):
        self.image = RUNNING[self.step // 5]
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y
        self.step += 1

    def jump(self):
        self.image = JUMPING
        self.rect.y -= self.jump_velocity * 4
        self.jump_velocity -= 0.8
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.jump_velocity = self.JUMP_VELOCITY
            self.action = DINO_RUNNING
            self.rect.y = self.POSITION_Y

    def ducking(self):
        self.rect = self.image.get_rect()
        self.rect.y = self.POSITION_Y_DUCK
        self.rect.x = self.POSITION_X
        self.image = DUCKING[self.step // 5]
        self.step += 1

    def reset(self):
        self.rect.y = self.POSITION_Y
        self.rect.x = self.POSITION_X
        self.jump_velocity = self.JUMP_VELOCITY

    def on_pick_power_up(self, power_up):
        self.type = power_up.type
        self.power_up_time_up = power_up.start_time + (power_up.duration * 1000)
    
    def check_power_up(self, screen):
        if self.type == SHIELD_TYPE:
            time_to_show = round((self.power_up_time_up - pygame.time.get_ticks()) /1000, 2)
            if time_to_show >= 0:
                pass
                draw_text(screen, f"{self.type.capitalize()} enabled for {time_to_show} seconds.", True, 16, 0, 50, (0,0,0))
            else:
                self.type = DEFAULT_TYPE
                self.power_up_time_up = 0