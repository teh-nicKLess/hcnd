'''
Created on 09.12.2014

@author: Matthias
'''
import pygame

from OpenGL.GL import *
import utilities
import collections

prints = collections.OrderedDict()
        
def update(name, value):
    '''Add new entries or update existing ones.'''
    if type(value) is float:
        text = "%s : %.2f" % (name, value)
    elif type(value) is tuple:
        text = "%s : " % name
        for part in value:
            text = text + "%.2f, " % part
        text = text[:-2]
    elif type(value) is utilities.vec2d.Vec2d:
        text = "%s : %.2f, %.2f" % (name, value.x, value.y)
    else:
        text = str(name + " : " + str(value))
    prints[name] = text
    
    
    
def remove(name):
    '''Remove an existing entry from the list'''
    prints.pop(name)
        
def printIt(screenSize):
        
    blending = False 
    if glIsEnabled(GL_BLEND) :
        blending = True
        
    offset = 1
    font = pygame.font.Font (None, 16)
    for name in prints:
        textSurface = font.render(prints[name], True, (0.4*255,0.4*255,0.6*255,255),)     
        textData = pygame.image.tostring(textSurface, "RGBA", True)     
        glWindowPos3d(10,screenSize[1] - (20*offset),0)
        offset += 1     
        glDrawPixels(textSurface.get_width(), textSurface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)
    
    if not blending :
        glDisable(GL_BLEND)
