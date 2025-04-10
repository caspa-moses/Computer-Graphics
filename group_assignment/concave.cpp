#include <GL/glut.h>
#include <iostream>
#include <vector>
#include <cmath>

struct Point
{
    float x, y;
    Point(float x_, float y_) : x(x_), y(y_) {}
};

std::vector<Point> concavePoly = {
    Point(100, 200), // P1
    Point(150, 250), // P2
    Point(200, 200), // P3
    Point(150, 150), // P4 <- concave
    Point(150, 100)  // P5
};

float crossZ(const Point &a, const Point &b, const Point &c)
{
    float abx = b.x - a.x;
    float aby = b.y - a.y;
    float bcx = c.x - b.x;
    float bcy = c.y - b.y;
    return abx * bcy - aby * bcx;
}

int findConcaveIndex(const std::vector<Point> &poly)
{
    int n = poly.size();
    for (int i = 0; i < n; ++i)
    {
        Point prev = poly[(i - 1 + n) % n];
        Point curr = poly[i];
        Point next = poly[(i + 1) % n];
        if (crossZ(prev, curr, next) < 0)
        {
            return i;
        }
    }
    return -1;
}

Point vectorIntersection(const Point &p1, const Point &p2, const Point &q1, const Point &q2)
{
    auto det = [](float a, float b, float c, float d)
    {
        return a * d - b * c;
    };

    float a1 = p2.y - p1.y, b1 = p1.x - p2.x;
    float c1 = a1 * p1.x + b1 * p1.y;

    float a2 = q2.y - q1.y, b2 = q1.x - q2.x;
    float c2 = a2 * q1.x + b2 * q1.y;

    float determinant = det(a1, b1, a2, b2);
    if (determinant == 0)
        return Point(-1, -1); // Parallel lines

    float x = det(c1, b1, c2, b2) / determinant;
    float y = det(a1, c1, a2, c2) / determinant;
    return Point(x, y);
}

void drawPolygon(const std::vector<Point> &poly, const float color[3])
{
    glColor3fv(color);
    glBegin(GL_POLYGON);
    for (const auto &p : poly)
    {
        glVertex2f(p.x, p.y);
    }
    glEnd();
}

void drawOutline(const std::vector<Point> &poly, const float color[3])
{
    glColor3fv(color);
    glBegin(GL_LINE_LOOP);
    for (const auto &p : poly)
    {
        glVertex2f(p.x, p.y);
    }
    glEnd();
}

void drawLine(const Point &a, const Point &b, const float color[3])
{
    glColor3fv(color);
    glBegin(GL_LINES);
    glVertex2f(a.x, a.y);
    glVertex2f(b.x, b.y);
    glEnd();
}

std::vector<Point> translatePolygon(const std::vector<Point> &poly, float dx, float dy)
{
    std::vector<Point> translated;
    for (const auto &p : poly)
    {
        translated.push_back(Point(p.x + dx, p.y + dy));
    }
    return translated;
}

void splitPolygon(const std::vector<Point> &poly, std::vector<Point> &poly1, std::vector<Point> &poly2, int &concaveIndex, int &splitIndex)
{
    int n = poly.size();
    concaveIndex = findConcaveIndex(poly);

    if (concaveIndex == -1)
    {
        poly1 = poly; // Already convex
        return;
    }

    // Find a valid split line using vector intersection
    Point concavePoint = poly[concaveIndex];
    for (int i = 0; i < n; ++i)
    {
        if (i == concaveIndex || i == (concaveIndex - 1 + n) % n || i == (concaveIndex + 1) % n)
        {
            continue;
        }
        Point splitPoint = poly[i];

        // Check if the line intersects with any other edges
        bool valid = true;
        for (int j = 0; j < n; ++j)
        {
            Point p1 = poly[j];
            Point p2 = poly[(j + 1) % n];
            if (p1.x == concavePoint.x && p1.y == concavePoint.y || p2.x == concavePoint.x && p2.y == concavePoint.y ||
                p1.x == splitPoint.x && p1.y == splitPoint.y || p2.x == splitPoint.x && p2.y == splitPoint.y)
            {
                continue;
            }
            if (vectorIntersection(concavePoint, splitPoint, p1, p2).x != -1)
            {
                valid = false;
                break;
            }
        }

        if (valid)
        {
            splitIndex = i;
            break;
        }
    }

    // Form two new polygons
    poly1.clear();
    int i = concaveIndex;
    while (true)
    {
        poly1.push_back(poly[i]);
        if (i == splitIndex)
        {
            break;
        }
        i = (i + 1) % n;
    }

    poly2.clear();
    i = concaveIndex;
    while (true)
    {
        poly2.push_back(poly[i]);
        if (i == (splitIndex - 1 + n) % n)
        {
            break;
        }
        i = (i - 1 + n) % n;
    }
    poly2.push_back(poly[splitIndex]);
}

void display()
{
    glClear(GL_COLOR_BUFFER_BIT);

    // Draw the original concave polygon on the left
    const float red[3] = {1.0f, 0.0f, 0.0f};
    drawOutline(concavePoly, red);

    // Split the polygon into two convex parts
    std::vector<Point> poly1, poly2;
    int concaveIndex, splitIndex;
    splitPolygon(concavePoly, poly1, poly2, concaveIndex, splitIndex);

    // Draw the split line on the original polygon
    const float black[3] = {0.0f, 0.0f, 0.0f};
    drawLine(concavePoly[concaveIndex], concavePoly[splitIndex], black);

    // Translate the split polygons to the right side with more spacing
    poly1 = translatePolygon(poly1, 350, 50);
    poly2 = translatePolygon(poly2, 350, -50);

    // Draw the split polygons on the right
    const float green[3] = {0.3f, 0.8f, 0.3f};
    drawPolygon(poly1, green);
    drawOutline(poly1, green);

    const float blue[3] = {0.2f, 0.4f, 0.9f};
    drawPolygon(poly2, blue);
    drawOutline(poly2, blue);

    glutSwapBuffers();
}

void initOpenGL()
{
    glClearColor(1.0f, 1.0f, 1.0f, 1.0f); // Set background color to white
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    glOrtho(0, 700, 0, 300, -1, 1); // Set orthographic view
}

int main(int argc, char **argv)
{
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB);
    glutInitWindowSize(700, 300);
    glutCreateWindow("Concave Polygon Split");

    initOpenGL();

    glutDisplayFunc(display); // Set display function
    glutMainLoop();           // Enter GLUT event processing loop

    return 0;
}
