


import pygame
import random
import time

pygame.init()
update = pygame.display.update

win = pygame.display.set_mode((1400,900))
surfaceCreation = pygame.font.SysFont('Comic Sans MS',50)
pygame.display.set_caption("Gladitor's Sanctum")
white = (255, 255, 255) 

font = pygame.font.Font('freesansbold.ttf', 32)
fontLarge = pygame.font.Font('freesansbold.ttf', 52)
winnerFont = pygame.font.Font('freesansbold.ttf', 72)
text = font.render('GeeksForGeeks',True,white)

#images below----------
hellBackground = pygame.image.load('hellBackground.png')
hellBackground = pygame.transform.scale(hellBackground,(1400,900))
pongImg = pygame.image.load('pongImg.png')
pongImg = pygame.transform.scale(pongImg,(50,50))



#Player Images----------
playerTwoImg = pygame.image.load('playerTwoImg.png')
playerTwoImg = pygame.transform.scale(playerTwoImg,(200,100))
playerTwoImgEmpowered = pygame.image.load('playerTwoImgEmpowered.png')
playerTwoImgEmpowered = pygame.transform.scale(playerTwoImgEmpowered,(200,100))
playerTwoWin = pygame.image.load('playerTwoWin.png')
playerTwoWin = pygame.transform.scale(playerTwoWin,(1400,900))



playerOneImg = pygame.image.load('playerOneImg.png')
playerOneImg = pygame.transform.scale(playerOneImg,(200,100))
playerOneImgEmpowered = pygame.image.load('playerOneImgEmpowered.png')
playerOneImgEmpowered = pygame.transform.scale(playerOneImgEmpowered,(200,100))
playerOneWin = pygame.image.load('playerOneWin.png')
playerOneWin = pygame.transform.scale(playerOneWin,(1400,900))



class Listener:
    displayText = ''
    playerOneNameFound = False
    playerTwoNameFound = False

    
listener = Listener()

class Players:
    points = 0
    size = 200
    sizeY = 100
    empowered = False
    
    def __init__(self,name,currentX,currentY,img,empoweredImg):
        self.name = name
        self.currentX = currentX
        self.currentY = currentY
        self.img = img
        self.originalImg = img
        self.empoweredImg = empoweredImg

        self.playerText = font.render(f'{name}: {self.points}',True,white)
        

    def move(self,direction):
        
        if direction == 'L':
            if self.currentX >= 0:
                self.currentX -= 18
                
        elif direction == 'R':
            if self.currentX + self.size <= 1400:
                self.currentX += 18


playerOne = Players('',650,800,playerOneImg,playerOneImgEmpowered)
playerTwo = Players('',650,0,playerTwoImg,playerTwoImgEmpowered)

class orb:
    size = 25
    xrange = 0
    yrange = 0
    
    def __init__(self,currentX,currentY,img):
        self.currentX = currentX
        self.currentY = currentY
        self.img = img
        self.directionX = 2
        self.directionY = 6

        
    def shift(self,upDownLeftRight,paddle):
        self.directionX = random.choice([-10,-8,-4,0,4,8,10])
         
        if upDownLeftRight == 'U':
            if paddle.empowered:
                self.directionY = random.choice([-19,-20])
                paddle.empowered = False
            else:
                self.directionY = random.choice([-13,-14])
            
                
        elif upDownLeftRight == 'D':
    
            if paddle.empowered:
                self.directionY = random.choice([19,20])
                paddle.empowered = False
            else:
                self.directionY = random.choice([13,14])
                
        elif upDownLeftRight == 'L':
            self.directionX = random.choice([-4,-8,-10])
            
        elif upDownLeftRight == 'R':
            self.directionX = random.choice([4,8,10])
            

    def resetPong(self):
        self.currentX = 650
        self.currentY = 450
        self.directionX = 2
        self.directionY = random.choice([6,-6])
        
    def move(self):
        self.currentX += self.directionX
        self.currentY += self.directionY
        
    def getTopAndBot(self):
        self.topX = int(self.currentX + self.size / 2)
        self.topY = self.currentY

        self.botX = self.topX
        self.botY = self.currentY + self.size

    def getLeftAndRight(self):
        self.rightX = self.currentX + self.size
        self.leftX = self.currentX
        
pong = orb(650,450,pongImg)        
        

def drawGame():
    
    def checkEmpowerment(paddle):
        if paddle.empowered:
            paddle.img = paddle.empoweredImg
        else:
            paddle.img = paddle.originalImg

    checkEmpowerment(playerOne)
    checkEmpowerment(playerTwo)
    
    win.blit(hellBackground,(0,0))
    win.blit(playerOne.img,(playerOne.currentX,playerOne.currentY))
    win.blit(playerTwo.img,(playerTwo.currentX,playerTwo.currentY))
    win.blit(pong.img,(pong.currentX,pong.currentY))
    win.blit(playerOne.playerText,(100,600))
    win.blit(playerTwo.playerText,(100,100))

def givePoints(player):
    player.points += 1
    
def checkCollision():
    pong.getTopAndBot()
    pong.getLeftAndRight()
    

#Paddle/ terrain collisions

    if pong.botX in range(playerOne.currentX, playerOne.currentX + playerOne.size) and pong.botY in range(playerOne.currentY - 22, playerOne.currentY):
        pong.shift('U',playerOne)
        
    if pong.currentX + pong.size >= 1380:
        pong.shift('L',None)

    if pong.currentX <= 0:
        pong.shift('R',None)

    if pong.topX in range(playerTwo.currentX, playerTwo.currentX + playerTwo.size) and pong.topY in range(playerTwo.currentY + 85, playerTwo.currentY + 106):
        pong.shift('D',playerTwo)



    

#point collisions
        
    if pong.currentY <= 0:
        playerOne.points += 1
        playerOne.playerText = font.render(f'{playerOne.name}: {playerOne.points}',True,white)
        pong.resetPong()
        
    elif pong.currentY >= 900:
        playerTwo.points += 1
        playerTwo.playerText = font.render(f'{playerTwo.name}: {playerTwo.points}',True,white)
        pong.resetPong()


def setupControls():
    inputtedLetter = ''
    
    for events in pygame.event.get():
        if events.type == pygame.KEYDOWN:
            if pygame.key.name(events.key) == 'space':
                inputtedLetter = ' '
                
            elif pygame.key.name(events.key) == 'backspace':
                if len(listener.displayText) > 0:
                    listener.displayText = listener.displayText[:-1]
                    
            elif pygame.key.name(events.key) == 'return':
                
                if not listener.playerOneNameFound:
                    
                    playerOne.name = listener.displayText
                    listener.displayText = ''
                    listener.playerOneNameFound = True
                    
                    
                elif not listener.playerTwoNameFound:
                    
                    playerTwo.name = listener.displayText
                    listener.displayText = ''
                    listener.playerTwoNameFound = True
                    
            else:
                inputtedLetter = pygame.key.name(events.key)
               
    
    listener.displayText += inputtedLetter
    finalStringText = fontLarge.render(listener.displayText.title(),True,white)
    win.blit(finalStringText,(565,500))
   

def runControls():
    event = pygame.event.poll()
    mousePosition = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()  #checking pressed keys

    if playerOne.points >= 5:
       
        winnerName = winnerFont.render(playerOne.name.title(),True,white)
        win.blit(playerOneWin,(0,0))
        win.blit(winnerName,(800,750))
        update()
        time.sleep(2.5)
        resetGame()
        
    elif playerTwo.points >= 5:
        
        winnerName = winnerFont.render(playerTwo.name.title(),True,white)
        win.blit(playerTwoWin,(0,0))
        win.blit(winnerName,(800,750))
        update()
        time.sleep(2.5)
        resetGame()
            
            
    #P1 Controls
    if keys[pygame.K_LEFT]:
        playerOne.move('L')
        
    if keys[pygame.K_RIGHT]:
        playerOne.move('R')

    if keys[pygame.K_UP]:
        playerOne.empowered = True
        
    
    if keys[pygame.K_a]:
        playerTwo.move('L')
        
    if keys[pygame.K_d]:
        playerTwo.move('R')

    if keys[pygame.K_w]:
        playerTwo.empowered = True

    
    #control the pong
    checkCollision()
    pong.move()


def resetGame():
    playerOne.name = ''
    playerTwo.name = ''
    playerOne.points = 0
    playerTwo.points = 0
    playerOne.currentX = 650
    playerTwo.currentX = 650
    listener.playerOneNameFound = False
    listener.playerTwoNameFound = False
    
    setupGame()
    
def setupGame():

    playerOneAlert = 'Player One please enter your name!'
    playerTwoAlert = 'Player Two please enter your name!'
    playerOneAlertMsg = font.render(playerOneAlert,True,white)
    playerTwoAlertMsg = font.render(playerTwoAlert,True,white)
    
    while True:
        
        win.blit(hellBackground,(0,0))
        setupControls()
        
        if not listener.playerOneNameFound:
            win.blit(playerOneAlertMsg,(400,300))
            
        if listener.playerOneNameFound:
            win.blit(playerTwoAlertMsg,(400,300))
            
        if listener.playerOneNameFound and listener.playerTwoNameFound:
            playerOne.playerText = font.render(f'{playerOne.name}: {playerOne.points}',True,white)
            playerTwo.playerText = font.render(f'{playerTwo.name}: {playerTwo.points}',True,white)
            print('still listening')
            break
            
        update()
        


setupGame()
while True:
    runControls()
    drawGame()
    update()
    
    

