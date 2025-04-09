#include <GL/glut.h>
#include <iostream>
#include <cmath>


void drawBresenhamCircle(int xc, int yc, int r, bool fill = false) {
    
    if (fill) {
        glBegin(GL_TRIANGLE_FAN);
    } else {
        glBegin(GL_LINE_LOOP);  
    }
    
    // Center point
    glVertex2f(xc, yc);
    
    // Calculate points around the circle
    const int segments = 360;  
    for (int i = 0; i <= segments; i++) {
        float angle = 2.0f * M_PI * i / segments;
        float x = xc + r * cos(angle);
        float y = yc + r * sin(angle);
        glVertex2f(x, y);
    }
    
    glEnd();
}


void display() {
    glClear(GL_COLOR_BUFFER_BIT);
    
    

    glColor3f(0.0, 1.0, 1.0);  // Cyan color (#00FFFF)
    drawBresenhamCircle(-1, -1, 6, true);

    glLineWidth(2.0);  
    glColor3f(1.0, 0.0, 0.0);  // Red color
    drawBresenhamCircle(3, 5, 6, false);
    
    
    glPointSize(5.0);
    glBegin(GL_POINTS);
    
    
    glColor3f(0.0, 1.0, 1.0);
    // Center point
    glVertex2f(-1, -1);
    // Points at radius distance (6 units)
    glVertex2f(-1, 5);     // Top
    glVertex2f(-1, -7);    // Bottom
    glVertex2f(5, -1);     // Right
    glVertex2f(-7, -1);    // Left
    
    // Points for second circle (red)
    glColor3f(1.0, 0.0, 0.0);
    // Center point
    glVertex2f(3, 5);
    // Points at radius distance (6 units)
    glVertex2f(3, 11);    // Top
    glVertex2f(3, -1);    // Bottom
    glVertex2f(9, 5);     // Right
    glVertex2f(-3, 5);    // Left
    glEnd();
    

    glLineWidth(1.0);  
    glColor3f(1.0, 1.0, 1.0);  // White color for axes
    glBegin(GL_LINES);
    // X-axis
    glVertex2i(-15, 0);
    glVertex2i(15, 0);
    // Y-axis
    glVertex2i(0, -15);
    glVertex2i(0, 15);
    
    
    for (int i = -15; i <= 15; i++) {
        if (i != 0) {  
            glVertex2i(i, -0.1);
            glVertex2i(i, 0.1);
        }
    }
    
    
    for (int i = -15; i <= 15; i++) {
        if (i != 0) {  
            glVertex2i(-0.1, i);
            glVertex2i(0.1, i);
        }
    }
    glEnd();
    
    // Draw coordinate points for circles with small dots
    glPointSize(3.0);
    glBegin(GL_POINTS);
    // Point for first circle (3, 5)
    glColor3f(1.0, 0.0, 0.0);  // Red
    glVertex2i(3, 5);
    // Point for second circle (-1, -1)
    glColor3f(0.0, 1.0, 1.0);  // Cyan
    glVertex2i(-1, -1);
    glEnd();
    
    // Draw axis labels and numbers in white
    glColor3f(1.0, 1.0, 1.0);
    // X-axis label
    glRasterPos2f(14, 0.3);
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, 'X');
    // Y-axis label
    glRasterPos2f(0.3, 14);
    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, 'Y');
    
    // Draw numbers on X-axis (every unit)
    for (int i = -15; i <= 15; i++) {
        if (i != 0) {  // Skip origin
            glRasterPos2f(i - 0.1, -0.4);
            std::string num = std::to_string(i);
            for (char c : num) {
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c);
            }
        }
    }
    
    // Draw numbers on Y-axis (every unit)
    for (int i = -15; i <= 15; i++) {
        if (i != 0) {  // Skip origin
            glRasterPos2f(-0.5, i - 0.1);
            std::string num = std::to_string(i);
            for (char c : num) {
                glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c);
            }
        }
    }
    
    // Draw coordinate labels for the circles
    // First circle coordinates
    glRasterPos2f(3.2, 5.2);
    std::string coord1 = "(3, 5)";
    for (char c : coord1) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c);
    }
    
    // Second circle coordinates
    glRasterPos2f(-0.8, -1.4);
    std::string coord2 = "(-1, -1)";
    for (char c : coord2) {
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_10, c);
    }
    
    glFlush();
}

// Reshape callback function
void reshape(int width, int height) {
    glViewport(0, 0, width, height);
    glMatrixMode(GL_PROJECTION);
    glLoadIdentity();
    
    // Set up coordinate system (-15 to 15 on both axes) to fit the circles
    gluOrtho2D(-15, 15, -15, 15);
    
    glMatrixMode(GL_MODELVIEW);
    glLoadIdentity();
}

// Main function
int main(int argc, char** argv) {
    glutInit(&argc, argv);
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB);
    glutInitWindowSize(800, 600);
    glutInitWindowPosition(100, 100);
    glutCreateWindow("Bresenham Circle Drawing");
    
    glClearColor(0.0, 0.0, 0.0, 0.0);  // Black background
    
    glutDisplayFunc(display);
    glutReshapeFunc(reshape);
    
    glutMainLoop();
    
    return 0;
}