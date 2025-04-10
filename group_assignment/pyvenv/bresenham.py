import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Function to draw Bresenham Circle (simulated via OpenGL points)
def drawBresenhamCircle(xc, yc, r, fill=False):
    if fill:
        glBegin(GL_TRIANGLE_FAN)
        glVertex2f(xc, yc)  # Center
    else:
        glBegin(GL_LINE_LOOP)

    segments = 360
    for i in range(segments + 1):
        angle = 2.0 * math.pi * i / segments
        x = xc + r * math.cos(angle)
        y = yc + r * math.sin(angle)
        glVertex2f(x, y)

    glEnd()

# Main display function
def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # --- Draw filled circle (cyan) ---
    glColor3f(0.0, 1.0, 1.0)
    drawBresenhamCircle(-5, -5, 4, fill=True)

    # --- Draw outlined circle (red) ---
    glLineWidth(2.0)
    glColor3f(1.0, 0.0, 0.0)
    drawBresenhamCircle(5, 5, 4, fill=False)

    # --- Draw points on each circle ---
    glPointSize(5.0)
    glBegin(GL_POINTS)
    
    # Points for filled circle
    glColor3f(0.0, 1.0, 1.0)
    glVertex2f(-5, -5)  # Center
    glVertex2f(-5, -1)  # Top
    glVertex2f(-5, -9)  # Bottom
    glVertex2f(1, -5)   # Right
    glVertex2f(-9, -5)  # Left

    # Points for outlined circle
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(5, 5)
    glVertex2f(5, 9)
    glVertex2f(5, 1)
    glVertex2f(9, 5)
    glVertex2f(1, 5)
    glEnd()

    # --- Draw coordinate axes (thin lines only) ---
    glLineWidth(0.5)
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_LINES)
    glVertex2f(-10, 0)  
    glVertex2f(10, 0)   # X-axis
    glVertex2f(0, -10)  
    glVertex2f(0, 10)   # Y-axis
    glEnd()

    # --- Draw ticks on axes ---
    for i in range(-10, 11):
        if i != 0:
            glBegin(GL_LINES)
            glVertex2f(i, -0.1)
            glVertex2f(i, 0.1)   # X-axis ticks
            glVertex2f(-0.1, i)
            glVertex2f(0.1, i)   # Y-axis ticks
            glEnd()

    # # --- Label axes ---
    font = pygame.font.SysFont('Arial', 12)
    # for i in range(-10, 11):
    #     if i != 0:
    #         # X-axis labels
    #         text = font.render(str(i), True, (255, 255, 255))
    #         textData = pygame.image.tostring(text, 'RGBA', True)
    #         glRasterPos3d(i - 0.3, -0.5, 0)  # Adjusted position for better alignment
    #         glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    #         # Y-axis labels
    #         text = font.render(str(i), True, (255, 255, 255))
    #         textData = pygame.image.tostring(text, 'RGBA', True)
    #         glRasterPos3d(-0.5, i - 0.3, 0)  # Adjusted position for better alignment
    #         glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    # --- Label circles ---
    text = font.render("(5, 5)", True, (255, 255, 255))
    textData = pygame.image.tostring(text, 'RGBA', True)
    glRasterPos3d(5.2, 5.2, 0)
    glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    text = font.render("(-5, -5)", True, (255, 255, 255))
    textData = pygame.image.tostring(text, 'RGBA', True)
    glRasterPos3d(-6.5, -6.5, 0)
    glDrawPixels(text.get_width(), text.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, textData)

    pygame.display.flip()

# Initialize and run window
def main():
    pygame.init()
    display_width, display_height = 800, 600
    pygame.display.set_mode((display_width, display_height), DOUBLEBUF | OPENGL)
    gluOrtho2D(-10, 10, -10, 10)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                return
        display()

if __name__ == "__main__":
    main()
