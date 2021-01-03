import pygame, sys, keyboard, random, math
from pygame.locals import *

BLACK = (0,0,0)
WHITE = (255,255,255)

window_width = 800
window_height = 700
paddle_size = 150
paddle_offset = 20
paddle_thickness = 20
paddle_start_position = (window_height - paddle_size) /2

display_surf = pygame.display.set_mode((window_width,window_height))

#Main Function
def main():
    pygame.init()
    global display_surf
    display_surf = pygame.display.set_mode((window_width,window_height))
    pygame.display.set_caption('Pong')

#Draws the arena. 
def drawArena():
    display_surf.fill((0,0,0))
    #Draw center lines
    pygame.draw.line(display_surf, WHITE, ((window_width/2),0),((window_width/2),window_height),5)
    pygame.draw.line(display_surf, BLACK, ((window_width/2),0),((window_width/2),window_height),3)
    

class Paddle:
    def __init__(self, x, y, front):
        self.x = x
        self.y = y
        self.face = x + front
    
    def draw(self):
        pygame.draw.rect(display_surf, WHITE, (self.x,self.y,paddle_thickness,paddle_size),2)
    
    def move(self, key):
        if key == "w" and self.y > 0:
            self.y -=1
        elif key == "s" and self.y < window_height - paddle_size:
            self.y +=1

class Ball:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.radius = 10
        self.speed = 0.5
        self.direction = random.random()*math.pi*2
        while abs(math.pi/2 - self.direction)< math.pi/6 or abs(3*math.pi/2 - self.direction)< math.pi/6:
            self.direction = random.random()*math.pi*2
    
    def draw(self):
        pygame.draw.circle(display_surf, WHITE, (self.x,self.y), self.radius, 2)
    
    def move(self, paddle1, paddle2):
        if self.y >= window_height-self.radius or self.y <= self.radius:
            self.horizontal_bounce()
        if self.y == paddle1.y and self.x<paddle_thickness+paddle_offset and self.x > paddle_offset:
            self.horizontal_bounce
        if abs(self.x - paddle1.face) <= self.radius and abs(paddle1.y + paddle_size/2-self.y) <= paddle_size/2:
            self.vertical_bounce()
        if abs(paddle2.face-self.x) <= self.radius and abs(paddle2.y + paddle_size/2-self.y) <= paddle_size/2:
            self.vertical_bounce()
        self.x += math.cos(self.direction) * self.speed
        self.y -= math.sin(self.direction) * self.speed
    
    def horizontal_bounce(self):
        self.direction *=-1
        if self.speed < 3:
            self.speed += 0.05

    def vertical_bounce(self):
        self.direction = (math.pi-self.direction)
        if self.speed < 3:
            self.speed += 0.05

paddle1 = Paddle(paddle_offset, paddle_start_position,paddle_thickness)

paddle2 = Paddle(window_width-paddle_offset - paddle_thickness, paddle_start_position,0)

boll = Ball(window_width/2, window_height/2)

clock = pygame.time.Clock()

#Main Game Loop
while True:
    clock.tick()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keyboard.is_pressed('q'):
            pygame.quit()
            sys.exit()
    if keyboard.is_pressed('w'):
        paddle1.move("w")
    if keyboard.is_pressed('s'):
        paddle1.move("s")
    if keyboard.is_pressed('i'):
        paddle2.move("w")
    if keyboard.is_pressed('k'):
        paddle2.move("s")
    if (boll.x > window_width - boll.radius or boll.x <boll.radius):
        del(boll)
        boll = Ball(window_width/2, window_height/2);
    drawArena()
    paddle1.draw()
    paddle2.draw()
    time = clock.get_time()
    boll.move(paddle1,paddle2,time)
    print(time)
    boll.draw()

    pygame.time.delay(2)
    pygame.display.update()

if __name__=='__main__':
    main()
