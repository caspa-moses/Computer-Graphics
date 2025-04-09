import pygame
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math

# Function to draw Bresenham Circle
def drawBresenhamCircle(xc, yc, r, fill=False):
    if fill:
        glBegin(GL_TRIANGLE_FAN)
    else:
        glBegin(GL_LINE_LOOP)

    # Center point
    glVertex2f(xc, yc)

    # Calculate points around the circle
    segments = 360
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        x = xc + r * math.cos(angle)
        y = yc + r * math.sin(angle)
        glVertex2f(x, y)

    glEnd()

# Function to draw text labels
def drawText(x, y, label):
    glRasterPos2f(x, y)
    for c in label:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(c))

# Function to display everything
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # Draw the first circle (filled) in cyan
    glColor3f(0.0, 1.0, 1.0)  # Cyan color (#00FFFF)
    drawBresenhamCircle(-1, -1, 6, fill=True)

    # Draw the second circle (unfilled) in red
    glLineWidth(2.0)
    glColor3f(1.0, 0.0, 0.0)  # Red color
    drawBresenhamCircle(3, 5, 6, fill=False)

    # Draw points on the circle
    glPointSize(5.0)
    glBegin(GL_POINTS)
    
    # Points for first circle (cyan)
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(-1, -1)   # Center point
    glVertex2f(-1, 5)    # Top
    glVertex2f(-1, -7)   # Bottom
    glVertex2f(5, -1)    # Right
    glVertex2f(-7, -1)   # Left

    # Points for second circle (red)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(3, 5)     # Center point
    glVertex2f(3, 11)    # Top
    glVertex2f(3, -1)    # Bottom
    glVertex2f(9, 5)     # Right
    glVertex2f(-3, 5)    # Left
    glEnd()

    # Draw coordinate axes
    glLineWidth(1.0)
    glColor3f(1.0, 1.0, 1.0)  # White color
    glBegin(GL_LINES)
    glVertex2i(-15, 0)
    glVertex2i(15, 0)  # X-axis
    glVertex2i(0, -15)
    glVertex2i(0, 15)  # Y-axis
    glEnd()

    # Draw ticks on X and Y axes
    for i in range(-15, 16):
        if i != 0:
            glBegin(GL_LINES)
            glVertex2i(i, -0.1)
            glVertex2i(i, 0.1)
            glVertex2i(-0.1, i)
            glVertex2i(0.1, i)
            glEnd()

    # Draw axis labels and numbers in white
    glColor3f(1.0, 1.0, 1.0)
    glRasterPos2f(14, 0.3)
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord('X'))
    glRasterPos2f(0.3, 14)
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord('Y'))

    # Draw numbers on X and Y axes
    for i in range(-15, 16):
        if i != 0:  # Skip origin
            glRasterPos2f(i - 0.1, -0.4)
            num = str(i)
            for c in num:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))
            glRasterPos2f(-0.5, i - 0.1)
            for c in num:
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))

    # Draw coordinates for the circles
    glRasterPos2f(3.2, 5.2)
    coord1 = "(3, 5)"
    for c in coord1:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))
    
    glRasterPos2f(-0.8, -1.4)
    coord2 = "(-1, -1)"
    for c in coord2:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, ord(c))

    glFlush()

# Reshape function to adjust viewport
def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-15, 15, -15, 15)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# Main function to initialize OpenGL and start the event loop
def main():
    pygame.init()
    display_width, display_height = 800, 600
    pygame.display.set_mode((display_width, display_height), pygame.DOUBLEBUF | pygame.OPENGL)
    gluOrtho2D(-15, 15, -15, 15)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        display()

# Run the main function
if __name__ == "__main__":
    main()
