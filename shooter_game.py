import pygame
from random import randint
pygame.init()


#класс-родитель для спрайтов
class GameSprite(pygame.sprite.Sprite):
   #конструктор класса
    def __init__(self, player_image:str, player_x:int, player_y:int, player_speed:int, w:int , h:int):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = pygame.transform.scale(pygame.image.load(player_image), (w, h))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.width = w
        self.height = h

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Hero(GameSprite):

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        #если вышли за границу, то спрайт пермещается на другую сторону
        if self.rect.x < -self.width+35: 
            self.rect.x = WIN_SIZE[0]-35
        if self.rect.x > WIN_SIZE[0]-35:
            self.rect.x = -self.width+35
    
    def fire(self):
        kick.play() # играем звук выстрела
        bullet = Bullet('bullet.png', self.rect.x + self.width/2 - 10, self.rect.y, 6, 20, 30) #создает пульку в точке, где сам находится
        bullets.append(bullet) #добавляем спрайт пульки в список 

class Enemy(GameSprite):
    def move(self):
        global loses
        self.rect.y += self.speed
        if self.rect.y > WIN_SIZE[1]:
            self.rect.y = -80
            self.rect.x = randint(0, WIN_SIZE[0]-70)
            self.speed = randint(1,2)
            loses += 1

class Bullet(GameSprite):
    def move(self):
        self.rect.y -= self.speed
        if self.rect.y <= -30: #если пулька вышла за границу экрана, то удаляем её
            bullets.remove(self) #удаляем спрайт из списка

class AnimateObject(GameSprite):
    images = ['images/1.png', 'images/2.png', 'images/3.png', 'images/4.png', 'images/5.png', 'images/6.png', 'images/7.png', 'images/8.png']
    current_image = 0

    def animate(self):
        self.current_image += 1
        self.image = pygame.transform.scale(pygame.image.load(self.images[self.current_image // 3]), (self.width, self.height))
        if self.current_image >= 3*len(self.images) - 1:
            animate_objects.remove(self)

class AnimateObject1(GameSprite):
    images = [f"images1/{i}.png" for i in range(1,17)] 
    current_image = 0 #номер текущей картинки для анимации

    def animate(self):
        self.current_image += 1
        self.image = pygame.transform.scale(pygame.image.load(self.images[self.current_image // 5]), (self.width, self.height))
        if self.current_image >= 5*len(self.images)-1:
            animate_objects.remove(self)

class Asteroid(GameSprite):
    health = 3
    speedx = randint(-2, 2)
    def move(self):
        global loses
        self.rect.y += self.speed
        self.rect.x += self.speedx
        if self.rect.y > WIN_SIZE[1]:
            self.rect.y = -self.height
            self.rect.x = randint(0, WIN_SIZE[0]-self.width)
            self.speed = randint(1,10)
            self.speedx = randint(-2, 2)
            self.health = 3


#основные переменные
WIN_SIZE = (700, 500) 
FPS = 60
game = True
vol = 0 #количество громкости
score = 0 #сбитые враги
loses = 0 #количество пропущенных врагов
health = 10 #жизни главного героя
animate_objects = []

k = 20 #кол-во патронов
t = 100 #время перезарядки патронов
is_reload = False #признак перезарядки патронов


#текстовые спрайты
font = pygame.font.SysFont('Arial', 20)
font1 = pygame.font.SysFont('Arial', 50)
reload_text = font.render('Reload', True, (255,0, 0))
win_text = font1.render('You win', True, (0,255,0))
lose_text = font1.render('You lose', True, (255,0,0))


window = pygame.display.set_mode(WIN_SIZE)
pygame.display.set_caption("Космический бой!")
clock = pygame.time.Clock()

#музыка
pygame.mixer.music.load("Sounds/space.ogg") #загрузка музыки заднего фона
pygame.mixer.music.play(-1) #проигрывание музыки бесконечно 
kick = pygame.mixer.Sound("Sounds/fire.ogg") #загрузка выстрела
hit_sound_bullet = pygame.mixer.Sound("Sounds/1.wav")
hit_sound_hero1 = pygame.mixer.Sound('Sounds/2.wav')
hit_sound_hero2 = pygame.mixer.Sound('Sounds/3.wav')
hit_sound_hero3 = pygame.mixer.Sound('Sounds/4.wav')
hit_sounds_heroes = [hit_sound_hero1, hit_sound_hero2, hit_sound_hero3]
exploid = pygame.mixer.Sound("sounds/exploid.wav")

#объекты-спрайты
background = GameSprite("galaxy.jpg", 0, 0, 0, 700, 500)
hero = Hero("rocket.png", 350-35,420,5,70,80)

enemies = []
for i in range(5):
    enemy = Enemy("ufo.png",randint(0, WIN_SIZE[0]-70),-80,randint(1,4),70,80)
    enemies.append(enemy)

asteroids = []
for i in range(7):
    asteroid = Asteroid("asteroid.png",randint(0, WIN_SIZE[0]-50),-50,randint(1,4),50,50)
    asteroids.append(asteroid)

bullets = [] #здесь будут храниться все пульки

def set_vol():
    global vol
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        vol += 0.01
    if keys[pygame.K_DOWN]:
        vol -= 0.01
    pygame.mixer.music.set_volume(vol) #установка громкости заднего фона
    kick.set_volume(vol) #установка громкости выстрела
    hit_sound_bullet.set_volume(vol)
    hit_sound_hero1.set_volume(vol)
    hit_sound_hero2.set_volume(vol)
    hit_sound_hero3.set_volume(vol)
    exploid.set_volume(vol)

finish = False

set_vol()

def restart():
    print('Рестарт')
    global vol, score, loses, health, k, t, is_reload, bullets, enemies, asteroids, finish
    animate_objects.clear()
    bullets.clear()
    enemies.clear()
    asteroids.clear()
    
    score = 0 #сбитые враги
    loses = 0 #количество пропущенных врагов
    health = 10 #жизни главного героя

    k = 20 #кол-во патронов
    t = 100 #время перезарядки патронов
    is_reload = False #признак перезарядки патронов

    hero.rect.x = 350-35
    hero.rect.y = 420
    for i in range(5):
        enemy = Enemy("ufo.png",randint(0, WIN_SIZE[0]-70),-80,randint(1,4),70,80)
        enemies.append(enemy)
    for i in range(7):
        asteroid = Asteroid("asteroid.png",randint(0, WIN_SIZE[0]-50),-50,randint(1,4),50,50)
        asteroids.append(asteroid)
    finish = False

while game:
    if not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if k > 0: #есть ли патроны в обойме
                        hero.fire() #герой выстрелил
                        k -= 1
                    else:
                        is_reload = True
                        
        if is_reload:
            t -= 1
            if t == 0:
                t = 100
                k = 20
                is_reload = False
                    
        
        background.reset(window) #отображение фона
        hero.reset(window) #отображение героя
        hero.move() #движение героя

        for enemy in enemies:
            enemy.reset(window)
            enemy.move()

        for asteroid in asteroids:
            asteroid.reset(window)
            asteroid.move()

        for bullet in bullets:
            bullet.reset(window)
            bullet.move()

        #отслеживание столкновений пульки и врага
        for enemy in enemies:
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    k = randint(1,2)
                    if k == 1:
                        a = AnimateObject('images/1.png', enemy.rect.x, enemy.rect.y, 0, 80, 80)
                    else:
                        a = AnimateObject1('images/1.png', enemy.rect.x, enemy.rect.y, 0, 80, 80)
                    #a = AnimateObject('images/1.png', enemy.rect.x, enemy.rect.y, 0, 80, 80) if randint(1,2) == 1 else AnimateObject1('images/1.png', enemy.rect.x, enemy.rect.y, 0, 80, 80)
                    animate_objects.append(a)
                    score += 1
                    bullets.remove(bullet) #удаляем пульку из списка
                    #перемещаем спрайт наверх
                    enemy.rect.y = -80
                    enemy.rect.x = randint(0, WIN_SIZE[0]-70)
                    enemy.speed = randint(1,2)
                    exploid.play()
                    hit_sound_bullet.play()

        for bullet in bullets:
            for asteroid in asteroids:
                if bullet.rect.colliderect(asteroid):
                    asteroid.health -= 1
                    if asteroid.health <= 0:
                        a = AnimateObject("images/1.png",bullet.rect.x,bullet.rect.y,0,bullet.width,bullet.height)
                        animate_objects.append(a)
                        asteroid.rect.y = -asteroid.height
                        asteroid.rect.x = randint(0, WIN_SIZE[0]-asteroid.width)
                        asteroid.speed = randint(1,2)
                        asteroid.speedx = randint(-2, 2)
                        asteroid.health = 3
                        bullets.remove(bullet)
                        exploid.play()
                    else:
                        try:
                            a = AnimateObject('images/1.png', bullet.rect.x, bullet.rect.y, 0, bullet.width, bullet.height)
                            animate_objects.append(a)
                            hit_sounds_heroes[1].play() #звук уничтожения пульки
                            try:
                                bullets.remove(bullet)
                            except:
                                pass
                        except:
                            pass

        for animate_obj in animate_objects:
            animate_obj.animate()
            animate_obj.reset(window)

        #отслеживание главного героя и врага    
        for enemy in enemies:
            if enemy.rect.colliderect(hero.rect): #если герой столкнулся с врагом
                #перемещаем спрайт наверх
                enemy.rect.y = -80 
                enemy.rect.x = randint(0, WIN_SIZE[0]-70)
                enemy.speed = randint(1,2)
                health -= 1
                # a = randint(0,2)
                hit_sounds_heroes[0].play() 

        for bullet in bullets:
            for asteroid in asteroids:
                if bullet.rect.colliderect(asteroid):
                    asteroid.health -= 1
                    if asteroid.health <= 0:
                        a = AnimateObject('images/1.png', asteroid.rect.x, asteroid.rect.y, 0, asteroid.width, asteroid.height)
                        animate_objects.append(a)
                        asteroid.rect.y = -asteroid.height
                        asteroid.rect.x = randint(0, WIN_SIZE[0]-asteroid.width)
                        asteroid.speed = randint(1,2)
                        asteroid.speedx = randint(-2, 2) 
                        asteroid.health = 3
                        exploid.play()
                    else:
                        try:
                            a = AnimateObject('images/1.png', bullet.rect.x, bullet.rect.y, 0, bullet.width, bullet.height)
                            animate_objects.append(a)
                            hit_sounds_heroes[1].play() #звук уничтожения пульки
                            try:
                                bullets.remove(bullet)
                            except:
                                pass
                        except:
                            pass

        for asteroid in asteroids:
            if asteroid.rect.colliderect(hero.rect):
                health -= 1
                a = AnimateObject('images/1.png', asteroid.rect.x, asteroid.rect.y, 0, asteroid.width, asteroid.height)
                animate_objects.append(a)
                asteroid.rect.y = -asteroid.height
                asteroid.rect.x = randint(0, WIN_SIZE[0]-asteroid.width)
                asteroid.speed = randint(1,2)
                asteroid.speedx = randint(-2, 2) 
                asteroid.health = 3
                hit_sound_hero3.play()

        text = font.render("Score: " + str(score), True, (255, 255, 255))
        text_health = font.render("Health: " + str(health), True, (255,255,255))
        text_loses = font.render("Loses: " + str(loses), True, (255,255,255))
        window.blit(text, (10, 10))
        window.blit(text_health, (10, 40))
        window.blit(text_loses, (10, 70))

        if is_reload:
            reload_text = font.render('Reload: ' + str(t), True, (255,0, 0))
            window.blit(reload_text, (WIN_SIZE[0]/2-40, WIN_SIZE[1]/2-10))

        set_vol() #установка громкости 
        #условие поражения
        if health <= 0 or loses >= 13:
            window.blit(lose_text, (WIN_SIZE[0]/2-100, WIN_SIZE[1]/2-20))
            finish = True
        #условие победы
        if score >= 20: 
            window.blit(win_text, (WIN_SIZE[0]/2-100, WIN_SIZE[1]/2-20))
            finish = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and finish:
                restart()

    set_vol() #установка громкости 
    clock.tick(FPS)
    pygame.display.update()