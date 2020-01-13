#!/usr/local/python3

from math import cos, sin, exp, pi
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

    
    coordinates = []
    for d in range(N):
        ang1 = (kA * d) * 2 * pi / N
        ang2 = (kB * d) * 2 * pi / N
   
        x1, y1 = helper.circle(ang1, radius)
        x2, y2 = helper.circle(ang2, radius)
        
        coordinates.append(
            (
                (x1, y1), # p0
                (x2, y2)  # p1
            )
        )

    # calculate scale to fit in image
    maxX = max(p[0] for points in coordinates for p in points)
    minX = min(p[0] for points in coordinates for p in points)

    maxY = max(p[1] for points in coordinates for p in points)
    minY = min(p[1] for points in coordinates for p in points)

    scale = imageWidth/max(maxX - minX, maxY - minY)

    # draw it
    for coords in coordinates:
        p0, p1 = coords

        ctx.set_source_rgba(.125, .05, .25, 1)
        ctx.move_to(p0[0] * scale + cx, p0[1] * scale + cy)
        ctx.line_to(p1[0] * scale + cx, p1[1] * scale + cy)
        ctx.stroke()
    
    surface.write_to_png(imageName)

if __name__ == "__main__":
    scriptName = os.path.basename(__file__)
    fileNum = scriptName[9 : len(scriptName)-3]
    imageName = 'image_{}.png'.format(fileNum)

    width = IMAGE_WIDTH_IN * DPI
    height = IMAGE_HEIGHT_IN * DPI
    makeImage(height, width, imageName)
