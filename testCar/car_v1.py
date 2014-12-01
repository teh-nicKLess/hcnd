'''
Created on 01.07.2014

@author: Matthias
@source: http://engineeringdotnet.blogspot.de/2010/04/simple-2d-car-physics-in-games.html
'''
import math

class MyClass(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        self.__carLocation  = 0, 0
        self.__carHeading   = 0.0
        self.__carSpeed     = 0.0
        self.__steerAngle   = 0.0
        self.__wheelBase    = 0.0 #the distance between the two axles
        
    def update(self, deltaTime):
        frontWheel = self.__carLocation + self.__wheelBase/2 * ( math.cos(self.__carHeading) , math.sin(self.__carHeading) );
        backWheel = self.__carLocation - self.__wheelBase/2 * ( math.cos(self.__carHeading) , math.sin(self.__carHeading) );  
        
        backWheel += self.__carSpeed * deltaTime * (math.cos(self.___carHeading) , math.sin(self.__carHeading));
        frontWheel += self.__carSpeed * deltaTime * (math.cos(self.__carHeading+self.__steerAngle) , math.sin(self.__carHeading+self.__steerAngle));
        
        self.__carLocation = (frontWheel + backWheel) / 2.0;
        self.__carHeading = math.atan2( frontWheel.Y - backWheel.Y , frontWheel.X - backWheel.X );

      