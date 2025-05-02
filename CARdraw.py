from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
total_distance = 0.0
headlight_opacity = 0.5  # Default opacity for headlightsq
# Car movement physics
speed = 2
max_speed = 2
acceleration = 0.05
deceleration = 0.15
steering_speed = 0.3
game_over = False
keys_pressed = set()  # Track which keys are currently pressed
steering_angle = 0  # Current steering angle
max_steering_angle = 30  # Maximum steering angle
steering_return_speed = 1.0

def draw_car(x, y, z, car_color=(1.0, 0.0, 0.0)):
    global total_distance, steering_angle, speed
    glPushMatrix()
    glTranslatef(x, y, z)

    # Wheel parameters
    wheel_radius = 15
    wheel_width = 12
    wheel_circumference = 2 * math.pi * wheel_radius
    # Calculate rolling angle (in degrees)
    rolling_angle = (total_distance / wheel_circumference) * 360.0

    # Front-left wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)  # Dark gray for tires
    glTranslatef(40, -30, 30)  # Front-left wheel position
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    # Visual marker to see rotation
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red marker
    glTranslatef(wheel_radius, 0, 0)  # On tire’s rim
    glScalef(5, 2, 2)
    glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()

    # Front-right wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(40, -30, -40)  # Front-right wheel position
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 20, 20)
    glPopMatrix()

    # Back-left wheel (no steering)
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-40, -30, 30)  # Back-left wheel position
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 20, 20)
    glPopMatrix()

    # Back-right wheel (no steering)
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-40, -30, -40)  # Back-right wheel position
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 20, 20)
    glPopMatrix()

    # Body (two cubes to simulate smoother edges)
    glPushMatrix()
    glColor3f(*car_color)
    glScalef(80, 15, 30)
    glutSolidCube(2.5)
    glPopMatrix()
    glPushMatrix()
    glColor3f(car_color[0] * 0.9, car_color[1] * 0.9, car_color[2] * 0.9)
    glTranslatef(0, 5, 0)
    glScalef(75, 12, 28)
    glutSolidCube(2.5)
    glPopMatrix()

    # Roof
    glPushMatrix()
    glColor3f(car_color[0] * 0.8, car_color[1] * 0.8, car_color[2] * 0.8)
    glTranslatef(0, 30, 0)
    glScalef(30, 15, 28)
    glutSolidCube(2)
    glPopMatrix()

    #  Windows
    glColor4f(0.2, 0.2, 0.2, 0.5)
    thickness = 1

    glPushMatrix()
    v1 = (28, 40, 28)
    v2 = (-28, 40, 28)
    v3 = (-72, 18.75, 28)
    v4 = (72, 18.75, 28)
    glBegin(GL_QUADS)
    glVertex3f(*v1)
    glVertex3f(*v2)
    glVertex3f(*v3)
    glVertex3f(*v4)
    glVertex3f(v1[0], v1[1], v1[2] + thickness)
    glVertex3f(v2[0], v2[1], v2[2] + thickness)
    glVertex3f(v3[0], v3[1], v3[2] + thickness)
    glVertex3f(v4[0], v4[1], v4[2] + thickness)
    glEnd()
    glPopMatrix()

    # Right Side Window
    glPushMatrix()
    v1 = (28, 40, -28)
    v2 = (-28, 40, -28)
    v3 = (-72, 18.75, -28)
    v4 = (72, 18.75, -28)
    glBegin(GL_QUADS)
    glVertex3f(*v1)
    glVertex3f(*v2)
    glVertex3f(*v3)
    glVertex3f(*v4)
    glVertex3f(v1[0], v1[1], v1[2] - thickness)
    glVertex3f(v2[0], v2[1], v2[2] - thickness)
    glVertex3f(v3[0], v3[1], v3[2] - thickness)
    glVertex3f(v4[0], v4[1], v4[2] - thickness)
    glEnd()
    glPopMatrix()

    # Windshield
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(50, 35, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-61, 1, 0, 0)
    glScalef(63, 40, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Rear Windshield
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(-50, 35, 0)
    glRotatef(-90, 0, 1, 0)
    glRotatef(-61, 1, 0, 0)
    glScalef(63, 40, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Left side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(58, 17, 48)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 8, 8)

    glPopMatrix()
    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(58, 17, 58)
    glRotatef(-180, 1, 0, 1)
    glScalef(5, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Right side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(63, 25, -52)
    glRotatef(-110, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 2, 2, 4, 8, 8)
    glPopMatrix()
    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(63, 25, -58)
    glRotatef(180, 1, 0, 1)
    glScalef(4, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Headlights
    headlight_radius = 5
    headlight_depth = 8

    # Left headlight (cylindrical housing)
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(90, 15, 20)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)  # Cylinder
    glPopMatrix()

    # Left headlight (conical light beam)
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, 0.5)
    glTranslatef(90 + headlight_depth, 15, 20)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Right headlight (cylindrical housing)
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(90, 15, -20)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Right headlight (conical light beam)
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, 0.5)
    glTranslatef(90 + headlight_depth, 15, -20)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    glPopMatrix()


def draw_truck(x, y, z, truck_color=(0.96, 0.96, 0.86)):  # Default color: beige
    global headlight_opacity, total_distance, steering_angle, speed
    glPushMatrix()
    glTranslatef(x, y, z)

    # Wheels (simplified style from your car code)
    wheel_radius = 20
    wheel_width = 15
    wheel_circumference = 2 * math.pi * wheel_radius
    # Calculate rolling angle (in degrees)
    rolling_angle = (total_distance / wheel_circumference) * 360.0

    # Front-left wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(100, -30, 35)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)

    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red marker
    glTranslatef(wheel_radius, 0, 0)  # On tire’s rim
    glScalef(5, 2, 2)
    glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()


    # Front-right wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(100, -30, -45)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-left wheels (dual wheels)
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-70, -30, 25)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-70, -30, 40)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-right wheels (dual wheels)
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-70, -30, -40)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-70, -30, -55)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Cab (two parts: base and top)
    # Base of the cab
    glPushMatrix()
    glColor3f(*truck_color)
    glTranslatef(50, 5, 0)
    glScalef(80, 20, 30)
    glutSolidCube(2.5)
    glPopMatrix()
    # Top of the cab
    glPushMatrix()
    glColor3f(*truck_color)
    glTranslatef(50, 40, 0)
    glScalef(10, 10, 10)
    glutSolidCube(2.5)
    glPopMatrix()

    # Cargo Box
    glPushMatrix()
    glColor3f(truck_color[0] * 0.7, truck_color[1] * 0.7, truck_color[2] * 0.7)
    glTranslatef(-20, 25, 0)
    glScalef(90, 30, 35)
    glutSolidCube(2.5)
    glPopMatrix()

    # Cargo Box Panels (vertical ribs for detail)
    glPushMatrix()
    glColor3f(truck_color[0] * 0.6, truck_color[1] * 0.6, truck_color[2] * 0.6)
    glTranslatef(-20, 25, 43)
    glScalef(65, 15, 1)
    glutSolidCube(2.5)
    glPopMatrix()
    glPushMatrix()
    glColor3f(truck_color[0] * 0.6, truck_color[1] * 0.6, truck_color[2] * 0.6)
    glTranslatef(-20, 25, -43)
    glScalef(65, 15, 1)
    glutSolidCube(2.5)
    glPopMatrix()

    # Cargo Box Rear Door Outline
    glPushMatrix()
    glColor3f(truck_color[0] * 0.6, truck_color[1] * 0.6, truck_color[2] * 0.6)
    glTranslatef(-133, 25, 0)
    glScalef(1, 20, 25)
    glutSolidCube(2.5)
    glPopMatrix()

    # Exhaust Pipe (on the right side)
    glPushMatrix()
    glColor3f(0.4, 0.4, 0.4)
    glTranslatef(50, 30, -50)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 5, 5, 20, 10, 10)
    glPopMatrix()

    # Left side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(120, 17, 48)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 10, 8, 8)
    glPopMatrix()

    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(120, 17, 58)
    glRotatef(-180, 1, 0, 1)
    glScalef(5, 4, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Right side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(120, 17, -48)
    glRotatef(-110, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 2, 2, 10, 8, 8)
    glPopMatrix()

    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(120, 17, -58)
    glRotatef(180, 1, 0, 1)
    glScalef(5, 4, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Windshield
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(110, 20, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-45, 1, 0, 0)
    glScalef(80, 40, 1)
    glutSolidCube(1)
    glPopMatrix()



    # Headlights
    headlight_radius = 5
    headlight_depth = 8

    # Left headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(125, 10, 25)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Left headlight
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, 0.5)
    glTranslatef(125 + headlight_depth, 10, 25)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Right headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(125, 10, -25)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Right headlight
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, 0.5)
    glTranslatef(125 + headlight_depth, 10, -25)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Roof (slightly darker)
    glPushMatrix()
    glColor3f(truck_color[0] * 0.8, truck_color[1] * 0.8, truck_color[2] * 0.8)
    glTranslatef(-15, 70, 0)
    glScalef(85, 5, 30)
    glutSolidCube(2.5)
    glPopMatrix()

    glPopMatrix()


def draw_bus(x, y, z, bus_color=(0.9, 0.9, 0.1)):

    global  total_distance, steering_angle, speed

    glPushMatrix()
    glTranslatef(x, y, z)

    # Wheels
    wheel_radius = 30
    wheel_width = 25

    wheel_circumference = 2 * math.pi * wheel_radius
    # Calculate rolling angle (in degrees)
    rolling_angle = (total_distance / wheel_circumference) * 360.0

    # Front-left wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(100, -30, 55)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Front-right wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(100, -30, -80)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-left wheels
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-110, -30, 45)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-110, -30, 60)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-right wheels
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-110, -30, -80)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-110, -30, -65)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Main Body
    glPushMatrix()
    glColor3f(*bus_color)
    glTranslatef(0, 20, 0)
    glScalef(150, 50, 50)
    glutSolidCube(2.5)
    glPopMatrix()

    # Door
    glPushMatrix()
    glColor3f(bus_color[0] * 0.7, bus_color[1] * 0.7, bus_color[2] * 0.7)
    glTranslatef(80, 20, -51)
    glScalef(15, 30, 1)
    glutSolidCube(2.5)
    glPopMatrix()
    # Door window
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(80, 40, -51)
    glScalef(10, 10, 1)
    glutSolidCube(2.5)
    glPopMatrix()

    # Windows
    window_color = (0.2, 0.2, 0.2, 0.5)
    for i in range(-80, 60, 30):
        # Left side windows
        glPushMatrix()
        glColor4f(*window_color)
        glTranslatef(i, 40, 51)
        glScalef(10, 10, 1)
        glutSolidCube(2.5)
        glPopMatrix()
        # Right side windows
        glPushMatrix()
        glColor4f(*window_color)
        glTranslatef(i, 40, -51)
        glScalef(10, 10, 1)
        glutSolidCube(2.5)
        glPopMatrix()

    # Front Windshield
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(180, 40, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-0, 1, 0, 0)
    glScalef(80, 40, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Headlights
    headlight_radius = 5
    headlight_depth = 8

    # Left headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(190, 10, 80)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Left headlight
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, headlight_opacity)
    glTranslatef(200, 10, 80)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Right headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(190, 10, -80)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Right headlight
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, headlight_opacity)
    glTranslatef(200, 10, -80)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Roof (slightly darker)
    glPushMatrix()
    glColor3f(bus_color[0] * 0.8, bus_color[1] * 0.8, bus_color[2] * 0.8)
    glTranslatef(0, 70, 0)
    glScalef(145, 5, 40)
    glutSolidCube(2.5)
    glPopMatrix()

    glPopMatrix()


def draw_suv(x, y, z, car_color=(0.0, 0.5, 0.0)):

    global total_distance, steering_angle, speed

    glPushMatrix()
    glTranslatef(x, y, z)

    # Wheels
    wheel_radius = 20
    wheel_width = 15
    wheel_circumference = 2 * math.pi * wheel_radius
    # Calculate rolling angle (in degrees)
    rolling_angle = (total_distance / wheel_circumference) * 360.0

    # Front-left wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(50, -25, 40)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red marker
    glTranslatef(wheel_radius, 0, 0)  # On tire’s rim
    glScalef(5, 2, 2)
    glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()

    # Front-right wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(50, -25, -55)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-left wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-30, -25, 40)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-right wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-30, -25, -55)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Main Body
    glPushMatrix()
    glColor3f(*car_color)
    glTranslatef(0, 10, 0)
    glScalef(65, 30, 35)
    glutSolidCube(2.5)
    glPopMatrix()

    # Roof
    glPushMatrix()
    glColor3f(car_color[0] * 0.9, car_color[1] * 0.9, car_color[2] * 0.9)
    glTranslatef(0, 40, 0)
    glScalef(55, 5, 30)
    glutSolidCube(2.5)
    glPopMatrix()

    # Hood
    glPushMatrix()
    glColor3f(car_color[0] * 0.8, car_color[1] * 0.8, car_color[2] * 0.8)
    glTranslatef(50, 5, 0)
    glScalef(25, 20, 30)
    glutSolidCube(2.5)
    glPopMatrix()

    # Front Grille
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(75, 10, 0)
    glScalef(1, 15, 25)
    glutSolidCube(2.5)
    glPopMatrix()

    # Grille accents
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(75, 12, 0)
    glScalef(1, 2, 20)
    glutSolidCube(2.5)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(75, 8, 0)
    glScalef(1, 2, 20)
    glutSolidCube(2.5)
    glPopMatrix()

    # Windshield (front)
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(60, 30, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-30, 1, 0, 0)
    glScalef(50, 25, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Rear Windshield
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(-40, 30, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(30, 1, 0, 0)
    glScalef(50, 25, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Side Windows
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(10, 30, 35)
    glScalef(40, 15, 1)
    glutSolidCube(2.5)
    glPopMatrix()
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(10, 30, -35)
    glScalef(40, 15, 1)
    glutSolidCube(2.5)
    glPopMatrix()

    # Roof Rails
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 45, 15)
    glScalef(50, 1, 1)
    glutSolidCube(2.5)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(0, 45, -15)
    glScalef(50, 1, 1)
    glutSolidCube(2.5)
    glPopMatrix()

    # Headlights
    headlight_radius = 5
    headlight_depth = 8

    # Left headlight (cylindrical housing)
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(70, 15, 20)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Left headlight (conical light beam)
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, 0.5)
    glTranslatef(70 + headlight_depth, 15, 20)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Right headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(70, 15, -20)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Right headlight
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, 0.5)
    glTranslatef(70 + headlight_depth, 15, -20)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Left side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(50, 25, 36)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 8, 8)
    glPopMatrix()

    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(50, 25, 41)
    glRotatef(-180, 1, 0, 1)
    glScalef(5, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Right side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(50, 25, -36)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 8, 8)
    glPopMatrix()

    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(50, 25, -41)
    glRotatef(180, 1, 0, 1)
    glScalef(5, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Roof
    glPushMatrix()
    glColor3f(car_color[0] * 0.8, car_color[1] * 0.8, car_color[2] * 0.8)
    glTranslatef(0, 50, 0)
    glScalef(50, 2, 30)
    glutSolidCube(2.5)
    glPopMatrix()

    glPopMatrix()


def draw_pickup_truck(x, y, z, car_color=(0.7, 0.3, 0.0)):

    global total_distance, steering_angle, speed

    glPushMatrix()
    glTranslatef(x, y, z)

    # Wheels
    wheel_radius = 18
    wheel_width = 12
    wheel_circumference = 2 * math.pi * wheel_radius
    # Calculate rolling angle (in degrees)
    rolling_angle = (total_distance / wheel_circumference) * 360.0

    # Front-left wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(50, -20, 40)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red marker
    glTranslatef(wheel_radius, 0, 0)  # On tire’s rim
    glScalef(5, 2, 2)
    glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()

    # Front-right wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(50, -20, -50)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-left wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-60, -20, 40)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Back-right wheel
    glPushMatrix()
    glColor3f(0.1, 0.1, 0.1)
    glTranslatef(-60, -20, -50)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 10, 10)
    glPopMatrix()

    # Cab
    glPushMatrix()
    glColor3f(*car_color)
    glTranslatef(30, 5, 0)
    glScalef(40, 20, 30)
    glutSolidCube(2.5)
    glPopMatrix()

    # Cab Roof
    glPushMatrix()
    glColor3f(car_color[0] * 0.9, car_color[1] * 0.9, car_color[2] * 0.9)
    glTranslatef(20, 35, 0)
    glScalef(20, 5, 25)
    glutSolidCube(2.5)
    glPopMatrix()

    # Cargo Bed
    glPushMatrix()
    glColor3f(car_color[0] * 0.8, car_color[1] * 0.8, car_color[2] * 0.8)
    glTranslatef(-30, 0, 0)
    glScalef(50, 10, 35)
    glutSolidCube(2.5)
    glPopMatrix()

    # Cargo Sides
    glPushMatrix()
    glColor3f(car_color[0] * 0.7, car_color[1] * 0.7, car_color[2] * 0.7)
    glTranslatef(-30, 10, 35)
    glScalef(45, 10, 1)
    glutSolidCube(2.5)
    glPopMatrix()
    glPushMatrix()
    glColor3f(car_color[0] * 0.7, car_color[1] * 0.7, car_color[2] * 0.7)
    glTranslatef(-30, 10, -35)
    glScalef(45, 10, 1)
    glutSolidCube(2.5)
    glPopMatrix()

    # Front Grille
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(75, 5, 0)
    glScalef(1, 5, 25)
    glutSolidCube(2.5)
    glPopMatrix()

    # Windshield (front)
    glPushMatrix()
    glColor4f(0.2, 0.2, 0.2, 0.5)
    glTranslatef(60, 30, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-50, 1, 0, 0)
    glScalef(60, 30, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Left side mirror
    # Mirror arm (metallic cylinder)
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(65, 20, 48)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 8, 8)
    glPopMatrix()

    # Mirror surface (reflective rectangle)
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(65, 20, 53)
    glRotatef(-180, 1, 0, 1)
    glScalef(5, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Right side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(65, 20, -48)
    glRotatef(-90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 8, 8)
    glPopMatrix()

    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(65, 20, -53)
    glRotatef(180, 1, 0, 1)
    glScalef(5, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Headlights
    headlight_radius = 5
    headlight_depth = 8

    # Left headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(75, 10, 20)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Left headlight
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, headlight_opacity)
    glTranslatef(75, 10, 20)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    # Right headlight (cylindrical housing)
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(78, 10, -20)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 10, 10)
    glPopMatrix()

    # Right headlight (conical light beam)
    glPushMatrix()
    glColor4f(1.0, 1.0, 0.8, headlight_opacity)
    glTranslatef(78, 10, -20)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 10, 10, 10)
    glPopMatrix()

    glPopMatrix()


def draw_sports_car(x, y, z, car_color=(0.1, 0.1, 0.9)):

    global total_distance, steering_angle, speed

    glPushMatrix()
    glTranslatef(x, y, z)

    # Wheels
    wheel_radius = 25
    wheel_width = 25
    wheel_circumference = 2 * math.pi * wheel_radius
    # Calculate rolling angle (in degrees)
    rolling_angle = (total_distance / wheel_circumference) * 360.0

    # Front-left wheel
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(60, -15, 45)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 12, 12)
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)  # Red marker
    glTranslatef(wheel_radius, 0, 0)  # On tire’s rim
    glScalef(5, 2, 4)
    glutSolidCube(1.0)
    glPopMatrix()
    glPopMatrix()

    # Front-right wheel
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(60, -15, -65)
    glRotatef(steering_angle, 0, 1, 0)  # Steering rotation (Y-axis)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 12, 12)
    glPopMatrix()

    # Rear-left wheel
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(-60, -15, 45)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 12, 12)
    glPopMatrix()

    # Rear-right wheel
    glPushMatrix()
    glColor3f(0.2, 0.2, 0.2)
    glTranslatef(-60, -15, -65)
    if speed >= 0:
        glRotatef(rolling_angle, 0, 0, 1)
    else:
        glRotatef(-rolling_angle, 0, 0, 1)
    gluCylinder(gluNewQuadric(), wheel_radius, wheel_radius, wheel_width, 12, 12)
    glPopMatrix()

    # Main Body
    glPushMatrix()
    glColor3f(*car_color)
    glTranslatef(0, 0, 0)
    glScalef(110, 15, 45)
    glutSolidCube(2.5)
    glPopMatrix()

    # Hood
    glPushMatrix()
    glColor3f(car_color[0] * 0.95, car_color[1] * 0.95, car_color[2] * 0.95)
    glTranslatef(50, 10, 0)
    glRotatef(-10, 0, 0, 1)
    glScalef(60, 10, 40)
    glutSolidCube(2.5)
    glPopMatrix()

    # Roof
    glPushMatrix()
    glColor3f(car_color[0] * 0.9, car_color[1] * 0.9, car_color[2] * 0.9)
    glTranslatef(0, 25, 0)
    glScalef(50, 8, 30)
    glutSolidCube(2.5)
    glPopMatrix()

    # Front Windshield
    glPushMatrix()
    glColor4f(0.1, 0.1, 0.1, 0.6)
    glTranslatef(35, 20, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(-70, 1, 0, 0)
    glScalef(80, 25, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Rear Windshield
    glPushMatrix()
    glColor4f(0.1, 0.1, 0.1, 0.6)
    glTranslatef(-35, 20, 0)
    glRotatef(90, 0, 1, 0)
    glRotatef(60, 1, 0, 0)
    glScalef(70, 25, 1)
    glutSolidCube(1)
    glPopMatrix()

    # Rear Spoiler
    glPushMatrix()
    glColor3f(car_color[0] * 0.8, car_color[1] * 0.8, car_color[2] * 0.8)
    glTranslatef(-100, 20, 0)
    glScalef(20, 2, 40)
    glutSolidCube(2.5)
    glPopMatrix()

    # Headlights
    headlight_radius = 3
    headlight_depth = 6

    # Left headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(135, 10, 30)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 12, 12)
    glPopMatrix()

    # Left headlight
    glPushMatrix()
    glDepthMask(GL_FALSE)
    glColor4f(1.0, 1.0, 0.9, 0.5)
    glTranslatef(140, 10, 30)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 8, 12, 12)
    glDepthMask(GL_TRUE)
    glPopMatrix()

    # Right headlight
    glPushMatrix()
    glColor3f(0.7, 0.7, 0.7)
    glTranslatef(135, 10, -30)
    glRotatef(90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, headlight_radius, headlight_depth, 12, 12)
    glPopMatrix()

    glPushMatrix()
    glDepthMask(GL_FALSE)
    glColor4f(1.0, 1.0, 0.9, 0.5)
    glTranslatef(140, 10, -30)
    glRotatef(-90, 0, 1, 0)
    quad = gluNewQuadric()
    gluCylinder(quad, headlight_radius, 0, 8, 12, 12)
    glDepthMask(GL_TRUE)
    glPopMatrix()

    # Front
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(100, 5, 0)
    glScalef(5, 5, 30)
    glutSolidCube(2.5)
    glPopMatrix()

    # Left side mirror
    # Mirror arm (metallic cylinder)
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(58, 17, 48)
    glRotatef(90, 1, 0, 0)
    gluCylinder(gluNewQuadric(), 2, 2, 5, 8, 8)
    glPopMatrix()

    # Mirror surface (reflective rectangle)
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(58, 17, 58)
    glRotatef(-180, 1, 0, 1)
    glScalef(5, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Right side mirror
    # Mirror arm
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(58, 17, -52)
    glRotatef(-110, 0, 0, 1)
    gluCylinder(gluNewQuadric(), 2, 2, 4, 8, 8)
    glPopMatrix()

    # Mirror surface
    glPushMatrix()
    glColor3f(0.9, 0.9, 0.9)
    glTranslatef(58, 17, -58)
    glRotatef(180, 1, 0, 1)
    glScalef(4, 2, 0.5)
    glutSolidCube(2.5)
    glPopMatrix()

    # Exhaust Pipes
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(-100, 5, 20)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 3, 3, 10, 10, 10)
    glPopMatrix()
    glPushMatrix()
    glColor3f(0.5, 0.5, 0.5)
    glTranslatef(-100, 5, -20)
    glRotatef(90, 0, 1, 0)
    gluCylinder(gluNewQuadric(), 3, 3, 10, 10, 10)
    glPopMatrix()

    glPopMatrix()