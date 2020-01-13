import os
import numpy as np

from PIL import Image
from math import cos, sin, tan, pi, sqrt, log
from random import uniform

SINGLE_COLOR = 1
GRADIENT_COLOR = 2

def saveImage(data, imageName, imageWidth, imageHeight, 
              bg = None, fg = None):
    maxCount = max(data)

    if bg == None:
        bg = [255, 255, 255]

    
    if fg == None:  
        fg = [  0,   0, 255]
    
    rgb = np.zeros((imageHeight, imageWidth, 3), 'uint8')
    for y in range(imageHeight):
        for x in range(imageWidth):
            cnt = data[y * imageWidth + x]
            if cnt == 0:
                alpha = 0
            else:
                alpha = log(cnt)/log(maxCount)
               
            color = fg

            rgb[y, x, 0] = int(alpha * color[0] + (1 - alpha) * bg[0] + .5)
            rgb[y, x, 1] = int(alpha * color[1] + (1 - alpha) * bg[1] + .5)
            rgb[y, x, 2] = int(alpha * color[2] + (1 - alpha) * bg[2] + .5)
            
    img = Image.fromarray(rgb)
    img.save(imageName)
    
def getImageName(sourceScriptName):
    scriptName = os.path.basename(sourceScriptName)
    fileNum = scriptName[9 : len(scriptName)-3]
    imageName = 'image_{}.png'.format(fileNum)
    return imageName

# Parametric equations

def circle(theta, radius, cx = 0, cy = 0):
    x = cos(theta) * radius + cx
    y = sin(theta) * radius + cy
    return (x, y)

def rose(theta, radius, n, cx, cy):
    '''
    Info: http://mathworld.wolfram.com/Rose.html
    '''
    x = cos(n * theta) * cos(theta) * radius + cx
    y = cos(n * theta) * sin(theta) * radius + cy
    return (x, y)

def lemniscate(theta, radius, cx = 0, cy = 0):
    '''
    Info: http://mathworld.wolfram.com/Lemniscate.html
    '''
    c = cos(theta)
    s = sin(theta)
    x = (radius * c)/(1 + s * s)
    y = (radius * s * c)/(1 + s * s)
    return (x + cx, y + cy)   

def hypocycloid(theta, radius, R, r, cx, cy):
    '''
    Info: http://mathworld.wolfram.com/Hypocycloid.html

    R: outer circle radius
    r: inner circle radius
    '''
    x = ((R-r) * cos(theta) + r * cos((R-r)/r * theta)) * radius + cx
    y = ((R-r) * sin(theta) - r * sin((R-r)/r * theta)) * radius + cx
    return (x, y)  

def hypotrochoid(theta, radius, R, r, d, cx, cy):
    '''
    Info: http://mathworld.wolfram.com/Hypotrochoid.html

    R: outer circle radius
    r: inner circle radius
    d: distance from the center of the interior circle. 
    '''
    x = ((R-r) * cos(theta) + d * cos((R-r)/r * theta)) * radius + cx
    y = ((R-r) * sin(theta) - d * sin((R-r)/r * theta)) * radius + cx
    return (x, y)  

def square(theta, radius, cx, cy, rotAng = 0):
    '''
    One way to do a square with a parametric equation.

    rotAng : radians. Rotates the square
    '''
    n = int (theta / (2 * pi))
    theta = theta - n * 2 * pi
    if theta < 0:
        theta += 2 * pi

    if theta >= pi / 4 and theta < 3 * pi / 4:
        x = cos(theta)/sin(theta)
        y = 1
    elif theta >= 3 * pi / 4 and theta < 5 * pi / 4:
        x = -1
        y = -tan(theta)
    elif theta >= 5 * pi / 4 and theta < 7 * pi / 4:
        x = -cos(theta)/sin(theta)
        y = -1
    else:
        x = 1
        y = tan(theta)

    x1 = x * radius
    y1 = y * radius

    x = x1 * cos(rotAng) - y1 * sin(rotAng) +  cx
    y = y1 * cos(rotAng) + x1 * sin(rotAng) +  cy

    return x, y

def rotate(x, y, angle):
    '''
    rotate around origin
    '''
    return (x * cos(angle) - y * sin(angle), 
            x * sin(angle) + y * cos(angle))

def randomPointOnPath( pathPoints ):
    if len(pathPoints) < 2: 
        raise Exception("Need at least two points in path")

    pathLength = 0
    currPoint = pathPoints[0]
    for point in pathPoints[1:]:
        pathLength += sqrt(pow(currPoint[0] - point[0], 2) +
                           pow(currPoint[1] - point[1], 2))
        currPoint = point
      
    r = uniform(0, 1)
    targetDist = r * pathLength

    dist = 0
    currPoint = pathPoints[0]
    for point in pathPoints[1:]:
        segmentLen = sqrt(pow(currPoint[0] - point[0], 2) +
                          pow(currPoint[1] - point[1], 2))

        if dist + segmentLen >= targetDist:
            pointDist = (targetDist - dist)/segmentLen
            A = currPoint
            B = point
            C = [
                    (1 - pointDist) * A[0] + pointDist * B[0],
                    (1 - pointDist) * A[1] + pointDist * B[1]
                ]
            return C
        dist += segmentLen
        currPoint = point

    print("PATLEN", pathLength)
    print("SEGLEN", segmentLen)
    print("TARLEN", targetDist)
    return None

     
