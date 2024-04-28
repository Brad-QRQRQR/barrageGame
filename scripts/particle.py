import pygame
from pygame.locals import *

class CircleParticle:
    def __init__(self):
        self.particles = []
        
    def add(self, pos_x, pos_y, x_move, y_move, radius, size_minus):
        self.particles.append([[pos_x, pos_y], [x_move, y_move], [radius, size_minus]])

    def draw(self, display, color, light = False, light_color = (255, 255, 255), multiple = 2, effect = BLEND_ADD):
        for p in self.particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2][0] -= p[2][1]

            if p[2][0] <= 0:
                self.particles = [new for new in self.particles if new != p]
            else:
                pygame.draw.circle(display, color, [int(p[0][0]), int(p[0][1])], int(p[2][0]))

            if light:
                light_radius = int(p[2][0] * multiple)
                display.blit(
                    self.add_lighting_surf(light_radius, light_color),
                    [int(p[0][0]) - light_radius, int(p[0][1]) - light_radius],
                    special_flags = effect
                )

    def add_lighting_surf(self, radius, color):
        surf = pygame.Surface((radius * 2, radius * 2))
        pygame.draw.circle(surf, color, [radius, radius], radius)
        surf.set_colorkey((0, 0, 0))
        return surf

class RectParticle:
    def __init__(self):
        self.particles = []

    def add(self, pos_x, pos_y, x_move, y_move, width, height, w_minus, h_minus):
        self.particles.append([[pos_x, pos_y], [x_move, y_move], [width, height], [w_minus, h_minus]])

    def draw(self, display, color):
        for p in self.particles:
            p[0][0] += p[1][0]
            p[0][1] += p[1][1]
            p[2][0] -= p[3][0]
            p[2][1] -= p[3][1]

            if p[2][0] <= 0:
                self.particles = [new for new in self.particles if new != p]
            else:
                pygame.draw.rect(display, color, [p[0], [int(p[2][0]), int(p[2][1])]])