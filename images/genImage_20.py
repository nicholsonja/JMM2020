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
    drawingCx = imageWidth * .9
    drawingCy = .1 * imageHeight
    circleRadius = imageWidth * .5
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

    # scale, rotate, and move to position
    dist = sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2))
    lineTheta = atan2(y2 - y1, x2 - x1)
    minRadius = dist/2
    lineCx = (x1+x2)/2
    lineCy = (y1+y2)/2

    x, y = helper.lemniscate(0, minRadius)
    x, y = helper.rotate(x, y, lineTheta)
    ctx.move_to(x + lineCx + drawingCx, y + lineCy + drawingCy)
    numSegments = 361
    for t in range(1, numSegments):
        theta = t/(numSegments-1) * 2 * pi
        x, y = helper.lemniscate(theta, minRadius)
        x, y = helper.rotate(x, y, lineTheta)
        ctx.line_to(x + lineCx + drawingCx, y + lineCy + drawingCy)
    ctx.stroke()

    # dots and labels
    ctx.set_source_rgba(0, 0, 0, 1)
    ctx.select_font_face("Arial", cairo.FONT_SLANT_NORMAL, 
                         cairo.FONT_WEIGHT_NORMAL)
    ctx.set_font_size(3 * lineSize)
    for i in range(N):
        ang = i * 2 * pi / N
        pX, pY = helper.circle(ang, circleRadius)
        ctx.arc(pX + drawingCx, 
                pY + drawingCy, 
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

        pX, pY = helper.circle(ang, circleRadius * 1.1)
        ctx.move_to(pX + drawingCx - lab_width/2, 
                    pY + drawingCy + lab_height/2)
        ctx.show_text(label)
        ctx.fill()
        

    surface.write_to_png(imageName)

if __name__ == "__main__":
    scriptName = os.path.basename(__file__)
    fileNum = scriptName[9 : len(scriptName)-3]
    imageName = 'image_{}.png'.format(fileNum)

    width = IMAGE_WIDTH_IN * DPI
    height = IMAGE_HEIGHT_IN * DPI
    makeImage(height, width, imageName)
