from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

# Constants
NUM_BULLETS = 90
NUM_BUBBLES = random.randint(3, 5)
points = 0
missed = 3

class Bullet:
    def __init__(self):
        self.X_center = 0
        self.Y_center = 0
        self.r = 10
        self.active = False
        self.speed = 1.5

class Bubble:
    def __init__(self):
        self.X_center = 0
        self.Y_center = 0
        self.r = 20
        self.speed = random.uniform(1.0, 1.5)

shooter_X_center = 250
shooter_Y_center = 30
shooter_r = 20

bullets = [Bullet() for _ in range(NUM_BULLETS)]
bubbles = [Bubble() for _ in range(NUM_BUBBLES)]

def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def mid_point_circle_draw(x_center, y_center, radius):
    x_main = 0
    y_main = radius
    d_initial = 1 - radius

    while x_main < y_main:
        draw_points(x_main + x_center, y_main + y_center)
        draw_points(-x_main + x_center, y_main + y_center)
        draw_points(x_main + x_center, -y_main + y_center)
        draw_points(-x_main + x_center, -y_main + y_center)
        draw_points(y_main + x_center, x_main + y_center)
        draw_points(-y_main + x_center, x_main + y_center)
        draw_points(y_main + x_center, -x_main + y_center)
        draw_points(-y_main + x_center, -x_main + y_center)

        if d_initial >= 0:
            d_initial = d_initial + 2 *x_main - 2 * y_main + 5
            x_main = x_main + 1
            y_main = y_main - 1
        else:
            d_initial = d_initial + 2 * x_main + 3
            x_main = x_main + 1

def draw_shooter():
    global shooter_X_center, shooter_Y_center, shooter_r
    mid_point_circle_draw(shooter_X_center, shooter_Y_center, shooter_r)

def draw_bubble():
    global bubbles
    for bubble in bubbles:
        mid_point_circle_draw(bubble.X_center, bubble.Y_center, bubble.r)

def reset_bubble():
    global bubbles
    bubbles = [Bubble() for _ in range(NUM_BUBBLES)]
    for i in range(NUM_BUBBLES):
        bubbles[i].X_center = random.randint(45, 455)
        bubbles[i].Y_center = 450

def draw_bullets():
    global bullets
    for bullet in bullets:
        if bullet.active:
            mid_point_circle_draw(bullet.X_center, bullet.Y_center, bullet.r)

def update_bullets():
    global bullets
    for bullet in bullets:
        if bullet.active:
            bullet.Y_center += bullet.speed
            if bullet.Y_center + bullet.r > 500:
                bullet.active = False

def shoot_bullet():
    global bullets
    for bullet in bullets:
        if not bullet.active:
            bullet.X_center = shooter_X_center
            bullet.Y_center = shooter_Y_center
            bullet.active = True
            bullet.speed = 1.0
            break

def specialKeyboardListener(key, x, y):
    global shooter_X_center

    if key == GLUT_KEY_LEFT:
        shooter_X_center -= 20
    elif key == GLUT_KEY_RIGHT:
        shooter_X_center += 20
    shooter_X_center = max(45, min(455, shooter_X_center))
    glutPostRedisplay()

def keyboardListener(key, x, y):
    global bullet_active

    if key == b" ":
        shoot_bullet()

def check_shoot(bullet,bubble):
    distance = math.sqrt((bullet.X_center - bubble.X_center)**2 + (bullet.Y_center - bubble.Y_center)**2)
    return distance < (bullet.r + bubble.r)

def update_scene(value):
    global bullets, bubbles, points, missed

    if bubbles[0].Y_center - bubbles[0].r < 0 and bubbles != []:
        reset_bubble()

    update_bullets()

    for bullet in bullets:
        if bullet.active:
            if bubbles:
                for bubble in bubbles:
                    if check_shoot(bullet, bubble):
                        
                        bullet.active = False
                        bubbles.remove(bubble)
                        points += 1
                        print("Points:", points)
                        if bubbles == []:
                            reset_bubble()
                        break

    for bubble in bubbles:
        bubble.Y_center -= bubble.speed

        if bubble.Y_center - bubble.r <= 0:
            missed -= 1
            print("Missed:", missed)
            reset_bubble()
            break

    if missed == 0:
        print("Game Over")
        glutLeaveMainLoop()

    glutPostRedisplay()
    glutTimerFunc(16, update_scene, 0)


def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_shooter()
    draw_bubble()
    draw_bullets()
    glColor3f(random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1))
    glRasterPos2f(10, 480)
    for c in str(points):
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))
    glRasterPos2f(480, 480)
    for c in str(missed):
        glutBitmapCharacter(GLUT_BITMAP_9_BY_15, ord(c))
    glutSwapBuffers()

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow(b"OpenGL Coding Practice")
glutDisplayFunc(showScreen)
glutSpecialFunc(specialKeyboardListener)
glutKeyboardFunc(keyboardListener)
glutTimerFunc(25, update_scene, 0)

glutMainLoop()