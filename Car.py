'''
Created on 27.06.2014

@author: Matthias
'''
from OpenGL.GL import *
from pygame.locals import *
    
import pygame

class Car(object):
    '''
    represents a car with all essential parts.
    What did YOU think this is?!
    '''

    def __init__(self, xPos, yPos, horsePower, weight, color):
        '''
        Constructor
        '''
        
        self.__xPos         = xPos
        self.__yPos         = yPos
        self.__horsePower   = horsePower
        self.__weight       = weight
        self.__color        = color
        self.__speed        = 0.0
        self.__direction    = 0.0 #direction in degrees
        
        self.width          = 20
        self.length         = 50
    
    # power between 0.0 and 1.0    
    def accelerate(self, timeSlice, power=1.0):
        #TODO: acceleration depending on horsePower, weight and time of use (timeSlice).
        # return resulting speed.
        pass
        
    def brake(self, timeSlice):
        #TODO: depends on time and weight...
        pass
    
    def render(self):
        glBegin(GL_QUADS)
        glColor4fv(self.__color)
        glVertex3f(self.__xPos - self.width/2, self.__yPos - self.length / 2, 0.0)
        glVertex3f(self.__xPos + self.width/2, self.__yPos - self.length / 2, 0.0)
        glVertex3f(self.__xPos + self.width/2, self.__yPos + self.length / 2, 0.0)
        glVertex3f(self.__xPos - self.width/2, self.__yPos + self.length / 2, 0.0)
        glEnd()