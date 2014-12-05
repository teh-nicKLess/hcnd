'''
Created on 05.12.2014

@author: Matthias
'''
from OpenGL.GL import *
from pygame.locals import *

import pygame

from car_v2 import Car

screenSize  = 800, 600
proportion  = 1.0 / 0.067

carStartPos = 2, 10
car = Car(Car.MAZDA, (200,20,20), carStartPos)


def resize((width, height)):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-10.0, width + 10.0, height + 10.0, -10.0, -6.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity

def init():
    glClearColor(0.6, 0.6, 0.4, 0.0)
    
    
def render():
    global proportion
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    
    car.render(proportion)
    
    pygame.display.flip()

def main():
    global car, proportion
    video_flags = OPENGL | HWSURFACE | DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode(screenSize, video_flags)
    
    resize(screenSize)
    init()
    
    newTime = pygame.time.get_ticks()
    
    driveMode   = Car.ROLL
    steering    = Car.STRAIGHT
    
    playing = True
    while playing:
        oldTime = newTime
        newTime = pygame.time.get_ticks()
        deltaTime = (newTime - oldTime)/1000.0
        
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            playing = False 
                
        
        pressed = pygame.key.get_pressed() # a list of booleans for all keys
        
        if pressed[pygame.K_r]:
            car = Car(Car.MAZDA, (200,20,20), carStartPos)
            
        
        if pressed[pygame.K_DOWN]:
            driveMode = Car.BRAKE    
        elif pressed[pygame.K_UP]:
            driveMode = Car.ACCELERATE
        else:
            driveMode = Car.ROLL
        
        
        if pressed[pygame.K_LEFT]:
            steering = Car.LEFT
        elif pressed [pygame.K_RIGHT]:
            steering = Car.RIGHT
        else:
            steering = Car.STRAIGHT
        
        if pressed[K_z]:
            pass
        
        car.update(proportion, driveMode, steering, 12.8, deltaTime)
        render()
        
if __name__ == '__main__':
    main()