# python C:\Users\Nurhat\OneDrive\Desktop\pygamelab9\2.py
import pygame, random
pygame.init()
width=600
height=600
screen=pygame.display.set_mode((width, height))
cell=30
colorWHITE=(255, 255, 255)
colorGRAY=(200, 200, 200)
colorRed=(255, 0, 0)
colorYELLOW=(255, 255, 0)
colorGREEN=(0, 255, 0)
FPS=7
font=pygame.font.SysFont("Arial", 24)  #отображение счета и уровня
#сетка
def draw_grid_chess():
    colors =[colorWHITE,colorGRAY]
    for i in range(height//cell):
        for j in range(width//cell):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * cell, j * cell, cell, cell), 1)
#класс точки
class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
#класс змейки
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0
        self.grow = False
    def move(self):
        new_head = Point(self.body[0].x + self.dx, self.body[0].y + self.dy)
        #выход через противоположную сторону
        new_head.x %= width // cell
        new_head.y %= height // cell
        #проверка столкновения с самим собой
        for segment in self.body:
            if new_head.x == segment.x and new_head.y == segment.y:
                return False
        self.body.insert(0,new_head)
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False
        return True
    def draw(self):
        pygame.draw.rect(screen,colorRed,(self.body[0].x*cell,self.body[0].y*cell,cell,cell))
        for segment in self.body[1:]:
            pygame.draw.rect(screen,colorYELLOW,(segment.x*cell,segment.y*cell,cell,cell))
    #проверка на столкновение головы с едой
    def check_collision(self,food):
        if self.body[0].x==food.pos.x and self.body[0].y==food.pos.y:
            self.grow=True
            return True
        return False
#класс еды
class Food:
    def __init__(self,snake):
        self.spawn_time=pygame.time.get_ticks()
        self.weight=random.choice([1,2,3])  #1-маленькая, 2 -средняя, 3-большая
        self.pos = self.get_random_pos(snake)
    def get_random_pos(self, snake):
        while True:
            x=random.randint(0, (width//cell)-1)
            y=random.randint(0, (height//cell)-1)
            if not any(part.x==x and part.y==y for part in snake.body):
                return Point(x,y)
    def draw(self):
        pygame.draw.rect(screen,colorGREEN,(self.pos.x*cell,self.pos.y*cell,cell,cell))
    def respawn(self,snake):
        self.spawn_time=pygame.time.get_ticks()
        self.weight=random.choice([1, 2, 3])
        self.pos=self.get_random_pos(snake)
clock=pygame.time.Clock()
snake=Snake()
food=Food(snake)
running=True
score=0 #счет
level=1 #уровень
foods_eaten=0 #количество съеденной еды
while running:
    screen.fill((0,0,0))
    draw_grid_chess()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_RIGHT and snake.dx==0:
                snake.dx=1; snake.dy=0
            elif event.key==pygame.K_LEFT and snake.dx==0:
                snake.dx=-1; snake.dy=0
            elif event.key==pygame.K_UP and snake.dy==0:
                snake.dx=0; snake.dy=-1
            elif event.key==pygame.K_DOWN and snake.dy==0:
                snake.dx=0; snake.dy=1
    if not snake.move():
        print("Game Over!")
        running = False
    #исчезновение еды через 5 секунд
    if pygame.time.get_ticks() - food.spawn_time > 5000:
        food.respawn(snake)
    #если змейка съела еду, увеличиваем счет и проверяем уровень
    if snake.check_collision(food):
        score += food.weight
        foods_eaten += 1
        food.respawn(snake)
        if foods_eaten >=3:  #каждые 3 еды - новый уровень
            level+=1
            foods_eaten = 0
            FPS+=2 #увеличиваем скорость игры
    snake.draw()
    food.draw()
    #отображение счета и уровня
    text=font.render("Score: " + str(score) + "  Level: " + str(level), True, (255,255,255))
    screen.blit(text,(10,10))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()


