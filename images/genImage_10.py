#!/usr/local/python3

from math import cos, sin, exp, pi, sqrt, atan2
import os
import cairo
import helper

IMAGE_WIDTH_IN = 5
IMAGE_HEIGHT_IN = 5
DPI = 300

STROKE = 2

def makeImage(height, width, imageName):
    N = 200
    kA = 2
    kB = 3
 
    imageWidth = min(width, height)
    imageHeight = max(width, height)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, imageWidth, imageHeight)
    ctx = cairo.Context(surface)
    ctx.set_tolerance(.1)
    ctx.set_antialias(False)
    
    cx = imageWidth/2
    cy = imageHeight/2
    radius  = imageWidth
    
    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, imageWidth, imageHeight)
    ctx.fill()
    ctx.stroke()
    
    # lines
    ctx.set_line_width(STROKE)
    startColor = (1, 0, 0)
    endColor = (0, 0, 1)

    # unit line to draw
    n = 100
    points = []
    for i in range(n):
        t = 2 * pi * i /(n-1)
        points.append([i/(n-1), .25 * sin(t) ])


    coordinates = []
    for d in range(N):
        ang1 = (kA * d) * 2 * pi / N
        ang2 = (kB * d) * 2 * pi / N
   
        x1, y1 = helper.circle(ang1, radius)
        x2, y2 = helper.circle(ang2, radius)

        dist = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        theta = atan2(y2 - y1, x2 - x1)
        tmpPoints = []
        for p in points:
            c = cos(theta) 
            s = sin(theta)
  
            x = p[0] * c - p[1] * s;
            y = p[0] * s + p[1] * c;

            tmpPoints.append([x * dist + x1, y * dist + y1])

        
        coordinates.append( tmpPoints )


    # calculate scale to fit in image
    maxX = max(p[0] for points in coordinates for p in points)
    minX = min(p[0] for points in coordinates for p in points)

    maxY = max(p[1] for points in coordinates for p in points)
    minY = min(p[1] for points in coordinates for p in points)

    scale = imageWidth/max(maxX - minX, maxY - minY)

    # draw it
    for coords in coordinates:
        ctx.set_source_rgba(.125, .05, .25, 1)

        ctx.move_to((coords[0][0] - (maxX + minX)/2) * scale + cx, 
                    (coords[0][1] - (maxY + minY)/2) * scale + cy)

        for c in coords[1:]:
            ctx.line_to((c[0] - (maxX + minX)/2) * scale + cx, 
                        (c[1] - (maxY + minY)/2) * scale + cy)

        ctx.stroke()

    surface.write_to_png(imageName)

if __name__ == "__main__":
    scriptName = os.path.basename(__file__)
    fileNum = scriptName[9 : len(scriptName)-3]
    imageName = 'image_{}.png'.format(fileNum)

    width = IMAGE_WIDTH_IN * DPI
    height = IMAGE_HEIGHT_IN * DPI
    makeImage(height, width, imageName)
