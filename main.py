import pygame
import time
import random

class Window:
    def __init__(self):
        self.background_colour = (255,255,255)
        (width, height) = (1080, 720)
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Hugh's Game")

    def draw(self):
        pygame.display.flip()
        self.screen.fill(self.background_colour)

class Player:
    def __init__(self):
        self.x = 1080/2
        self.y = 720/3
        self.xvel = 0
        self.yvel = 0
        self.xacc = 0.8
        self.width = 50
        self.height = 100

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.colour = (50, 50, 255)

        self.keypressedUD = False
        self.keypressedLR = False

    def draw(self, window):
        pygame.draw.rect(window.screen, self.colour, self.rect)

    def update(self):
        self.keyboardInput()

        if not self.keypressedLR:
            if self.xvel > 0.8:
                self.xvel -= 0.8
            elif self.xvel < -0.8:
                self.xvel += 0.8
            else:
                self.xvel = 0

        if not self.keypressedUD:
            if self.yvel > 0.8:
                self.yvel -= 0.8
            elif self.yvel < -0.8:
                self.yvel += 0.8
            else:
                self.yvel = 0

        if self.xvel > 15:
            self.xvel = 15
        elif self.xvel < -15:
            self.xvel = -15

        if self.yvel > 15:
            self.yvel = 15
        elif self.yvel < -15:
            self.yvel = -15

        if self.x < 0:
            self.xvel = 0
            self.x = 0
        elif self.x + self.width > 1080:
            self.xvel = 0
            self.x = 1080 - self.width

        if self.y < 0:
            self.yvel = 0
            self.y = 0
        elif self.y + self.height > 720:
            self.yvel = 0
            self.y = 720 - self.height

        self.y += self.yvel
        self.x += self.xvel

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def keyboardInput(self):
        keys = pygame.key.get_pressed()
        xinput = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * self.xacc
        yinput = (keys[pygame.K_UP] - keys[pygame.K_DOWN]) * -self.xacc

        if xinput == 0:
            self.keypressedLR = False
        else:
            self.xvel += xinput
            self.keypressedLR = True

        if yinput == 0:
            self.keypressedUD = False
        else:
            self.yvel += yinput
            self.keypressedUD = True

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 80
        self.colour = (175, 100, 50)

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.xvel = 5
    
    def draw(self, window):
        pygame.draw.rect(window.screen, self.colour, self.rect)

    def update(self):
        self.x -= self.xvel
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 10
        self.size = 8
        self.colour = (0, 0, 0)
    
    def draw(self, window):
        pygame.draw.circle(window.screen, self.colour, (self.x, self.y), self.size)

    def update(self):
        self.x += 10

if __name__ == "__main__":
    window = Window()
    player = Player()
    enemies = []
    bullets = []

    numberOfEnemies = 10
    
    for i in range(10):
        enemies.append(Enemy(1080 + 400 * i, random.randint(0,650)))
    
    running = True

    enemyTimer = time.time() * 1000

    score = 0


    while running:
        timea = time.time() * 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(player.x + 20 , player.y + 20))


        player.update()

        if timea - enemyTimer > 5 * 1000:
            enemyTimer = timea
            numberOfEnemies += 1   

        for e in enemies:
            for b in bullets:
                if b.x > e.x and b.x < e.x + e.width and b.y > e.y and b.y < e.y + e.height:
                    enemies.remove(e)
                    bullets.remove(b)
                    score += 1  
                    print(score)
                     
            if e.x + e.width < 0:
                enemies.remove(e)

            if e.rect.colliderect(player.rect):
                running = False

            e.update()
            e.draw(window)

        if len(enemies) < numberOfEnemies:
            enemies.append(Enemy(1080 + 400, random.randint(0,650)))

        for b in bullets:
            if b.x > 1080:
                bullets.remove(b)
            b.update()
            b.draw(window)

        player.draw(window)
        window.draw()
        
        while time.time() * 1000 - timea < 16:
            pass
            