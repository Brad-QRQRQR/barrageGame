import pygame

class Set:
    def __init__(self):
        self.SIZE = (700, 680)
        self.caption = '勇者'
        self.color = (255, 201, 14)
        self.done = True
        self.clock = pygame.time.Clock()
        self.FPS = 60