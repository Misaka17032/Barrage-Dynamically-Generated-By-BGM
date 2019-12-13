import sys
from pygame.locals import *
from config.settings import *
from src.plane import OurPlane
from src.enemy import SmallEnemy
from src.bullet import Bullet
import read
import random
bg_size = 1404, 790
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("被人称呼为小红程度的能力")
background = pygame.image.load(os.path.join(BASE_DIR, "material/image/background.png"))
color_black = (0, 0, 0)
color_green = (0, 255, 0)
color_red = (255, 0, 0)
color_white = (255, 255, 255)
our_plane = OurPlane(bg_size)
def add_small_enemies(group1, group2, num):
    for i in range(num):
        small_enemy = SmallEnemy(bg_size)
        #if speed != None:
            #return speed
        group1.add(small_enemy)
        group2.add(small_enemy)
    #return None
def avg_time(count):
    a = 1000 / count
    result = []
    for x in range(count - 1):
        result.append(int(a*(x+1)))
    if result[len(result) - 1] > 1000:
        result.pop()
    result.append(1000)
    return result
def summon_enemy(note,time,distance):
    if time > 176:
        time -= 176
    time = int(time/1000)
    speed = []
    count = []
    l = 0
    for i in note:
        if i[2] == time:
            l += 1
            speed.append(distance/(i[0]/960))
            count.append(i[3])
    return speed,count,l
def get_enemy(note,t,bg_size,small_enemies,enemies):
    s,count,l = summon_enemy(note,t,bg_size[1])
    speed = []
    for n in range(l):
        added = []
        if count[n] > 1:
            rg = avg_time(count[n])
            for i in range(len(rg)):
                added.append(False)
            for i in range(len(rg) - 1):
                if (t % 1000) <= rg[i] and (t % 1000) <= rg[i + 1] and added[i] == False:
                    add_small_enemies(small_enemies, enemies, 1)
                    added[i] = True
    for i in range(len(count)):
        for j in range(count[i]):
            speed.append(int(s[i]/20))
    return speed
def main():
    note = read.read_xml("./material/xml/2.musicxml")
    #time.sleep(2)
    music = False
    running = True
    switch_image = False
    delay = 60
    enemies = pygame.sprite.Group()
    small_enemies = pygame.sprite.Group()
    bullet_index = 0
    e1_destroy_index = 0
    me_destroy_index = 0
    bullet1 = []
    bullet_num = 60
    bullet_start = True
    death = 0
    killed = 0
    for i in range(bullet_num):
        bullet1.append(Bullet(our_plane.rect.midtop))
    bullet_sound.play()
    bullets = bullet1
    bullets[bullet_index].reset(our_plane.rect.midtop)
    bullet_index = (bullet_index + 1) % bullet_num
    while running:    #50ms per loop
        if music == False:
            pygame.mixer.music.play()
            music = True
        t = pygame.time.get_ticks()
        speed = get_enemy(note,t,bg_size,small_enemies,enemies)
        key_pressed = pygame.key.get_pressed()
        screen.blit(background, (0, 0))
        clock = pygame.time.Clock()
        clock.tick(60)
        if not delay % 3:
            switch_image = not switch_image
        si = 0
        if len(speed) == 0:
            for i in range(len(small_enemies)):
                speed.append(random.randint(15,30))
        for each in small_enemies:
            #print(len(small_enemies),len(speed),si)
            if each.active:
                if si >= len(speed):
                    each.move(speed[len(speed) - 1])
                else:
                    each.move(speed[si])
                screen.blit(each.image, each.rect)
                '''
                pygame.draw.line(screen, color_black,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.right, each.rect.top - 5),
                                 2)
                energy_remain = each.energy / SmallEnemy.energy
                if energy_remain > 0.2:
                    energy_color = color_green
                else:
                    energy_color = color_red
                pygame.draw.line(screen, energy_color,
                                 (each.rect.left, each.rect.top - 5),
                                 (each.rect.left + each.rect.width * energy_remain, each.rect.top - 5),
                                 2)
                '''
            else:
                if e1_destroy_index == 0:
                    enemy1_down_sound.play()
                screen.blit(each.destroy_images[e1_destroy_index], each.rect)
                e1_destroy_index = (e1_destroy_index + 1) % 4
                if e1_destroy_index == 0:
                    each.reset()
                    small_enemies.remove(each)
                    enemies.remove(each)
            si += 1
        if our_plane.active:
            if switch_image:
                screen.blit(our_plane.image_one, our_plane.rect)
            else:
                screen.blit(our_plane.image_two, our_plane.rect)
            #if (key_pressed[K_k]):
            bullet_start = True
            if not (delay % 5):
                if bullet_start == True:
                    bullet_sound.play()
                    bullets = bullet1
                    bullets[bullet_index].reset(our_plane.rect.midtop)
                    bullet_index = (bullet_index + 1) % bullet_num
                    bullet_start = False
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemies_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemies_hit:
                        b.active = False
                        for e in enemies_hit:
                            e.active = False
                        killed += 1
                        if killed == 5:
                            killed -= 5
                            death -= 1
        else:
            if not (delay % 3):
                screen.blit(our_plane.destroy_images[me_destroy_index], our_plane.rect)
                me_destroy_index = (me_destroy_index + 1) % 4
                if me_destroy_index == 0:
                    me_down_sound.play()
                    our_plane.reset()
                    death += 1
        enemies_down = pygame.sprite.spritecollide(our_plane, enemies, True, pygame.sprite.collide_mask)
        if enemies_down:
            our_plane.active = False
            for row in enemies:
                row.active = False
        for event in pygame.event.get():
            if event.type == 12:
                pygame.quit()
                sys.exit()
        if delay == 0:
            delay = 60
        delay -= 1
        if key_pressed[K_w] or key_pressed[K_UP]:
            our_plane.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            our_plane.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            our_plane.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            our_plane.move_right()
        draw_death = pygame.font.SysFont("华文宋体",50)
        if death >= 0:
            draw_death_fmt = draw_death.render("Death count:" + str(death), 1, (225,225,225))   #Misaka #17032 get 3 death for best
        else:
            draw_death_fmt = draw_death.render(str(0 - death) + " Extra life!", 1, (225,225,225))
        screen.blit(draw_death_fmt,(10,10))
        if t > 188000:
            pygame.quit()
            sys.exit()
        pygame.display.flip()