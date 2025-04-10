import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

concavePoly = [
    Point(100, 200),  # P1
    Point(150, 250),  # P2
    Point(200, 200),  # P3
    Point(150, 150),  # P4 <- concave
    Point(150, 100)   # P5
]

def crossZ(a, b, c):
    abx = b.x - a.x
    aby = b.y - a.y
    bcx = c.x - b.x
    bcy = c.y - b.y
    return abx * bcy - aby * bcx

def findConcaveIndex(poly):
    n = len(poly)
    for i in range(n):
        prev = poly[(i - 1) % n]
        curr = poly[i]
        next = poly[(i + 1) % n]
        if crossZ(prev, curr, next) < 0:
            return i
    return -1

def vectorIntersection(p1, p2, q1, q2):
    """Finds the intersection point of two line segments (p1-p2 and q1-q2)."""
    def det(a, b, c, d):
        return a * d - b * c

    a1, b1 = p2.y - p1.y, p1.x - p2.x
    c1 = a1 * p1.x + b1 * p1.y

    a2, b2 = q2.y - q1.y, q1.x - q2.x
    c2 = a2 * q1.x + b2 * q1.y

    determinant = det(a1, b1, a2, b2)
    if determinant == 0:
        return None  # Parallel lines

    x = det(c1, b1, c2, b2) / determinant
    y = det(a1, c1, a2, c2) / determinant
    return Point(x, y)

def splitPolygon(poly):
    n = len(poly)
    concaveIndex = findConcaveIndex(poly)

    if concaveIndex == -1:
        return [poly]  # Already convex

    # Find a valid split line using vector intersection
    concavePoint = poly[concaveIndex]
    for i in range(n):
        if i == concaveIndex or i == (concaveIndex - 1) % n or i == (concaveIndex + 1) % n:
            continue
        splitPoint = poly[i]

        # Check if the line intersects with any other edges
        valid = True
        for j in range(n):
            p1 = poly[j]
            p2 = poly[(j + 1) % n]
            if p1 == concavePoint or p2 == concavePoint or p1 == splitPoint or p2 == splitPoint:
                continue
            if vectorIntersection(concavePoint, splitPoint, p1, p2):
                valid = False
                break

        if valid:
            splitIndex = i
            break

    # Form two new polygons
    poly1 = []
    i = concaveIndex
    while True:
        poly1.append(poly[i])
        if i == splitIndex:
            break
        i = (i + 1) % n

    poly2 = []
    i = concaveIndex
    while True:
        poly2.append(poly[i])
        if i == (splitIndex - 1 + n) % n:
            break
        i = (i - 1 + n) % n
    poly2.append(poly[splitIndex])

    return poly1, poly2, concaveIndex, splitIndex

def drawPolygon(poly, color):
    glColor3f(*color)
    glBegin(GL_POLYGON)
    for p in poly:
        glVertex2f(p.x, p.y)
    glEnd()

def drawOutline(poly, color=(0, 0, 0)):
    glColor3f(*color)
    glBegin(GL_LINE_LOOP)
    for p in poly:
        glVertex2f(p.x, p.y)
    glEnd()

def drawText(x, y, text):
    font = pygame.font.SysFont('Arial', 16)
    text_surface = font.render(text, True, (0, 0, 0))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    glRasterPos2f(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)

def drawLine(a, b, color=(0, 0, 0)):
    glColor3f(*color)
    glBegin(GL_LINES)
    glVertex2f(a.x, a.y)
    glVertex2f(b.x, b.y)
    glEnd()

def translatePolygon(poly, dx, dy):
    return [Point(p.x + dx, p.y + dy) for p in poly]

def drawScene():
    glClear(GL_COLOR_BUFFER_BIT)
    
    # Draw the original concave polygon on the left
    drawOutline(concavePoly, (1, 0, 0))

    # Split the polygon into two convex parts
    poly1, poly2, ci, si = splitPolygon(concavePoly)

    # Draw the split line on the original polygon
    drawLine(concavePoly[ci], concavePoly[si], (0, 0, 0))

    # Translate the split polygons to the right side with more spacing
    poly1 = translatePolygon(poly1, 350, 50)  # Adjusted translation for more spacing
    poly2 = translatePolygon(poly2, 350, -50)  # Adjusted translation for more spacing

    # Draw the split polygons on the right
    drawPolygon(poly1, (0.3, 0.8, 0.3))
    drawOutline(poly1)

    drawPolygon(poly2, (0.2, 0.4, 0.9))
    drawOutline(poly2)

    pygame.display.flip()


def init():
    pygame.init()
    screen = pygame.display.set_mode((700, 300), DOUBLEBUF | OPENGL)
    glClearColor(1, 1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, 700, 0, 300)

def main():
    init()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == QUIT:
                running = False
        drawScene()
    pygame.quit()

if __name__ == "__main__":
    main()
