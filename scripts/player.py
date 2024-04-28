import pygame
from pygame.locals import *

def lighting_surf2(radius, color, width):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius, width)
    surf.set_colorkey((0, 0, 0))
    return surf

class Player:
    def __init__(self, setting):
        self.setting = setting

        self.speed = 4

        self.alive = True

        self.health = 800
        self.health_bar_image = pygame.image.load('images/health_bar.png').convert()
        self.health_bar_image.set_colorkey((255, 255, 255))
        self.health_bar_rect = self.health_bar_image.get_rect()
        self.health_bar_size = 16
        self.health_bar_rect.x = int(self.setting.SIZE[0] / 2 - self.health / self.health_bar_size - 10)
        self.health_bar_rect.y = 5
        self.health_line_rect = self.health_bar_rect.copy()
        self.health_line_rect.x += 2
        self.health_line_rect.y += 4
        self.health_line_rect.width -= 8
        self.health_line_rect.height -= 8

        self.image = pygame.image.load('images/player2.png').convert()
        self.image_c = pygame.image.load('images/player2.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.image_c.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()
        
        self.rect.x = setting.SIZE[0] / 4 - self.rect.width / 2
        self.rect.y = 284

        self.move_right = False
        self.move_left = False
        self.move_up = False
        self.move_down = False
        self.r_escalate = False
        self.l_escalate = False
        self.c_escalate = False
        self.r_attack = False
        self.l_attack = False
        self.c_attack = False

        self.turn = 0
        self.limit_turn = 45
        self.turn_speed = -1
        self.attack_timer = [0, 0, 0, 0] #n0 l1 r2 c3
        self.limit_power = 15
        self.circle_line = 1
        self.power_bar_image = pygame.image.load('images/power_bar.png').convert()
        self.power_bar_image2 = pygame.image.load('images/power_bar2.png').convert()
        self.power_bar_rect = self.power_bar_image.get_rect()

    def healht_report(self, display):
        self.health_line_rect.width = int(self.health / self.health_bar_size)
        display.blit(self.health_bar_image, self.health_bar_rect)
        pygame.draw.rect(display, (0, 255, 0), self.health_line_rect)

    @property
    def attack_timer(self):
        for i in range(len(self.__attack_timer)):
            if i == 0:
                pass
            else:
                if self.__attack_timer[i] >= self.power_bar_rect.width:
                    self.__attack_timer[i] = self.power_bar_rect.width
        return self.__attack_timer

    @attack_timer.setter
    def attack_timer(self, value):
        self.__attack_timer = value

    def update(self):
        if self.move_right and self.check_right_edge():
            self.rect.x += self.speed
        if self.move_left and self.check_left_edge():
            self.rect.x -= self.speed
        if self.move_up and self.check_up_edge():
            self.rect.y -= self.speed
        if self.move_down and self.check_down_edge():
            self.rect.y += self.speed

    def draw(self, display):
        display.blit(self.image, self.rect)
    
    def check_right_edge(self):
        if self.rect.x + self.rect.width >= int(self.setting.SIZE[0] / 2):
            self.rect.x = self.setting.SIZE[0] / 2 - self.rect.width
            return False
        return True

    def check_left_edge(self):
        if self.rect.x <= 0:
            self.rect.x = 0
            return False
        return True

    def check_up_edge(self):
        if self.rect.y <= 50 + 10 + 10 * 10:
            self.rect.y = 50 + 10 + 10 * 10
            return False
        return True

    def check_down_edge(self):
        if self.rect.y + self.rect.height >= int(self.setting.SIZE[1] / 2):
            self.rect.y = self.setting.SIZE[1] / 2 - self.rect.height
            return False
        return True

    def power_bar_render(self, display, displayheight, displaywidth, attack_way):
        if attack_way == 3:
            display.blit(self.power_bar_image2, [int(displaywidth / 2 - self.power_bar_rect.width / 2), displayheight- self.power_bar_rect.height - 10])
        else:
            display.blit(self.power_bar_image, [int(displaywidth / 2 - self.power_bar_rect.width / 2), displayheight- self.power_bar_rect.height - 10])
        pygame.draw.line(display, (0, 162, 232), [int(displaywidth / 2 - self.power_bar_rect.width / 2), displayheight- self.power_bar_rect.height - 10], [int(displaywidth / 2 - self.power_bar_rect.width / 2) + self.attack_timer[attack_way], displayheight- self.power_bar_rect.height - 10], self.power_bar_rect.height)

    def change_turn(self, attack_way):
        self.attack_timer[attack_way] += 1
        if attack_way == 1 or attack_way == 2:  
            self.turn += self.turn_speed
            if self.turn <= self.limit_turn - 5:
                self.turn_speed = 1
            if self.turn >= self.limit_turn + 1:
                self.turn_speed = -1
        if attack_way == 3:
            self.turn += self.turn_speed
            if self.turn <= -5:
                self.turn_speed = 1
            if self.turn >= 5:
                self.turn = -1
    
    def escalate_power(self, direction):
        self.attack_timer[0] = 0
        if direction == 'left':
            self.change_turn(1)
            self.image = pygame.transform.rotate(self.image_c, self.turn)
        elif direction == 'right':
            self.change_turn(2)
            self.image = pygame.transform.rotate(self.image_c, -1 * self.turn)
        elif direction == 'circle':
            self.change_turn(3)
            self.image = pygame.transform.rotate(self.image_c, self.turn)

    def release_power(self, direction, display):
        if direction == 'left':
            self.turn_speed = -1
            self.turn += self.turn_speed
            self.image = pygame.transform.rotate(self.image_c, self.turn)
        elif direction == 'right':
            self.turn_speed = -1
            self.turn += self.turn_speed
            self.image = pygame.transform.rotate(self.image_c, -1 * self.turn)
        elif direction == 'circle' and self.attack_timer[3] >= self.limit_power:
            self.attack_timer[0] = 0
            self.turn_speed = 10
            if self.turn % 120 in [60, 80, 100]:
                self.circle_line -= 2
            elif self.turn % 120 in [0, 20, 40]:
                self.circle_line += 2
            self.turn += self.turn_speed
            if self.turn == 10:
                self.center = self.rect.center
            self.image = pygame.transform.rotate(self.image_c, self.turn)
            self.rect.x = self.center[0] - self.image.get_width() / 2
            self.rect.y = self.center[1] - self.image.get_height() / 2
            display.blit(
                lighting_surf2(24, (0, 162, 232), self.circle_line),
                [self.rect.center[0] - 20, self.rect.center[1] - 24], 
                special_flags = BLEND_RGB_ADD
            )
            if self.turn >= 360:
                self.turn = 0
                self.turn_speed = -1
                self.circle_line = 3
                self.attack_timer[3] = 0
                del self.center
                self.c_attack = False           