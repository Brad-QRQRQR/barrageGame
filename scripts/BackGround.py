import random
import pygame

class MapTile:
    def __init__(self, path):
        self.image = pygame.image.load(path).convert()
        self.rect = self.image.get_rect()

class GameMap:
    def __init__(self):
        self.tiles = []
        self.tile_size = (16, 17)
        self.shake_amount = 0

    def load_map(self, displaywidth, displayheight):
        for i in range(displayheight // self.tile_size[0] + 2):
            self.tiles.append([])
            for j in range(displaywidth // self.tile_size[1] + 2):
                tile = MapTile('images/background_tile3.png')
                tile.rect.x = j * self.tile_size[0]
                tile.rect.y = (i - 1) * self.tile_size[1]
                self.tiles[i].append(tile)

    def update(self):
        if self.shake_amount:
            add = self.shake_amount
        else:
            add = 1
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[1])):
                self.tiles[i][j].rect.y += add
        if self.tiles[0][0].rect.y >= 0:
            self.tiles.insert(0, self.tiles.pop())
            for i in range(len(self.tiles[1])):
                self.tiles[0][i].rect.x = i * self.tile_size[0]
                self.tiles[0][i].rect.y = -1 * self.tile_size[1]

    def shake(self, do):
        if do:
            self.shake_amount = random.randint(0, 14) - 7
        else:
            self.shake_amount = 0

    def draw(self, display):
        for i in range(len(self.tiles)):
            for j in range(len(self.tiles[1])):
                display.blit(self.tiles[i][j].image, self.tiles[i][j].rect)

def add_corners(displaywidth, displayheight):
    corners = []
    for i in range(2):
        for j in range(2):
            corner = MapTile('images/corner.png')
            if i == 0:
                image_c = pygame.transform.rotate(corner.image, -90 * j)
            else:
                image_c = pygame.transform.rotate(corner.image, 90 * (j + 1))
            corner.image = image_c
            corner.image.set_colorkey((255, 255, 255))
            corner.rect.x = (displaywidth - corner.rect.width) * j
            corner.rect.y = (displayheight - corner.rect.height) * i
            corners.append(corner)
    return corners

def shake_corners(corners, shake_amount):
    for c in corners:
        c.rect.y += shake_amount

def recover_corners(corners, displaywidth, displayheight):
    index = 0
    for i in range(int(len(corners) / 2)):
        for j in range(int(len(corners) / 2)):
            corners[index].rect.x = (displaywidth - corners[index].rect.width) * j
            corners[index].rect.y = (displayheight - corners[index].rect.height) * i
            index += 1

def blit_corners(corners, display):
    for c in corners:
        display.blit(c.image, c.rect)

def lighting_surf3(color, displaywidth, displayheight, width):
    surf = pygame.Surface((displaywidth, displayheight))
    pygame.draw.rect(surf, color, [[0, 0], [displaywidth, displayheight]], width)
    surf.set_colorkey((0, 0, 0))
    return surf