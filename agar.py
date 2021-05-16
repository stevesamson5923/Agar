import pygame
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
        self.image = pygame.transform.scale(pygame.image.load('bg2.jpg'),(self.width,self.height)).convert_alpha()
    def draw(self,win):
        self.rect = win.blit(self.image,(self.x,self.y))
    def update(self,win):
        if self.dirx == 'right':
            self.x = self.x + 1
        if self.dirx == 'left':
            self.x = self.x - 1
        if self.diry == 'up':
            self.y = self.y - 1
        if self.diry == 'down':
            self.y = self.y + 1
        self.draw(win)

player = Player(WIDTH//2,HEIGHT//2,(140, 46, 184),50)
center_bg = BG(0,0,WIDTH,HEIGHT,0,0)

def redrawwindow(mousexy):
    win.fill((0,0,0))
    player.centerx,player.centery = mousexy   
    center_bg.update(win)
    player.update(win)
    pygame.display.flip()

run=True

while run:
    #pygame.time.delay(3)
    #clock.tick(90) 
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    mousexy = pygame.mouse.get_pos()
    
    relxy = pygame.mouse.get_rel()
    if relxy[0] < 0:
        center_bg.dirx = 'right'
    if relxy[1] < 0:
        center_bg.diry = 'down'
    if relxy[0] > 0:
        center_bg.dirx = 'left'
    if relxy[1] > 0:
        center_bg.diry = 'up'

    redrawwindow(mousexy)
pygame.quit()