'''
Created on 08.12.2014

@author: Matthias
'''
from OpenGL.GL import *
from utilities.vec2d import Vec2d
import pygame
import math
from math import ceil


class TireTrack(object):
    '''
    tracks that are made by tires if they wheelspin
    '''


    def __init__(self, start, end, tireWidth):
        '''
        Constructor
        '''
    
        self._start     = start
        self._length    = Vec2d(end - start).get_length()
        
        self._angle     = Vec2d(start - end).get_angle()
        
        self._width     = tireWidth
        self._color     = pygame.Color(60, 40, 30).normalize()
        
#         print "Length: %.2f" % self._length
        
    
    def render(self, proportion):
        
        pixelStart      = self._start * proportion
        pixelLength     = ceil(self._length * proportion)
        pixelWidth      = self._width * proportion
        
        glPushMatrix()
        glTranslatef(pixelStart.x, pixelStart.y, 0.0)
        glRotatef(self._angle, 0.0, 0.0, 1.0)
        
        glBegin(GL_QUADS)
        glColor4fv(self._color)
        glVertex3f(0.0, -pixelWidth/2.0, 0.0)
        glVertex3f(0.0, pixelWidth/2.0, 0.0)
        glVertex3f(pixelLength, pixelWidth/2.0, 0.0)
        glVertex3f(pixelLength, -pixelWidth/2.0, 0.0)
        glEnd()
        
        glPopMatrix()
        
        