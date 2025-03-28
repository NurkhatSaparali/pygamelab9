# python C:\Users\Nurhat\OneDrive\Desktop\pygamelab9\3.py
import pygame
pygame.init()
#параметры окна
width=800
height=600
screen=pygame.display.set_mode((width, height))
screen.fill((255, 255, 255))  #заливка фона белым
#настройки рисования
thickness=5
lmbpressed=False
start_pos=None
mode="line"  #по умолчанию линия
#цвета
color_red=(255,0,0)
color_blue=(0,0,255)
color_black=(0,0,0)
color_white=(255,255,255)
color_green=(0,255,0)
color_yellow=(255,255,0)
color_purple=(128,0,128)
color_orange=(255,165,0)
current_color = color_black  #черный цвет по умолчанию
#управление
print("""
Управление:
0 - белый
1 - красный
2 - синий
3 - черный
4 - зеленый
5 - желтый
6 - фиолетовый
7 - оранжевый
L - линия
R - прямоугольник
S - квадрат
C - круг
T - равносторонний треугольник
Y - прямоугольный треугольник
D - ромб
E - ластик
""")
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        #смена цвета и режима
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_r:
                mode="rectangle"
            elif event.key==pygame.K_s:
                mode = "square"
            elif event.key==pygame.K_c:
                mode="circle"
            elif event.key==pygame.K_t:
                mode="triangle_equilateral"
            elif event.key==pygame.K_y:
                mode="triangle_right"
            elif event.key==pygame.K_d:
                mode="rhombus"
            elif event.key==pygame.K_l:
                mode="line"
            elif event.key==pygame.K_e:
                mode="eraser"
            elif event.key==pygame.K_0:
                current_color=color_white
            elif event.key==pygame.K_1:
                current_color=color_red
            elif event.key==pygame.K_2:
                current_color=color_blue
            elif event.key==pygame.K_3:
                current_color=color_black
            elif event.key==pygame.K_4:
                current_color=color_green
            elif event.key==pygame.K_5:
                current_color=color_yellow
            elif event.key==pygame.K_6:
                current_color=color_purple
            elif event.key==pygame.K_7:
                current_color=color_orange
        #начало рисования
        if event.type==pygame.MOUSEBUTTONDOWN and event.button==1:
            lmbpressed=True
            start_pos=event.pos
        #процесс рисования(линии и ластик)
        if event.type==pygame.MOUSEMOTION and lmbpressed:
            if mode=="line":
                pygame.draw.line(screen,current_color,start_pos,event.pos,thickness)
                start_pos=event.pos
            elif mode=="eraser":
                pygame.draw.line(screen, color_white, start_pos, event.pos, thickness * 3)
                start_pos=event.pos
        #завершение рисования фигур
        if event.type==pygame.MOUSEBUTTONUP and event.button==1:
            lmbpressed=False
            x1,y1=start_pos
            x2,y2=event.pos
            if mode=="rectangle":
                rect=pygame.Rect(min(x1,x2),min(y1,y2),abs(x2-x1),abs(y2-y1))
                pygame.draw.rect(screen,current_color, rect, thickness)
            elif mode=="square":
                side=min(abs(x2-x1),abs(y2-y1))
                rect=pygame.Rect(x1,y1,side,side)
                pygame.draw.rect(screen,current_color,rect,thickness)
            elif mode=="circle":
                radius=int(((x2-x1)**2+(y2-y1)**2)**0.5)
                pygame.draw.circle(screen, current_color, start_pos, radius, thickness)
            elif mode=="triangle_equilateral":
                height=abs(y2 - y1)
                pygame.draw.polygon(screen,current_color,[(x1,y2), (x2,y2), ((x1+x2)//2,y2-height)],thickness)
            elif mode=="triangle_right":
                pygame.draw.polygon(screen, current_color, [(x1, y2), (x2, y2), (x1, y1)], thickness)
            elif mode=="rhombus":
                center_x=(x1+x2)//2
                center_y=(y1+y2)//2
                dx=abs(x2-x1)//2
                dy=abs(y2-y1)//2
                pygame.draw.polygon(screen,current_color,[(center_x,y1),(x2,center_y),(center_x,y2),(x1,center_y)],thickness)
    pygame.display.flip()
pygame.quit()

