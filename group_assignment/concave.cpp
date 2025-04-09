#include <GL/glut.h>
#include <vector>
#include <cmath>
#include <iostream>

struct Point
{
    float x, y;
};

std::vector<Point> concavePoly = {
    {100, 200}, // P1
    {150, 250}, // P2
    {200, 200}, // P3
    {150, 150}, // P4 <- inward (concave)
    {150, 100}  // P5
};

float crossZ(Point a, Point b, Point c)
{
    float v1x = b.x - a.x;
    float v1y = b.y - a.y;
    float v2x = c.x - b.x;
    float v2y = c.y - b.y;
    return v1x * v2y - v1y * v2x;
}

int findConcaveIndex(const std::vector<Point> &poly)
{
    int n = poly.size();
    for (int i = 0; i < n; ++i)
    {
        Point a = poly[(i - 1 + n) % n];
        Point b = poly[i];
        Point c = poly[(i + 1) % n];
        if (crossZ(a, b, c) < 0)
        {
            return i;
        }
    }
    return -1;
}

void drawPolygon(const std::vector<Point> &poly, float r, float g, float b)
{
    glColor3f(r, g, b);
    glBegin(GL_POLYGON);
    for (auto &p : poly)
        glVertex2f(p.x, p.y);
    glEnd();
}

void drawText(float x, float y, const char *label)
{
    glRasterPos2f(x, y);
    for (const char *c = label; *c; c++)
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, *c);
}

void drawLine(Point a, Point b, float r = 0, float g = 0, float bCol = 0)
{
    glColor3f(r, g, bCol);
    glBegin(GL_LINES);
    glVertex2f(a.x, a.y);
    glVertex2f(b.x, b.y);
    glEnd();
}

void display()
{
    glClear(GL_COLOR_BUFFER_BIT);

    // Original polygon (left)
    glColor3f(1.0, 0.0, 0.0);
    glBegin(GL_LINE_LOOP);
    for (auto &p : concavePoly)
        glVertex2f(p.x, p.y);
    glEnd();
    drawText(90, 270, "Original Concave Polygon");

    // Detect concave vertex
    int concaveIndex = findConcaveIndex(concavePoly);
    if (concaveIndex == -1)
        return;

    int n = concavePoly.size();

    // Pick target to split with
    int splitTarget = 1;
    if (splitTarget == concaveIndex || (splitTarget + 1) % n == concaveIndex || (splitTarget - 1 + n) % n == concaveIndex)
        splitTarget = 4;

    // Offset polygon
    std::vector<Point> offsetPoly;
    int offsetX = 300;
    for (auto &p : concavePoly)
        offsetPoly.push_back({p.x + offsetX, p.y});

    std::vector<Point> poly1, poly2;
    int i = concaveIndex;
    while (true)
    {
        poly1.push_back(offsetPoly[i]);
        if (i == splitTarget)
            break;
        i = (i + 1) % n;
    }

    i = concaveIndex;
    while (true)
    {
        poly2.push_back(offsetPoly[i]);
        if (i == (splitTarget - 1 + n) % n)
            break;
        i = (i - 1 + n) % n;
    }
    poly2.push_back(offsetPoly[splitTarget]);

    // Draw split polygons
    drawPolygon(poly1, 0.0, 1.0, 0.0);
    drawPolygon(poly2, 0.0, 0.0, 1.0);

    glColor3f(0, 0, 0);
    glBegin(GL_LINE_LOOP);
    for (auto &p : offsetPoly)
        glVertex2f(p.x, p.y);
    glEnd();

    // Draw diagonal line used to split
    drawLine(concavePoly[concaveIndex], concavePoly[splitTarget], 0, 0, 0); // left
    drawLine(offsetPoly[concaveIndex], offsetPoly[splitTarget], 0, 0, 0);   // right

    drawText(360, 270, "Split Using Vector Method");

    glFlush();
}

void init()
{
    glClearColor(1, 1, 1, 1);
    glMatrixMode(GL_PROJECTION);
    gluOrtho2D(0, 700, 0, 300);
}

int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(700, 300);
    glutCreateWindow("Concave Polygon Split - Vector Method");
    init();
    glutDisplayFunc(display);
    glutMainLoop();
    return 0;
}
