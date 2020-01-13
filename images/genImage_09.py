#!/usr/local/python3

from math import cos, sin, exp, pi, atan2, sqrt
import os
import cairo
import helper

IMAGE_WIDTH_IN = 5
IMAGE_HEIGHT_IN = 5
DPI = 500

STROKE = 2

def makeImage(height, width, imageName):
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

    # big circle
    drawingCx = imageWidth * 1.025
    drawingCy = 0 # -.05 * imageWidth
    circleRadius = imageWidth * .9
    N = 33
    lineSize = 50

    ctx.set_line_width(lineSize)
    ctx.set_source_rgba(1, 0, 0, 1)
    ctx.arc(drawingCx, drawingCy, circleRadius, 0, 2 * pi)
    ctx.stroke()

    #line
    ctx.set_source_rgba(0, 0, 1, 1)

    ang1 = 16 * 2 * pi / N
    x1, y1 = helper.circle(ang1, circleRadius)

    ang2 = 9 * 2 * pi / N
    x2, y2 = helper.circle(ang2, circleRadius)

    # unit line to draw
    n = 100
    points = []
    for i in range(n):
        t = 2 * pi * i /(n-1)
        points.append([i/(n-1), .25 * sin(t) ])



    # scale, rotate, and move to position
    dist = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    theta = atan2(y2 - y1, x2 - x1)
    tmpPoints = []
    for p in points:
        c = cos(theta) 
        s = sin(theta)
  
        x = p[0] * c - p[1] * s;
        y = p[0] * s + p[1] * c;

        tmpPoints.append([x * dist + x1, y * dist + y1])
    points = tmpPoints

    ctx.move_to(points[0][0] + drawingCx, points[0][1] + drawingCy)
    for p in points[1:]:
        ctx.line_to(p[0] + drawingCx, p[1] + drawingCy)
    ctx.stroke()

    # dots and labels
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(3 * lineSize)
    for i in range(N):
        ang = i * 2 * pi / N
        x1, y1 = helper.circle(ang, circleRadius)
        ctx.arc(x1 + drawingCx, 
                y1 + drawingCy, 
                lineSize * 1.25, 0, 2 * pi)
        ctx.fill()

        # label
        if i == 16:
            label = "A"
        elif i == 9:
            label = "B"
        else:
            label = "{}".format(i)
            label = " "

        (lab_x, lab_y, lab_width, 
         lab_height, lab_dx, lab_dy) = ctx.text_extents(label)

        x1, y1 = helper.circle(ang, circleRadius * 1.075)
        ctx.move_to(x1 + drawingCx - lab_width/2, 
                    y1 + drawingCy + lab_height/2)
        ctx.show_text(label)
        ctx.fill()
        

    '''
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
   
    '''
    surface.write_to_png(imageName)

if __name__ == "__main__":
    scriptName = os.path.basename(__file__)
    fileNum = scriptName[9 : len(scriptName)-3]
    imageName = 'image_{}.png'.format(fileNum)

    width = IMAGE_WIDTH_IN * DPI
    height = IMAGE_HEIGHT_IN * DPI
    makeImage(height, width, imageName)
