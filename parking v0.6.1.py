from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from CARdraw import *

headlight_opacity=0.5
# Window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# Game state
game_state = "HOME"  # "HOME" for home screen, "PLAY" for gameplay
health = 5  # Player health

# Game constants
fovY = 120
GRID_LENGTH = 1000

# Current game level
current_level = 1

# Car and camera settings
car_model = 'sports_car'  # Default car model
car_color = (0.1, 0.1, 0.9)  # Default car color (blue)
camera_pos = [0, 900, 500]
camera_angle = 0
camera_mode = "third_person"
player_pos = [0, 30, 600]  # Starting position adjusted for level 1
player_angle = 180

# Car movement physics
speed = 0.02
max_speed = 1.5
acceleration = 0.15
deceleration = 0.15
steering_speed = 0.3
game_over = False
keys_pressed = set()  # Track which keys are currently pressed
steering_angle = 0  # Current steering angle
max_steering_angle = 30  # Maximum steering angle
steering_return_speed = 1.0  # How quickly steering returns to center

# Level 1
# Simple straight road with minimal obstacles and clear parking area
level1_parked_cars = [
    {"model": "suv", "color": (0.0, 0.5, 0.0), "pos": [-400, 30, -400], "angle": 90},
    {"model": "car", "color": (1.0, 0.0, 0.0), "pos": [-200, 30, -400], "angle": 90}
]

level1_obstacles = [
    {"type": "cone", "pos": [0, 0, 300]},
    {"type": "cone", "pos": [0, 0, 0]},
    {"type": "barrier", "pos": [-300, 0, 0], "angle": 0}
]

level1_parking_spots = [
    {"pos": [0, 0, -400], "angle": 90, "occupied": False},
    {"pos": [400, 0, -600], "angle": 90, "occupied": False}
]

level2_parked_cars = [
    {"model": "suv", "color": (0.0, 0.5, 0.0), "pos": [200, 30, -400], "angle": 90},
    {"model": "car", "color": (1.0, 0.0, 0.0), "pos": [50, 30, -250], "angle": 90}
]

level2_obstacles = [
    {"type": "cone", "pos": [0, 0, 100]},
    {"type": "cone", "pos": [0, 0, -100]},
    {"type": "barrier", "pos": [-200, 0, 0], "angle": 0}
]

level2_parking_spots = [
    {"pos": [0, 0, -200], "angle": 270, "occupied": False},
    {"pos": [200, 0, -400], "angle": 180, "occupied": False}
]

# Car model selection options
car_models = {
    '1': ('car', (1.0, 0.0, 0.0)),  # Red car
    '2': ('truck', (0.96, 0.96, 0.86)),  # Beige truck
    '3': ('bus', (0.9, 0.9, 0.1)),  # Yellow bus
    '4': ('suv', (0.0, 0.5, 0.0)),  # Green SUV
    '5': ('pickup_truck', (0.7, 0.3, 0.0)),  # Brown pickup
    '6': ('sports_car', (0.1, 0.1, 0.9))  # Blue sports car
}

car_sizes = {
    'car': 50,
    'truck': 140,
    'bus': 160,
    'suv': 100,
    'pickup_truck': 120,
    'sports_car': 60
}
vehicle_size = car_sizes[car_model]

# Fuel settings
fuel = 100  # Initial fuel level (0 to 100)
max_fuel = 100  # Maximum fuel capacity
fuel_depletion_rate = 0.0002  # Base depletion rate per frame (slow)
fuel_speed_depletion_factor = 0.005 # Additional depletion based on speed

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):  # all given
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


def draw_stroke_text(x, y, text, font=GLUT_STROKE_ROMAN):
    """Draws 3D stroke font text using an orthographic projection."""
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glTranslatef(x, y, 0)
    glScalef(0.5, 0.5, 0.5)
    for ch in text:
        glutStrokeCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def draw_roads():
    """Draws two vertical ash-colored roads but moves both roads outside."""
    glColor3f(0.5, 0.5, 0.5)

    # Left road moved outside (closer to the text)
    glBegin(GL_QUADS)
    glVertex2f(200, 0)
    glVertex2f(320, 0)
    glVertex2f(320, WINDOW_HEIGHT)
    glVertex2f(200, WINDOW_HEIGHT)
    glEnd()

    # Right road moved outside (closer to the text)
    glBegin(GL_QUADS)
    glVertex2f(940, 0)
    glVertex2f(1060, 0)
    glVertex2f(1060, WINDOW_HEIGHT)
    glVertex2f(940, WINDOW_HEIGHT)
    glEnd()


def draw_parking_spots():
    """Draws outlined parking spots with an open side facing the road."""
    glColor3f(0.7, 0.7, 0.7)  # White outlines

    # Left-side parking spots (open side toward road)
    for y in range(50, WINDOW_HEIGHT, 120):
        glLineWidth(3)
        glBegin(GL_LINES)
        # Bottom horizontal line (open toward road)
        glVertex2f(30, y)
        glVertex2f(180, y)
        glVertex2f(30, y + 80)
        glVertex2f(180, y + 80)
        # Left vertical line
        glVertex2f(30, y)
        glVertex2f(30, y + 80)

        glEnd()

    # Right-side parking spots (open side toward road)
    for y in range(50, WINDOW_HEIGHT, 120):
        glLineWidth(3)
        glBegin(GL_LINES)
        # Bottom horizontal line (open toward road)
        glVertex2f(1090, y)
        glVertex2f(1250, y)
        glVertex2f(1250, y + 80)
        glVertex2f(1090, y + 80)
        # Right vertical line
        glVertex2f(1250, y)
        glVertex2f(1250, y + 80)
        glEnd()
        draw_rotated_text(100, y + 30, "P", 90)  # Left-side spots
        draw_rotated_text(1150, y + 50, "P", -90)  # Right-side spots


def draw_road_markings():
    """Adds yellow dashed markings on both roads."""
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for road markings

    glLineWidth(3)
    glBegin(GL_LINES)
    for y in range(0, WINDOW_HEIGHT, 90):
        glVertex2f(260, y)
        glVertex2f(260, y + 30)
    glEnd()

    glLineWidth(3)
    glBegin(GL_LINES)
    for y in range(0, WINDOW_HEIGHT, 90):
        glVertex2f(1010, y)
        glVertex2f(1010, y + 30)
    glEnd()


def draw_rotated_text(x, y, text, angle, font=GLUT_STROKE_ROMAN):
    """Draws rotated text using OpenGL transformations."""
    glColor3f(1, 1, 1)  # White color for text
    glPushMatrix()
    glTranslatef(x, y, 0)  # Move text to position
    glRotatef(angle, 0, 0, 1)  # Apply rotation (angle in degrees)
    glScalef(0.3, 0.3, 0.3)  # Keep the "P" small
    for ch in text:
        glutStrokeCharacter(font, ord(ch))
    glPopMatrix()


def draw_health_bar():
    global health

    # Base position and size of the health bar
    bar_x = 50
    bar_y = WINDOW_HEIGHT - 50
    bar_width = 200
    bar_height = 25
    segment_width = bar_width / 5

    for i in range(5):
        if i < health:
            glColor3f(0, 1, 0)  # Green for remaining health
        else:
            glColor3f(1, 0, 0)  # Red for missing health
        glBegin(GL_QUADS)
        glVertex2f(bar_x + i * segment_width, bar_y)
        glVertex2f(bar_x + (i + 1) * segment_width, bar_y)
        glVertex2f(bar_x + (i + 1) * segment_width, bar_y - bar_height)
        glVertex2f(bar_x + i * segment_width, bar_y - bar_height)
        glEnd()
    glPushMatrix()
    glTranslatef(bar_x, bar_y - bar_height - 40, 0)  # Position the text
    glScalef(0.25, 0.3, 0.25)  # Reduce the size of the font
    glColor3f(1, 1, 1)
    for ch in "Health":
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
        glTranslatef(20, 0, 0)
    glPopMatrix()

def draw_fuel_bar():
    global fuel

    bar_x = 300
    bar_y = WINDOW_HEIGHT - 50
    bar_width = 200
    bar_height = 25

    #filled portion of the bar based on fuel level
    filled_width = (fuel / 100) * bar_width

    if fuel > 50:
        bar_color = (0, 1, 0)  # Green
    elif fuel > 20:
        bar_color = (1, 0.5, 0)  # Orange
    else:
        bar_color = (1, 0, 0)  # Red

    #filled portion of the fuel bar
    glColor3f(*bar_color)
    glBegin(GL_QUADS)
    glVertex2f(bar_x, bar_y)
    glVertex2f(bar_x + filled_width, bar_y)
    glVertex2f(bar_x + filled_width, bar_y - bar_height)
    glVertex2f(bar_x, bar_y - bar_height)
    glEnd()

    # empty portion of the fuel bar in gray
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex2f(bar_x + filled_width, bar_y)
    glVertex2f(bar_x + bar_width, bar_y)
    glVertex2f(bar_x + bar_width, bar_y - bar_height)
    glVertex2f(bar_x + filled_width, bar_y - bar_height)
    glEnd()

    # white border
    glColor3f(1, 1, 1)
    glPointSize(3)
    glBegin(GL_POINTS)

    point_spacing = 2

    # Top border
    for i in range(0, bar_width, point_spacing):
        glVertex2f(bar_x + i, bar_y)

    # Bottom border
    for i in range(0, bar_width, point_spacing):
        glVertex2f(bar_x + i, bar_y - bar_height)

    # Left border
    for i in range(0, bar_height, point_spacing):
        glVertex2f(bar_x, bar_y - i)

    # Right border
    for i in range(0, bar_height, point_spacing):
        glVertex2f(bar_x + bar_width, bar_y - i)

    glEnd()

    # "Fuel" label
    glPushMatrix()
    glTranslatef(bar_x, bar_y - bar_height - 40, 0)
    glScalef(0.25, 0.3, 0.25)
    glColor3f(1, 1, 1)
    for ch in "Fuel":
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
        glTranslatef(20, 0, 0)
    glPopMatrix()

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
    glTranslatef(0, height / 2, GRID_LENGTH + thick / 2)
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
        if car_model == "bus":
            if b's' in keys_pressed or b'S' in keys_pressed:
                # Rear-view: flip the camera to look behind the car
                angle_rad += math.pi
            head_x = player_pos[0] + 180 * math.sin(angle_rad)
            head_y = player_pos[1] + 120  # Up a bit for driver's view
            head_z = player_pos[2] + 180 * math.cos(angle_rad)

            look_ahead = 100
            look_x = head_x + (math.sin(angle_rad) * look_ahead)  # Look further ahead from the new position
            look_y = head_y - 70  # Adjust height offset for natural driver's view
            look_z = head_z + (math.cos(angle_rad) * look_ahead)
        elif car_model == "truck":
            if b's' in keys_pressed or b'S' in keys_pressed:
                # Rear-view: flip the camera to look behind the car
                angle_rad += math.pi
            head_x = player_pos[0] + 140 * math.sin(angle_rad)
            head_y = player_pos[1] + 80  # Up a bit for driver's view
            head_z = player_pos[2] + 140 * math.cos(angle_rad)

            look_ahead = 100
            look_x = head_x + (math.sin(angle_rad) * look_ahead)  # Look further ahead from the new position
            look_y = head_y - 70  # Adjust height offset for natural driver's view
            look_z = head_z + (math.cos(angle_rad) * look_ahead)
        else:
            if b's' in keys_pressed or b'S' in keys_pressed:
                # Rear-view: flip the camera to look behind the car
                angle_rad += math.pi
                # Position camera in the car's "driver seat"
            head_x = player_pos[0] + 20 * math.sin(angle_rad)
            head_y = player_pos[1] + 60  # Up a bit for driver's view
            head_z = player_pos[2] + 20 * math.cos(angle_rad)

            # Look ahead in the direction the car is facing
            px, py, pz = player_pos
            look_ahead = 100
            look_x = px + (math.sin(angle_rad) * 100)
            look_y = py + 30
            look_z = pz + (math.cos(angle_rad) * 100)

        gluLookAt(
            head_x, head_y, head_z,
            look_x, look_y, look_z,
            0, 1, 0
        )

# Updated fuel logic in update_car_position()
def update_car_position():
    """Updates the car position based on current speed and direction"""
    global player_pos, player_angle, speed, keys_pressed, fuel, game_over

    # Handle acceleration/deceleration based on current keys
    if b'w' in keys_pressed or b'W' in keys_pressed:  # Accelerate forward
        speed = min(speed + acceleration * 0.1, max_speed)
    elif b's' in keys_pressed or b'S' in keys_pressed:  # Brake/reverse
        speed = max(speed - acceleration * 0.1, -max_speed / 2)
    else:  # Natural deceleration when no movement keys are pressed
        if abs(speed) < deceleration:
            speed = 0
        elif speed > 0:
            speed -= deceleration * 0.5
        elif speed < 0:
            speed += deceleration * 0.5

    # Apply steering only when the car is moving (speed > 0 for forward, speed < 0 for reverse)
    # Using a much smaller threshold to detect movement
    if abs(speed) > 0.01:  # Only turn if we're moving at least a tiny bit
        if b'a' in keys_pressed or b'A' in keys_pressed:  # Left turn
            # In reverse, turning is opposite (like in real cars)
            if speed > 0:
                player_angle += steering_speed  # Turn left in forward gear
            else:
                player_angle -= steering_speed  # Turn right in reverse gear

        if b'd' in keys_pressed or b'D' in keys_pressed:  # Right turn
            # In reverse, turning is opposite (like in real cars)
            if speed > 0:
                player_angle -= steering_speed  # Turn right in forward gear
            else:
                player_angle += steering_speed  # Turn left in reverse gear

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

    # Fuel logic
    if not game_over:
        # Base fuel depletion rate
        fuel_depletion = fuel_depletion_rate

        # If the car is moving, increase the depletion rate based on speed
        if abs(speed) > 0:
            fuel_depletion += fuel_speed_depletion_factor * abs(speed)

        # Update fuel level
        fuel = max(fuel - fuel_depletion, 0)  # Ensure fuel doesn't go below 0

        # Check for game over when fuel runs out
        if fuel <= 0:
            game_over = True

def keyboard_listener(key, x, y):
    global player_pos, player_angle, camera_mode, speed, car_model, car_color, game_over, keys_pressed, game_state

    # Reset game if needed
    if game_over:
        if key == b'r' or key == b'R':
            reset_game()
        return

    # Add key to pressed keys set
    keys_pressed.add(key)

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
    if key == b'\x1b':  # Escape key
        game_state = "HOME"
        return


def keyboard_up_listener(key, x, y):
    """Handle key release events to track which keys are no longer pressed"""
    global keys_pressed

    # Remove the key from the pressed keys set
    if key in keys_pressed:
        keys_pressed.remove(key)


def special_key_listener(key, x_unused, y_unused):
    global camera_angle, camera_pos

    if camera_mode == "third_person" and not game_over:
        rotation = 5
        height_change = 20
        radius = 500
        min_y = 50
        max_y = 900
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
    """Handles mouse click events for both game interaction and menu buttons."""
    global camera_mode, game_state

    if game_state == "HOME" and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        # Convert window coordinates to OpenGL coordinates
        opengl_x = x
        opengl_y = WINDOW_HEIGHT - y  # Flip the y-coordinate

        # Check if "PLAY" is clicked
        if 550 <= opengl_x <= 750 and 400 <= opengl_y <= 450:  # Approximate bounds for "PLAY"
            game_state = "PLAY"
            print("Play button clicked. Starting the game...")

        # Check if "QUIT" is clicked
        elif 550 <= opengl_x <= 750 and 300 <= opengl_y <= 350:  # Approximate bounds for "QUIT"
            print("Quit button clicked. Exiting the game...")
            glutLeaveMainLoop()  # Exit the game

    # Original camera toggle functionality in game mode
    elif game_state == "PLAY" and button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        if camera_mode == "third_person":
            camera_mode = "first_person"
        else:
            camera_mode = "third_person"

    glutPostRedisplay()


def reset_game():
    global player_pos, player_angle, speed, game_over, fuel, max_fuel, camera_mode

    player_pos = [0, 30, 0]
    player_angle = 180
    speed = 0
    fuel = max_fuel
    game_over = False
    camera_mode = "third_person"


def idle():
    update_car_position()
    glutPostRedisplay()


def show_screen():
    """Handles rendering for both home screen and gameplay."""
    global game_state, game_over, fuel

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if game_state == "HOME":
        # Draw home screen
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw the home screen elements
        draw_roads()
        draw_parking_spots()
        draw_road_markings()
        draw_stroke_text(300, 600, "PARKING SIMULATOR")
        draw_stroke_text(550, 400, "PLAY")
        draw_stroke_text(550, 300, "QUIT")

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    elif game_state == "PLAY":
        # Draw game screen
        glLoadIdentity()
        setupCamera()
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)

        # Draw the gameplay elements
        draw_grid()
        draw_boundary()
        draw_game_environment()  # Draw all parking lot elements
        draw_player()

        # Draw the health bar on top of the 3D scene
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        draw_health_bar()
        draw_fuel_bar()

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    glutSwapBuffers()


def draw_parking_spot(x, y, z, angle=0, occupied=False):
    """Draws a single parking spot with marked lines on the ground"""
    width = 200
    length = 300
    line_width = 5

    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(angle, 0, 1, 0)

    # Draw the parking spot base - using a solid color instead of transparent blend
    if occupied:
        glColor3f(0.5, 0.2, 0.2)  # Darker red for occupied spots
    else:
        glColor3f(0.2, 0.4, 0.2)  # Darker green for available spots

    # Draw the parking spot surface
    glBegin(GL_QUADS)
    glVertex3f(-width / 2, 0.5, -length / 2)
    glVertex3f(width / 2, 0.5, -length / 2)
    glVertex3f(width / 2, 0.5, length / 2)
    glVertex3f(-width / 2, 0.5, length / 2)
    glEnd()

    # Draw distinctive pattern inside the parking spot (checkered pattern)
    square_size = 30
    if not occupied:
        glColor3f(0.3, 0.5, 0.3)  # Slightly different green for the pattern
    else:
        glColor3f(0.6, 0.3, 0.3)  # Slightly different red for the pattern

    for i in range(int(-width / 2), int(width / 2), square_size):
        for j in range(int(-length / 2), int(length / 2), square_size):
            # Only draw every other square for a checkered effect
            if (i // square_size + j // square_size) % 2 == 0:
                glBegin(GL_QUADS)
                glVertex3f(i, 0.6, j)
                glVertex3f(i + square_size, 0.6, j)
                glVertex3f(i + square_size, 0.6, j + square_size)
                glVertex3f(i, 0.6, j + square_size)
                glEnd()

    # Draw more visible lines around the parking spot
    glLineWidth(5.0)
    glBegin(GL_LINES)
    # Draw all sides with solid lines
    glColor3f(1.0, 1.0, 1.0)  # White lines for better visibility

    # Left line
    glVertex3f(-width / 2, 1, -length / 2)
    glVertex3f(-width / 2, 1, length / 2)
    # Right line
    glVertex3f(width / 2, 1, -length / 2)
    glVertex3f(width / 2, 1, length / 2)
    # Front line
    glVertex3f(-width / 2, 1, -length / 2)
    glVertex3f(width / 2, 1, -length / 2)
    # Back line
    glVertex3f(-width / 2, 1, length / 2)
    glVertex3f(width / 2, 1, length / 2)
    glEnd()

    # Draw parking spot identifier
    if not occupied:
        # Draw the "P" marking in the center of the spot
        glColor3f(1.0, 1.0, 1.0)  # White for the "P"
        glPushMatrix()
        glTranslatef(0, 1, 0)
        glRotatef(90, 1, 0, 0)  # Rotate to lay flat on the ground
        glScalef(1.5, 1.5, 1.5)  # Make it larger and more visible
        for ch in "P":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
        glPopMatrix()

        # Add corner markers for better depth perception
        glColor3f(1.0, 1.0, 0.0)  # Yellow for corner markers
        corner_size = 30

        # Draw L-shaped corner markers
        for xm in [-1, 1]:
            for zm in [-1, 1]:
                # Horizontal part of L
                glBegin(GL_LINES)
                glVertex3f(xm * width / 2, 1.5, zm * length / 2)
                glVertex3f(xm * (width / 2 - corner_size), 1.5, zm * length / 2)
                # Vertical part of L
                glVertex3f(xm * width / 2, 1.5, zm * length / 2)
                glVertex3f(xm * width / 2, 1.5, zm * (length / 2 - corner_size))
                glEnd()

    glPopMatrix()


def draw_road(x1, z1, x2, z2, width=200, y=0.5):
    """Draws a road segment from (x1,z1) to (x2,z2) with given width"""
    # Calculate road direction vector
    dx = x2 - x1
    dz = z2 - z1
    length = math.sqrt(dx * dx + dz * dz)

    # Normalize direction vector
    if length > 0:
        dx /= length
        dz /= length

    # Calculate perpendicular direction for road width
    px = -dz
    pz = dx

    # Calculate the four corners of the road segment
    p1x = x1 + (px * width / 2)
    p1z = z1 + (pz * width / 2)

    p2x = x1 - (px * width / 2)
    p2z = z1 - (pz * width / 2)

    p3x = x2 - (px * width / 2)
    p3z = z2 - (pz * width / 2)

    p4x = x2 + (px * width / 2)
    p4z = z2 + (pz * width / 2)

    # Draw the road surface
    glColor3f(0.2, 0.2, 0.2)  # Dark gray for road
    glBegin(GL_QUADS)
    glVertex3f(p1x, y, p1z)
    glVertex3f(p2x, y, p2z)
    glVertex3f(p3x, y, p3z)
    glVertex3f(p4x, y, p4z)
    glEnd()

    # Draw yellow center line
    glColor3f(1.0, 0.8, 0.0)  # Yellow
    glLineWidth(3.0)
    glBegin(GL_LINES)
    glVertex3f(x1, y + 0.1, z1)
    glVertex3f(x2, y + 0.1, z2)
    glEnd()


def draw_traffic_cone(x, y, z):
    """Draws a traffic cone obstacle"""
    cone_height = 40
    base_radius = 15

    glPushMatrix()
    glTranslatef(x, y, z)

    # Draw the base (cylinder)
    glColor3f(0.1, 0.1, 0.1)  # Black base
    glutSolidCylinder(base_radius, 5, 20, 1)

    # Draw the cone
    glColor3f(1.0, 0.5, 0.0)  # Orange cone
    glutSolidCone(base_radius, cone_height, 20, 20)

    # Draw reflective stripes
    glColor3f(1.0, 1.0, 1.0)  # White stripe
    glTranslatef(0, 10, 0)
    glutSolidTorus(2, base_radius - 4, 20, 20)

    glPopMatrix()


def draw_barrier(x, y, z, angle=0):
    """Draws a road barrier/block"""
    barrier_length = 100
    barrier_height = 30
    barrier_width = 25

    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(angle, 0, 1, 0)

    # Main barrier block
    glColor3f(0.8, 0.2, 0.2)  # Red
    glPushMatrix()
    glTranslatef(0, barrier_height / 2, 0)
    glScalef(barrier_length, barrier_height, barrier_width)
    glutSolidCube(1)
    glPopMatrix()

    # Reflective stripes
    glColor3f(0.9, 0.9, 0.9)  # White stripes
    for i in range(-40, 41, 40):
        glPushMatrix()
        glTranslatef(i, barrier_height / 2, barrier_width / 2 + 0.5)
        glScalef(20, barrier_height - 10, 1)
        glutSolidCube(1)
        glPopMatrix()

        glPushMatrix()
        glTranslatef(i, barrier_height / 2, -barrier_width / 2 - 0.5)
        glScalef(20, barrier_height - 10, 1)
        glutSolidCube(1)
        glPopMatrix()

    glPopMatrix()


def draw_game_environment():
    """Draw all the parking lot elements: roads, parking spots, parked cars, and obstacles"""

    # Draw the main roads
    # Horizontal road (East-West)
    draw_road(-GRID_LENGTH, 0, GRID_LENGTH, 0, 250)
    # Vertical road (North-South)
    draw_road(0, -GRID_LENGTH, 0, GRID_LENGTH, 250)

    # Road to parking area
    draw_road(0, 0, 0, -500, 150)
    # Parking area horizontal road
    draw_road(-900, -400, 300, -400, 150)

    # Draw all parking spots
    for spot in level2_parking_spots:
        draw_parking_spot(spot["pos"][0], spot["pos"][1], spot["pos"][2],
                          spot["angle"], spot["occupied"])

    # Draw parked cars
    for car in level2_parked_cars:
        glPushMatrix()
        glTranslatef(car["pos"][0], car["pos"][1], car["pos"][2])
        glRotatef(car["angle"], 0, 1, 0)

        if car["model"] == "car":
            draw_car(0, 0, 0, car["color"])
        elif car["model"] == "truck":
            draw_truck(0, 0, 0, car["color"])
        elif car["model"] == "bus":
            draw_bus(0, 0, 0, car["color"])
        elif car["model"] == "suv":
            draw_suv(0, 0, 0, car["color"])
        elif car["model"] == "pickup_truck":
            draw_pickup_truck(0, 0, 0, car["color"])
        elif car["model"] == "sports_car":
            draw_sports_car(0, 0, 0, car["color"])

        glPopMatrix()

    # Draw obstacles
    for obstacle in level2_obstacles:
        if obstacle["type"] == "cone":
            draw_traffic_cone(obstacle["pos"][0], obstacle["pos"][1], obstacle["pos"][2])
        elif obstacle["type"] == "barrier":
            draw_barrier(obstacle["pos"][0], obstacle["pos"][1], obstacle["pos"][2], obstacle["angle"])


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)  # Window position
    wind = glutCreateWindow(b"Parking Simulator")  # Updated window title
    glutDisplayFunc(show_screen)
    glutKeyboardFunc(keyboard_listener)
    glutKeyboardUpFunc(keyboard_up_listener)  # Add key release callback
    glutSpecialFunc(special_key_listener)
    glutMouseFunc(mouse_listener)
    glutIdleFunc(idle)
    glutMainLoop()


if __name__ == "__main__":
    main()