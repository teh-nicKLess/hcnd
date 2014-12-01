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
        self._heading   = 0.0
        self._speed     = 0.0
        self.__steerAngle   = 0.0
        self._wheelBase    = 0.0 #the distance between the two axles
        
    def update(self, deltaTime):
        frontWheel = self.__carLocation + self._wheelBase/2 * ( math.cos(self._heading) , math.sin(self._heading) );
        backWheel = self.__carLocation - self._wheelBase/2 * ( math.cos(self._heading) , math.sin(self._heading) );  
        
        backWheel += self._speed * deltaTime * (math.cos(self.___carHeading) , math.sin(self._heading));
        frontWheel += self._speed * deltaTime * (math.cos(self._heading+self.__steerAngle) , math.sin(self._heading+self.__steerAngle));
        
        self.__carLocation = (frontWheel + backWheel) / 2.0;
        self._heading = math.atan2( frontWheel.Y - backWheel.Y , frontWheel.X - backWheel.X );

      