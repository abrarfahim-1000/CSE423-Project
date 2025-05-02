from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from CARdraw import *

# Game constants
fovY = 120
GRID_LENGTH = 600

# Car and camera settings
car_model = 'sports_car'  # Default car model
car_color = (0.1, 0.1, 0.9)  # Default car color (blue)
camera_pos = [0, 500, 500]
camera_angle = 0
camera_mode = "third_person"
player_pos = [0, 30, 0]
player_angle = 180

# Car movement physics
speed = 20
max_speed = 150
acceleration = 15
deceleration = 15
steering_speed = 3
game_over = False

# Car model selection options
car_models = {
    '1': ('car', (1.0, 0.0, 0.0)),          # Red car
    '2': ('truck', (0.96, 0.96, 0.86)),     # Beige truck
    '3': ('bus', (0.9, 0.9, 0.1)),          # Yellow bus
    '4': ('suv', (0.0, 0.5, 0.0)),          # Green SUV
    '5': ('pickup_truck', (0.7, 0.3, 0.0)), # Brown pickup
    '6': ('sports_car', (0.1, 0.1, 0.9))    # Blue sports car
}

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18): #all given
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1280, 0, 720)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    # Draw text at (x, y) in screen coordinates
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    # Restore original projection and modelview matrices
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def draw_grid():
    cell = 93
    for x in range(-GRID_LENGTH, GRID_LENGTH, cell):
        for z in range(-GRID_LENGTH, GRID_LENGTH, cell):
            row = x // cell
            col = z // cell
            if (row + col) % 2 == 0:  # checks even
                glColor3f(1, 1, 1)
            else:
                glColor3f(0.6, 0.5, 0.7)
            glBegin(GL_QUADS)
            glVertex3f(x + cell, 0, z + cell)
            glVertex3f(x, 0, z + cell)
            glVertex3f(x, 0, z)
            glVertex3f(x + cell, 0, z)
            glEnd()

def draw_boundary():
    height = 90
    thick = 5

    glPushMatrix()
    glColor3f(1, 1, 1)  # White
    glTranslatef(0, height / 2, GRID_LENGTH + thick  / 2)
    glScalef(GRID_LENGTH * 2, height, thick)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0.8, 0.8)  # Blue
    glTranslatef(0, height / 2, -GRID_LENGTH - thick / 2)
    glScalef(GRID_LENGTH * 2, height, thick)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 0, 1)  # Dark Blue
    glTranslatef(-GRID_LENGTH - thick / 2, height / 2, 0)
    glScalef(thick, height, GRID_LENGTH * 2)
    glutSolidCube(1)
    glPopMatrix()

    glPushMatrix()
    glColor3f(0, 1, 0)  # Green
    glTranslatef(GRID_LENGTH + thick / 2, height / 2, 0)
    glScalef(thick, height, GRID_LENGTH * 2)
    glutSolidCube(1)
    glPopMatrix()

def draw_player():
    global car_model, car_color
    
    glPushMatrix()
    glTranslatef(player_pos[0], player_pos[1], player_pos[2])
    glRotatef(player_angle, 0, 1, 0)
    glRotatef(270, 0, 1, 0)  # Add 90-degree rotation to the right (clockwise)
    
    # Call the appropriate car model drawing function based on current selection
    if car_model == 'car':
        draw_car(0, 0, 0, car_color)
    elif car_model == 'truck':
        draw_truck(0, 0, 0, car_color)
    elif car_model == 'bus':
        draw_bus(0, 0, 0, car_color)
    elif car_model == 'suv':
        draw_suv(0, 0, 0, car_color)
    elif car_model == 'pickup_truck':
        draw_pickup_truck(0, 0, 0, car_color)
    elif car_model == 'sports_car':
        draw_sports_car(0, 0, 0, car_color)
    
    glPopMatrix()

def setupCamera():
    global fovY, camera_pos, player_pos, player_angle, camera_mode
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(fovY, 1.25, 1.0, 1500)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if camera_mode == "third_person":
        
        # Third-person camera view behind car
        gluLookAt(camera_pos[0], camera_pos[1], camera_pos[2], 0, 0, 0, 0, 1, 0)
    elif camera_mode == "first_person":
        # First-person view from car driver perspective
        angle_rad = math.radians(player_angle)
        
        # Position camera in the car's "driver seat"
        head_x = player_pos[0] + 20 * math.sin(angle_rad)
        head_y = player_pos[1] + 60  # Up a bit for driver's view
        head_z = player_pos[2] + 20 * math.cos(angle_rad)
        
        # Look ahead in the direction the car is facing
        px,py,pz=player_pos
        look_ahead = 100
        look_x = px + (math.sin(angle_rad) * 100)
        look_y = py + 30
        look_z = pz + (math.cos(angle_rad) * 100)
        
        gluLookAt(
            head_x, head_y, head_z,
            look_x, look_y, look_z,
            0, 1, 0
        )

def update_car_position():
    """Updates the car position based on current speed and direction"""
    global player_pos, player_angle, speed
    
    # Apply deceleration when no keys are pressed (natural slowing down)
    if abs(speed) < deceleration:
        speed = 0
    elif speed > 0:
        speed -= deceleration * 0.5
    elif speed < 0:
        speed += deceleration * 0.5
    
    # Convert angle to radians for movement calculation
    angle_rad = player_angle * (math.pi / 180)
    sin_val = math.sin(angle_rad)
    cos_val = math.cos(angle_rad)
    
    # Calculate new position
    new_x = player_pos[0] + (speed * sin_val)
    new_z = player_pos[2] + (speed * cos_val)
    
    # Boundary checks to keep car within the grid
    boundary_margin = 50  # Keep some distance from walls
    if -GRID_LENGTH + boundary_margin <= new_x <= GRID_LENGTH - boundary_margin:
        player_pos[0] = new_x
    else:
        # Collision with wall, stop the car
        speed = 0
        
    if -GRID_LENGTH + boundary_margin <= new_z <= GRID_LENGTH - boundary_margin:
        player_pos[2] = new_z
    else:
        # Collision with wall, stop the car
        speed = 0

def keyboard_listener(key, x, y):
    global player_pos, player_angle, camera_mode, speed, car_model, car_color, game_over
    
    # Reset game if needed
    if game_over:
        if key == b'r' or key == b'R':
            reset_game()
        return
    
    # Movement controls
    if key == b'w' or key == b'W':  # Accelerate forward
        speed = min(speed + acceleration, max_speed)
    elif key == b's' or key == b'S':  # Brake/reverse
        speed = max(speed - acceleration, -max_speed/2)  # Reverse is slower than forward
    
    # Steering controls
    if key == b'a' or key == b'A':  # Turn left
        player_angle += steering_speed
    elif key == b'd' or key == b'D':  # Turn right
        player_angle -= steering_speed
    
    # Camera view toggle
    if key == b'c' or key == b'C':
        if camera_mode == "third_person":
            camera_mode = "first_person"
        else:
            camera_mode = "third_person"
    
    # Car model selection
    if key in [b'1', b'2', b'3', b'4', b'5', b'6']:
        selection = chr(key[0])
        if selection in car_models:
            car_model, car_color = car_models[selection]

def special_key_listener(key, x_unused, y_unused):
    global camera_angle, camera_pos

    if camera_mode == "third_person" and not game_over:
        rotation = 5
        height_change = 20
        radius = 500
        min_y = 50
        max_y = 800
        x, y, z = camera_pos

        if key == GLUT_KEY_LEFT or key == GLUT_KEY_RIGHT:
            if key == GLUT_KEY_LEFT:
                camera_angle -= rotation
            elif key == GLUT_KEY_RIGHT:
                camera_angle += rotation

            camera_angle = camera_angle % 360
            rad = math.radians(camera_angle)
            sin_val = math.sin(rad)
            cos_val = math.cos(rad)
            x = radius * sin_val
            z = radius * cos_val

        elif key == GLUT_KEY_UP:
            y += height_change
            if y > max_y:
                y = max_y
        elif key == GLUT_KEY_DOWN:
            y -= height_change
            if y < min_y:
                y = min_y

        camera_pos = [x, y, z]
        glutPostRedisplay()


def mouse_listener(button, state, x, y):
    global camera_mode
    
    # Right mouse button toggles camera view
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if camera_mode == "third_person":
            camera_mode = "first_person"
        else:
            camera_mode = "third_person"
        glutPostRedisplay()


def reset_game():
    global player_pos, player_angle, speed, game_over
    
    player_pos = [0, 30, 0]
    player_angle = 180
    speed = 0
    game_over = False
    camera_mode = "third_person"


def idle():
    update_car_position()
    glutPostRedisplay()


def show_screen():
    global game_over
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) #g
    glLoadIdentity() #g
    setupCamera() #g
    glViewport(0, 0, 1000, 800)  # need to use

    draw_grid()
    draw_boundary()
    draw_player()
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Car Driving Simulation")  # Create the window
    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard_listener)
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()