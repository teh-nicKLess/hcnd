'''
Created on 24.06.2014

@author: teh_nicKLess
'''
from OpenGL.GL import *
from pygame.locals import *

import pygame

from Car import Car

screenSize = 800, 600

carStartPos = screenSize[0]/2, screenSize[1]/2
car = Car( carStartPos, 0, 0, pygame.Color(255,0,0).normalize())

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
    glClearColor(0.0, 0.0, 0.0, 0.0)
    
    
def render():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    
    
    glBegin(GL_LINES)
    glColor3f(1.0, 1.0, 0.0)
    glVertex3f(1.0, 0.0, 0.0)
    glVertex3f(1.0, 20.0, 0.0)
    glEnd()
    
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
        timeSlice = (newTime - oldTime)/1000.0
        
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            playing = False 
                
        pressed = pygame.key.get_pressed() # a list of booleans for all keys
            
        if pressed[pygame.K_UP]:
            car.accelerate(timeSlice)
        
        if pressed[pygame.K_DOWN]:
            car.brake(timeSlice)
        
        if pressed[pygame.K_LEFT]:
            car.steer(timeSlice, Car.LEFT)
        elif pressed [pygame.K_RIGHT]:
            car.steer(timeSlice, Car.RIGHT)
        else:
            car.steer(timeSlice, Car.STRAIGHT)
        
               
            
            
        car.update(timeSlice)
        render()
        
if __name__ == '__main__':
    main()