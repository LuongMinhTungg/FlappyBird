import pygame
from pygame.locals import * 
import random,sys

pygame.init()

black = (0,0,0)
red = (200,0,0)
green = (0,200,0)

bright_red = (255,0,0)
bright_green = (0,255,0)

wHeight = 500
wWidth = 700

FPS = 60
fpsClock = pygame.time.Clock()

BG = pygame.image.load(r'C:\Users\Admin\OneDrive\Documents\python.py\game02\vi du\fbird\image\background.png')
BGover = pygame.image.load(r'C:\Users\Admin\OneDrive\Documents\python.py\game02\vi du\fbird\image\gameover3.jpg')
screen = pygame.display.set_mode((wWidth, wHeight))
pygame.display.set_caption('Flappy Bird')

bWidth = 20
bHeight = 20
G = 0.5
V = -8
BirdImg = pygame.image.load(r'C:\Users\Admin\OneDrive\Documents\python.py\game02\vi du\fbird\image\redbird.png')

angle = 0
scale = 1
mouse = pygame.mouse.get_pos()

img = BirdImg


cWidth = 48
cHeight = 300
Blank = 200
Distance = 300
cSpeed = 2
ColumnImg = pygame.image.load(r'C:\Users\Admin\OneDrive\Documents\python.py\game02\vi du\fbird\image\pipe.png')
a = []
b = []
pause = False

def getSurf(textF, size, msg, color):
    font = pygame.font.SysFont(textF, size)
    textSurf = font.render(msg, True, color)
    return textSurf 

def getSize(textSurf):
    textSize = textSurf.get_size() 
    return textSize

class Column:
    def __init__(self):
        self.Width = cWidth
        self.Height = cHeight
        self.Blank = Blank
        self.Distance = Distance
        self.Speed= cSpeed
        self.surface = ColumnImg       
        self.ls = []
        for i in range(3):
            x = wWidth + i * self.Distance
            y = random.randrange(60, wHeight - self.Blank -60, 20)
            self.ls.append([x,y])
    def draw(self):
        for i in range(3):
            screen.blit(self.surface,(self.ls[i][0], self.ls[i][1] - self.Height))
            screen.blit(self.surface,(self.ls[i][0], self.ls[i][1] + self.Blank))
    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.Speed
        if self.ls[0][0] < -self.Width:
            self.ls.pop(0)
            x = self.ls[1][0] + self.Distance
            y = random.randrange(60, wHeight - self.Blank- 60,10)
            self.ls.append([x,y])
            

class Bird:
    def __init__(self):
        self.width = bWidth
        self.height = bHeight
        self.x = (wWidth - bWidth)/5
        self.y = (wHeight - bHeight)/2
        self.angle = angle
        self.scale = scale
        self.speed = 0
        self.surface = BirdImg
        self.img = img

    def draw(self):       
        screen.blit(self.img,(int(self.x), int(self.y)))
    def draw1(self):
        self.angle = -70
        self.img = pygame.transform.rotozoom(self.surface,self.angle, self.scale)
        screen.blit(self.img,(350,465))
    def update(self, mouseClick):
        self.y += self.speed + 0.5*G
        self.speed += G 
        if mouseClick == True:
            self.angle += 4
            self.img = pygame.transform.rotozoom(self.surface,self.angle, self.scale)
            self.speed = V
        if mouseClick == False:
            self.angle = -20
            self.img = pygame.transform.rotozoom(self.surface,self.angle, self.scale)
        
            
            
            
class Score(): 
    def __init__(self):
        self.score = 0
        self.addscore = True
    def draw(self):      
        textSurf = getSurf('consolas', 40, str(self.score), black)
        textSize = getSize(textSurf)
        screen.blit(textSurf, (int((wWidth - textSize[0])/2), 100))

    def update(self, bird, column):
        collision = False
        for i in range(3):
            rectColumn = [column.ls[i][0] + column.Width, column.ls[i][1], 1, column.Blank]
            rectBird = [bird.x, bird.y, bird.width, bird.height]
            if rectCollision(rectBird, rectColumn) == True:
                collision = True
                break
        if collision == True:
            if self.addScore == True:
                self.score += 1
                
            self.addScore = False
        else:
            
            self.addScore = True
    

    

def rectCollision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False

def isGameover(bird, column):
    for i in range(3):
        rectBird = [bird.x, bird.y, bird.width, bird.height]
        rectCol1 = [column.ls[i][0] , column.ls[i][1]  - column.Height, column.Width, column.Height]
        rectCol2 = [column.ls[i][0], column.ls[i][1]  + column.Blank , column.Width, column.Height]
        if rectCollision(rectBird, rectCol1) == True:
            return True
        if rectCollision(rectBird, rectCol2) == True:            
            return True
    if bird.y < 0 or bird.y > wHeight:
        return True 




def button(msg,x,y,w,h,ic,ac, action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac,(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic,(x,y,w,h))
    
    
    textSurf = getSurf('consolas',20, msg, black)
    textRect = textSurf.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    screen.blit(textSurf, textRect)
    
    
def paused():
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
       
        textSurf = getSurf('consolas', 60, 'Pause', bright_red)
        textRect = textSurf.get_rect()
        textRect.center = ((wWidth/2),(wHeight/2))
        screen.blit(textSurf, textRect)
        button('Continue',150,350,100,50,green,bright_green,unpause)
        button('Quit',500,350,100,50,red,bright_red,quitgame)

        pygame.display.update()
        fpsClock.tick(15)            
def quitgame():
    pygame.quit()
    quit()

def unpause():
    global pause
    pause = False

def bScore(score):
    a.append(score.score)
    a.sort(reverse = True)
    return a[0]
def yScore(score):
    b.append(score.score)
    return b[len(b)-2]



def gameover(score):
    score = Score()
    bird = Bird()

    replaySurf = getSurf('consolas', 20, 'press Space to replay', black)
    replaySize = getSize(replaySurf)
    quitSurf = getSurf('consolas', 20, 'press Q to quit', black)
    quitSize = getSize(quitSurf)
    goSurf = getSurf('Consolas', 60, 'Game Over', red)
    goSize = getSize(goSurf)
    bsSurf = getSurf('consolas', 30, 'Best Score: '+ str(bScore(score)), red)
    bsSize = getSize(bsSurf)
    ysSurf = getSurf('consolas', 20, 'Your Score: '+str(yScore(score)), black)
    ysSize = getSize(ysSurf)
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                quitgame()
            if event.type == KEYUP:
                if event.key == K_SPACE:
                    return False
                if event.key == K_q:
                    quitgame()
        
        screen.blit(BG,(0,0))
        bird.draw1()

        screen.blit(goSurf,(int((wWidth - goSize[0])/2), 100))
        screen.blit(replaySurf, (int((wWidth - replaySize[0])/2), 325))
        screen.blit(quitSurf, (int((wWidth - quitSize[0])/2), 350))
        screen.blit(bsSurf, (0,0))
        screen.blit(ysSurf, (int((wWidth - ysSize[0])/2), 225))
        
        pygame.display.update()
        fpsClock.tick(FPS)

def gameplay(bird, column, score):
    global pause
    running = True
    mouseclick = False
    bird.__init__()
    bird.speed = V
    column.__init__()
    score.__init__()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
            if event.type == MOUSEBUTTONDOWN:               
                mouseclick = True               
            if event.type == MOUSEBUTTONUP:
                mouseclick = False
            
        screen.blit(BG,(0,0))
        
        bird.draw()
        bird.update(mouseclick)
        
        column.draw()
        column.update()

        score.draw()
        score.update(bird, column)
        
        if isGameover(bird, column) == True:
            bScore(score)
            yScore(score)
            return False

        pygame.display.update()
        fpsClock.tick(FPS)
def gameStart(bird):
    bird.__init__()
   
    headingSurface = getSurf('consolas', 60, 'FLAPPY BIRD', bright_red)
    headingSize = getSize(headingSurface)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            

        screen.blit(BG, (0, 0))
        bird.draw()
        
        screen.blit(headingSurface, (int((wWidth - headingSize[0])/2), 100))
        
        
        button('easy',150,350,100,50,green,bright_green,easy)
        button('hard',500,350,100,50,red,bright_red,hard)
        pygame.display.update()
        fpsClock.tick(FPS)
def easy():
    global cSpeed
    cSpeed = 2
    bird = Bird()
    column = Column()
    score = Score()
    bird.__init__()
    bird.speed = V
    column.__init__()
    score.__init__()
    gameplay(bird, column, score)
    gameover(score) 

def hard():
    global cSpeed
    cSpeed = 10
    bird = Bird()
    column = Column()
    score = Score()
    bird.__init__()
    bird.speed = V
    column.__init__()
    score.__init__()
    
    gameplay(bird, column, score)
    gameover(score)

def main():
    bird = Bird()
    column = Column()
    score = Score()
    while True:
        gameStart(bird)
        
        
             
        
        
main()
