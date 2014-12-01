'''
Created on 27.06.2014

@author: Matthias
'''

class Car(object):
    '''
    represents a car with all essentiel parts.
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
    
    # power between 0.0 and 1.0    
    def accelerate(self, timeSlice, power=1.0):
        #TODO: acceleration depending on horsePower, weight and time of use (timeSlice).
        # return resulting speed.
        pass
        
    def brake(self, timeSlice):
        #TODO: depends on time and weight...
        pass