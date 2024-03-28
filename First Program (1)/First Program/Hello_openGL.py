import sys
import random
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Constants
GRID_SIZE = 10
GRID_WIDTH = 50
GRID_HEIGHT = 50
WINDOW_WIDTH = GRID_SIZE * GRID_WIDTH
WINDOW_HEIGHT = GRID_SIZE * GRID_HEIGHT
SNAKE_INITIAL_LENGTH = 3
UPDATE_INTERVAL = 300  # milliseconds

# Directions
DIR_UP = 1
DIR_DOWN = -1
DIR_LEFT = 2
DIR_RIGHT = -2

# Colors
COLOR_SNAKE = (0, 1, 0)
COLOR_FOOD = (1, 0, 0)

# Variables
snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
direction = DIR_DOWN
food = None
score = 0

def draw_rect(x, y, color):
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(x, y)
    glVertex2f(x + GRID_SIZE, y)
    glVertex2f(x + GRID_SIZE, y + GRID_SIZE)
    glVertex2f(x, y + GRID_SIZE)
    glEnd()

def draw_snake():
    for segment in snake:
        draw_rect(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, COLOR_SNAKE)

def draw_food():
    if food:
        draw_rect(food[0] * GRID_SIZE, food[1] * GRID_SIZE, COLOR_FOOD)

def generate_food():
    global food
    while True:
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        if (x, y) not in snake:
            food = (x, y)
            break

def check_collision():
    head = snake[0]
    # Check if snake hits the walls
    if (
        head[0] < 0
        or head[0] >= GRID_WIDTH
        or head[1] < 0
        or head[1] >= GRID_HEIGHT
    ):
        return True
    # Check if snake hits itself
    if head in snake[1:]:
        return True
    return False

def update_snake():
    global direction, snake, food, score
    head = snake[0]
    if direction == DIR_UP:
        new_head = (head[0], head[1] + 1)
    elif direction == DIR_DOWN:
        new_head = (head[0], head[1] - 1)
    elif direction == DIR_LEFT:
        new_head = (head[0] - 1, head[1])
    elif direction == DIR_RIGHT:
        new_head = (head[0] + 1, head[1])

    # Check if snake eats food
    if new_head == food:
        score += 1
        snake.insert(0, new_head)
        generate_food()
    else:
        # Move snake
        snake.pop()
        snake.insert(0, new_head)

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_snake()
    draw_food()
    glutSwapBuffers()

def keyboard(key, x, y):
    global direction
    if key == GLUT_KEY_UP and direction != DIR_DOWN:
        direction = DIR_UP
    elif key == GLUT_KEY_DOWN and direction != DIR_UP:
        direction = DIR_DOWN
    elif key == GLUT_KEY_LEFT and direction != DIR_RIGHT:
        direction = DIR_LEFT
    elif key == GLUT_KEY_RIGHT and direction != DIR_LEFT:
        direction = DIR_RIGHT


def timer(value):
    update_snake()
    if check_collision():
        print("Game Over! Score:", score)
        glutLeaveMainLoop()
    glutPostRedisplay()
    glutTimerFunc(UPDATE_INTERVAL, timer, 0)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
glutCreateWindow(b"Snake Game")
glClearColor(0, 0, 0, 1)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
glutDisplayFunc(display)
glutTimerFunc(UPDATE_INTERVAL, timer, 0)
glutSpecialFunc(keyboard)
generate_food()
glutMainLoop()

