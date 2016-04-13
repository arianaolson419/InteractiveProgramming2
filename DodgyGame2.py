import pygame
from pygame.locals import QUIT
import time
from random import *
import cv2
import numpy as np


class SkyModel(object):
    '''Represents the game state for Dodgy Game'''

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.BIRD_Y = 0
        self.USER_X = 250
        self.RADIUS = 10
        self.bird = Bird(randint(0, 1000), self.BIRD_Y, self.RADIUS)
        self.bird2 = Bird(randint(600, 1000), self.BIRD_Y - 500, self.RADIUS-9)
        self.user = User(self.USER_X, 1000, 140)
        self.heart = Heart()

    def update(self):
        '''Update the model state'''
        self.bird.update()
        self.bird2.update()
   


class View(object):
    """ Provides a view of the Dodgy Game model in a pygame
        window """

    def __init__(self, model, size):
        """ Initialize with the specified model """
        self.model = model
        self.screen = pygame.display.set_mode(size)
        self.end = pygame.transform.scale(pygame.image.load('gameover.png'), (1000,1000))
        self.eyes = pygame.transform.scale(
            pygame.image.load('eyes.png'), (self.model.user.radius, self.model.user.radius))
        self.life = pygame.transform.scale(pygame.image.load('red-heart.png'), 
            (self.model.heart.width/(self.model.heart.count+1),
                self.model.heart.height/2))

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
        
        pygame.draw.rect(self.screen, pygame.Color('white'), (self.model.heart.left, self.model.heart.top, self.model.heart.width, self.model.heart.height))
        self.screen.blit(self.life, (self.model.heart.left+self.model.heart.width/(self.model.heart.count+1), self.model.heart.top + 
                self.model.heart.height/2))


        if (self.model.bird.center_x + self.model.bird.radius >= self.model.user.center_x - self.model.user.radius)  and \
                (self.model.bird.center_y + self.model.bird.radius >= self.model.user.center_y - (self.model.user.radius - 20)) and \
                (self.model.bird.center_x - self.model.bird.radius <= self.model.user.center_x + self.model.user.radius - 20 )  and \
                (self.model.bird.center_y + self.model.bird.radius >= self.model.user.center_y - (self.model.user.radius - 20)):
            # determining if a collision happened
            self.screen.blit(self.end, (0, 0))

        if (self.model.bird2.center_x + self.model.bird2.radius >= self.model.user.center_x - self.model.user.radius)  and \
                (self.model.bird2.center_y + self.model.bird2.radius >= self.model.user.center_y - (self.model.user.radius - 20)) and \
                (self.model.bird2.center_x - self.model.bird2.radius <= self.model.user.center_x + self.model.user.radius - 20 )  and \
                (self.model.bird2.center_y + self.model.bird2.radius >= self.model.user.center_y - (self.model.user.radius - 20)):
            # determining if a collision happened
            self.screen.blit(self.end, (0, 0))
        pygame.display.update()


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

    def __init__(self, left = 10, top = 10, width = 50, height = 30, count = 3):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.count = count

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
    running = True
    
    while running:
        ret, frame = movement.cap.read()
        faces = movement.face_cascade.detectMultiScale(
            frame, scaleFactor=1.2, minSize=(20, 20))
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            else:
                movement.handle_event(event)
        model.update()
        
        view.draw()
        time.sleep(.01)
    movement.cap.release()
    cv2.destroyAllWindows()
