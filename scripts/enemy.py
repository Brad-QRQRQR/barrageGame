import pygame
from pygame.locals import *
from pygame.sprite import *
import random, math
from scripts.boss import rect_to_rect_collide

class Enemy:
    hurt = 5

    def __init__(self):
        super().__init__()
        self.speed = 3
        
        self.action = 1
        self.action_timer = 0
        self.action_timer_limited = 10
        
        self.act1 = pygame.image.load('images/enemy_2.png').convert()
        self.act2 = pygame.image.load('images/enemy_3.png').convert()
        self.image = pygame.image.load('images/enemy.png').convert()
        
        self.image.set_colorkey((255, 255, 255))
        self.act1.set_colorkey((255, 255, 255))
        self.act2.set_colorkey((255, 255, 255))
        
        self.rect = self.image.get_rect()

        self.rect.width = int(1.5 * self.rect.width)
        self.rect.height = int(1.5 * self.rect.height)
        
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.act1 = pygame.transform.scale(self.act1, (self.rect.width, self.rect.height))
        self.act2 = pygame.transform.scale(self.act2, (self.rect.width, self.rect.height))

        self.act1_c = self.act1.copy()
        self.act2_c = self.act2.copy()
        self.image_c = self.image.copy()

        self.rect.x = 30 * random.randint(1, 10)
        self.rect.y = -10

        self.fly_attack = False
        self.angel = 0

    def update(self):
        if self.fly_attack and self.angel != 0:
            self.rect.centerx += self.speed * math.sin(self.angel * math.pi / 180)
            self.rect.centery += self.speed * math.cos(self.angel * math.pi / 180)
        else:
            self.rect.y += self.speed
        self.action_timer += 1
        if self.action_timer >= self.action_timer_limited:
            self.action += 1
            self.action_timer = 0
        if self.action > 3:
            self.action = 1

    def attack(self, player):
        if self.fly_attack:
            pass
        else:
            if self.rect.x < player.rect.x + player.rect.width and self.rect.x + self.rect.width > player.rect.x:
                pass
            elif self.rect.y >= player.rect.y:
                pass
            else:
                self.angel = math.atan((self.rect.center[0] - player.rect.center[0]) / (self.rect.center[1] - player.rect.center[1])) / (math.pi / 180)
                self.image = pygame.transform.rotate(self.image_c, self.angel)
                self.act1 = pygame.transform.rotate(self.act1_c, self.angel)
                self.act2 = pygame.transform.rotate(self.act2_c, self.angel)
                self.rect.x -= self.rect.width - self.image.get_width()
                self.rect.y -= self.rect.height - self.image.get_height()

def add_enemy(enemies):
    enemy = Enemy()
    enemies.append(enemy)

def blit_enemy(window, enemies, player):
    for e in enemies:
        if judge_fly_attack(e, player):
            e.attack(player)
            e.fly_attack = True
        e.update()
        if e.action == 1:
            window.blit(e.image, (e.rect.x, e.rect.y))
        if e.action == 2:
            window.blit(e.act1, (e.rect.x, e.rect.y))
        if e.action == 3:
            window.blit(e.act2, (e.rect.x, e.rect.y))
        if e.rect.y + e.rect.height >= 340:
            enemies.remove(e)

def judge_fly_attack(enemy, player):
    judgment = math.sqrt((enemy.rect.x - player.rect.x) ** 2 + (enemy.rect.y - player.rect.y) ** 2)
    if judgment < enemy.speed * 30:
        return True
    else:
        return False

def add_fly_particles(particles, enemy, player):
    addition = [[random.randint(5, 10), random.randint(i, 2 * i)] for i in range(3)]
    if player.rect.x < enemy.rect.x:
        for a in addition:
            for i in range(a[0]):
                particles.add(
                    player.rect.center[0] + i * a[1] * math.sin(random.uniform(0.1, math.pi / 4 - 0.1)), 
                    player.rect.center[1] - i * a[1] * math.cos(random.uniform(0.1, math.pi / 4 - 0.1)), 
                    -enemy.speed * math.sin(enemy.angel * math.pi / 180), 
                    -enemy.speed * math.cos(enemy.angel * math.pi / 180), 
                    5 - i * 0.1, 
                    0.2
                )
    else:
        for a in addition:
            for i in range(a[0]):
                particles.add(
                    player.rect.center[0] - i * a[1] * math.sin(random.uniform(0.1, math.pi / 4 - 0.1)), 
                    player.rect.center[1] - i * a[1] * math.cos(random.uniform(0.1, math.pi / 4 - 0.1)), 
                    -enemy.speed * math.sin(enemy.angel * math.pi / 180), 
                    -enemy.speed * math.cos(enemy.angel * math.pi / 180), 
                    5 - i * 0.1, 
                    0.2
                )
    
def show_fly_particles(particles, display):
    particles.draw(display, (0, 0, 0))

def add_death_particles(death_particles, enemy):
    for _ in range(5):
        death_particles.add(enemy.rect.x + int(enemy.rect.width / 2), enemy.rect.y + int(enemy.rect.height / 2), random.randint(-2, 2), -random.randint(0, 2), random.randint(10, 14), random.randint(10, 14), 0.5, 0.5)

def show_death_effects(death_particles, display):
    death_particles.draw(display, (65, 54, 52))

def enemy_collide(bullets, enemies, score, death_particles, sound):
    for e in enemies:
        if e.rect.y > 0:
            for b in bullets:
                if rect_to_rect_collide(b, e):
                    add_death_particles(death_particles, e)
                    sound.play()
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 1
                    break
    return score

def enemy_to_skill12_collide(bullets, enemies, score, death_particles, sound):
    if len(bullets) > 0:
        for e in enemies:
            if e.rect.y > 0:
                for b in bullets:
                    if rect_to_rect_collide(e, b):
                        enemies.remove(e)
                        add_death_particles(death_particles, e)
                        sound.play()
                        score += 1
                        break
    return score

def cattack_to_enemy_collide(enemies, player, death_particles, sound):
    for e in enemies:
        player.rect.x -= 5
        player.rect.y -= 5
        player.rect.width += 10
        player.rect.height += 10
        if rect_to_rect_collide(e, player):
            add_death_particles(death_particles, e)
            sound.play()
            enemies.remove(e)
        player.rect.x += 5
        player.rect.y += 5
        player.rect.width -= 10
        player.rect.height -= 10

def player_to_enemy_collide(enemies, player, particles, sound):
    for e in enemies:
        if rect_to_rect_collide(e, player):
            player.health -= e.hurt
            sound.play()
            add_fly_particles(particles, e, player)
            enemies.remove(e)