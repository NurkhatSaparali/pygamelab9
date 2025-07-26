import pygame,sys,random,time
from pygame.locals import *
pygame.init()
#музыка
pygame.mixer.init()
pygame.mixer.music.load(r"C:\Users\Nurhat\OneDrive\Desktop\pygamelab8\background.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5)
#настройки игры
fps=60
frame_per_sec=pygame.time.Clock()
screen_width=400
screen_height=600
speed=5 #начальная скорость врагов
score=0 #счет игры
coins_count=0 #счет собранных монет
coin_threshold=10 #порог для увеличения скорости при сборе монет
next_coin_threshold=coin_threshold #следующий порог для увеличения скорости
#цвета
blue=(0,0,255)
red=(255,0,0)
black=(0,0,0)
white=(255,255,255)
#шрифты
font=pygame.font.SysFont("Verdana",60)
font_small=pygame.font.SysFont("Verdana",20)
game_over_text=font.render("game over",True,black)
#фон
background=pygame.image.load("AnimatedStreet.png")
#экран
display_surf=pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("game")
#класс противника
class enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("Enemy.png")
        self.rect=self.image.get_rect()
        self.rect.center=(random.randint(40,screen_width-40),0)
    def move(self):
        global score
        self.rect.move_ip(0, speed) #движение вниз
        if self.rect.bottom >screen_height:
            score+=1
            self.rect.top=0
            self.rect.center=(random.randint(40,screen_width-40),0)
#класс игрока
class player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("Player.png")
        self.rect=self.image.get_rect()
        self.rect.center=(160,520)
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left>0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5,0)
        if self.rect.right<screen_width and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5,0)
#класс монеты
class coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load("Coin.png")
        self.image=pygame.transform.scale(self.image, (30, 30))
        self.rect=self.image.get_rect()
        self.respawn()
    def respawn(self):
        self.rect.center=(random.randint(40,screen_width-40), screen_height-60)
        self.weight=random.choice([1,3,5]) #новый случайный вес монеты
    def move(self):
        global coins_count, speed, next_coin_threshold
        if pygame.sprite.collide_rect(p1, self):
            coins_count+=self.weight #увеличиваем счет монет на вес монеты
            self.respawn()  #создаем новую монету
            if coins_count>=next_coin_threshold:
                speed+=1
                next_coin_threshold+=coin_threshold
# спрайты
p1=player()
e1=enemy()
c1=coin()
coins_group=pygame.sprite.Group()
coins_group.add(c1)
enemies=pygame.sprite.Group()
enemies.add(e1)
all_sprites=pygame.sprite.Group()
all_sprites.add(p1,e1,c1)
#увеличение скорости
inc_speed=pygame.USEREVENT+1
pygame.time.set_timer(inc_speed,1000)
#цикл игры
while True:
    for event in pygame.event.get():
        if event.type==inc_speed:
            speed+=0.5
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
    display_surf.blit(background,(0,0))
    scores=font_small.render(str(score), True, black)
    coins_text=font_small.render(f"coins: {coins_count}", True, black)
    display_surf.blit(scores,(10,10))
    display_surf.blit(coins_text,(300,10))
    for entity in all_sprites:
        entity.move()
        display_surf.blit(entity.image, entity.rect)
    if pygame.sprite.spritecollideany(p1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        display_surf.fill(red)
        display_surf.blit(game_over_text, (30,250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()
    pygame.display.update()
    frame_per_sec.tick(fps)



