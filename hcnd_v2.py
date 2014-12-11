'''
Created on 05.12.2014

@author: Matthias
'''
try:
    import sys
    from OpenGL.GL import *
    from pygame.locals import *
    
    import pygame
    from utilities import console
    
    from Car.car_v2 import Car
except ImportError, err:
    print "Could not load module. %s" % (err)
    sys.exit(2)
    

screenSize  = 800, 600
proportion  = 1.0 / 0.067
fps = 0
enableConsole  = True

carStartPos = 3, 10
car     = Car(Car.MAZDA, (200,20,20), carStartPos)


def resize((width, height)):
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, height, 0.0, -6.0, 0.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity

def init():
    glClearColor(0.6, 0.6, 0.4, 1.0)
    
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    
#     glEnable(GL_POLYGON_SMOOTH)
#     glLineWidth(1.5)
    
    
def render():
    global proportion, screenSize
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    
    for track in car.getTracks():
        track.render(proportion)
    
    car.render(proportion)
    if enableConsole:
        console.printIt(screenSize), (0,0)
        
#     glBegin(GL_TRIANGLES)
#     glColor4f(0.0,0.0,0.0,0.5)
#     glVertex3f(0.0,0.0,0.0)
#     glVertex3f(0.0,80.0,0.0)
#     glVertex3f(80.0, 0.0, 0.0)
#     glEnd()
        
    pygame.display.flip()
    

def main():
    global car, proportion, fps, enableConsole
    video_flags = OPENGL | HWSURFACE | DOUBLEBUF
    
    pygame.init()
    pygame.display.set_mode(screenSize, video_flags)
    pygame.display.set_caption('Here Car, Now Drive!')
    
    resize(screenSize)
    init()
    
    newTime     = pygame.time.get_ticks()
    startTime   = newTime
    fpsTime     = 0
    console.update('FPS', 0)
    
    driveMode   = Car.ROLL
    steering    = Car.STRAIGHT
    
    playing = True
    while playing:
        oldTime = newTime
        newTime = pygame.time.get_ticks()
        deltaTime = (newTime - oldTime)/1000.0
        
        event = pygame.event.poll()
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            playing = False
        elif event.type == KEYDOWN and event.key == K_F1:
            enableConsole = not enableConsole 
                
        
        pressed = pygame.key.get_pressed() # a list of booleans for all keys
        
        if pressed[pygame.K_r]:
            car = Car(Car.MAZDA, (200,20,20), carStartPos)
            
        
        if pressed[pygame.K_DOWN]:
            driveMode = Car.BRAKE    
        elif pressed[pygame.K_UP]:
            driveMode = Car.ACCELERATE
        else:
            driveMode = Car.ROLL
        
        
        if pressed[pygame.K_LEFT]:
            steering = Car.LEFT
        elif pressed [pygame.K_RIGHT]:
            steering = Car.RIGHT
        else:
            steering = Car.STRAIGHT
        
        # to toggle breakpoint at custom times
        if pressed[K_z]:
            pass
        
        fpsTime += newTime - oldTime
        fps += 1
        if fpsTime >= 1000:
            console.update('FPS', fps) 
            fpsTime -= 1000
            fps = 0
        
#         if car._speed > 100/3.6:
#             playing = False
#             print newTime - startTime
               
        car.update(driveMode, steering, 12.8, deltaTime)
        render()
        
if __name__ == '__main__':
    main()