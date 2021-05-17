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
        self.collision = False
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.centerx,self.centery),self.radius)
    def update(self,win,enemy_list):
        #player and enemy collision
        
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
        self.collision = False  #when food is eaten by enemy or player
        self.visible = True  # when food moves off boundary
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
        
        #food and player collision
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

class Enemy:
    def __init__(self,x,y,r):
        self.centerx = x
        self.centery = y
        self.radius = r
        self.directions = [0,1,2,3]
        self.dirx = random.randint(0,1)
        self.diry = random.randint(2,3)
        self.velx = 1
        self.vely = 1
        self.collision = False
        self.color = (random.randint(100,220),random.randint(100,220),random.randint(100,220))
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.centerx,self.centery),self.radius)
        pygame.draw.line(win,(255,255,255),(self.centerx,self.centery),(self.centerx+self.radius,self.centery+self.radius),5)
        pygame.draw.line(win,(255,255,255),(self.centerx,self.centery),(self.centerx-self.radius,self.centery+self.radius),5)
        pygame.draw.line(win,(255,255,255),(self.centerx,self.centery),(self.centerx,self.centery-(self.radius+5)),5)
    def update(self,win,food_list):  #0 for left, 1 for right, 2 for up , 3 for down
        #Change direction
        if self.centerx < 0 or self.centerx > WIDTH or self.centery < 0 or self.centery > HEIGHT:
            if self.dirx == 0:
                self.dirx = 1
            else:
                self.dirx = 0
            if self.diry == 2:
                self.diry = 3
            else:
                self.diry = 2
        
        #food and enemy collision
        for food in food_list:
            dist = math.hypot(food.x-self.centerx,food.y-self.centery)            
            if dist <= food.radius + self.radius:
                food.collision = True
                self.radius = self.radius + int(food.radius * 0.02)

        if self.dirx == 0 and self.diry == 2: #left and up 
            self.centerx = self.centerx - self.velx
            self.centery = self.centery - self.vely
        if self.dirx == 0 and self.diry == 3: #left and down
            self.centerx = self.centerx - self.velx
            self.centery = self.centery + self.vely
        if self.dirx == 1 and self.diry == 2: #right and up
            self.centerx = self.centerx + self.velx
            self.centery = self.centery - self.vely
        if self.dirx == 1 and self.diry == 3: #right and down
            self.centerx = self.centerx + self.velx
            self.centery = self.centery + self.vely
        self.draw(win)

player = Player(WIDTH//2,HEIGHT//2,(140, 46, 184),30)
center_bg = BG(0,0,WIDTH,HEIGHT,0,0)
food_list=[]
food_count = 40
for i in range(food_count):
    food = Food(random.randint(10,1200),random.randint(10,600),random.randint(3,7))
    food_list.append(food)

enemy_list = []
enemy_count = 10
def check_player_enemy_collision(ex,ey,er):
    global enemy_list    
    dist = math.hypot(ex-player.centerx,ey-player.centery)
    if dist <= player.radius+er:
        return True
    for e in enemy_list:
        dist2 = math.hypot(ex-e.centerx,ey-e.centery)
        if dist2 <= e.radius + er:
            return True
    return False

for i in range(enemy_count):
    res = True
    ex,ey,er=0,0,0
    while res == True:
        ex = random.randint(10,1200)
        ey = random.randint(10,600)
        er = random.randint(30,40)
        res = check_player_enemy_collision(ex,ey,er)    
    enemy = Enemy(ex,ey,er)
    enemy_list.append(enemy)

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

    score = player.score
    score_msg = 'Score: '+str(score)
    textsurface1 = myfont.render(score_msg, False, (255,255,255))
    pygame.draw.rect(win,(255,255,255),(5,5,200,65))
    pygame.draw.rect(win,(194, 59, 17),(8,8,194,59))
    win.blit(textsurface1,(11,11))
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
    
    #check enemy collision with other enemies
    for i in range(len(enemy_list)):
        for j in range(len(enemy_list)):
            if j == i:
                continue
            else:
                dist = math.hypot(enemy_list[i].centerx-enemy_list[j].centerx,enemy_list[i].centery-enemy_list[j].centery)
                if dist <= enemy_list[i].radius + enemy_list[j].radius:
                    if enemy_list[i].radius > enemy_list[j].radius: #i eats j
                        enemy_list[j].collision = True
                        enemy_list[i].radius = enemy_list[i].radius + int(enemy_list[j].radius * 0.05)
                    elif enemy_list[i].radius < enemy_list[j].radius: #j eats i
                        enemy_list[i].collision = True
                        enemy_list[j].radius = enemy_list[j].radius + int(enemy_list[i].radius * 0.05)

    #remove dead enemies and spawn new enemies
    for enemy in enemy_list:
        if enemy.collision == True:
            enemy_list.remove(enemy)
            res = True
            while res == True:
                ex = random.randint(10,1200)
                ey = random.randint(10,600)
                er = random.randint(30,40)
                res = check_player_enemy_collision(ex,ey,er) 
            enemy = Enemy(ex,ey,er)
            enemy_list.append(enemy)
        else:
            enemy.update(win,food_list)    

    player.update(win,enemy_list)
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