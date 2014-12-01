'''
Created on 27.06.2014

@author: Matthias
'''
from OpenGL.GL import *
from pygame.locals import *
    
import pygame
import math

class Car(object):
    '''
    represents a car with all essential parts.
    What did YOU think this is?!
    '''
    
    LEFT     = -1
    RIGHT    = 1
    STRAIGHT = 0

    def __init__(self, pos, horsePower, weight, color):
        '''
        Constructor
        '''
        
        
        self._horsePower   = horsePower
        self._weight       = weight
        self._color        = color
        
        self._posX         = pos[0]
        self._posY         = pos[1]
        self._speed        = 0.0
        self._heading      = 0.0 #direction in radians
        self._steerAngle   = 0.0
        
        self._width          = 20
        self._length         = 50
        self._wheelBase      = 40
    
    # power between 0.0 and 1.0    
    def accelerate(self, timeSlice, power=1.0):
        #TODO: acceleration depending on horsePower, weight and time of use (timeSlice).
        # return resulting speed.
        self._speed = self._speed + timeSlice*power*10
        
    def brake(self, timeSlice):
        #TODO: depends on time and weight...
        self._speed = self._speed - timeSlice*20
        if (self._speed < 0.0):
            self._speed = 0.0
            
    def steer(self, timeSlice, direction):
        self._steerAngle += direction*timeSlice*math.pi/4.0
        if self._steerAngle > math.pi/4.0:
            self._steerAngle = math.pi/4.0
        if direction == 0:
            self._steerAngle = 0
            
    def update(self, timeSlice):
        
        
#         frontWheel = self._pos + self._wheelBase/2 * ( math.cos(self._heading) , math.sin(self._heading) )
#         backWheel = self._pos - self._wheelBase/2 * ( math.cos(self._heading) , math.sin(self._heading) )

        frontWheelX = self._posX + self._wheelBase/2 * math.cos(self._heading)
        frontWheelY = self._posY + self._wheelBase/2 * math.sin(self._heading)
        backWheelX  = self._posX - self._wheelBase/2 * math.cos(self._heading)
        backWheelY  = self._posY - self._wheelBase/2 * math.sin(self._heading)  
        
#         backWheel += self._speed * timeSlice * (math.cos(self._heading) , math.sin(self._heading))
#         frontWheel += self._speed * timeSlice * (math.cos(self._heading+self._steerAngle) , math.sin(self._heading+self._steerAngle))

        backWheelX  += self._speed * timeSlice * math.cos(self._heading)
        backWheelY  += self._speed * timeSlice * math.sin(self._heading)
        frontWheelX += self._speed * timeSlice * math.cos(self._heading+self._steerAngle)
        frontWheelY += self._speed * timeSlice * math.sin(self._heading+self._steerAngle)
        
        self._posX = (frontWheelX + backWheelX) / 2.0
        self._posY = (frontWheelY + backWheelY) / 2.0
        self._heading = math.atan2( frontWheelY - backWheelY , frontWheelX - backWheelX )
        
        
#         self.pos[0] = self._pos[0] + math.sin(self._carHeading)*self._speed
#         self._pos[1] = self._pos[1] + math.cos(self._carHeading)*self._speed
    
    def render(self):
        #TODO: fix this...
        glPushMatrix()
        glTranslatef(self._posX, self._posY, 0.0)
        glRotatef(math.degrees(self._heading),0.0, 1.0, 0.0)
        
#         backPosX  = self._posX - self._length / 2 * math.cos(self._heading)
#         frontPosX = self._posX + self._length / 2 * math.cos(self._heading)
#         leftPosY  = self._posY - self._width / 2 * math.cos(self._heading)
#         rightPosY = self._posY + self._width / 2 * math.cos(self._heading)
#         print backPosX, frontPosX, leftPosY, rightPosY
        glBegin(GL_TRIANGLE_STRIP)
        glColor4fv(self._color)
        glVertex3f(self._length/2, -self._width/2, 0.0)
        glVertex3f(-self._length/2, -self._width/2, 0.0)
        glVertex3f(self._length/2, self._width/2, 0.0)
        glVertex3f(-self._length/2, self._width/2, 0.0)
        glEnd()
        
        glPopMatrix()