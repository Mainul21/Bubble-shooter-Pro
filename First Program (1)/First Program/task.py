import random
import math
import glut

# Initialization of variables
shooter_X_center = 250
shooter_Y_center = 450
shooter_r = 10

bullet_X_center = 0
bullet_Y_center = 0
bullet_r = 5
bullet_speed = 10
bullet_active = False

bubble_X_center = 0
bubble_Y_center = 0
bubble_r = 20
falling_speed = 0

def mid_point_circle_draw(x_center, y_center, r):
    glBegin(GL_POINTS)
    for i in range(0, 360):
        x = x_center + r * math.cos(math.radians(i))
        y = y_center + r * math.sin(math.radians(i))
        glVertex2f(x, y)
    glEnd()

def draw_shooter():
    global shooter_X_center, shooter_Y_center, shooter_r
    mid_point_circle_draw(shooter_X_center, shooter_Y_center, shooter_r)

def draw_bubble():
    global bubble_X_center, bubble_Y_center, bubble_r, falling_speed
    mid_point_circle_draw(bubble_X_center, bubble_Y_center, bubble_r)
    if bubble_Y_center - bubble_r < 0:
        reset_bubble()

def reset_bubble():
    global bubble_X_center, bubble_Y_center, bubble_r, falling_speed
    bubble_Y_center = 450
    bubble_X_center = random.randint(45, 455)
    falling_speed = random.uniform(1.0, 1.5)

def draw_bullet():
    global bullet_X_center, bullet_Y_center, bullet_r, bullet_speed
    mid_point_circle_draw(bullet_X_center, bullet_Y_center, bullet_r)

def shoot_bullet():
    global bullet_X_center, bullet_Y_center, bullet_r, bullet_active
    bullet_X_center = shooter_X_center
    bullet_Y_center = shooter_Y_center
    bullet_active = True

def update_bullet(value):
    global bullet_active, bullet_Y_center
    if bullet_active:
        bullet_Y_center -= bullet_speed
        if bullet_Y_center + bullet_r < 0:
            bullet_active = False
        glutPostRedisplay()

def check_collision():
    global bubble_X_center, bubble_Y_center, bullet_X_center, bullet_Y_center, bullet_r
    distance = math.sqrt((bubble_X_center - bullet_X_center)**2 + (bubble_Y_center - bullet_Y_center)**2)
    if distance < bubble_r + bullet_r:
        reset_bubble()
        bullet_active = False

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global bubble_X_center, bubble_Y_center, bullet_active
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    draw_shooter()
    draw_bubble()
    draw_bullet()
    check_collision()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(500,500)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Shoot The Circles!")
    glutDisplayFunc(showScreen)
    glutIdleFunc(showScreen)
    glutSpecialFunc(lambda key, x, y: glutTimerFunc(100, update_bullet, 0))

    glutMainLoop()

if __name__ == "__main__":
    main()