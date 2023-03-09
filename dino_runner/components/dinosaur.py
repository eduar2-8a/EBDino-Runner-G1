from pygame.sprite import Sprite

from dino_runner.utils.constants import RUNNING, JUMPING, DUCKING, DEFAULT_TYPE, SHIELD_TYPE, DUCKING_SHIELD, JUMPING_SHIELD, RUNNING_SHIELD, DINO_DEAD, RUNNING_HAMMER, JUMPING_HAMMER, DUCKING_HAMMER, HAMMER_TYPE
from dino_runner.components.text import draw_text

import pygame


DINO_RUNNING = "running"
DINO_JUMPING = "jumping"
DINO_DUCKING = "ducking"

DUCK_IMG = {DEFAULT_TYPE: DUCKING, SHIELD_TYPE: DUCKING_SHIELD, HAMMER_TYPE: DUCKING_HAMMER}
JUMP_IMG = {DEFAULT_TYPE: JUMPING, SHIELD_TYPE: JUMPING_SHIELD, HAMMER_TYPE: JUMPING_HAMMER}
RUN_IMG = {DEFAULT_TYPE: RUNNING, SHIELD_TYPE: RUNNING_SHIELD, HAMMER_TYPE: RUNNING_HAMMER}

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

    def update_image(self, image, is_animated = True):
        if not is_animated:
            self.image = image
        else:
            self.image = image[self.step//5]
        self.step += 1

    def run(self):
        self.update_image(RUN_IMG.get(self.type))
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y

    def jump(self):
        self.update_image(JUMP_IMG.get(self.type), False)
        self.rect.y -= self.jump_velocity * 4
        self.jump_velocity -= 0.8
        if self.jump_velocity < -self.JUMP_VELOCITY:
            self.jump_velocity = self.JUMP_VELOCITY
            self.rect.y = self.POSITION_Y
            self.action = DINO_RUNNING

    def ducking(self):
        self.update_image(DUCK_IMG.get(self.type))
        self.rect = self.image.get_rect()
        self.rect.x = self.POSITION_X
        self.rect.y = self.POSITION_Y_DUCK

    def reset(self):
        self.jump_velocity = self.JUMP_VELOCITY
        self.rect.y = self.POSITION_Y
        self.action = DINO_RUNNING
        self.type = DEFAULT_TYPE
        self.power_up_time_up = 0
        self.step = 0

    def on_pick_power_up(self, power_up):
        self.type = power_up.type
        self.power_up_time_up = power_up.start_time + (power_up.duration * 1000)
    
    def check_power_up(self, screen):
        if self.type != DEFAULT_TYPE:
            time_to_show = round((self.power_up_time_up - pygame.time.get_ticks()) / 1000, 0)
            if time_to_show > 0:
                draw_text(screen, f"{self.type.capitalize()} enabled for {time_to_show} seconds.", True, 16, 0, 50, (0,0,0))
            else:
                self.type = DEFAULT_TYPE
                self.power_up_time_up = 0

    def on_death(self):
        if self.action == DINO_DUCKING:
            self.rect.y = self.POSITION_Y
            self.update_image(DINO_DEAD, False)    
        else:
            self.update_image(DINO_DEAD, False)

    def hammer_time(self):
        self.jump_velocity = self.JUMP_VELOCITY
        self.action == DINO_JUMPING