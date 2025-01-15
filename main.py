import math

# This file contains the mathematical functions used to find TTC

# This function finds the angle created by two line when given their endpoints (a,b) and (x,y)
def findAngle( a, b, x, y):
    #dot product
    dotProduct = (a[0] - b[0]) * (x[0] - y[0]) + (a[1] - b[1]) * (x[1] - y[1])
    #calculate angle between vectors
    firstVMagnitude = math.sqrt(math.pow(a[0] - b[0], 2) + math.pow(a[1] - b[1], 2))
    secondVMagnitude = math.sqrt(math.pow(x[0] - y[0], 2) + math.pow(x[1] - y[1], 2))
    angle = math.degrees(math.acos( dotProduct / (firstVMagnitude * secondVMagnitude)))
    return angle

# This function calculates TTC with the current angle, previous angle, and time between frames
def TTC(current_angle, prev_angle, time):
    value = ( 2* (math.radians(current_angle)-math.radians(prev_angle))/time ) / (math.sin(2 * math.radians(current_angle)))
    if value == 0:
        return 0
    return math.fabs( 1/value )