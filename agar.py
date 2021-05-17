import pygame
import random
import math
pygame.init()

WIDTH = 1280
HEIGHT = 650
win = pygame.display.set_mode((WIDTH,HEIGHT))

pygame.display.set_caption("First Game")
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)
clock = pygame.time.Clock()

class Player:
    def __init__(self,x,y,color,r):
        self.centerx = x
        self.centery = y
        self.color = color
        self.radius= r
        self.score = 0
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.centerx,self.centery),self.radius)
    def update(self,win):
        self.draw(win)

class BG:
    def __init__(self,x,y,w,h,dx,dy):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.dirx = dx
        self.diry = dy
        self.image = pygame.transform.scale(pygame.image.load('bg2.jpg'),(self.width,self.height)).convert()
        self.rect = self.image.get_rect()
        self.velx = 2
        self.vely = 2
        self.donex = 0
        self.doney = 0
        self.donexy = 0
    def draw(self,win):
        win.blit(self.image,(self.x,self.y))
    def update(self,win):
        if self.dirx == 'right':
            self.x = self.x + self.velx
        if self.dirx == 'left':
            self.x = self.x - self.velx
        if self.diry == 'up':
            self.y = self.y - self.vely
        if self.diry == 'down':
            self.y = self.y + self.vely
        self.draw(win)

class Food:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.radius = r
        self.color = (random.randint(1,220),random.randint(1,220),random.randint(1,220))
        self.dirx = 0
        self.diry = 0
        self.velx = 1
        self.vely = 1
        self.collision = False
        self.visible = True
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)            
    def update(self,win,player):
        
        if self.dirx == 'right':
            self.x = self.x + self.velx
        if self.dirx == 'left':
            self.x = self.x - self.velx
        if self.diry == 'up':
            self.y = self.y - self.vely
        if self.diry == 'down':
            self.y = self.y + self.vely
        
        distance = math.hypot(player.centerx-self.x,player.centery-self.y)
        if distance <= player.radius + self.radius:
            self.collision = True
            player.score = player.score + int(self.radius * .50)
            player.radius = player.radius + int(self.radius * .05)
            #print(player.score)
        
        if self.x < 0 or self.x > WIDTH or self.y < 0 or self.y > HEIGHT:
            self.visible = False
        else:
            self.visible = True
        if self.visible:   
            self.draw(win)

player = Player(WIDTH//2,HEIGHT//2,(140, 46, 184),30)
center_bg = BG(0,0,WIDTH,HEIGHT,0,0)
food_list=[]
food_count = 40
for i in range(food_count):
    food = Food(random.randint(10,1200),random.randint(10,600),random.randint(3,7))
    food_list.append(food)

bg_list = []
bg_list.append(center_bg)
count = 0
def create_new_bg():
    length = len(bg_list)

    for i in range(length):
        if bg_list[i].x > 0 and bg_list[i].x < WIDTH and bg_list[i].y == 0 and bg_list[i].donex != 1:
            new_bg = BG(bg_list[i].x-bg_list[i].width,bg_list[i].y,WIDTH,HEIGHT,bg_list[i].dirx,bg_list[i].diry)
            bg_list.append(new_bg)
            bg_list[i].donex = 1
            print('inside going right')
        # if bg_list[i].y > 0 and bg_list[i].y < HEIGHT and bg_list[i].x == 0 and bg_list[i].doney != 1:
        #     new_bg = BG(bg_list[i].x,bg_list[i].y-bg_list[i].height,WIDTH,HEIGHT,bg_list[i].dirx,bg_list[i].diry)
        #     bg_list.append(new_bg)
        #     bg_list[i].doney = 1          
        # if bg_list[i].x > 0 and bg_list[i].x < WIDTH and bg_list[i].y > 0 and bg_list[i].y < HEIGHT and bg_list[i].donexy != 1:
        #     new_bg = BG(bg_list[i].x-bg_list[i].width,bg_list[i].y-bg_list[i].height,WIDTH,HEIGHT,bg_list[i].dirx,bg_list[i].diry)
        #     bg_list.append(new_bg)
        #     bg_list[i].donexy = 1
        
        if bg_list[i].x < 0 and bg_list[i].x+bg_list[i].width > 0 and bg_list[i].y == 0 and bg_list[i].donex != -1:
            new_bg = BG(bg_list[i].x+bg_list[i].width,bg_list[i].y,WIDTH,HEIGHT,bg_list[i].dirx,bg_list[i].diry)
            bg_list.append(new_bg)
            bg_list[i].donex = -1
            print('inside going left')
        
        # if bg_list[i].y < 0 and bg_list[i].y+bg_list[i].height > 0 and bg_list[i].x == 0 and bg_list[i].doney != -1:
        #     new_bg = BG(bg_list[i].x,bg_list[i].y+bg_list[i].height,WIDTH,HEIGHT,bg_list[i].dirx,bg_list[i].diry)
        #     bg_list.append(new_bg)
        #     bg_list[i].doney = -1
        
        # if bg_list[i].x < 0 and bg_list[i].y < 0 and bg_list[i].x+bg_list[i].width >0 and bg_list[i].y+bg_list[i].height > 0 and bg_list[i].donexy != -1:
        #     new_bg = BG(bg_list[i].x+bg_list[i].width,bg_list[i].y+bg_list[i].height,WIDTH,HEIGHT,bg_list[i].dirx,bg_list[i].diry)
        #     bg_list.append(new_bg)
        #     bg_list[i].donexy = -1
        
def check_bg_in_view():
    length = len(bg_list)
    delete_index = []
    for bg in bg_list:
        if bg.x >= 0 and bg.x <= WIDTH and bg.y>=0 and bg.y <= HEIGHT:
            print('check1')
            continue
        if bg.x+bg.width >= 0 and bg.x+bg.width <= WIDTH and bg.y >= 0 and bg.y <= HEIGHT:
            print('check2')
            continue
        if bg.x+bg.width >=0 and bg.x+bg.width <= WIDTH and bg.y + bg.height >= 0 and bg.y + bg.height <= HEIGHT:
            print('check3')
            continue
        if bg.x >= 0 and bg.x <= WIDTH and bg.y + bg.height >= 0 and bg.y + bg.height <= HEIGHT:
            print('check4')
            continue
        bg_list.remove(bg)
        print('deleted')

resize_event = pygame.USEREVENT + 3
pygame.time.set_timer(resize_event,5000)

def redrawwindow():
    global count
    win.fill((0,0,0))   
    mousexy = pygame.mouse.get_pos() 
    player.centerx,player.centery = mousexy   
    
    
    #create_new_bg()
    #print('length :',len(bg_list))
    #check_bg_in_view()
    
    #for bg in bg_list:
    #    bg.update(win)
    #center_bg.update(win)
    for food in food_list:
        if food.collision:
            food_list.remove(food)
    
    #create more food
    for food in food_list:
        if food.visible:
            count = count + 1
    #print('Total food count:',count)
    if count < 40:
        #print('Total food count:',count)
        for i in range(40-count):
            food = Food(random.randint(10,1200),random.randint(10,600),random.randint(3,7))
            food.dirx = food_list[0].dirx
            food.diry = food_list[0].diry
            food_list.append(food)
        count = 0
    else:
        count = 0
    
    for food in food_list:
        food.update(win,player)
    
    player.update(win)
    pygame.display.update()

run=True

while run:
    #pygame.time.delay(3)
    #clock.tick(90) 
    redrawwindow()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.USEREVENT + 3:
            #print('called')
            for food in food_list:
                food.radius = food.radius + 1
    
    relxy = pygame.mouse.get_rel()
    if relxy[0] < 0: #mouse is moving in left direction
        for bg in bg_list:
            bg.dirx = 'right'
        for food in food_list:
            food.dirx = 'right'
    if relxy[1] < 0 :    #mouse is moving in up direction
        for bg in bg_list:
            bg.diry = 'down'
        for food in food_list:
            food.diry = 'down'
    if relxy[0] > 0 :    #mouse is moving in right direction
        for bg in bg_list:
            bg.dirx = 'left'
        for food in food_list:
            food.dirx = 'left'
    if relxy[1] > 0 :    #mouse is moving in down direction
        for bg in bg_list:
            bg.diry = 'up'
        for food in food_list:
            food.diry = 'up'
    # if relxy[0] == 0 and relxy[1] == 0:
    #     for bg in bg_list:
    #         bg.dirx = 0
    #         bg.diry = 0
    
pygame.quit()