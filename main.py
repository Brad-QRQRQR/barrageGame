import pygame, sys, random

from pygame.locals import *

from scripts.setting import *
from scripts.bullet import *
from scripts.player import *
from scripts.enemy import *
from scripts.BackGround import *
from scripts.boss import *
from scripts.particle import *


#初始化
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

pygame.mixer.set_num_channels(64)

#類的呼叫
SETTING = Set()

DISPLAY_WIDTH = 350
DISPLAY_HEIGHT = 340

#視窗大小及名稱
window = pygame.display.set_mode(SETTING.SIZE)
caption = pygame.display.set_caption(SETTING.caption)

display = pygame.Surface((DISPLAY_WIDTH, DISPLAY_HEIGHT))
display_rect = display.get_rect()

saying_font = pygame.font.SysFont('Calibri', 16)

#菜單
def menu(display):
    button_image = pygame.image.load('images/button.png').convert()
    button_image.set_colorkey((0, 0, 0))
    button_rect = button_image.get_rect()
    button_rect.x, button_rect.y = int(DISPLAY_WIDTH / 2 - button_rect.width / 2), int(DISPLAY_HEIGHT / 2 - button_rect.height / 2)
    title = pygame.image.load('images/title.png').convert()
    title = pygame.transform.scale(title, (title.get_width() * 3, title.get_height() * 3))
    title.set_colorkey((255, 255, 255))

    background = GameMap()
    background.load_map(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    corners = add_corners(DISPLAY_WIDTH, DISPLAY_HEIGHT)

    click = False
    while True:
        display.fill(SETTING.color)

        background.update()
        background.draw(display)
        blit_corners(corners, display)

        mx, my = pygame.mouse.get_pos()

        #display.blit(title, (int(DISPLAY_WIDTH / 2 - title.get_width() / 2), 100))
        display.blit(button_image, button_rect)
        #display.blit(saying_font.render('Start game', False, (255, 255, 255)), [button_rect.x + 8, button_rect.y + 4])

        if button_rect.collidepoint((int(mx / 2), int(my / 2))):
            if click:
                game(display, background, corners)

        surf = pygame.transform.scale(display, SETTING.SIZE)
        window.blit(surf, (display_rect.x, display_rect.y))

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        SETTING.clock.tick(SETTING.FPS)

#遊戲
def game(display, background, corners, dream = False):
    running = True

    dream_level = 1

    click = False
    
    window_shake = 0
    hit_surf = lighting_surf3((100, 0, 0), DISPLAY_WIDTH, DISPLAY_HEIGHT, 20)

    ray_sound = pygame.mixer.Sound('music/ray.wav')
    hit_sound = pygame.mixer.Sound('music/hit.wav')
    enemy_hurt_sound = pygame.mixer.Sound('music/enemy_hurt.wav')
    enemy_burn_sound = pygame.mixer.Sound('music/enemy_burn.wav')
    shake_sound = pygame.mixer.Sound('music/shake.wav')
    es_power = pygame.mixer.Sound('music/escalate_power.wav')
    shoot = pygame.mixer.Sound('music/shoot.wav')
    circle_attack = pygame.mixer.Sound('music/circle_attack.wav')
    bomb = pygame.mixer.Sound('music/bomb.wav')

    ray_sound.set_volume(0.1)
    hit_sound.set_volume(0.3)
    enemy_hurt_sound.set_volume(0.3)
    enemy_burn_sound.set_volume(0.3)
    shake_sound.set_volume(0.1)
    es_power.set_volume(0.3)
    shoot.set_volume(0.4)
    circle_attack.set_volume(0.3)
    bomb.set_volume(0.4)

    pygame.mixer.music.load('music/background_music.mp3')
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

    player = Player(SETTING)
    player_death = CircleParticle()
    
    score_font_size = 8
    score_font = pygame.font.SysFont('Calibri', score_font_size)
    score = 0
    score_cdn = (DISPLAY_WIDTH - score_font_size * 4, DISPLAY_HEIGHT - score_font_size)

    restart_rect = pygame.Rect([int(DISPLAY_WIDTH / 2 - 96 / 2), int(DISPLAY_HEIGHT / 2 - 16 / 2)], [96, 16])
    restart_font = pygame.font.SysFont('Calibri', 14)

    bg_particles = CircleParticle()
    bg_particles_timer = 0
    death_particles = RectParticle()
    cb_particles = CircleParticle()
    fly_partciels = CircleParticle()

    bullets = []
    right_bullets = []
    left_bullets = []
    circle_bullets = []
    bullet_timer_limited = 0.6

    enemies = []
    enemy_timer = 0
    enemy_timer_limited = 0.7

    boss = Boss(DISPLAY_WIDTH)
    is_boss = False
    boss_death = CircleParticle()

    left_tentacle = []
    right_tentacle = []

    parts = 15
    
    boss_timers = {'new_leftten' : 0, 'new_rightten' : 0, 'flamebomb' : 0, 'ray_attack' : 0, 'leftten_attack' : 0, 'rightten_attack' : 0}
    new_leftten_timer = 0
    new_rightten_timer = 0
    n_leftten_timer = 0
    n_rightten_timer = 0
    t_leftten_timer = 0
    t_rightten_timer = 0
    flamebomb_timer = 0
    ray_timer = 0
    
    leftten_number = 0
    rightten_number = 0
    
    new_leftten = True
    new_rightten = True
    leftten_alive = False
    rightten_alive = False
    f_attack = False
    leftten_attack = False
    rightten_attack = False
    ray_attack = False

    leftten_health = 1000
    rightten_health = 1000
    
    new_tentaclepart(left_tentacle, parts, boss)
    new_tentaclepart(right_tentacle, parts, boss, left = False)
    
    flamebomb = FlameBomb(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    f_particles = CircleParticle()

    rays = []

    while running:
        #更新螢幕
        display.fill(SETTING.color)

        if window_shake > 0:
            window_shake -= 1

        if window_shake:
            background.shake(True)
            shake_sound.play()
            #shake_corners(corners, background.shake_amount)
        else:
            #recover_corners(corners, DISPLAY_WIDTH, DISPLAY_HEIGHT)
            background.shake(False)
        
        #背景
        background.update()
        background.draw(display)
        blit_corners(corners, display)

        #粒子特效
        bg_particles_timer += 1
        if bg_particles_timer >= 3:
            bg_particles_timer = 0
            bg_particles.add(10 * int(random.uniform(0.0, 5.0) * 14), 0, 0, random.randint(5, 10), random.randint(2, 3), 0.001)
        bg_particles.draw(display, (0, 0, 0))

        #魔王出現
        if score >= 200 * dream_level and not boss.appear and not is_boss and boss.alive:
            boss.rect.y = 0
            boss.appear = True

        if boss.appear:
            boss.appear_timer += 1
            if boss.appear_timer % 3 == 0:
                boss.rect.y += 1
            display.blit(boss.image, boss.rect)
            if boss.rect.y == 10:
                is_boss = True
                boss.appear = False

        if is_boss:
            display.blit(boss.image, boss.rect)
            boss.health_report(display)

            if boss_timers['new_leftten'] >= 720:
                new_tentaclepart(left_tentacle, parts, boss)
                boss_timers['new_leftten'] = 0
                new_leftten = True

            if boss_timers['new_rightten'] >= 720:
                new_tentaclepart(right_tentacle, parts, boss, left = False)
                boss_timers['new_rightten'] = 0
                new_rightten = True

            if new_leftten:
                new_leftten_timer, new_leftten, leftten_alive, leftten_number = new_tentaclepart_animation(left_tentacle, new_leftten_timer, parts, new_leftten, 1)
                leftten_health = 1000

            if new_rightten:
                new_rightten_timer, new_rightten, rightten_alive, rightten_number = new_tentaclepart_animation(right_tentacle, new_rightten_timer, parts, new_rightten, -1)
                rightten_health = 1000
            
            if leftten_health <= 0:
                leftten_alive = False

            if rightten_health <= 0:
                rightten_alive = False

            if leftten_alive and rightten_alive:
                if not leftten_attack and not rightten_attack:
                    boss_timers['flamebomb'] += 1
                if not ray_attack:
                    boss_timers['ray_attack'] += 1
                
                if boss_timers['flamebomb'] >= 15 * 3 + 9 + 133:
                    boss_timers['flamebomb'] = 0
                    f_attack = True
                    angel_to_zero(left_tentacle)
                    positive_angel_speed(left_tentacle)
                    angel_to_zero(right_tentacle)
                    negative_angel_speed(right_tentacle)

                if boss_timers['ray_attack'] >= 15 * 3 + 9 + 340:
                    boss_timers['ray_attack'] = 0
                    ray_attack = True

                if f_attack:
                    flamebomb_timer, f_attack, f_particles = flomebomb_attack(left_tentacle, right_tentacle, flamebomb, flamebomb_timer, parts, f_attack, f_particles, display)
                    leftten_number = parts
                    rightten_number = parts
                    if not f_attack:
                        angel_to_zero(left_tentacle)
                        positive_angel_speed(left_tentacle)
                        angel_to_zero(right_tentacle)
                        negative_angel_speed(right_tentacle)

                if ray_attack:
                    ray_timer += 1
                    if ray_timer <= 40 * 10:
                        if ray_timer % 40 == 0:
                            new_ray(rays, DISPLAY_HEIGHT, DISPLAY_WIDTH)    
                    else:
                        ray_attack = False
                        ray_timer = 0

            if leftten_alive:
                if boss_timers['leftten_attack'] >= 15 * 3 + 9 + 125:
                    boss_timers['leftten_attack'] = 0
                    leftten_attack = True
                if leftten_attack and not f_attack:
                    t_leftten_timer += 1
                    if t_leftten_timer > 0 and t_leftten_timer <= 50:
                        if t_leftten_timer <= 30:
                            l_angel = angel_track(left_tentacle, player)
                        left_tentacle[-1].turn_image(l_angel, True)
                        if t_leftten_timer % 2 == 0 or t_leftten_timer >= 30:
                            tentacle_track(left_tentacle, player, l_angel, DISPLAY_HEIGHT, DISPLAY_WIDTH, display)
                        if t_leftten_timer == 50:
                            l_time = extension_time(left_tentacle, player, l_angel, DISPLAY_HEIGHT, DISPLAY_WIDTH)
                            l_s_up = 1
                            l_tmp = [left_tentacle[-1].rect.x, left_tentacle[-1].rect.y]
                    elif t_leftten_timer > 50 and t_leftten_timer < 50 + 10 * (l_time - 1):
                        if t_leftten_timer == 51:
                            extend(left_tentacle)
                        change_angel(left_tentacle, l_angel)
                        if not tentacle_attack(left_tentacle, l_angel, DISPLAY_HEIGHT, DISPLAY_WIDTH, l_tmp):
                            if l_s_up <= len(left_tentacle) - 1:
                                l_s_up += 1
                                left_tentacle[-l_s_up].shake(-1)
                        else:
                            extend(left_tentacle)
                            window_shake = tentacle_to_player_collide(left_tentacle, player, window_shake, leftten_health, CircleBullet.hurt, display, hit_surf, shake_sound)
                        leftten_number = len(left_tentacle)
                    elif t_leftten_timer >= 50 + 10 * l_time:
                        tentacle_back(left_tentacle, l_angel, l_tmp)
                        del_tentacle_length(left_tentacle, parts)
                        leftten_number = len(left_tentacle)
                        if len(left_tentacle) == parts:
                            leftten_attack = False
                            t_leftten_timer = 0
                            leftten_number = parts
                            angel_to_zero(left_tentacle)
                            left_tentacle_to_original(left_tentacle, boss)
                            positive_angel_speed(left_tentacle)
                if not f_attack and not leftten_attack:
                    boss_timers['leftten_attack'] += 1
                    n_leftten_timer = tentacle_normally_shake(left_tentacle, parts, n_leftten_timer)
                    leftten_number = parts
                else:
                    n_leftten_timer = 0
            else:
                if not new_leftten:
                    left_tentacle = []
                    leftten_number = 0
                    n_leftten_timer = 0
                    t_leftten_timer = 0
                    boss_timers['flamebomb'] = 0
                    boss_timers['new_leftten'] += 1
            
            if rightten_alive:
                boss_timers['rightten_attack'] += 1
                if boss_timers['rightten_attack'] >= 15 * 3 + 9 + 200:
                    boss_timers['rightten_attack'] = 0
                    rightten_attack = True
                if rightten_attack and not f_attack:
                    t_rightten_timer += 1
                    if t_rightten_timer > 0 and t_rightten_timer <= 50:
                        r_angel = angel_track(right_tentacle, player)
                        right_tentacle[-1].turn_image(r_angel, True)
                        if t_rightten_timer % 2 == 0 or t_rightten_timer >= 30:
                            tentacle_track(right_tentacle, player, r_angel, DISPLAY_HEIGHT, DISPLAY_WIDTH, display)
                        if t_rightten_timer == 50:
                            r_time = extension_time(right_tentacle, player, r_angel, DISPLAY_HEIGHT, DISPLAY_WIDTH)
                            r_s_up = 1
                            r_tmp = [right_tentacle[-1].rect.x, right_tentacle[-1].rect.y]
                    elif t_rightten_timer > 50 and t_rightten_timer < 50 + 10 * r_time:
                        if t_rightten_timer == 51:
                            extend(right_tentacle)
                        change_angel(right_tentacle, r_angel)
                        if not tentacle_attack(right_tentacle, r_angel, DISPLAY_HEIGHT, DISPLAY_WIDTH, r_tmp):
                            if r_s_up <= len(right_tentacle) - 1:
                                r_s_up += 1
                                right_tentacle[-r_s_up].shake(-1)
                        else:
                            extend(right_tentacle)
                            window_shake = tentacle_to_player_collide(right_tentacle, player, window_shake, rightten_health, CircleBullet.hurt, display, hit_surf, shake_sound)
                        rightten_number = len(right_tentacle)
                    elif t_rightten_timer >= 50 + 10 * r_time:
                        tentacle_back(right_tentacle, r_angel, r_tmp)
                        del_tentacle_length(right_tentacle, parts)
                        rightten_number = len(right_tentacle)
                        if len(right_tentacle) == parts:
                            rightten_attack = False
                            t_rightten_timer = 0
                            rightten_number = parts
                            angel_to_zero(right_tentacle)
                            right_tentacle_to_original(right_tentacle, boss)
                            negative_angel_speed(right_tentacle)
                if not f_attack and not rightten_attack:
                    n_rightten_timer = tentacle_normally_shake(right_tentacle, parts, n_rightten_timer)
                    rightten_number = parts
                else:
                    n_rightten_timer = 0
            else:
                if not new_rightten:
                    right_tentacle = []
                    rightten_number = 0
                    n_rightten_timer = 0
                    boss_timers['flamebomb'] = 0
                    boss_timers['new_rightten'] += 1

            rays_update(rays)
            blit_rays(rays, display, DISPLAY_HEIGHT)

            flamebomb.update()
            flamebomb.draw(display)

            blit_tentacle(left_tentacle, display, leftten_number)
            blit_tentacle(right_tentacle, display, rightten_number)

            ray_to_player_collide(rays, player, display, hit_surf, ray_sound)

            for c in flamebomb.circles:
                if flamebomb_collide(c, player):
                    flamebomb.circles = [new for new in flamebomb.circles if new != c]
                    if player.c_attack:
                        pass
                    else:
                        bomb.play()
                        display.blit(hit_surf, (0, 0), special_flags = BLEND_RGB_ADD)
                        player.health -= flamebomb.hurt

            if not f_attack:
                if not new_leftten and not leftten_attack:
                    leftten_health = tentacle_to_bullet_collide(left_tentacle, bullets, leftten_health, hit_sound)
                    leftten_health = tentacle_to_skill12_collide(left_tentacle, left_bullets, leftten_health, hit_sound)
                    leftten_health = tentacle_to_skill12_collide(left_tentacle, right_bullets, leftten_health, hit_sound)
                if not new_rightten and not rightten_attack:
                    rightten_health = tentacle_to_bullet_collide(right_tentacle, bullets, rightten_health, hit_sound)
                    rightten_health = tentacle_to_skill12_collide(right_tentacle, left_bullets, leftten_health, hit_sound)
                    rightten_health = tentacle_to_skill12_collide(right_tentacle, right_bullets, leftten_health, hit_sound)

            boss_to_bullet_collide(boss, bullets, hit_sound)
            boss_to_skill12_collide(boss, left_bullets, hit_sound)
            boss_to_skill12_collide(boss, right_bullets, hit_sound)

        #敵人
        if not is_boss and player.alive and boss.alive:
            show_death_effects(death_particles, display)
            if score <= 200 * dream_level:
                enemy_timer += 0.1
            if enemy_timer >= enemy_timer_limited:
                enemy_timer = 0
                add_enemy(enemies)
            blit_enemy(display, enemies, player)
            #碰撞檢測
            score = enemy_collide(bullets, enemies, score, death_particles, enemy_hurt_sound)
            score = enemy_to_skill12_collide(left_bullets, enemies, score, death_particles, enemy_hurt_sound)
            score = enemy_to_skill12_collide(right_bullets, enemies, score, death_particles, enemy_hurt_sound)
            if player.c_attack:
                cattack_to_enemy_collide(enemies, player, death_particles, enemy_hurt_sound)
            else:
                player_to_enemy_collide(enemies, player, fly_partciels, enemy_burn_sound)
        
        #玩家
        player.update()
        player.healht_report(display)
        if player.alive:
            player.draw(display)
            if player.l_escalate:
                player.escalate_power('left')
                player.power_bar_render(display, DISPLAY_HEIGHT, DISPLAY_WIDTH, 1)
            if player.l_attack and player.turn > 0:
                player.release_power('left', display)
                player.attack_timer[1] = 0
            if player.r_escalate:
                player.escalate_power('right')
                player.power_bar_render(display, DISPLAY_HEIGHT, DISPLAY_WIDTH, 2)
            if player.r_attack and player.turn > 0:
                player.release_power('right', display)
                player.attack_timer[2] = 0
            if player.c_escalate:
                player.escalate_power('circle')
                player.power_bar_render(display, DISPLAY_HEIGHT, DISPLAY_WIDTH, 3)
            if player.c_attack:
                player.release_power('circle', display)
            else:
                if len(circle_bullets) > 0:
                    circle_attack.fadeout(1000)
                    circle_bullets.pop()
            #子彈
            player.attack_timer[0] += 0.1
            if player.attack_timer[0] >= bullet_timer_limited:
                player.attack_timer[0] = 0
                add_bullet(bullets, player)
            shoot_bullet(bullets, display)
            shoot_left_bullet(left_bullets, display)
            shoot_right_bullet(right_bullets, display, DISPLAY_WIDTH)
            shoot_circle_bullet(circle_bullets, display, player, cb_particles, circle_attack)
            show_cb_particles(cb_particles, display)
            show_fly_particles(fly_partciels, display)
        else:
            if len(player_death.particles) > 0:
                pygame.time.wait(20)
            else:
                pygame.mixer.music.fadeout(1000)
            player_death.draw(display, (0, 162, 232))
        
        #分數
        #score_msg = score_font.render(f'Score:{str(score)}', True, (0, 0, 0))
        #display.blit(score_msg, score_cdn)

        #玩家死亡後的畫面
        if player.health <= 0:
            if player.alive:
                for _ in range(20):
                    move_x = random.randint(3, 5) * math.cos(random.uniform(0, math.pi * 2))
                    move_y = random.randint(3, 5) * math.sin(random.uniform(0, math.pi * 2))
                    player_death.add(
                        player.rect.centerx, 
                        player.rect.centery,
                        move_x,
                        move_y,
                        random.randint(6, 8),
                        0.3
                    )
            player.alive = False

        #魔王死亡
        if boss.health <= 0:
            if boss.alive:
                p_or_n = [1, -1]
                for i in range(20):
                    for _ in range(10):
                        boss_death.add(
                            boss.rect.x + boss.rect.width / 2 + i * 6 * random.choice(p_or_n) * math.sin(random.uniform(80 * math.pi / 180, 100 * math.pi / 180)),
                            boss.rect.y + boss.rect.height + i * 6 * random.choice(p_or_n) * math.cos(random.uniform(80 * math.pi / 180, 100 * math.pi / 180)),
                            random.randint(0, 8) - 4,
                            random.randint(0, 8) - 4,
                            random.randint(6, 8),
                            random.uniform(0.1, 0.5)
                        )
                boss.rect.x = DISPLAY_WIDTH / 2 - boss.image.get_width() / 2
            if len(boss_death.particles) > 0:
                pygame.time.wait(20)
            else:
                boss.rect.y -= 2
            boss_death.draw(display, (37, 34, 20))
            boss.alive = False
            is_boss = False
            if len(boss_death.particles) == 0:
                pygame.mixer.music.fadeout(1000)

        if not player.alive and len(player_death.particles) == 0:
            mx, my = pygame.mouse.get_pos()
            display.blit(
                lighting_surf3((20, 20, 20), DISPLAY_WIDTH, DISPLAY_HEIGHT, 0), 
                (0, 0),
                special_flags = BLEND_RGB_MULT
            )
            display.blit(restart_font.render('LOSE', False, (255, 255, 255)), [int(DISPLAY_WIDTH / 2 - 7 * 2), 100])
            pygame.draw.rect(display, (100, 100, 100), restart_rect)
            display.blit(restart_font.render('BACK TO MENU', False, (255, 255, 255)), [restart_rect.x + 3, restart_rect.y])
            if restart_rect.collidepoint((int(mx / 2), int(my / 2))):
                if click:
                    running = False
            click = False

        if not boss.alive and len(boss_death.particles) == 0:
            mx, my = pygame.mouse.get_pos()
            display.blit(
                lighting_surf3((20, 20, 20), DISPLAY_WIDTH, DISPLAY_HEIGHT, 0), 
                (0, 0),
                special_flags = BLEND_RGB_MULT
            )
            display.blit(restart_font.render('WIN', False, (255, 255, 255)), [int(DISPLAY_WIDTH / 2 - 7 * 3 / 2), 100])
            pygame.draw.rect(display, (100, 100, 100), restart_rect)
            display.blit(restart_font.render('BACK TO MENU', False, (255, 255, 255)), [restart_rect.x + 3, restart_rect.y])
            if restart_rect.collidepoint((int(mx / 2), int(my / 2))):
                if click:
                    running = False
            click = False
        

        #pygame事件迴圈
        for event in pygame.event.get():
            if event.type == pygame.QUIT: #離開
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == KEYDOWN:
                if event.key in [K_RIGHT, K_d]: #玩家向右
                    player.move_right = True
                if event.key in [K_LEFT, K_a]: #玩家向左
                    player.move_left = True
                if event.key in [K_UP, K_w]:
                    player.move_up = True
                if event.key in [K_DOWN, K_s]:
                    player.move_down = True
                if event.key in [K_j]:
                    player.l_escalate = True
                    player.r_escalate = False
                    player.c_escalate = False
                    player.l_attack = False
                    player.r_attack = False
                    player.c_attack = False
                    player.turn = 0
                    player.speed -= 2
                    es_power.play()
                if event.key in [K_k]:
                    player.l_escalate = False
                    player.r_escalate = False
                    player.c_escalate = True
                    player.l_attack = False
                    player.r_attack = False
                    player.c_attack = False
                    player.turn = 0
                    player.speed -= 3
                    es_power.play()
                if event.key in [K_l]:
                    player.l_escalate = False
                    player.r_escalate = True
                    player.c_escalate = False
                    player.l_attack = False
                    player.r_attack = False
                    player.c_attack = False
                    player.turn = 0
                    player.speed -= 2
                    es_power.play()
            if event.type == KEYUP:
                if event.key in [K_RIGHT, K_d]:
                    player.move_right = False
                if event.key in [K_LEFT, K_a]:
                    player.move_left = False
                if event.key in [K_UP, K_w]:
                    player.move_up = False
                if event.key in [K_DOWN, K_s]:
                    player.move_down = False
                if event.key in [K_j]:
                    player.l_escalate = False
                    player.r_escalate = False
                    player.c_escalate = False
                    player.l_attack = True
                    player.r_attack = False
                    player.c_attack = False
                    player.speed += 2
                    add_left_bullet(left_bullets, player, shoot)
                if event.key in [K_k]:
                    player.l_escalate = False
                    player.r_escalate = False
                    player.c_escalate = False
                    player.l_attack = False
                    player.r_attack = False
                    player.turn = 0
                    player.speed += 3
                    if player.attack_timer[3] >= player.power_bar_rect.width:
                        player.c_attack = True
                        player.circle_line = 3
                        add_circle_bullet(circle_bullets, player)
                    else:
                        player.attack_timer[3] = 0
                        player.c_attack = False
                        player.image = pygame.transform.rotate(player.image_c, player.turn)
                if event.key in [K_l]:
                    player.l_escalate = False
                    player.r_escalate = False
                    player.c_escalate = False
                    player.l_attack = False
                    player.r_attack = True
                    player.c_attack = False
                    player.speed += 2
                    add_right_bullet(right_bullets, player, shoot)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        #畫布
        surf = pygame.transform.scale(display, SETTING.SIZE)
        window.blit(surf, (display_rect.x, display_rect.y))
        
        #全部更新
        pygame.display.update()

        #FPS
        SETTING.clock.tick(SETTING.FPS)

        

if __name__ == '__main__':
    menu(display)
    #game(display)