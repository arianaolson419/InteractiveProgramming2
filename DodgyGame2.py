import pygame
from pygame.locals import QUIT
import time
from random import *
import cv2
import numpy as np

class View(object):
    """ Provides a view of the Dodgy Game model in a pygame
        window """

    def __init__(self, model, size):
        """ Initialize with the specified model """
        self.model = model
        self.size = size
        self.screen = pygame.display.set_mode(size)
        self.end = pygame.transform.scale(pygame.image.load('gameover.png'), (1000,1000))
        self.eyes = pygame.transform.scale(
            pygame.image.load('eyes.png'), (self.model.user.radius, self.model.user.radius))
        self.lives = 3
        
    def draw_button(self):
        self.screen.fill(pygame.Color(135, 206, 250))
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        coords = pygame.Rect(self.model.button.x, self.model.button.y, self.model.button.w, self.model.button.h)
        ac = pygame.Color('white')
        ic = pygame.Color('yellow')

        if self.model.button.x+self.model.button.w > mouse[0] > self.model.button.x and self.model.button.y + self.model.button.h > mouse[1] > self.model.button.y:
            pygame.draw.rect(self.screen, ac, coords)

        else: 
            pygame.draw.rect(self.screen, ic, coords)

        font = pygame.font.SysFont("monospace", 140)
        label = font.render(self.model.button.msg, 1, (135, 206, 255))
        text_pos = label.get_rect()
        text_pos.centerx = coords.centerx
        text_pos.centery = coords.centery
        
        self.screen.blit(label, (text_pos[0], text_pos[1]))
        pygame.display.update()
    def draw(self):
        """ Draw the game to the pygame window """
        self.screen.fill(pygame.Color(135, 206, 250))  # sky

        pygame.draw.circle(self.screen,  # 'bird'
                           self.model.bird.color,
                           (self.model.bird.center_x,
                            self.model.bird.center_y),
                           self.model.bird.radius)
        self.ostrich = pygame.transform.scale(pygame.image.load(
            'ostrich.png'), (self.model.bird.radius * 2, self.model.bird.radius * 2))
        self.screen.blit(self.ostrich, (self.model.bird.center_x -
                                        self.model.bird.radius, self.model.bird.center_y - self.model.bird.radius))
        pygame.draw.circle(self.screen,  # 'bird'
                           self.model.bird2.color,
                           (self.model.bird2.center_x,
                            self.model.bird2.center_y),
                           self.model.bird2.radius)
        self.ostrich = pygame.transform.scale(pygame.image.load(
            'ostrich.png'), (self.model.bird2.radius * 2, self.model.bird2.radius * 2))
        self.screen.blit(self.ostrich, (self.model.bird2.center_x -
                                        self.model.bird2.radius, self.model.bird2.center_y - self.model.bird2.radius))

        pygame.draw.circle(self.screen,  # player
                           pygame.Color('white'),
                           (self.model.user.center_x,
                            self.model.user.center_y),
                           self.model.user.radius)
        self.screen.blit(
            self.eyes, (self.model.user.center_x - 70, self.model.user.center_y - 140))



        if (self.model.bird.center_x + self.model.bird.radius >= self.model.user.center_x - self.model.user.radius)  and \
                (self.model.bird.center_y + self.model.bird.radius >= self.model.user.center_y - (self.model.user.radius - 20)) and \
                (self.model.bird.center_x - self.model.bird.radius <= self.model.user.center_x + self.model.user.radius - 20 )  and \
                (self.model.bird.center_y + self.model.bird.radius >= self.model.user.center_y - (self.model.user.radius - 20)):
            
            self.model.bird.center_y = self.size[1]+1
            self.lives -= 1
            

        if (self.model.bird2.center_x + self.model.bird2.radius >= self.model.user.center_x - self.model.user.radius)  and \
                (self.model.bird2.center_y + self.model.bird2.radius >= self.model.user.center_y - (self.model.user.radius - 20)) and \
                (self.model.bird2.center_x - self.model.bird2.radius <= self.model.user.center_x + self.model.user.radius - 20 )  and \
                (self.model.bird2.center_y + self.model.bird2.radius >= self.model.user.center_y - (self.model.user.radius - 20)):
            
            self.model.bird2.center_y = self.size[1]+1
            self.lives -= 1  


        for heart in self.model.hearts[0:self.lives]:
            h = pygame.transform.scale(
                pygame.image.load('heart.png'), (heart.width, heart.height))
            self.screen.blit(h, (heart.left, heart.top))

        pygame.display.update()
    def gameover(self):
        self.screen.blit(self.end, (0, 0))
        pygame.display.update()

class SkyModel(object):
    '''Represents the game state for Dodgy Game'''

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.BIRD_Y = 0
        self.USER_X = 250
        self.RADIUS = 10
        self.HEART_WIDTH = 100
        self.HEART_HEIGHT = 100
        self.MARGIN = 20
        self.bird = Bird(randint(0, 1000), self.BIRD_Y, self.RADIUS)
        self.bird2 = Bird(randint(600, 1000), self.BIRD_Y - 500, self.RADIUS-9)
        self.user = User(self.USER_X, 1000, 140)
        self.button = Button('START', self.width, self.height)
        
        self.hearts = []
        for left in range(self.MARGIN, 3*(self.MARGIN+self.HEART_WIDTH),self.MARGIN+self.HEART_WIDTH):
            self.hearts.append(Heart(left, self.MARGIN, self.HEART_WIDTH, self.HEART_HEIGHT)) 


    def update(self):
        '''Update the model state'''
        self.bird.update()
        self.bird2.update()

class Button(object):
    '''represents the initial screen with a start button'''
    def __init__(self, msg, screenw, screenh, w = 500, h = 300): #left is (screen width - button width)/2 similar for top
        self.msg = msg
        self.x = (screenw-w)/2
        self.y = (screenh-h)/2
        self.w = w
        self.h = h

class Bird(object):
    """ Represents a bird in dodging game """

    def __init__(self, center_x, center_y, radius, color=pygame.Color('yellow')):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.growth = 2  # rate that the bird gets bigger as it gets 'closer'
        self.color = color

    def update(self):
        """ Update the position of the ball due to time passing """
        self.radius += self.growth

        if self.center_y < 1000:
            # if the bird has not reached the bottom of the screen
            self.center_y += 35

        else:
            # restart position at top of screen
            self.center_y = 0
            self.radius = 20
            self.center_x = randint(0, 500)


class User(object):
    """ Represents the user in my dodging game """

    def __init__(self, center_x, center_y, radius):
        """ Create a ball object with the specified geometry """
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius

class Heart(object):
    '''represents the number of lives that the user has left. The player always starts with 3 lives'''

    def __init__(self, left, top , width, height):
        self.left = left
        self.top = top
        self.width = width
        self.height = height

class Movement(object):
    def __init__(self, model):
        self.model = model
        self.MOVE = pygame.USEREVENT + 1
        move_event = pygame.event.Event(self.MOVE)
        # this event occurs every millisecond
        pygame.time.set_timer(self.MOVE, 1)
        self.cap = cv2.VideoCapture(0)
        self.face_cascade = cv2.CascadeClassifier(
            '/home/arianaolson/haarcascade_frontalface_alt.xml')

    def handle_event(self, event):
        '''uses the position of player's face to control the user'''
        for (x, y, w, h) in faces:
            if x > 0 and x < 1000-160:
                self.model.user.center_x = 1000 - (2 * x)





if __name__ == '__main__':
    pygame.init()
    size = (1000, 1000)

    model = SkyModel(size[0], size[1])
    view = View(model, size)
    movement = Movement(model)

    screen_on = True
    while screen_on:
        starting = True
        while starting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    starting = False
                    running = False
                    screen_on = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    starting = False
                    running = True
            view.draw_button()
            time.sleep(.01)
                    
        while running:
            ret, frame = movement.cap.read()
            faces = movement.face_cascade.detectMultiScale(
                frame, scaleFactor=1.2, minSize=(20, 20))
            for event in pygame.event.get():
                if event.type == QUIT:
                    ending = False
                    running = False
                    screen_on = False
                else:
                    movement.handle_event(event)
                    if view.lives == 0:
                        ending = True
                        running = False

            model.update()
            
            view.draw()
            time.sleep(.01)

        while ending:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen_on = False
                    ending = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    starting = True
                    ending = False

            view.gameover()
            time.sleep(.01)
    movement.cap.release()
    cv2.destroyAllWindows()
