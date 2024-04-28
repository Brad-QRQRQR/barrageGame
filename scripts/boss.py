from scripts.particle import CircleParticle
import pygame, math, random
from pygame.locals import *
from scripts.bullet import lighting_surf


def lighting_surf_line(width, height, color, s_x, s_y, e_x, e_y, line_width):
    surf = pygame.Surface((width, height))
    pygame.draw.line(surf, color, [s_x, s_y], [e_x, e_y], line_width)
    surf.set_colorkey((0, 0, 0))
    return surf

class Boss:
    def __init__(self, DISPLAY_WIDTH):
        self.image = pygame.image.load('images/Boss_images/Boss.png').convert()
        self.image.set_colorkey((0, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.y = 10

        self.font_size = 8
        self.font = pygame.font.SysFont('Calibri', self.font_size)

        self.health = 125 * 20 #5000
        self.health_barrect = pygame.Rect([DISPLAY_WIDTH / 2 - 125 / 2, self.rect.y - 6, int(self.health / 40), 5])
        self.under_bar = pygame.Rect([DISPLAY_WIDTH / 2 - 125 / 2, self.rect.y - 6, 125, 5])
        self.health_barcolor = [(0, 0, 100), (255, 201, 14), (255, 0,0)]
        self.health_barcolor_tag = 0

        self.appear = False
        self.appear_timer = 0
        self.alive = True

    @property
    def health_barcolor_tag(self):
        return self.__health_barcolor_tag

    @health_barcolor_tag.setter
    def health_barcolor_tag(self, new):
        self.__health_barcolor_tag = new
        if self.__health_barcolor_tag >= 3:
            self.__health_barcolor_tag = 0

    def health_report(self, display):
        #self.health -= 1
        #self.health_barrect.width -= 1
        if self.health_barrect.width < 0:
            self.health_barrect.width = self.health % 125
            self.health_barcolor_tag += 1

        if self.health >= 125:
            pygame.draw.rect(display, self.health_barcolor[self.health_barcolor_tag + 1 if self.health_barcolor_tag < 2 else 0], self.under_bar)
        pygame.draw.rect(display, self.health_barcolor[self.health_barcolor_tag], self.health_barrect)
        display.blit(self.font.render(f'x{str(self.health // 125)}', False, (0, 0, 0)), [self.health_barrect.x + 125 - 8 * 2, self.health_barrect.y])

class TentaclePart:
    hurt = 1
    def __init__(self, x, y, angel_speed, radius, path):
        self.original_image = pygame.image.load(path).convert()
        self.image = pygame.image.load(path).convert()
        self.original_image.set_colorkey((255, 255, 255))
        self.image.set_colorkey((255, 255, 255))

        self.original_rect = self.original_image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.x += x
        self.rect.y += y
        self.original_rect.x = self.rect.x
        self.original_rect.y = self.rect.y

        self.angel = 0
        self.angel_speed = angel_speed

        self.radius = radius

    def __rad_trans(self, angel):
        return angel * (math.pi / 180)
    
    def angel_change(self):
        self.angel += self.angel_speed

    def change_cdn(self, root):
        self.rect.x = root.rect.x + self.radius * math.sin(self.__rad_trans(self.angel))
        self.rect.y = root.rect.y + self.radius * math.cos(self.__rad_trans(self.angel))

    def update(self, root):
        self.turn_image()
        self.change_cdn(root)

    def turn_image(self, angel = 0, special_angel = False):
        if special_angel:
            self.image = pygame.transform.rotate(self.original_image, angel)
        else:
            self.image = pygame.transform.rotate(self.original_image, self.angel)

    def shake(self, speed):
        self.rect.x += speed * math.sin(self.__rad_trans(self.angel))
        self.rect.y += speed * math.cos(self.__rad_trans(self.angel))

class FlameBomb:
    hurt = 20
    def __init__(self, DISPLAY_WIDTH, DISPLAY_HEIGHT):
        self.circles = []

        self.color = (255, 255, 255)

        self.right_edge = DISPLAY_WIDTH
        self.left_edge = 0
        self.bottom_edge = DISPLAY_HEIGHT

    def add(self, number, postion_x, positon_y, speed, size):
        for _ in range(number):
            angel = random.uniform(0.1, math.pi - 0.1)
            if len(self.circles) > 0:
                a = []
                for c in self.circles:
                    a.append(c[1][0])
                while speed * math.cos(angel) in a:
                    angel = random.uniform(0.6, math.pi)
            self.circles.append([[postion_x, positon_y], [speed * math.cos(angel), speed * abs(math.sin(angel))], size])
    
    def update(self):
        for c in self.circles:
            c[0][0] += c[1][0]
            c[0][1] += c[1][1]
            self.check_edge(c)

    def check_edge(self, circle):
        if circle[0][0] >= self.right_edge:
            circle[1][0] = -1 * circle[1][0]
        if circle[0][0] <= self.left_edge:
            circle[1][0] = -1 * circle[1][0]
        if circle[0][1] >= self.bottom_edge - 1:
            self.circles = [c for c in self.circles if c != circle]

    def draw(self, display):
        for c in self.circles:
            radius = 1.5 * c[2]
            color = (200, 0, 0)
            display.blit(
                lighting_surf(int(radius), color),
                [int(c[0][0]) - int(radius), int(c[0][1]) - int(radius)],
                special_flags = BLEND_MAX
            )
            pygame.draw.circle(display, self.color, [int(c[0][0]), int(c[0][1])], c[2])

class Ray:
    hurt = 5
    def __init__(self, x, y, displayheight):
        self.rect = pygame.Rect([x, y], [1, displayheight - y])
        self.timer = 0
        self.warning_time = 30
        self.limited_width = 15

    def update(self):
        self.timer += 1
        if self.timer > self.warning_time and self.timer <= self.warning_time + self.limited_width:
            self.rect.width += 1
        elif self.timer > self.warning_time + self.limited_width:
            self.rect.width -= 1

    def draw(self, display, dispalyheight):
        pygame.draw.line(display, (0, 0, 0), [self.rect.x, self.rect.y], [self.rect.x, dispalyheight], self.rect.width)

def new_tentaclepart(tentacle, parts, boss, left = True):
    for i in range(parts):
        if i < parts - 1:
            path = 'images/Boss_images/boss_tentacle_tile_3.png'
        elif i == parts - 1:
            path = 'images/Boss_images/boss_tentacle_front.png'
        
        if left:
            new = TentaclePart(34, 32 + boss.rect.y + (i * 10), 0.2 * (i + 1), (i * 10), path)
            tentacle.append(new)
        else:
            new = TentaclePart(298, 32 + boss.rect.y + (i * 10), -0.2 * (i + 1), (i * 10), path)
            tentacle.append(new)

def new_tentaclepart_animation(tentacle, timer, parts, new_ten, turn, multiple = 3): #15*3+9
    ten_alive = False
    number = parts

    timer += 1
    
    if timer == 1:
        for i in range(len(tentacle)):
            tentacle[i].angel_speed = turn * 0.1 * i
    elif timer == parts * multiple:
        for i in range(len(tentacle)):
            tentacle[i].angel_speed = turn * -0.1 * i

    if timer < parts * multiple:
        turn_tentacle(tentacle, parts)
        number = timer // multiple
    elif timer >= parts * multiple + 10 and timer < parts * multiple * 2 + 9:
        turn_tentacle(tentacle, parts)
        number = parts
    elif timer == parts * multiple * 2 + 9:
        new_ten = False
        ten_alive = True
        timer = 0
        for i in range(len(tentacle)):
            tentacle[i].angel_speed = turn * 0.2 * (i + 1)

    return timer, new_ten, ten_alive, number

def tentacle_normally_shake(tentacle, parts, timer, shake = True, during = 6):
    if shake:
        timer += 1
        if timer % during == 0:
            turn_tentacle(tentacle, parts)
        if timer % (during * 5) == 0:
            change_angel_speed(tentacle)
        if timer == (during * 5) * 2:
            timer = 0
    return timer

def angel_to_zero(tentacle):
    for i in range(len(tentacle)):
        tentacle[i].angel = 0

def positive_angel_speed(tentacle):
    for i in range(len(tentacle)):
        tentacle[i].angel_speed = abs(tentacle[i].angel_speed)

def negative_angel_speed(tentacle):
    for i in range(len(tentacle)):
        tentacle[i].angel_speed = -1 * abs(tentacle[i].angel_speed)

def left_tentacle_to_original(tentacle, boss):
    for i in range(len(tentacle)):
        tentacle[i].rect.x = 34
        tentacle[i].rect.y = 32 + boss.rect.y + (i * 10)

def right_tentacle_to_original(tentacle, boss):
    for i in range(len(tentacle)):
        tentacle[i].rect.x = 298
        tentacle[i].rect.y = 32 + boss.rect.y + (i * 10)

def angel_track(tentacle, player):
    if player.rect.center[1] == tentacle[-1].rect.center[1]:
        if player.rect.x > tentacle[-1].rect.x:
            angel = 45
        elif player.rect.x < tentacle[-1].rect.x:
            angel = -45
        else:
            angel = 0
    elif player.rect.center[1] > tentacle[-1].rect.center[1]:
        angel = math.atan((player.rect.center[0] - tentacle[-1].rect.center[0]) / (player.rect.center[1] - tentacle[-1].rect.center[1])) / (math.pi / 180)
    else:
        angel = 180 - (-1) * math.atan((player.rect.center[0] - tentacle[-1].rect.center[0]) / (player.rect.center[1] - tentacle[-1].rect.center[1])) / (math.pi / 180)
    #print(angel)
    #if player.rect.x > tentacle[-1].rect.x:
    #    angel = math.atan((player.rect.center[0] - tentacle[-1].rect.center[0]) / (player.rect.center[1] - tentacle[-1].rect.center[1])) / (math.pi / 180)
    #elif player.rect.x == tentacle[-1].rect.x:
    #    angel = 0
    #else:
    #    angel = math.atan((tentacle[-1].rect.center[0] - player.rect.center[0]) / (tentacle[-1].rect.center[1] - player.rect.center[1])) / (math.pi / 180)
    return angel

def tentacle_track(tentacle, player, angel, displayheight, displaywidth, display):
    pygame.draw.line(display, (0, 0, 0), [tentacle[-1].rect.center[0], tentacle[-1].rect.y + tentacle[-1].rect.height], [player.rect.x, player.rect.y])

def extension_time(tentacle, player, angel, displayheight, displaywidth):
    if player.rect.y > tentacle[-1].rect.y:
        adds = (displayheight - tentacle[-1].rect.y) * 1 / math.cos(angel * math.pi / 180)
    elif player.rect.y < tentacle[-1].rect.y:
        adds = math.sqrt(
            (tentacle[-1].rect.center[0] - displaywidth) ** 2 +
            (tentacle[-1].rect.y + tentacle[-1].rect.height - tentacle[-1].rect.center[1] + (displaywidth - tentacle[-1].rect.center[0]) / math.tan(angel * math.pi / 180)) ** 2
        )
    else:
        adds = abs(displaywidth - tentacle[-1].rect.y)
    adds = int(adds) // 10 + 1
    return adds

def extend(tentacle):
    add = TentaclePart(tentacle[0].rect.x, tentacle[0].rect.y, tentacle[0].angel_speed, tentacle[0].radius, 'images/Boss_images/boss_tentacle_tile_3.png')
    tentacle.insert(1, add)

def del_tentacle_length(tentacle, parts):
    if len(tentacle) > parts:
        if tentacle[1].rect.y <= tentacle[0].rect.y:
            tentacle.pop(1)

def tentacle_attack(tentacle, angel, displayheight, displaywidth, tmp, speed = 10):
    if tentacle[-1].rect.y < displayheight - 10:
        if int(angel) % 360 >= 0 and int(angel) % 360 <= 180:
            if tentacle[-1].rect.x >= displaywidth - 10:
                return False
        else:
            if tentacle[-1].rect.x <= 10:
                return False
        m = (tentacle[0].rect.x - tmp[0]) / (tentacle[0].rect.y - tmp[1])
        thita = math.atan(m)
        for i in range(1, len(tentacle)):
            tentacle[i].rect.y += speed * math.cos(thita)
            tentacle[i].rect.x = (tentacle[i].rect.y - tentacle[0].rect.y) * m + tentacle[0].rect.x
        tmp[0] += speed * math.sin(angel * math.pi / 180)
        tmp[1] += speed * math.cos(angel * math.pi / 180)
        return True
    else:
        return False

def tentacle_back(tentacle, angel, tmp, speed = 10):
    m = (tentacle[0].rect.x - tmp[0]) / (tentacle[0].rect.y - tmp[1])
    thita = math.atan(m)
    for i in range(1, len(tentacle)):
        tentacle[i].angel -= 2 if tentacle[i].angel < 0 else 0 
        tentacle[i].turn_image()
        tentacle[i].rect.y -= speed * math.cos(thita)
        tentacle[i].rect.x = (tentacle[i].rect.y - tentacle[0].rect.y) * m + tentacle[0].rect.x
    tmp[0] -= speed * math.sin(angel * math.pi / 180)
    tmp[1] -= speed * math.cos(angel * math.pi / 180)

def change_angel(tentacle, angel):
    for i in range(len(tentacle)):
        tentacle[i].angel = angel
        tentacle[i].turn_image()

def flomebomb_attack(left_ten, right_ten, flamebomb, timer, parts, attack, particles, display, multiple = 20): #25*3+3*15-1
    timer += 1
    if timer <= 3 * multiple:
        if timer % 3 == 0:
            turn_tentacle(left_ten, parts)
            turn_tentacle(right_ten, parts)
        if timer == 3 * multiple:
            change_angel_speed(left_ten)
            change_angel_speed(right_ten)
    elif timer > 3 * multiple and timer < 3 * (multiple + 10):
        r = (timer - (3 * multiple)) * 2

        if timer >= 3 * (multiple + 5) and timer < 3 * (multiple + 8):
            r = 3 * 5 * 2
        elif timer >= 3 * (multiple + 8):
            r = 3 * 5 * 2 - (timer - 3 * (multiple + 8)) * 3

        lines = [(175 + r * math.sin(math.pi * 2 / 20 * (i + 1)) + random.uniform(-6.0, 6.0), 70 + r * math.cos(math.pi * 2 / 20 * (i + 1))) for i in range(20)]
        pygame.draw.lines(display, (255, 255, 255), True, lines, 2)
 
        if r - 3 > 0:
            pygame.draw.circle(display, (255, 255 ,255), [175, 70], r - 3)
        
        display.blit(
            lighting_surf(r + 3, (100, 0, 0)), 
            (175 - (r + 3), 70 - (r + 3)),
            special_flags = BLEND_RGB_ADD
        )
        
        particles.add(175 + random.randint(-6, 6), 70 + random.randint(-6, 6), random.uniform(-2.0, 2.0), random.uniform(-2.0, 2.0), random.randint(2, 3), 0.1)
        particles.draw(display, (0, 0, 0))

        if timer == 3 * (multiple + 10) - 1:
            flamebomb.add(20, 175, 70, 4, 5)
    elif timer >= 3 * (multiple + 10):
        if timer % 3 == 0:
            turn_tentacle(left_ten, parts)
            turn_tentacle(right_ten, parts)
        if timer == 3 * (multiple + 10) + 3 * multiple - 1:
            change_angel_speed(left_ten)
            change_angel_speed(right_ten)
            timer = 0
            attack = False
            particles = CircleParticle()
    
    return timer, attack, particles

def new_ray(rays, displayheight, displaywidth):
    ray = Ray(random.randint(10, displaywidth), 0, displayheight)
    rays.append(ray)

def remove_ray(ray):
    if ray.rect.width <= 0:
        return True
    else:
        return False

def rays_update(rays):
    for r in rays:
        r.update()
        if remove_ray(r):
            rays = [new for new in rays if new != r]

def blit_rays(rays, display, displayheight):
    for r in rays:
        r.draw(display, displayheight)

def turn_tentacle(tentacle, number):    
    for i in range(-number, 0):
        tentacle[i].angel_change()
        tentacle[i].update(tentacle[0])
    return tentacle

def change_angel_speed(tentacle):
    for t in tentacle:
        t.angel_speed = -1 * t.angel_speed
    return tentacle

def blit_tentacle(tentacle, display, number):
    lines = []
    if number > 1:
        for i in range(number):
            lines.append([tentacle[i].rect.x + tentacle[i].image.get_width() / 2, tentacle[i].rect.y + tentacle[i].image.get_height() / 2])
        pygame.draw.lines(display, (255, 0, 0), False, lines, 6)

    for i in range(number):
        display.blit(tentacle[i].image, tentacle[i].rect)

def rect_to_rect_collide(a, b):
    if b.rect.x + b.rect.width > a.rect.x and b.rect.x < a.rect.x + a.rect.width:
        if b.rect.y < a.rect.y + a.rect.height and b.rect.y + b.rect.height > a.rect.y:
            return True
    return False

def boss_to_bullet_collide(boss, bullets, sound):
    for b in bullets:
        if rect_to_rect_collide(b, boss):
            sound.play()
            boss.health -= b.hurt
            boss.health_barrect.width -= b.hurt
            bullets.remove(b)

def boss_to_skill12_collide(boss, bullets, sound):
    if len(bullets) > 0:
        for b in bullets:
            if rect_to_rect_collide(b, boss):
                sound.play()
                boss.health -= b.hurt
                boss.health_barrect.width -= b.hurt
                bullets.remove(b)

def tentacle_to_bullet_collide(tentacle, bullets, tentacle_health, sound):
    for t in tentacle:
        for b in bullets:
            if rect_to_rect_collide(t, b):
                sound.play()
                tentacle_health -= b.hurt * 2
                bullets.remove(b)
    return tentacle_health

def tentacle_to_skill12_collide(tentacle, bullets, tentacle_health, sound):
    if len(bullets) > 0:
        for t in tentacle:
            for b in bullets:
                if rect_to_rect_collide(t, b):
                    sound.play()
                    tentacle_health -= b.hurt
                    bullets.remove(b)
    return tentacle_health

def tentacle_to_player_collide(tentacle, player, window_shake, ten_health, circle_hurt, display, hit_surf, sound):
    for t in tentacle:
        if rect_to_rect_collide(player, t):
            window_shake = 10
            if player.c_attack:
                ten_health -= circle_hurt
            else:
                sound.play()
                display.blit(hit_surf, (0, 0), special_flags = BLEND_RGB_ADD)
                player.health -= t.hurt
    return window_shake

def ray_to_player_collide(rays, player, display, hit_surf, sound):
    for r in rays:
        if r.timer > r.warning_time:
            if rect_to_rect_collide(player, r):
                sound.play()
                if player.c_attack:
                    pass
                else:
                    display.blit(hit_surf, (0, 0), special_flags = BLEND_RGB_ADD)
                    player.health -= r.hurt

def flamebomb_collide(circle, player):
    def see_range(minimal, maximum, num): #判斷圓形再矩形的哪邊
        if num <= minimal:
            return minimal
        elif num > minimal and num < maximum:
            return num
        elif num >= maximum:
            return maximum
    
    def collide(x1, y1, x2, y2, radius):
        d = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        return d <= radius

    x = see_range(player.rect.x, player.rect.x + player.rect.width, circle[0][0])
    y = see_range(player.rect.y, player.rect.y + player.rect.height, circle[0][1])
    return collide(x, y, circle[0][0], circle[0][1], circle[2])