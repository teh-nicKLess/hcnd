'''
Created on 03.12.2014

@author: Matthias
'''
from OpenGL.GL import *
from pygame.locals import *
from utilities.vec2d import Vec2d

import pygame
import math

class Car(object):
    ''''
    represents a car with all essential parts.
    What did YOU think this is?!
    
    Differences to v1:
    Movement is now based on physical forces rather than magic numbers.
    '''
    
    LEFT     = -1
    RIGHT    = 1
    STRAIGHT = 0
    
    #MODEL = (enginePower in kW, length in mm, width in mm, weight in kg)
    #Used proportion px:mm : 1:67
    MAZDA = (93, 4020, 1720, 1300)
    
    proportion = 1.0/67.0


    def __init__(self, model, color, startPos):
        '''
        Constructor
        '''
        self._enginePower   = model[0]
        self._length        = model[1]*self.proportion
        self._width         = model[2]*self.proportion
        self._weight        = model[3]
        self._color         = pygame.Color(color[0], color[1], color[2]).normalize()
        
        self._wheelBase      = abs(self._length*0.6)
        self._tireLenght     = abs(self._length/400.0)
        self._tireWidth      = abs(self._tireLenght/2.0)
        
        self._pos = Vec2d(startPos)
        
        self._velocity      = Vec2d(0.0, 0.0)
        self._speed         = 0.0 # == self._velocity.get_length()
        self._heading       = Vec2d(0.0, 0.0) # == self._velocity.normalized()
        self._steerAngle    = 0.0
        
        
      
    def physics(self, constDrag, constRollResist, deltaTime):
        #constDrag: aerodynamic drag
        #constRollResist: rolling resistance approx. 30 * constDrag
        forceTraction   = self._heading * self._enginePower
        forceDrag       = -constDrag * self._velocity * self._velocity.get_length()
        forceRollResist = -constRollResist * self._velocity
        forceLongitude  = forceTraction + forceDrag + forceRollResist
        
        acceleration    = forceLongitude / self._weight #not final, takes only longitude force
        
        self._velocity  = self._velocity + deltaTime*acceleration
        self._pos      = self._pos + deltaTime*self._velocity
    
    def steer(self, timeSlice, direction):
        #steering left/right
        self._steerAngle += direction*timeSlice*math.pi/5.0*1.5
        if self._steerAngle > math.pi/5.0:
            self._steerAngle = math.pi/5.0
        elif self._steerAngle < -math.pi/5.0:
            self._steerAngle = -math.pi/5.0
        
        # straightening wheels
        if direction == 0:
            if self._steerAngle > 0.0:
                self._steerAngle -= timeSlice*math.pi/5.0
                if self._steerAngle < 0.0:
                    self._steerAngle = 0
            elif self._steerAngle < 0.0:
                self._steerAngle += timeSlice*math.pi/5.0
                if self._steerAngle > 0.0:
                    self._steerAngle = 0
                    
                    
    def update(self, timeSlice):
        
        # Calculates current position of wheels depending on position and orientation
        # of the car
        frontWheelX = self._pos.x + self._wheelBase/2 * math.cos(self._heading.angle)
        frontWheelY = self._pos.y + self._wheelBase/2 * math.sin(self._heading.angle)
        backWheelX  = self._pos.x - self._wheelBase/2 * math.cos(self._heading.angle)
        backWheelY  = self._pos.y - self._wheelBase/2 * math.sin(self._heading.angle)  
        
        # Calculates the value by which the position of the wheels change based on
        # speed, orientation and current steering angle of the car
        backWheelX  += self._speed * timeSlice * math.cos(self._heading.angle)
        backWheelY  += self._speed * timeSlice * math.sin(self._heading.angle)
        frontWheelX += self._speed * timeSlice * math.cos(self._heading.angle+self._steerAngle)
        frontWheelY += self._speed * timeSlice * math.sin(self._heading.angle+self._steerAngle)
        
        # Calculates the resulting new position of the car by calculating the center 
        # between front and back wheel. Also updates the direction of the car.
        self._pos.x = (frontWheelX + backWheelX) / 2.0
        self._pos.y = (frontWheelY + backWheelY) / 2.0
#         self._heading = Vec2d(frontWheelY - backWheelY, frontWheelX - backWheelX).normalized()
        
        print "Heading: ", self._heading
        print "Heading angle: ", self._heading.angle
        print "FrontWheelY - BackWheelY: ",frontWheelY - backWheelY
        print "FrontWheelX - BackWheelX: ",frontWheelX - backWheelX
        
    def render(self):
        
        # transform to coordinates of the car
        glPushMatrix()
        glTranslatef(self._pos.x, self._pos.y, 0.0)
        glRotatef(self._heading.angle,0.0, 0.0, 1.0)
        
        #draw the back wheels
        glBegin(GL_QUADS)
        glColor3f(60.0/255, 40.0/255, 30.0/255)
        glVertex3f(-self._wheelBase/2-self._tireLenght/2.0, -self._width/2-self._tireWidth*0.4, 0.0)
        glVertex3f(-self._wheelBase/2+self._tireLenght/2.0, -self._width/2-self._tireWidth*0.4, 0.0)
        glVertex3f(-self._wheelBase/2+self._tireLenght/2.0, -self._width/2+self._tireWidth*0.6, 0.0)
        glVertex3f(-self._wheelBase/2-self._tireLenght/2.0, -self._width/2+self._tireWidth*0.6, 0.0)
        
        glVertex3f(-self._wheelBase/2-self._tireLenght/2.0, self._width/2+self._tireWidth*0.4, 0.0)
        glVertex3f(-self._wheelBase/2+self._tireLenght/2.0, self._width/2+self._tireWidth*0.4, 0.0)
        glVertex3f(-self._wheelBase/2+self._tireLenght/2.0, self._width/2-self._tireWidth*0.6, 0.0)
        glVertex3f(-self._wheelBase/2-self._tireLenght/2.0, self._width/2-self._tireWidth*0.6, 0.0)
        glEnd()
        
        #transform to coordinates of front left wheel
        glPushMatrix()
        glTranslatef(self._wheelBase/2, -self._width/2, 0.0)
        glRotatef(math.degrees(self._steerAngle), 0.0, 0.0, 1.0)
        
        #draw front left wheel
        glBegin(GL_QUADS)
        glVertex3f(-self._tireLenght/2, -self._tireWidth*0.4, 0.0)
        glVertex3f( self._tireLenght/2, -self._tireWidth*0.4, 0.0)
        glVertex3f( self._tireLenght/2,  self._tireWidth*0.6, 0.0)
        glVertex3f(-self._tireLenght/2,  self._tireWidth*0.6, 0.0)
        glEnd()
        
        glPopMatrix()
        
        #transform to coordinates of front right wheel
        glPushMatrix()
        glTranslatef(self._wheelBase/2, self._width/2, 0.0)
        glRotatef(math.degrees(self._steerAngle), 0.0, 0.0, 1.0)
        
        #draw front right wheel
        glBegin(GL_QUADS)
        glVertex3f(-self._tireLenght/2,  self._tireWidth*0.4, 0.0)
        glVertex3f( self._tireLenght/2,  self._tireWidth*0.4, 0.0)
        glVertex3f( self._tireLenght/2, -self._tireWidth*0.6, 0.0)
        glVertex3f(-self._tireLenght/2, -self._tireWidth*0.6, 0.0)
        glEnd()
         
        glPopMatrix()
        
        
        #draw the car body  
        glBegin(GL_TRIANGLE_FAN)
        glColor4fv(self._color)
        glVertex3f(0.0, 0.0, 0.0)
        #rear left
        glVertex3f(-self._length/2+3, -self._width/2, 0.0)
        glVertex3f(-self._length/2+1, -self._width/2+1, 0.0)
        glVertex3f(-self._length/2, -self._width/2+5, 0.0)
        
        #rear right
        glVertex3f(-self._length/2, self._width/2-5, 0.0)
        glVertex3f(-self._length/2+1, self._width/2-1, 0.0)
        glVertex3f(-self._length/2+3, self._width/2, 0.0)
        
        #front right
        glVertex3f(self._length/2-6, self._width/2, 0.0)
        glVertex3f(self._length/2-2, self._width/2-1, 0.0)
        glVertex3f(self._length/2, self._width/2-4, 0.0)
        
        #front left
        glVertex3f(self._length/2, -self._width/2+4, 0.0)
        glVertex3f(self._length/2-2, -self._width/2+1, 0.0)
        glVertex3f(self._length/2-6, -self._width/2, 0.0)
        glVertex3f(-self._length/2+3, -self._width/2, 0.0)
        
        glEnd()
        
        #draw details
        
        #side mirrors
        glBegin(GL_QUADS)
        glVertex3f(7, -self._width/2, 0.0)
        glVertex3f(9, -self._width/2, 0.0)
        glVertex3f(7, -self._width/2-2, 0.0)
        glVertex3f(6, -self._width/2-2, 0.0)
        
        glVertex3f(6, self._width/2+2, 0.0)
        glVertex3f(7, self._width/2+2, 0.0)
        glVertex3f(9, self._width/2, 0.0)
        glVertex3f(7, self._width/2, 0.0)
        glEnd()
        
        #hood lines
        glBegin(GL_LINES)
        glColor4fv(pygame.Color(120,20,20).normalize())
        glVertex3f(10, -self._width/2+1 , 0.0)
        glVertex3f(self._length/2-4, -self._width/2+2 , 0.0)
        
        glVertex3f(10, self._width/2-1 , 0.0)
        glVertex3f(self._length/2-4, self._width/2-2 , 0.0)
        glEnd()
        
        #trunk lines
        glBegin(GL_LINE_STRIP)
        glVertex3f(-self._length/2+1, -self._width/2+4, 0.0)
        glVertex3f(-self._length/2+7, -self._width/2+4, 0.0)
        glVertex3f(-self._length/2+9, -self._width/2+7, 0.0)
        glVertex3f(-self._length/2+9, self._width/2-7, 0.0)
        glVertex3f(-self._length/2+7, self._width/2-4, 0.0)
        glVertex3f(-self._length/2+1, self._width/2-4, 0.0)
        glEnd()
         
        #spoiler
        glBegin(GL_QUADS)
        glColor4fv(pygame.Color(240,50,50).normalize())
        glVertex3f(-self._length/2, -self._width/2+4, 0.0)
        glVertex3f(-self._length/2, self._width/2-4, 0.0)
        glVertex3f(-self._length/2+3, self._width/2-6, 0.0)
        glVertex3f(-self._length/2+3, -self._width/2+6, 0.0)
        glEnd()
        
        
        #draw the wind shield
        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(110.0/255, 140.0/255, 150.0/255)
        glVertex3f(9 , -self._width/2+1 , 0.0)
        glVertex3f(0 , -self._width/2+4 , 0.0)
        glVertex3f(11, -self._width/2+8 , 0.0)
        glVertex3f(2 , -self._width/2+10, 0.0)
        glVertex3f(11,  self._width/2-8 , 0.0)
        glVertex3f(2 ,  self._width/2-10, 0.0)
        glVertex3f(9 ,  self._width/2-1 , 0.0)
        glVertex3f(0 ,  self._width/2-4 , 0.0)
        glEnd()
        
        #draw the side windows
        #left window
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(6 , -self._width/2+1 , 0.0)
        glVertex3f(-2, -self._width/2+4 , 0.0)
        glVertex3f(-9, -self._width/2+1 , 0.0)
        glVertex3f(-11, -self._width/2+4 , 0.0)
        glEnd()
        
        #right window
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(6 , self._width/2-1 , 0.0)
        glVertex3f(-2, self._width/2-4 , 0.0)
        glVertex3f(-9, self._width/2-1 , 0.0)
        glVertex3f(-11, self._width/2-4 , 0.0)
        glEnd()
        
        #draw the folding top
        #upper part
        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(0.1,0.1,0.1)
        glVertex3f(-1, -self._width/2+4 , 0.0)
        glVertex3f(1 , -self._width/2+10, 0.0)
        glVertex3f(-11, -self._width/2+4, 0.0)
        glVertex3f(1 ,  self._width/2-10, 0.0)
        glVertex3f(-11, self._width/2-4 , 0.0)
        glVertex3f(-1 , self._width/2-4 , 0.0)
        glEnd()
        
        #rear part
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(-9,  -self._width/2+1 , 0.0)
        glVertex3f(-11, -self._width/2+4 , 0.0)
        glVertex3f(-18, -self._width/2+3 , 0.0)
        glVertex3f(-11,  self._width/2-4 , 0.0)
        glVertex3f(-18,  self._width/2-3 , 0.0)
        glVertex3f(-9,   self._width/2-1 , 0.0)
        glEnd()
        
        #draw the rear window
        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(70.0/255, 90.0/255, 100.0/255)
        glVertex3f(-13, -self._width/2+9 , 0.0)
        glVertex3f(-16, -self._width/2+8 , 0.0)
        glVertex3f(-13,  self._width/2-9 , 0.0)
        glVertex3f(-16,  self._width/2-8 , 0.0)
        glEnd()
        
        #draw headlamps
        glBegin(GL_TRIANGLE_STRIP)
        glColor4fv(pygame.Color(240,240,180).normalize())
        glVertex3f(self._length/2-3, -self._width/2+2, 0.0)
        glVertex3f(self._length/2-2, -self._width/2+2, 0.0)
        glVertex3f(self._length/2, -self._width/2+4, 0.0)
        glVertex3f(self._length/2-2, -self._width/2+6, 0.0)
        glVertex3f(self._length/2, -self._width/2+7, 0.0)
        glEnd()
        
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(self._length/2-3, self._width/2-2, 0.0)
        glVertex3f(self._length/2-2, self._width/2-2, 0.0)
        glVertex3f(self._length/2, self._width/2-4, 0.0)
        glVertex3f(self._length/2-2, self._width/2-6, 0.0)
        glVertex3f(self._length/2, self._width/2-7, 0.0)
        glEnd()
        
        glPopMatrix()