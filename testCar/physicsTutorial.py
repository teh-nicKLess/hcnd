'''
Created on 01.07.2014

@author: Matthias
'''
from OpenGL.GL import *
from pygame.locals import *

import pygame

screenSize = 800, 600

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
    
    pygame.display.flip()

def main():
    video_flags = OPENGL | HWSURFACE | DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode(screenSize, video_flags)
    
    resize(screenSize)
    init()
    
    while True:
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            break
        
        render()
        


if __name__ == '__main__':
    main()