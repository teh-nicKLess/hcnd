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
    
    ACCELERATE  = 1
    BRAKE       = -1
    ROLL        = 0
    
    #MODEL = (enginePower in kW, length in mm, width in mm, weight in kg, drag constant)
    #Used proportion px:mm : 1:67
    MAZDA = (93, 4.020, 1.720, 1300, 0.4257)
    


    def __init__(self, model, color, startPos):
        '''
        Constructor
        '''
        self._enginePower   = model[0]*100
        self._length        = model[1]
        self._width         = model[2]
        self._weight        = model[3]
        self._color         = pygame.Color(color[0], color[1], color[2]).normalize()
        
        # Constant for aerodynamic drag. Depends on frontal area of the car and shape.
        # for comparison: constDrag for a Corvette is approx. 0.4257
        self._constDrag     = model[4]
        
        self._wheelBase      = self._length*0.6
        self._tireLength     = self._length/6.0
        self._tireWidth      = self._tireLength/2.0
        
        self._pos = Vec2d(startPos)
        
        self._velocity      = Vec2d(0.0, 0.0)
        self._speed         = 0.0 # == self._velocity.get_length()
        self._heading       = Vec2d(1.0, 0.0) # == self._velocity.normalized()
        self._headingAngle  = math.radians(self._heading.angle)
        self._steerAngle    = 0.0
        
        
      
    def physics(self, driveMode, constRollResist, deltaTime):
        #constRollResist: rolling resistance approx. 30 * self._constDrag, depends on surface
        
        constBraking = 20000
        appliedForce = 0
        if driveMode == 1:
            forceTraction   = self._heading * self._enginePower
            appliedForce    = forceTraction
        elif driveMode == -1:
            forceBraking    = -self._heading * constBraking
            appliedForce    = forceBraking
        else:
            appliedForce = 0    
            
        forceDrag       = -self._constDrag * self._velocity * self._velocity.get_length()
        forceRollResist = -constRollResist * self._velocity
        
        forceLongitude  = appliedForce + forceDrag + forceRollResist
        
        acceleration    = forceLongitude / self._weight #not final, takes only longitude force
        
        self._velocity  = self._velocity + deltaTime*acceleration
        self._speed     = self._velocity.get_length()
    
    def steer(self, steering, deltaTime):
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
                    
                    
    def update(self, proportion, driveMode, steering, constRollResist, deltaTime):
        
        
        self.physics(driveMode, constRollResist, deltaTime)
        self.steer(steering, deltaTime)
        
        # Calculates current position of wheels depending on position and orientation
        # of the car
        backWheel   = self._pos - self._wheelBase/2 * self._heading
        frontWheel  = self._pos + self._wheelBase/2 * self._heading
        
        # Calculates the value by which the position of the wheels change based on
        # speed, orientation and current steering angle of the car
        backWheel.x  += self._speed * deltaTime * math.cos(self._headingAngle)
        backWheel.y  += self._speed * deltaTime * math.sin(self._headingAngle)
        frontWheel.x += self._speed * deltaTime * math.cos(self._headingAngle+self._steerAngle)
        frontWheel.y += self._speed * deltaTime * math.sin(self._headingAngle+self._steerAngle)        
        
        # Calculates the resulting new position of the car by calculating the center 
        # between front and back wheel. Also updates the direction of the car.
        self._pos           = (frontWheel + backWheel) / 2.0
        self._heading       = (frontWheel - backWheel).normalized()
        self._headingAngle  = math.radians(self._heading.angle)
        self._velocity      = self._heading * self._speed
        
#         print "Heading:", self._heading, " Heading angle:", math.degrees(self._headingAngle), " FrontWheel - BackWheel:",frontWheel - backWheel
        print "Speed:", self._speed
        
    def render(self, proportion):
        
        pixelPos        = (self._pos*proportion)
        pixelLength     = round(self._length*proportion)
        pixelWidth      = round(self._width*proportion)
        pixelWheelbase  = round(self._wheelBase*proportion)
        pixelTireLength = round(self._tireLength*proportion)
        pixelTireWidth  = round(self._tireWidth*proportion)
        
        # transform to coordinates of the car
        glPushMatrix()
        glTranslatef(pixelPos.x, pixelPos.y, 0.0)
        glRotatef(self._heading.angle,0.0, 0.0, 1.0)
        
        #draw the back wheels
        glBegin(GL_QUADS)
        glColor3f(60.0/255, 40.0/255, 30.0/255)
        glVertex3f(-pixelWheelbase/2-pixelTireLength/2.0, -pixelWidth/2-pixelTireWidth*0.4, 0.0)
        glVertex3f(-pixelWheelbase/2+pixelTireLength/2.0, -pixelWidth/2-pixelTireWidth*0.4, 0.0)
        glVertex3f(-pixelWheelbase/2+pixelTireLength/2.0, -pixelWidth/2+pixelTireWidth*0.6, 0.0)
        glVertex3f(-pixelWheelbase/2-pixelTireLength/2.0, -pixelWidth/2+pixelTireWidth*0.6, 0.0)
        
        glVertex3f(-pixelWheelbase/2-pixelTireLength/2.0, pixelWidth/2+pixelTireWidth*0.4, 0.0)
        glVertex3f(-pixelWheelbase/2+pixelTireLength/2.0, pixelWidth/2+pixelTireWidth*0.4, 0.0)
        glVertex3f(-pixelWheelbase/2+pixelTireLength/2.0, pixelWidth/2-pixelTireWidth*0.6, 0.0)
        glVertex3f(-pixelWheelbase/2-pixelTireLength/2.0, pixelWidth/2-pixelTireWidth*0.6, 0.0)
        glEnd()
        
        #transform to coordinates of front left wheel
        glPushMatrix()
        glTranslatef(pixelWheelbase/2, -pixelWidth/2, 0.0)
        glRotatef(math.degrees(self._steerAngle), 0.0, 0.0, 1.0)
        
        #draw front left wheel
        glBegin(GL_QUADS)
        glVertex3f(-pixelTireLength/2, -pixelTireWidth*0.4, 0.0)
        glVertex3f( pixelTireLength/2, -pixelTireWidth*0.4, 0.0)
        glVertex3f( pixelTireLength/2,  pixelTireWidth*0.6, 0.0)
        glVertex3f(-pixelTireLength/2,  pixelTireWidth*0.6, 0.0)
        glEnd()
        
        glPopMatrix()
        
        #transform to coordinates of front right wheel
        glPushMatrix()
        glTranslatef(pixelWheelbase/2, pixelWidth/2, 0.0)
        glRotatef(math.degrees(self._steerAngle), 0.0, 0.0, 1.0)
        
        #draw front right wheel
        glBegin(GL_QUADS)
        glVertex3f(-pixelTireLength/2,  pixelTireWidth*0.4, 0.0)
        glVertex3f( pixelTireLength/2,  pixelTireWidth*0.4, 0.0)
        glVertex3f( pixelTireLength/2, -pixelTireWidth*0.6, 0.0)
        glVertex3f(-pixelTireLength/2, -pixelTireWidth*0.6, 0.0)
        glEnd()
         
        glPopMatrix()
        
        
        #draw the car body  
        glBegin(GL_TRIANGLE_FAN)
        glColor4fv(self._color)
        glVertex3f(0.0, 0.0, 0.0)
        #rear left
        glVertex3f(-pixelLength/2+3, -pixelWidth/2, 0.0)
        glVertex3f(-pixelLength/2+1, -pixelWidth/2+1, 0.0)
        glVertex3f(-pixelLength/2, -pixelWidth/2+5, 0.0)
        
        #rear right
        glVertex3f(-pixelLength/2, pixelWidth/2-5, 0.0)
        glVertex3f(-pixelLength/2+1, pixelWidth/2-1, 0.0)
        glVertex3f(-pixelLength/2+3, pixelWidth/2, 0.0)
        
        #front right
        glVertex3f(pixelLength/2-6, pixelWidth/2, 0.0)
        glVertex3f(pixelLength/2-2, pixelWidth/2-1, 0.0)
        glVertex3f(pixelLength/2, pixelWidth/2-4, 0.0)
        
        #front left
        glVertex3f(pixelLength/2, -pixelWidth/2+4, 0.0)
        glVertex3f(pixelLength/2-2, -pixelWidth/2+1, 0.0)
        glVertex3f(pixelLength/2-6, -pixelWidth/2, 0.0)
        glVertex3f(-pixelLength/2+3, -pixelWidth/2, 0.0)
        
        glEnd()
        
        #draw details
        
        #side mirrors
        glBegin(GL_QUADS)
        glVertex3f(7, -pixelWidth/2, 0.0)
        glVertex3f(9, -pixelWidth/2, 0.0)
        glVertex3f(7, -pixelWidth/2-2, 0.0)
        glVertex3f(6, -pixelWidth/2-2, 0.0)
        
        glVertex3f(6, pixelWidth/2+2, 0.0)
        glVertex3f(7, pixelWidth/2+2, 0.0)
        glVertex3f(9, pixelWidth/2, 0.0)
        glVertex3f(7, pixelWidth/2, 0.0)
        glEnd()
        
        #hood lines
        glBegin(GL_LINES)
        glColor4fv(pygame.Color(120,20,20).normalize())
        glVertex3f(10, -pixelWidth/2+1 , 0.0)
        glVertex3f(pixelLength/2-4, -pixelWidth/2+2 , 0.0)
        
        glVertex3f(10, pixelWidth/2-1 , 0.0)
        glVertex3f(pixelLength/2-4, pixelWidth/2-2 , 0.0)
        glEnd()
        
        #trunk lines
        glBegin(GL_LINE_STRIP)
        glVertex3f(-pixelLength/2+1, -pixelWidth/2+4, 0.0)
        glVertex3f(-pixelLength/2+7, -pixelWidth/2+4, 0.0)
        glVertex3f(-pixelLength/2+9, -pixelWidth/2+7, 0.0)
        glVertex3f(-pixelLength/2+9, pixelWidth/2-7, 0.0)
        glVertex3f(-pixelLength/2+7, pixelWidth/2-4, 0.0)
        glVertex3f(-pixelLength/2+1, pixelWidth/2-4, 0.0)
        glEnd()
         
        #spoiler
        glBegin(GL_QUADS)
        glColor4fv(pygame.Color(240,50,50).normalize())
        glVertex3f(-pixelLength/2, -pixelWidth/2+4, 0.0)
        glVertex3f(-pixelLength/2, pixelWidth/2-4, 0.0)
        glVertex3f(-pixelLength/2+3, pixelWidth/2-6, 0.0)
        glVertex3f(-pixelLength/2+3, -pixelWidth/2+6, 0.0)
        glEnd()
        
        
        #draw the wind shield
        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(110.0/255, 140.0/255, 150.0/255)
        glVertex3f(9 , -pixelWidth/2+1 , 0.0)
        glVertex3f(0 , -pixelWidth/2+4 , 0.0)
        glVertex3f(11, -pixelWidth/2+8 , 0.0)
        glVertex3f(2 , -pixelWidth/2+10, 0.0)
        glVertex3f(11,  pixelWidth/2-8 , 0.0)
        glVertex3f(2 ,  pixelWidth/2-10, 0.0)
        glVertex3f(9 ,  pixelWidth/2-1 , 0.0)
        glVertex3f(0 ,  pixelWidth/2-4 , 0.0)
        glEnd()
        
        #draw the side windows
        #left window
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(6 , -pixelWidth/2+1 , 0.0)
        glVertex3f(-2, -pixelWidth/2+4 , 0.0)
        glVertex3f(-9, -pixelWidth/2+1 , 0.0)
        glVertex3f(-11, -pixelWidth/2+4 , 0.0)
        glEnd()
        
        #right window
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(6 , pixelWidth/2-1 , 0.0)
        glVertex3f(-2, pixelWidth/2-4 , 0.0)
        glVertex3f(-9, pixelWidth/2-1 , 0.0)
        glVertex3f(-11, pixelWidth/2-4 , 0.0)
        glEnd()
        
        #draw the folding top
        #upper part
        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(0.1,0.1,0.1)
        glVertex3f(-1, -pixelWidth/2+4 , 0.0)
        glVertex3f(1 , -pixelWidth/2+10, 0.0)
        glVertex3f(-11, -pixelWidth/2+4, 0.0)
        glVertex3f(1 ,  pixelWidth/2-10, 0.0)
        glVertex3f(-11, pixelWidth/2-4 , 0.0)
        glVertex3f(-1 , pixelWidth/2-4 , 0.0)
        glEnd()
        
        #rear part
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(-9,  -pixelWidth/2+1 , 0.0)
        glVertex3f(-11, -pixelWidth/2+4 , 0.0)
        glVertex3f(-18, -pixelWidth/2+3 , 0.0)
        glVertex3f(-11,  pixelWidth/2-4 , 0.0)
        glVertex3f(-18,  pixelWidth/2-3 , 0.0)
        glVertex3f(-9,   pixelWidth/2-1 , 0.0)
        glEnd()
        
        #draw the rear window
        glBegin(GL_TRIANGLE_STRIP)
        glColor3f(70.0/255, 90.0/255, 100.0/255)
        glVertex3f(-13, -pixelWidth/2+9 , 0.0)
        glVertex3f(-16, -pixelWidth/2+8 , 0.0)
        glVertex3f(-13,  pixelWidth/2-9 , 0.0)
        glVertex3f(-16,  pixelWidth/2-8 , 0.0)
        glEnd()
        
        #draw headlamps
        glBegin(GL_TRIANGLE_STRIP)
        glColor4fv(pygame.Color(240,240,180).normalize())
        glVertex3f(pixelLength/2-3, -pixelWidth/2+2, 0.0)
        glVertex3f(pixelLength/2-2, -pixelWidth/2+2, 0.0)
        glVertex3f(pixelLength/2, -pixelWidth/2+4, 0.0)
        glVertex3f(pixelLength/2-2, -pixelWidth/2+6, 0.0)
        glVertex3f(pixelLength/2, -pixelWidth/2+7, 0.0)
        glEnd()
        
        glBegin(GL_TRIANGLE_STRIP)
        glVertex3f(pixelLength/2-3, pixelWidth/2-2, 0.0)
        glVertex3f(pixelLength/2-2, pixelWidth/2-2, 0.0)
        glVertex3f(pixelLength/2, pixelWidth/2-4, 0.0)
        glVertex3f(pixelLength/2-2, pixelWidth/2-6, 0.0)
        glVertex3f(pixelLength/2, pixelWidth/2-7, 0.0)
        glEnd()
        
        glPopMatrix()