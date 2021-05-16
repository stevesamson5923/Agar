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



player = Player(WIDTH//2,HEIGHT//2,(140, 46, 184),50)

def redrawwindow(mousexy):
    win.fill((0,0,0))
    player.centerx,player.centery = mousexy   
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

    redrawwindow(mousexy)
pygame.quit()