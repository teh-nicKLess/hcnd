'''
Created on 24.06.2014

@author: teh_nicKLess
'''
from OpenGL.GL import *
from pygame.locals import *

import pygame

from car_v1 import Car

screenSize = 800, 600

carStartPos = 40, screenSize[1]/2
car = Car( carStartPos, 0, 0, pygame.Color(200,20,20).normalize())
# car = Car(Car.MAZDA, (220,20,20), carStartPos)

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
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    
    car.render()
    
    pygame.display.flip()

def main():
    video_flags = OPENGL | HWSURFACE | DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode(screenSize, video_flags)
    
    resize(screenSize)
    init()
    
    newTime = pygame.time.get_ticks()
    
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
            car.__init__(carStartPos, 0, 0, pygame.Color(200,20,20).normalize())
            
        if pressed[pygame.K_UP]:
            car.accelerate(deltaTime)
        
        if pressed[pygame.K_DOWN]:
            car.brake(deltaTime)
        
        if pressed[pygame.K_LEFT]:
            car.steer(deltaTime, Car.LEFT)
        elif pressed [pygame.K_RIGHT]:
            car.steer(deltaTime, Car.RIGHT)
        else:
            car.steer(deltaTime, Car.STRAIGHT)
        
               
            
            
        car.update(deltaTime)
        render()
        
if __name__ == '__main__':
    main()