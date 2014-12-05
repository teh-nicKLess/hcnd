'''
Created on 27.06.2014

@author: Matthias Jaenicke

@source: Steering: http://engineeringdotnet.blogspot.de/2010/04/simple-2d-car-physics-in-games.html
@source: Car physics: http://www.asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html
'''
from OpenGL.GL import *
from pygame.locals import *
from utilities.vec2d import Vec2d
    
import pygame
import math

class Car(object):
    '''
    represents a car with all essential parts.
    What did YOU think this is?!
    '''
    
    '''
    Mazda MX5
    Length:         570px
    Width:          247px
    Position Wheels: front 60 px, back 75 px
    Wheels Length: 95px
    wind shield position: 175px from front (18,4)
    wind shield length: 100px (10,5)
    folding top length: 170px (18,x)
    '''
    
    LEFT     = -1
    RIGHT    = 1
    STRAIGHT = 0

    def __init__(self, pos, horsePower, weight, color):
        '''
        Constructor
        '''
        
        
        self._enginePower   = horsePower
        self._weight       = weight
        self._color        = color
        
        self._posX         = pos[0]
        self._posY         = pos[1]
        
        self._speed        = 0.0
        self._heading      = 0.0 #direction in radians
        self._steerAngle   = 0.0
        
        self._width          = 26
        self._length         = 60
        self._wheelBase      = abs(self._length*0.6)
        self._tireLenght     = 10
        self._tireWidth      = 5
    
    
    # power between 0.0 and 1.0    
    def accelerate(self, deltaTime, power=1.0):
        #TODO: acceleration depending on horsePower, weight and time of use (deltaTime).
        # return resulting speed.
        self._speed = self._speed + deltaTime*power*30
        
    def brake(self, timeSlice):
        #TODO: depends on time and weight...
        self._speed = self._speed - timeSlice*150
        if (self._speed < 0.0):
            self._speed = 0.0
            
    def steer(self, deltaTime, steering):
        #steering left/right
        self._steerAngle += steering*deltaTime*math.pi/5.0*1.5
        if self._steerAngle > math.pi/5.0:
            self._steerAngle = math.pi/5.0
        elif self._steerAngle < -math.pi/5.0:
            self._steerAngle = -math.pi/5.0
        
        # straightening wheels
        if steering == 0:
            if self._steerAngle > 0.0:
                self._steerAngle -= deltaTime*math.pi/5.0
                if self._steerAngle < 0.0:
                    self._steerAngle = 0
            elif self._steerAngle < 0.0:
                self._steerAngle += deltaTime*math.pi/5.0
                if self._steerAngle > 0.0:
                    self._steerAngle = 0
            

    def update(self, deltaTime):
        
        # Calculates current position of wheels depending on position and orientation
        # of the car
        frontWheelX = self._posX + self._wheelBase/2 * math.cos(self._heading)
        frontWheelY = self._posY + self._wheelBase/2 * math.sin(self._heading)
        backWheelX  = self._posX - self._wheelBase/2 * math.cos(self._heading)
        backWheelY  = self._posY - self._wheelBase/2 * math.sin(self._heading)  
        
        # Calculates the value by which the position of the wheels change based on
        # speed, orientation and current steering angle of the car
        backWheelX  += self._speed * deltaTime * math.cos(self._heading)
        backWheelY  += self._speed * deltaTime * math.sin(self._heading)
        frontWheelX += self._speed * deltaTime * math.cos(self._heading+self._steerAngle)
        frontWheelY += self._speed * deltaTime * math.sin(self._heading+self._steerAngle)
        
        # Calculates the resulting new position of the car by calculating the center 
        # between front and back wheel. Also updates the direction of the car.
        self._posX = (frontWheelX + backWheelX) / 2.0
        self._posY = (frontWheelY + backWheelY) / 2.0
        self._heading = math.atan2( frontWheelY - backWheelY , frontWheelX - backWheelX )
        
    
    def render(self):
        
        # transform to coordinates of the car
        glPushMatrix()
        glTranslatef(self._posX, self._posY, 0.0)
        glRotatef(math.degrees(self._heading),0.0, 0.0, 1.0)
        
        #draw the back wheels
        glBegin(GL_QUADS)
        glColor3f(60.0/255, 40.0/255, 30.0/255)
        glVertex3f(-self._wheelBase/2-5, -self._width/2-2, 0.0)
        glVertex3f(-self._wheelBase/2+5, -self._width/2-2, 0.0)
        glVertex3f(-self._wheelBase/2+5, -self._width/2+3, 0.0)
        glVertex3f(-self._wheelBase/2-5, -self._width/2+3, 0.0)
        
        glVertex3f(-self._wheelBase/2-5, self._width/2+2, 0.0)
        glVertex3f(-self._wheelBase/2+5, self._width/2+2, 0.0)
        glVertex3f(-self._wheelBase/2+5, self._width/2-3, 0.0)
        glVertex3f(-self._wheelBase/2-5, self._width/2-3, 0.0)
        glEnd()
        
        #transform to coordinates of front left wheel
        glPushMatrix()
        glTranslatef(self._wheelBase/2, -self._width/2, 0.0)
        glRotatef(math.degrees(self._steerAngle), 0.0, 0.0, 1.0)
        
        #draw front left wheel
        glBegin(GL_QUADS)
        glVertex3f(-5, -2, 0.0)
        glVertex3f(5, -2, 0.0)
        glVertex3f(5, 3, 0.0)
        glVertex3f(-5, 3, 0.0)
        glEnd()
        
        glPopMatrix()
        
        #transform to coordinates of front right wheel
        glPushMatrix()
        glTranslatef(self._wheelBase/2, self._width/2, 0.0)
        glRotatef(math.degrees(self._steerAngle), 0.0, 0.0, 1.0)
        
        #draw front right wheel
        glBegin(GL_QUADS)
        glVertex3f(-5, 2, 0.0)
        glVertex3f(5, 2, 0.0)
        glVertex3f(5, -3, 0.0)
        glVertex3f(-5, -3, 0.0)
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
        
        
# if __name__ == '__main__':
#     hcnd_v1.main()