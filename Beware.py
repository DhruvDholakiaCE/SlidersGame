from pygame import *
import time as t
ship = image.load("background.jpg")

init()
screenHeight = 700
screenWidth  = 700
gameWindow = display.set_mode([screenWidth,screenHeight])
# start_time=  t.time()

class PlayerLeft(sprite.Sprite):
    def __init__(self,x,y,color):
        sprite.Sprite.__init__(self)
        self.image = Surface((20,120))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedy = 0

    def update(self):
        self.speedy =0
        keystate = key.get_pressed()
        if keystate[K_w] :
            self.speedy = -5
        if keystate[K_s] :
            self.speedy= 5

        self.rect.y += self.speedy
        if self.rect.top < 2:
            self.rect.top = 2
        if self.rect.bottom > screenHeight-2:
            self.rect.bottom = screenHeight-2


        # print(self.rect.)

class PlayerRight(sprite.Sprite):
    def __init__(self,x,y,color):
        sprite.Sprite.__init__(self)
        self.image = Surface((20,120))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speedy = 0

    def update(self):
        self.speedy =0
        keystate = key.get_pressed()
        if keystate[K_UP] :
            self.speedy = -5
        if keystate[K_DOWN] :
            self.speedy= 5

        self.rect.y +=self.speedy
        if self.rect.top < 2:
            self.rect.top = 2
        if self.rect.bottom > screenHeight-2:
            self.rect.bottom = screenHeight-2

class Ball(sprite.Sprite):
    def __init__(self):
        sprite.Sprite.__init__(self)
        # self.image = Surface((20,20))
        self.image = image.load('fireball.png').convert_alpha()

        self.image = transform.scale(self.image, (40, 40))
        self.image = transform.flip(self.image, True, True)
        self.rect = self.image.get_rect()


        self.rect.centerx= screenWidth//2 -100
        self.rect.centery = screenHeight//2 - 100
        self.speedx = 2
        self.speedy = 2


    def updateX(self):
        self.speedx*= -1

    def updateY(self):
        self.speedy *= -1


    def update(self):
        # angle_rad = math.radians(self.angle)

        # Rotate the ship
        # self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        # self.rect.centerx += -self.speed * math.sin(angle_rad)
        # self.rect.centery += self.speed * math.cos(angle_rad)


        self.rect.y += self.speedy
        self.rect.x += self.speedx
        # if hits:s
        #     self.dx *= -1
        #     return
        if  self.rect.x < 0 or self.rect.x > screenWidth - self.image.get_width():
            self.image = transform.flip(self.image, True, True)
            self.updateX()

        if self.rect.bottom > screenHeight or  self.rect.top < 0 :
            self.updateY()

# class Obstacles(sprite.Sprite):
#     def __init__(self):
#         sprite.Sprite.__init__(self)
#         self.image = Surface((100,100))
#         self.image.fill((0,255,0))
#         # self.image = image.load('fireball.png').convert_alpha()
#         #
#         # self.image = transform.scale(self.image, (40, 40))
#         # self.image = transform.flip(self.image, True, True)
#         self.rect = self.image.get_rect()
#
#         self.rect.centerx= screenWidth//2
#         self.rect.centery = screenHeight//2 + 100




def EndScreen(scoreLeft, scoreRight):
    running = True
    while running:
        for ev in event.get():
            if ev.type == QUIT:
                running = False
        gameWindow.fill((0, 0, 0))
        gameOverFontStyle = font.SysFont(None, 100)
        gameOverFont = gameOverFontStyle.render('GAME OVER!', True, (0, 129, 255))
        finalScoreFontStyle = font.SysFont(None, 30)
        finalScores = finalScoreFontStyle.render(
            'Score Left = ' + str(scoreLeft) + '   Score Right = ' + str(scoreRight), True, (45, 134, 25))

        gameWindow.blit(gameOverFont, (screenWidth // 2 - 230, screenHeight // 2 - 100))
        gameWindow.blit(finalScores, (screenWidth // 2 - 160, screenHeight // 2))

        display.update()


def gameLoop():

    # Left right score drawing...................
    scoreLeft = 0
    scoreRight = 0
    scoreFont = font.SysFont(None, 25)

    imgLeft = scoreFont.render('score = ' + str(scoreLeft), True, (144, 232, 255))
    gameWindow.blit(imgLeft, (screenWidth // 2 - 50, 2))

    imgRight = scoreFont.render('score = ' + str(scoreRight), True, (0, 129, 255))
    gameWindow.blit(imgRight, (screenWidth // 2 + 50, 2))

    gameOver = False
    all_sprites = sprite.Group()

    b = Ball()

    # obs = Obstacles()
    # all_sprites.add(obs)
    # obstacleGroup = sprite.Group()
    # obstacleGroup.add(obs)

    ballGroup = sprite.Group()
    ballGroup.add(b)
    all_sprites.add(b)

    playerLeft = PlayerLeft(0, screenHeight // 2, (110, 212, 110))
    all_sprites.add(playerLeft)

    playerRight = PlayerRight(screenWidth - 20, screenHeight // 2, (255, 0, 0))
    all_sprites.add(playerRight)

    playerGroup = sprite.Group()
    playerGroup.add(playerLeft)
    playerGroup.add(playerRight)
    # time_updated = False
    clock = time.Clock()
    while not gameOver :
        for ev in event.get():
            if ev.type == QUIT:
                b.kill()
                gameOver = True
            if ev.type == KEYDOWN:
                if ev.key == K_ESCAPE:
                    b.kill()
                    return
        # if int(t.time() - start_time) > 14 and time_updated == False:
        #     b.speedx += 2
        #     b.speedy += 2
        #     time_updated = True


        # Collision with screen, playerLeft and Right.........................................
        hits = sprite.groupcollide(playerGroup, ballGroup, False, False)
        # obsHits = sprite.groupcollide(obstacleGroup, ballGroup, False, False)
        # for i in obsHits:
        #     if b.speedx < 0 and (b.speedy > 0 or b.speedy <0):
        #         if b.rect.left <= i.rect.right:
        #             b.updateX()
        #         elif b.rect.bottom >= i.rect.top:
        #             b.updateY()
        #         elif b.rect.top >= i.rect.bottom:
        #             b.updateY()
        #     elif b.speedx > 0 and (b.speedy > 0 or b.speedy <0):
        #         if b.rect.bottom >= i.rect.top:
        #             b.updateY()
        #         elif b.rect.right >= i.rect.left:
        #             b.updateX()
        #         elif b.rect.top >= i.rect.bottom:
        #             b.updateY()

            # if b.speedx < 0 and (b.speedy <0):
            #     if b.rect.left <= i.rect.right:
            #         b.updateX()
        if b.rect.left < b.image.get_width() - 25 or b.rect.right > screenWidth - b.image.get_width() + 25:
            EndScreen(scoreLeft, scoreRight)
            gameOver = True
        else:
            if playerLeft in hits:
                scoreLeft += 10
                b.image = transform.flip(b.image, True, True)
                b.updateX()
            elif playerRight in hits:
                scoreRight += 10
                b.image = transform.flip(b.image, True, True)
                b.updateX()

            gameWindow.fill((0, 0, 0))

            gameWindow.blit(ship, (0, 0))
            all_sprites.draw(gameWindow)

            #Update left score...............................
            imgLeft = scoreFont.render('score = ' + str(scoreLeft), True, (144, 232, 255))
            gameWindow.blit(imgLeft, (screenWidth // 2 - 100, 2))

            #Update right score...............................
            imgRight = scoreFont.render('score = ' + str(scoreRight), True, (0, 129, 255))
            gameWindow.blit(imgRight, (screenWidth // 2 + 30, 2))

            all_sprites.update()
        display.flip()
        clock.tick(120)

def LoadingScreen():
    red = (200, 0, 0)
    green = (0, 200, 0)

    bright_red = (255, 0, 0)
    bright_green = (0, 255, 0)


    gameOver  = False
    while not gameOver :

        for ev in event.get():
            if ev.type == QUIT:
                gameOver= True

        mous = mouse.get_pos()

        gameWindow.fill((0, 0, 0))
        button('S L I D E R S', 100, (0, 129, 255), 150, 200)

        #Start Button Logic
        startButton = draw.rect(gameWindow, bright_green,(220,350,100,50))
        quitButton = draw.rect(gameWindow, bright_red,(380,350,100,50))

        if startButton.collidepoint(mous):
            click = mouse.get_pressed()
            if click[0] == 1:
                gameLoop()
        else:
            startButton = draw.rect(gameWindow, green,(220,350,100,50))
        button('START', 30, (0, 0, 255), 240, 365)

        #Quit Button Logic
        if quitButton.collidepoint(mous):
            click = mouse.get_pressed()
            if click[0] == 1:
                gameOver = True
        else:
            quitButton  = draw.rect(gameWindow, red,(380,350,100,50))
        button('QUIT', 30, (0, 0, 255), 405, 365)

        display.update()

def button(text, size, color, x, y):
    textFont = font.SysFont(None, size)
    textObj = textFont.render(text , True, color)
    textRect = textObj.get_rect()
    textRect.topleft = (x, y)
    gameWindow.blit(textObj, textRect)

LoadingScreen()
#

