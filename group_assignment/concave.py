import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np

# Point structure to store vertices
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Original concave polygon (arrowhead shape)
concavePoly = [
    Point(100, 200),  # P1
    Point(150, 250),  # P2
    Point(200, 200),  # P3
    Point(150, 150),  # P4 <- inward (concave)
    Point(150, 100)   # P5
]

# Cross product (z-component only)
def crossZ(a, b, c):
    v1x = b.x - a.x
    v1y = b.y - a.y
    v2x = c.x - b.x
    v2y = c.y - b.y
    return v1x * v2y - v1y * v2x

# Find concave vertex index
def findConcaveIndex(poly):
    n = len(poly)
    for i in range(n):
        a = poly[(i - 1 + n) % n]
        b = poly[i]
        c = poly[(i + 1) % n]
        if crossZ(a, b, c) < 0:
            return i
    return -1

# Function to draw a polygon
def drawPolygon(poly, r, g, b):
    glColor3f(r, g, b)
    glBegin(GL_POLYGON)
    for p in poly:
        glVertex2f(p.x, p.y)
    glEnd()

# Function to draw text (a label)
def drawText(x, y, label):
    glRasterPos2f(x, y)
    for c in label:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

# Function to draw a line
def drawLine(a, b, r=0, g=0, bCol=0):
    glColor3f(r, g, bCol)
    glBegin(GL_LINES)
    glVertex2f(a.x, a.y)
    glVertex2f(b.x, b.y)
    glEnd()

# The main display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the original polygon (left side)
    glColor3f(1.0, 0.0, 0.0)  # Red outline
    glBegin(GL_LINE_LOOP)
    for p in concavePoly:
        glVertex2f(p.x, p.y)
    glEnd()
    drawText(90, 270, "Original Concave Polygon")

    # Detect the concave vertex
    concaveIndex = findConcaveIndex(concavePoly)
    if concaveIndex == -1:
        return

    n = len(concavePoly)

    # Pick a valid target vertex to split with
    splitTarget = 1
    if splitTarget == concaveIndex or (splitTarget + 1) % n == concaveIndex or (splitTarget - 1 + n) % n == concaveIndex:
        splitTarget = 4  # Try P5 if P2 is adjacent

    # Offset polygon to the right (draw it on the right side of the window)
    offsetPoly = [Point(p.x + 300, p.y) for p in concavePoly]

    # Create two split polygons
    poly1 = []
    poly2 = []

    # Build the first polygon (clockwise)
    i = concaveIndex
    while True:
        poly1.append(offsetPoly[i])
        if i == splitTarget:
            break
        i = (i + 1) % n

    # Build the second polygon (counter-clockwise)
    i = concaveIndex
    while True:
        poly2.append(offsetPoly[i])
        if i == (splitTarget - 1 + n) % n:
            break
        i = (i - 1 + n) % n
    poly2.append(offsetPoly[splitTarget])  # Complete the second polygon

    # Draw the split polygons (right side)
    drawPolygon(poly1, 0.0, 1.0, 0.0)  # Green polygon
    drawPolygon(poly2, 0.0, 0.0, 1.0)  # Blue polygon

    # Draw the diagonal used for splitting
    drawLine(concavePoly[concaveIndex], concavePoly[splitTarget], 0, 0, 0)  # Left
    drawLine(offsetPoly[concaveIndex], offsetPoly[splitTarget], 0, 0, 0)   # Right

    glColor3f(0, 0, 0)  # Black outline for the offset polygon
    glBegin(GL_LINE_LOOP)
    for p in offsetPoly:
        glVertex2f(p.x, p.y)
    glEnd()

    drawText(360, 270, "Split Using Vector Method")

    pygame.display.flip()

# Initialize pygame and set up OpenGL
def init():
    pygame.init()
    display_width, display_height = 700, 300
    pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF | pygame.OPENGL)
    gluOrtho2D(0, display_width, 0, display_height)

# Main function to start everything
def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        display()

# Run the program
if __name__ == "__main__":
    main()
