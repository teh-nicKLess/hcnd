'''
Created on 18.12.2014

@author: Matthias
'''
import math

'''
Used to implement new formulas before including them in the Car class.
'''

# torqueArray. Index * 500 = RPM. first two entries empty since minRpm = 1000
torqueArray = [0, 0, 141, 154, 166, 173, 175, 180, 185, 188, 189, 186, 180, 173, 160]


def lookUpTorqueCurve(rpm):
    '''
    Calculates max torque by linear interpolation between torque points in given array
    torqueArray has one entry every 500
    '''
    rawIndex = rpm/500.0
    
    # index for array
    torqueIndex = int(rawIndex)
    ratio = rawIndex - torqueIndex
    
    maxTorque = (1-ratio) * torqueArray[torqueIndex] + ratio * torqueArray[torqueIndex + 1]

maxTorque = lookUpTorqueCurve(rpm)
engineTorque = throttlePosition * maxTorque

# first entry is reverse, values for Corvette C5
gearRatio = [2.90, 2.66, 1.78, 1.30, 1.0, 0.74, 0.50]
diffRatio = 3.42

# values for Mazda MX5 NB8B
gearRatio = [3.90, 3.76, 2.27, 1.65, 1.26, 1.0, 0.84]
diffRatio = 3.64
tireRadius = 0.295
# longitudinal force of the rear wheels on the surface
driveTorque = direction * engineTorque * gearRatio[gear] * diffRatio * transmissionEfficiency
driveForce = driveTorque / wheelRadius

# get the rpm (1/min)

# get the wheelRotationRate (rad/s) from carSpeed (m/s)
wheelRotationRate = carSpeed / wheelRadius

rpm = wheelRotationRate * gearRatio * diffRatio * 60 / (2*math.pi)

# small tweak to keep rpm over 1000, since torque is not defined beneath that value. Imagine as clutch
if rpm < 1000:
    rpm = 1000