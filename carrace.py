import pygame
from sys import exit
from random import randint

dim = (600,600)
ssq = 10

rate = 20
fps = 30

def quit():
    pygame.quit()
    exit()

class Car:
    def __init__(self, screen, X, Y, color, vel):
        self.X = X
        self.Y = Y
        self.color = color
        self.vel = vel
        self.screen = screen
        
    def getRects(self):
        body = []
        for i in range(0,8):
            for j in range(1,4):
                body.append(pygame.Rect(self.X+j*ssq,self.Y+i*ssq,ssq,ssq))

        wheels = []
        for i in [1,2,5,6]:
            for j in [0,4]:
                wheels.append(pygame.Rect(self.X+j*ssq,self.Y+i*ssq,ssq,ssq))
        return body, wheels
    
    def draw(self):
        body , wheels = self.getRects()
        for i in body:
            pygame.draw.rect(self.screen,self.color,i)
        for i in wheels:
            pygame.draw.rect(self.screen,"black",i)
        pygame.display.update()
        
    def collision(self,c):
        def getPieces(x):
            body , wheels = x.getRects()
            return body + wheels
        p1 = getPieces(self)
        p2 = getPieces(c)
        for i in p1:
            for j in p2:
                if pygame.Rect.colliderect(i,j):
                    return True
        return False
        
class Player(Car):
    def __init__(self,screen):
        self.pos_car_y = dim[1]-8*ssq
        self.pos_car = [80,130,180,230,280,330,380,430,480]
        self.carx = 4
        super().__init__(screen, self.pos_car[self.carx],self.pos_car_y,"red",0)
        
    def move(self,side):
        self.carx += side
        self.X = self.pos_car[self.carx]
        
    def goOut(self):
        if (self.carx<1):
            self.move(1)
            return True
        if (self.carx>(len(self.pos_car)-2)):
            self.move(-1)
            return True
        return False
        
    def collision(self,cars):
        for i in cars:
            if super().collision(i):
                return True
        return False
        
class Car_Street(Car):
    def __init__(self,screen):
        pos_spawn = [130,180,230,280,330,380,430]
        colors = ["blue","green","yellow","orange","cyan","purple","magenta"]
        super().__init__(screen, pos_spawn[randint(0,len(pos_spawn)-1)],0,colors[randint(0,len(colors)-1)],1)
    def move(self, v=10):
        self.Y = self.Y+v*self.vel
        

class Game:
    def __init__(self,screen):
        self.clock = pygame.time.Clock()
        self.screen = screen
        
        self.font = pygame.font.SysFont('Comic Sans MS', 20)
        
        self.start()
        
    def drawStreet(self):
            X0 = 150
            width = 300
            pygame.draw.rect(self.screen,"gray",(X0-20,0,width+50,dim[1]))
            for i in range(0,4):
                pygame.draw.rect(self.screen,"white",(X0+i*100,0,10,dim[1]))
                
    def draw(self,b):
        self.screen.fill((0,128,0))
        self.drawStreet()
        if b:
            self.car.draw()
        for i in self.cars:
            i.draw()
        self.showText()
        pygame.display.update()
            
    def showText(self):           
        text_score1 = self.font.render('SCORE',True,"black")
        text_score2 = self.font.render(str(self.score),True,"black")
        text_hscore1 = self.font.render('HIGHSCORE',True,"black")
        text_hscore2 = self.font.render(str(self.highscore),True,"black")
        text_life = self.font.render('LIFE : '+str(self.life),True,"black")
        text_speed = self.font.render('SPEED : '+str(self.speed),True,"black")
        self.screen.blit(text_score1,(0,0))
        self.screen.blit(text_score2,(0,50))
        self.screen.blit(text_hscore1,(0,100))
        self.screen.blit(text_hscore2,(0,150))
        self.screen.blit(text_life,(0,200))
        self.screen.blit(text_speed,(0,250))
        
    def showGameOver(self):
        self.screen.fill("black")
        font = pygame.font.SysFont('Comic Sans MS', 50)
        text_game_over = font.render('GAME OVER',True,"white")
        text_score = font.render('SCORE : '+str(self.score),True,"white")
        rect1 = text_game_over.get_rect(center=(dim[0]//2, dim[1]//2))
        rect2 = text_score.get_rect(center=(dim[0]//2, 3*dim[1]//4))
        self.screen.blit(text_game_over,rect1)
        self.screen.blit(text_score,rect2)
        pygame.display.update()
        
    def move(self):
        for i in range(0,len(self.cars)):
            (self.cars[i]).move(self.speed)
            
    def remove(self):
        for i in range(0,len(self.cars)):
            if (self.cars[i]).Y > dim[1]:
                self.cars.pop(i)
                self.score+=(self.speed-self.min_speed+1)
            if (i==(len(self.cars)-1)):
                return
                
    def crash(self):
        self.life -= 1
        self.speed = self.min_speed
        pygame.time.delay(1000)
        cck = pygame.time.Clock() 
        self.cars = []
        for i in range(1,5):
            self.draw((i%2)==0)
            cck.tick(10)
    
    def key(self):  
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.saveHighScore()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.saveHighScore()
                    quit()
                elif event.key == pygame.K_n:
                    return True
                elif event.key == pygame.K_p:
                    self.on = not self.on
                elif event.key == pygame.K_LEFT:
                    self.car.move(-1)
                elif event.key == pygame.K_RIGHT:
                    self.car.move(1)
                elif event.key == pygame.K_UP:
                    if self.speed<self.max_speed:
                        self.speed += 1
                elif event.key == pygame.K_DOWN:
                    if self.speed>self.min_speed:
                        self.speed -= 1
        return False
        
    def loadHighScore(self):
        fp = open('highscore.num','r')
        x=(fp.readlines())[0]
        x = x.split('\n')
        x = int(x[0])
        fp.close()
        return x
        
    def saveHighScore(self):
        def checkHighScore():
            if self.score>self.highscore:
                self.highscore = self.score
        checkHighScore()
        fp = open('highscore.num','w')
        fp.writelines([str(self.highscore)+'\n'])
        fp.close()
        
    def start(self):
        self.score = 0
        self.highscore = self.loadHighScore()
        self.life = 3
        self.max_speed = 30
        self.min_speed = 10
        self.speed = self.min_speed
        self.car = Player(self.screen)
        self.cars = []
        
        count = 0
        self.on = True
        lose = False
        
        while True:
            if self.key():
                self.saveHighScore()
                break
            if self.on:
            
                self.move()
                self.remove()
                
                if count == 0:
                    self.cars.append(Car_Street(self.screen))
                           
                count = (count+1)%(rate//(self.speed//10))
                
                if (self.car.goOut() or self.car.collision(self.cars)):
                    self.crash()
                    
                if self.life==0:
                    self.on = False
                    lose = True
                    
                self.draw(True)
                self.clock.tick(fps)
                
            elif lose:
                self.saveHighScore()
                self.showGameOver()

def main():
    def draw():
        screen.fill("black")
        font1 = pygame.font.SysFont('Comic Sans MS', 50)
        font2 = pygame.font.SysFont('Comic Sans MS', 20)
        text_new = font1.render('CAR RACE',True,"white")
        text_quit = font2.render('< Press Space to New Game and \'q\' to Quit >',True,"white")
        rect1 = text_new.get_rect(center=(dim[0]//2, dim[1]//2))
        rect2 = text_quit.get_rect(center=(dim[0]//2, 3*dim[1]//4))
        screen.blit(text_new,rect1)
        screen.blit(text_quit,rect2)
        pygame.display.update()
        
    pygame.init()
    screen = pygame.display.set_mode(dim)
    pygame.display.set_caption("Car Race")
    pygame.display.flip()
    draw()
    while True:   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    quit()
                elif event.key == pygame.K_SPACE:
                    Game(screen)
                    draw()

if __name__=="__main__":
    main()