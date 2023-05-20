import random #импортирование библиотек
import pygame
from pygame import mixer
from pygame import transform 
import json
import time
import sys
from pygame.locals import *
 
click = False
 

 #запуск музыки


mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire = mixer.Sound('fire.ogg')

def draw_text(screen, text, size, x, y): #функиция для отрисовки текста
    font = pygame.font.SysFont('Arial', size)
    text = font.render(text, True, (255, 255, 255))
    text_rect = text.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text, text_rect)




WIDTH = 800 #размеры окна, кол-во обновлений сцены в секунду
HEIGHT = 800
FPS = 60

bg = transform.scale(pygame.image.load('galaxy.jpg'), (WIDTH, HEIGHT))


score = 0 #создание счетчиков убитых и пропущенных монстров
lost = 0

upgrade_ship = False #переключатель отвеающий за то, произошёл ли апгрейд корабля или нет

pygame.init() #инициализация пайгема
screen = pygame.display.set_mode((WIDTH, HEIGHT)) #создание экрана

pygame.display.set_caption("Шутер") #название экрана
clock = pygame.time.Clock() 



class Ship(pygame.sprite.Sprite): #класс корабля
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = transform.scale(pygame.image.load('rocket.png'),(100, 100))  
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.x = 0

    def update(self): 
        global shield#создание функции, отвечающей за передвижение корабля
        self.speedx = 0
        ks = pygame.key.get_pressed()
        if ks[pygame.K_LEFT]:
            self.x = -15
            self.rect.x += self.x
            if shield_upgrade == True:
                shield.rect.x -= 15
        if ks[pygame.K_RIGHT]:
            self.x = 15
            self.rect.x += self.x
            if shield_upgrade == True:
                shield.rect.x += 15
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            if shield_upgrade == True:
                shield.rect.right = WIDTH+30
        if self.rect.left < 0:
            self.rect.left = 0
            if shield_upgrade == True:
                shield.rect.left = -30

    def vistrel(self): #создание функции, которая отвечает за стрельбу корабля
        if upgrade_ship == True: #если переключатель, определяющий апгрейднут ли корабль = True, то вылетают 3 пули разом, если нет то по одной
            bullet1 = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet1)
            bullet1.rect.y += bullet1.speed_puli
            bullet1.rect.x -= bullet1.speed_puli
            if bullet1.rect.bottom < 0:
                bullet1.kill()
        if upgrade_ship == True:
            bullet2 = Bullet(self.rect.centerx - 30, self.rect.top)
            bullets.add(bullet2)
            bullet2.rect.y += bullet2.speed_puli
            bullet2.rect.x -= bullet2.speed_puli
            if bullet2.rect.bottom < 0:
                bullet2.kill()
        if upgrade_ship == True:
            bullet3 = Bullet(self.rect.centerx + 30, self.rect.top)
            bullets.add(bullet3)
            bullet3.rect.y += bullet2.speed_puli
            bullet3.rect.x -= bullet2.speed_puli
            if bullet3.rect.bottom < 0:
                bullet3.kill()
        else:
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            if bullet.rect.bottom < 0:
                bullet.kill()


            

        


shield_count = 0

class Enemy(pygame.sprite.Sprite): #класс врагов
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = transform.scale(pygame.image.load('asteroid.png'),(70, 70))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 650)
        self.rect.y = 0
        self.speed_padenia = random.randint(1, 5)
        self.rect.y = random.randint(-100, -40)

    def update(self): #передвижение врагов
        global lost
        self.rect.y += self.speed_padenia
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, 60)
            self.rect.y = random.randint(-100, -40)
            self.speed_padenia = random.randint(1, 5)
            lost += 1 



class Bullet(pygame.sprite.Sprite): #класс пули
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = transform.scale(pygame.image.load('bullet_lazer.png'),(30, 30))

        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speed_puli = -10





    def update(self): #передвижение пули
        self.rect.y += self.speed_puli
        if self.rect.bottom < 0:
            self.kill()

def upgrade_draw():
    if update == True:
        if perekluchatel == True:
            upgradies.add(upgrade)
            upgradies.update()
    upgradies.draw(screen)

def health_draw():
    if update == True:
        if perekluchatel == True:
            health_g.add(health1)
            health_g.update()
    health_g.draw(screen)

shield_icong = pygame.sprite.Group()

def shield_draw():
    if update == True:
        if perekluchatel == True:
            shield_icong.add(icon_shield)
            shield_icong.update()
    shield_icong.draw(screen)
    


health_g = pygame.sprite.Group()

shield_g = pygame.sprite.Group()

class Upgrade(pygame.sprite.Sprite): #класс спрайта который апгрейдит корабль
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = transform.scale(pygame.image.load('upgrade.png'),(100, 80))
        self.rect = self.image.get_rect()
    
        self.rect.x = random.randint(0, 550)
        self.rect.y = 0
        self.speed_upgrade = 5

    def update(self): #передвижение спрайта который апгрейдит корабль
        self.rect.y += self.speed_upgrade

class Health(pygame.sprite.Sprite): #класс спрайта который апгрейдит корабль
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = transform.scale(pygame.image.load('health.png'),(100, 80))
        self.rect = self.image.get_rect()
    
        self.rect.x = random.randint(0, 550)
        self.rect.y = 0
        self.speed_upgrade = 5

    def update(self): #передвижение спрайта который апгрейдит корабль
        self.rect.y += self.speed_upgrade

class Shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = transform.scale(pygame.image.load('shield_icon.png'),(100, 80))
        self.rect = self.image.get_rect()
    
        self.rect.x = random.randint(0, 550)
        self.rect.y = 0
        self.speed_upgrade = 5

    def update(self): #передвижение спрайта который апгрейдит корабль
        self.rect.y += self.speed_upgrade


player = Ship()


class Player_shield(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = transform.scale(pygame.image.load('shield.png'),(170, 150))
        self.rect = self.image.get_rect()
        self.rect.x = player.rect.x-37
        self.rect.y = player.rect.y-25




   

countdown2, text2 = 10, '10'
countdown, text = 10, '10'
pygame.time.set_timer(pygame.USEREVENT, 1000)


records = {'score':score}

icon_shield = Shield()


enemies = pygame.sprite.Group() #создание всех спрайтов, фонов
bullets = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
prewiew = transform.scale(pygame.image.load('prewiew.jpg'),(HEIGHT, WIDTH))
hp = transform.scale(pygame.image.load('hp.png'),(200, 20))
hp1 = transform.scale(pygame.image.load('hp1.png'),(200, 20))
hp2 = transform.scale(pygame.image.load('hp2.png'),(200, 20))
hp3 = transform.scale(pygame.image.load('hp3.png'),(200, 20))


player_g = pygame.sprite.Group()
player_g.add(player)
all_sprites.add(player)
upgradies = pygame.sprite.Group()



for i in range(5): #создание монстров
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

collide = False #переключатель столкновения

lose = 0



running = True #переключатель отвечающий за продолжение игры
def collide_func(): #функция с помощью которой отнимается хп
    global count_collide
    global running
    global lose

    if count_collide == 2:
        if pygame.sprite.groupcollide(enemies, player_g, True, False):
            lose = 1

        elif lose == 1:
            screen.blit(hp3, (player.rect.x - 45, player.rect.y - 40))
            draw_text(screen,'Вы проиграли :(', 70, WIDTH/2, HEIGHT/2-50)
            draw_text(screen,'Ваши очки:' + ' ' + str(score), 30, WIDTH/2, HEIGHT/2-100)

        else:
            screen.blit(hp2, (player.rect.x - 45, player.rect.y - 40))
    if count_collide == 1:
        if pygame.sprite.groupcollide(enemies, player_g, True, False):
            count_collide += 1
            screen.blit(hp2, (player.rect.x - 45, player.rect.y - 40))
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        else:
            screen.blit(hp1, (player.rect.x - 45, player.rect.y - 40))
    if count_collide == 0:
        if pygame.sprite.groupcollide(enemies, player_g, True, False):
            count_collide += 1 
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            screen.blit(hp1, (player.rect.x - 45, player.rect.y - 40))
        else:
            screen.blit(hp, (player.rect.x - 45, player.rect.y - 40))
count_collide = 0 #счетчик столкновений 
perekluchatel = False
upgrade = Upgrade()
health1 = Health()



try:
    with open('records.json', 'r', encoding='utf-8') as f:    
        records = json.load(f)

except:
    with open('records.json', 'w', encoding='utf-8') as f:    
        json.dump(records, f)
update = True

shield_upgrade = False

shield_conflict = 2


otrisovka1 = False
otrisovka2 = False
otrisovka3 = False

one = 1

max_score = records['score']

countdown_switch = False
def game():
    global otrisovka1
    global otrisovka2
    global otrisovka3
    global shield
    global shield_upgrade
    global shield_conflict
    global shield_count
    global shield_shield
    global generator
    global health
    global update
    global text2
    global perekluchatel
    global running
    global score
    global upgrade_ship
    global countdown2
    global lost
    global text 
    global countdown
    global count_collide
    global click
    global one 
    while running != False: #цикл игры
        records = {'score':score}
        click = False
        if shield_upgrade == True and shield_count == 0:
            shield = Player_shield() 
            shield_g.add(shield)
            shield_count += 1




        clock.tick(FPS) #фпс

        collidies = pygame.sprite.groupcollide(player_g, upgradies, False, False)

        healths = pygame.sprite.groupcollide(player_g, health_g, False, False)

        if lose == 1:            
            if one == 1:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
                one -= 1
            if score > max_score:
                with open('records.json', 'w', encoding='utf-8') as f:    
                    json.dump(records, f, ensure_ascii=False) 
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                            running = False
                            main_menu()

            update = False   



        for health in healths:    

            health1.rect.y = -100000000

            if count_collide == 0:
                None
            else:
                count_collide -= 1


        screen.blit(bg, (0, 0)) #отображение бекграунда

        for event in pygame.event.get(): #прописка всех ивентов (таймер, нажатия на клавиши)
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                    main_menu()
                if event.key == pygame.K_SPACE:
                    if update == True:
                        fire.play()
                        player.vistrel()
            if event.type == pygame.USEREVENT and upgrade_ship == False and update == True: 
                countdown -= 1
                text = str(countdown) 

            if event.type == pygame.USEREVENT and upgrade_ship == True and update == True: 
                countdown2 -= 1
                text2 = str(countdown2)



        if countdown == 0:
            perekluchatel = True

        if countdown == 0 and generator == 1:
            upgrade.rect.x = random.randint(0, 550)
            upgrade.rect.y = 0
            countdown = 10
            generator = random.randint(1, 3)
            otrisovka1 = True
        if countdown == 0 and generator == 2:
            health1.rect.x = random.randint(0, 550)
            health1.rect.y = 0
            countdown = 10
            generator = random.randint(1, 3)
            otrisovka2 = True

        if countdown == 0 and generator == 3:
            icon_shield.rect.x = random.randint(0, 550)
            icon_shield.rect.y = 0
            countdown = 10
            generator = random.randint(1, 3)
            otrisovka3 = True
            


        if otrisovka1 == True:
            upgrade_draw()

        if otrisovka2 == True:
            health_draw()

        if otrisovka3 == True:
            shield_draw()

        collide_func()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True) #столкновения

        shield_collidies = pygame.sprite.groupcollide(enemies, shield_g, True, False)

        bullets.draw(screen) #отрисовка пуль 

        p_s_collidies = pygame.sprite.groupcollide(player_g, shield_icong, False, False)

        for p_s_collide in p_s_collidies:
            icon_shield.rect.y = 1000000
            shield_upgrade = True

        for shield_collide in shield_collidies:
            shield_conflict -= 1
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        if shield_conflict == 0:
            shield.kill()
            shield_upgrade = False
            shield_count = 0
            shield_conflict = 2

        for collide in collidies:
            upgrade_ship = True
            upgrade.rect.y = -100000000

        if update == True:
            bullets.update()

        for hit in hits:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            score += 1 

        if update == True:
            all_sprites.update()

        all_sprites.draw(screen)
        shield_g.draw(screen)

        draw_text(screen, str(score), 30, WIDTH / 2, 10)
        draw_text(screen, 'Пропущено: ' + str(lost), 30, 100, 100)
        if upgrade_ship == False:
            draw_text(screen,'До усилителя:'+ (text), 30, 600, 50)

        if upgrade_ship == True:
            draw_text(screen,'До конца усилителя:'+ (text2), 30, 600, 100)
        if countdown2 == 0:
            upgrade_ship = False
            countdown2 = 10



        if lost >= 3:
            draw_text(screen,'Вы проиграли :(', 70, WIDTH/2, HEIGHT/2-50)
            draw_text(screen,'Ваши очки:' + ' ' + str(score), 30, WIDTH/2, HEIGHT/2-100)
            
            if score > max_score:
                with open('records.json', 'w', encoding='utf-8') as f:    
                    json.dump(records, f, ensure_ascii=False) 
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:
                    if event.key == K_ESCAPE:
                            running = False
                            main_menu()
            update = False


        pygame.display.flip()



        pygame.display.update()
        clock.tick(60)
def main_menu():
    while True:
        global one
        global generator
        global lose
        global update
        global perekluchatel
        global running
        global score
        global upgrade_ship
        global countdown2
        global lost
        global countdown
        global count_collide
        global running
        global click

        screen.blit(prewiew, (0, 0))
        draw_text(screen, 'Меню', 30, 400, 40)


        with open('records.json', 'r', encoding='utf-8') as f:    
            records = json.load(f)
        max_score = records['score']
        
        
        screen.blit(prewiew, (0, 0))
        draw_text(screen, 'Ваш рекорд:' + str(max_score), 30, 390, 100)

        mx, my = pygame.mouse.get_pos()

        button_1 = pygame.Rect(300, 390, 200, 50)

        running = True

        if button_1.collidepoint((mx, my)) and running == True:
            if click:
                generator = random.randint(1, 2)
                update = True
                lose = 0
                perekluchatel = False
                score = 0
                upgrade_ship = False
                countdown2 = 10
                lost = 0
                countdown = 10
                count_collide = 0
                one = 1
                game()



        pygame.draw.rect(screen, (100, 0, 150), button_1)
 
        draw_text(screen, 'ИГРАТЬ', 20, 400, 400)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
 
        pygame.display.update()
        clock.tick(60)
 

main_menu()
