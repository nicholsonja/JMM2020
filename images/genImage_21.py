#!/usr/local/python3

from math import cos, sin, exp, pi, atan2, sqrt
import os
import cairo
import helper
import numpy as np

IMAGE_WIDTH_IN = 5
IMAGE_HEIGHT_IN = 5
DPI = 500

def makeImage(height, width, imageName):
    imageWidth = min(width, height)
    imageHeight = max(width, height)

    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, imageWidth, imageHeight)
    ctx = cairo.Context(surface)
    ctx.set_tolerance(.1)
    ctx.set_antialias(False)
    
    cx = imageWidth/2
    cy = imageHeight/2
    radius  = imageWidth/2 * .7
    
    # background
    ctx.set_source_rgb(1, 1, 1)
    ctx.rectangle(0, 0, imageWidth, imageHeight)
    ctx.fill()
    ctx.stroke()

    N = 300
    lineSize = 1
    kA = 2
    kB = 3


    ctx.set_line_width(lineSize)
    ctx.set_source_rgba(0, 0, 1, 1)
    for d in range(N):
        ang1 = (kA * d) * 2 * pi / N
        ang2 = (kB * d) * 2 * pi / N
   
        x1, y1 = helper.circle(ang1, radius)
        x2, y2 = helper.circle(ang2, radius)

        # scale, rotate, and move to position
        dist = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
        lineTheta = atan2(y2 - y1, x2 - x1)

        lineRadius = dist/2
        lineCx = (x1+x2)/2
        lineCy = (y1+y2)/2

        x, y = helper.lemniscate(0, lineRadius)
        x, y = helper.rotate(x, y, lineTheta)
        ctx.move_to(x + lineCx + cx, y + lineCy + cy)
        numSegments = 361
        for t in range(1, numSegments):
            theta = t/(numSegments-1) * 2 * pi
            x, y = helper.lemniscate(theta, lineRadius)
            x, y = helper.rotate(x, y, lineTheta)
            ctx.line_to(x + lineCx + cx, y + lineCy + cy)
        ctx.stroke()


        ctx.stroke()


    surface.write_to_png(imageName)

if __name__ == "__main__":
    scriptName = os.path.basename(__file__)
    fileNum = scriptName[9 : len(scriptName)-3]
    imageName = 'image_{}.png'.format(fileNum)

    width = IMAGE_WIDTH_IN * DPI
    height = IMAGE_HEIGHT_IN * DPI
    makeImage(height, width, imageName)
