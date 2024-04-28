import pygame, random, math
from pygame.locals import *
from scripts.particle import CircleParticle

class Bullet:
    hurt = 5
    def __init__(self, player):
        self.speed = 6
        
        self.image = pygame.image.load('images/bullet2.png').convert()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.x = player.rect.x + player.rect.width / 2 - self.rect.width / 2
        self.rect.y = player.rect.y

    def update(self):
        self.rect.y -= self.speed

def add_bullet(bullets, player):
    bullet = Bullet(player)
    bullets.append(bullet)

def shoot_bullet(bullets, display):
    for b in bullets:
        b.update()
        display.blit(b.image, b.rect)
        if b.rect.y <= 0:
            bullets.remove(b)

# def add_shoot_particles(particles, bullet):
#     for _ in range(5):
#         particles.append([
#             [bullet.rect.x, bullet.rect.y], #座標
#             [random.randint(-2, 2), -1 * random.random()], #x和y移動量
#             random.randint(3, 4) #半徑
#         ])
#     return particles

def lighting_surf(radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    surf.set_colorkey((0, 0, 0))
    return surf

# def show_shoot_effects(particles, display):
#     for p in particles:
#         p[0][0] += p[1][0]
#         p[0][1] += p[1][1]
#         p[1][1] -= 0.5
#         p[2] -= 0.5
        
#         color_tag = random.randint(1, 2)

#         radius = int(p[2]) * 2

#         if color_tag == 1:
#             pygame.draw.circle(display, (255, 255, 255), (int(p[0][0]), int(p[0][1])), int(p[2]))
#         else:
#             pygame.draw.circle(display, (255, 0, 0), (int(p[0][0]), int(p[0][1])), int(p[2]))
        
#         display.blit(lighting_surf(radius, (227, 176, 0)), 
#             [int(p[0][0]) - radius, int(p[0][1]) - radius], 
#             special_flags = BLEND_RGB_ADD
#         )

#         if p[2] <= 0:
#             particles = [o for o in particles if o != p]
#     return particles

class LeftBullet:
    def __init__(self, player):
        self.speed = -6

        self.hurt = 5

        self.angel = 45 * math.pi / 180
        
        self.image = pygame.image.load('images/left_bullet.png').convert()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.x = player.rect.x - self.rect.width / 2
        self.rect.y = player.rect.y

    def update(self):
        self.rect.x += self.speed * math.sin(self.angel)
        self.rect.y += self.speed * math.cos(self.angel)

def add_left_bullet(bullets, player, sound):
    if player.attack_timer[1] >= player.limit_power:
        bullet = LeftBullet(player)
        bullet.hurt += player.attack_timer[1] * 2
        bullets.append(bullet)
        sound.play()

def shoot_left_bullet(bullets, display):
    if len(bullets) > 0:
        for b in bullets:
            b.update()
            display.blit(b.image, b.rect)
            if b.rect.x <= 0 or b.rect.y <= 0:
                bullets.remove(b)
    
class RightBullet:
    def __init__(self, player):
        self.speed = -6

        self.hurt = 5

        self.angel = -45 * math.pi / 180

        self.image = pygame.image.load('images/right_bullet.png').convert()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()

        self.rect.x = player.rect.x + player.rect.width / 2 - self.rect.width / 2
        self.rect.y = player.rect.y

    def update(self):
        self.rect.x += self.speed * math.sin(self.angel)
        self.rect.y += self.speed * math.cos(self.angel)

def add_right_bullet(bullets, player, sound):
    if player.attack_timer[2] >= player.limit_power:
        bullet = RightBullet(player)
        bullet.hurt += player.attack_timer[2] * 2
        bullets.append(bullet)
        sound.play()

def shoot_right_bullet(bullets, display, displaywidth):
    if len(bullets) > 0:
        for b in bullets:
            b.update()
            display.blit(b.image, b.rect)
            if b.rect.x >= displaywidth or b.rect.y <= 0:
                bullets.remove(b)

class CircleBullet:
    hurt = 75
    def __init__(self):
        self.image = pygame.image.load('images/circle_bullet2.png').convert()
        self.image.set_colorkey((0, 0, 0))
        
        self.rect = self.image.get_rect()

    def update(self, player):
        self.rect.x = player.rect.center[0] + (player.rect.width / 2) * math.sin((player.turn + 180) * math.pi / 180)
        self.rect.y = player.rect.center[1] + (player.rect.height / 2) * math.cos((player.turn + 180) * math.pi / 180) - self.rect.height

    def draw(self, display):
        display.blit(self.image, self.rect)

def add_circle_bullet(bullets, player):
    bullet = CircleBullet()
    bullets.append(bullet)

def shoot_circle_bullet(bullets, display, player, particles, sound):
    for b in bullets:
        sound.play()
        b.update(player)
        add_cb_particles(particles, player, b)
        display.blit(b.image, b.rect)

def add_cb_particles(particles, player, bullet):
    for i in range(2):
        particles.add(bullet.rect.x + i, bullet.rect.y + i, 3 * math.sin(player.turn + 180), 3 * math.cos(player.turn + 180), 2, 0.1)

def show_cb_particles(particles, display):
    particles.draw(display, (0, 162, 232))