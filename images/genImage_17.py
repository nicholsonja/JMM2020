#!/usr/local/python3

from math import cos, sin, exp, pi, atan2, sqrt
import os
import cairo
import helper
import numpy as np

IMAGE_WIDTH_IN = 5
IMAGE_HEIGHT_IN = 5
DPI = 500

def drawLabel(label, num, radius, ang, cx, cy, ctx):
    x1, y1 = helper.circle(ang, radius)

    (lab_x, lab_y, lab_width, 
     lab_height, lab_dx, lab_dy) = ctx.text_extents(label) 
     
    ctx.move_to(x1 + cx - lab_width/2, y1 + cy + lab_height/2)
    ctx.show_text(label)
    ctx.move_to(x1 + cx - lab_width/4, y1 + cy + lab_height)
    ctx.show_text("  " + num)
    ctx.fill()

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

    N = 30
    lineSize = 20
    kA = 1
    kB = 2

    # unit line to draw
    n = 100
    points = []
    for i in range(n):
        x = 2.0 * i/(n-1) - 1
        y = x*x
        points.append([.5 * x + .5, .5 * y - .5])

    for d in range(N):
        ang1 = (kA * d) * 2 * pi / N
        ang2 = (kB * d) * 2 * pi / N
   
        x1, y1 = helper.circle(ang1, radius)
        x2, y2 = helper.circle(ang2, radius)

        if ((ang2-ang1)%(2*pi)) > pi:
            x1, x2 = x2, x1
            y1, y2 = y2, y1
            ang1, ang2 = ang2, ang1


        #ctx.move_to(x1 + cx, y1 + cy)
        #ctx.line_to(x2 + cx, y2 + cy)
        #ctx.stroke() 
        
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

        if d == 3 or d == 27:
            ctx.set_line_width(lineSize)
            ctx.set_source_rgba(0, 0, 1, 1)
        else:
            ctx.set_line_width(lineSize * .25)
            ctx.set_source_rgba(.4, .4, .4, .5)
        ctx.move_to(tmpPoints[0][0] + cx, tmpPoints[0][1] + cy)
        for p in tmpPoints[1:]:
            ctx.line_to(p[0] + cx, p[1] + cy)
        ctx.stroke()


    # big circle
    ctx.set_line_width(lineSize)
    ctx.set_source_rgba(1, 0, 0, 1)
    ctx.arc(cx, cy, radius, 0, 2 * pi)
    ctx.stroke()

    # dots
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(4 * lineSize)
    for i in range(N):
        ang = i * 2 * pi / N
        x1, y1 = helper.circle(ang, radius)
        ctx.arc(x1 + cx, 
                y1 + cy, 
                lineSize * 1.2, 0, 2 * pi)
        ctx.fill()

        if i == 3 or i == 27:
            if i == 3:
                labelA = "n=3"
                labelB = "n=6"
                rad = radius * .75
            else:
                labelA = "n=27"
                labelB = "n=54=24"
                rad = radius * .75

            ang1 = (kA * i) * 2 * pi / N
            ang2 = (kB * i) * 2 * pi / N

            drawLabel("A", labelA, rad, ang1, cx, cy, ctx)
            drawLabel("B", labelB, rad, ang2, cx, cy, ctx)


    surface.write_to_png(imageName)

if __name__ == "__main__":
    scriptName = os.path.basename(__file__)
    fileNum = scriptName[9 : len(scriptName)-3]
    imageName = 'image_{}.png'.format(fileNum)

    width = IMAGE_WIDTH_IN * DPI
    height = IMAGE_HEIGHT_IN * DPI
    makeImage(height, width, imageName)
