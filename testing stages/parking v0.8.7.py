from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
from CARdraw import *
from level0 import *
from level1 import *
from level2 import *
from level3 import *

headlight_opacity = 0.5
# Window dimensions
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720

# Game state
game_state = "HOME"  # "HOME" for home screen, "PLAY" for gameplay
# health = 5  # Player health

# Game constants
fovY = 120
GRID_LENGTH = 1000

# Current game level
current_level = 0
if current_level == 0:
    player_pos = player_pos0
    player_angle = player_angle0  # Initial angle facing down the road
    current_level_obstacles = level0_obstacles
    current_level_parked_cars = level0_parked_cars
    current_level_parking_spots = level0_parking_spots
    current_level_road = road0
elif current_level == 1:
    player_pos = player_pos1
    player_angle = player_angle1  # Initial angle facing down the road
    current_level_obstacles = level1_obstacles
    current_level_parked_cars = level1_parked_cars
    current_level_parking_spots = level1_parking_spots
    current_level_road = road1
elif current_level == 2:
    player_pos = player_pos2
    player_angle = player_angle2  # Initial angle facing down the road
    current_level_obstacles = level2_obstacles
    current_level_parked_cars = level2_parked_cars
    current_level_parking_spots = level2_parking_spots
    current_level_road = road2
elif current_level == 3:
    player_pos = player_pos3
    player_angle = player_angle3  # Initial angle facing down the road
    current_level_obstacles = level3_obstacles
    current_level_parked_cars = level3_parked_cars
    current_level_parking_spots = level3_parking_spots
    current_level_road = road3
# Car and camera settings
car_model = 'sports_car'  # Default car model
car_color = (0.1, 0.1, 0.9)  # Default car color (blue)
camera_pos = [0, 900, 500]
camera_angle = 0
camera_mode = "third_person"

# Car movement physics
speed = 2
max_speed = 2
acceleration = 0.15
deceleration = 0.15
steering_speed = 0.3
game_over = False
keys_pressed = set()  # Track which keys are currently pressed
steering_angle = 0  # Current steering angle
max_steering_angle = 30  # Maximum steering angle
steering_return_speed = 1.0  # How quickly steering returns to center


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
fuel_depletion_rate = 0.002  # Base depletion rate per frame (slow)
fuel_speed_depletion_factor = 0.005  # Additional depletion based on speed
fuel_depletion_active = False  # Add this with other global variables

sphere_radii = {
    'car': {'front': 55, 'back': 55, 'distance': 40},
    'truck': {'front': 55, 'back': 55, 'distance': 60},
    'bus': {'front': 85, 'back': 85, 'distance': 65},
    'suv': {'front': 40, 'back': 40, 'distance': 35},
    'pickup_truck': {'front': 50, 'back': 50, 'distance': 40},
    'sports_car': {'front': 65, 'back': 65, 'distance': 60}
}

# Radii for obstacles
obstacle_radii = {
    'cone': 14,
    'barrier': 25
}

max_collisions = 5
health = max_collisions
# Collision cooldown
collision_cooldown_frames = 60
frames_since_last_collision = 0  # Frames since last collision

# Timer settings
level_time_limit = 60
current_level_time = 0
frames_per_second = 192
frame_count = 0
timer_active = False

def distance_3d(pos1, pos2):
    # 3D Euclidean distance
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    dz = pos1[2] - pos2[2]
    return math.sqrt(dx * dx + dy * dy + dz * dz)


def check_sphere_collision(pos1, radius1, pos2, radius2):
    # Check if two spheres collide based on their centers and radii
    distance = distance_3d(pos1, pos2)
    return distance < (radius1 + radius2)


def check_boundary_collision(new_pos, radius):
    # Check if the car's sphere collides with grid boundarie
    boundary_margin = radius  # Use radius as margin
    return (new_pos[0] < -GRID_LENGTH + boundary_margin or
            new_pos[0] > GRID_LENGTH - boundary_margin or
            new_pos[2] < -GRID_LENGTH + boundary_margin or
            new_pos[2] > GRID_LENGTH - boundary_margin)


def get_vehicle_spheres(pos, angle, model):
    # Returns positions of collision spheres for a vehicle
    angle_rad = math.radians(angle)
    spheres = []

    # All vehicles get two spheres - front and back
    distance = sphere_radii[model]['distance']

    # Front sphere
    front_x = pos[0] + distance * math.sin(angle_rad)
    front_z = pos[2] + distance * math.cos(angle_rad)
    spheres.append({
        'pos': [front_x, pos[1], front_z],
        'radius': sphere_radii[model]['front']
    })

    # Back sphere
    back_x = pos[0] - distance * math.sin(angle_rad)
    back_z = pos[2] - distance * math.cos(angle_rad)
    spheres.append({
        'pos': [back_x, pos[1], back_z],
        'radius': sphere_radii[model]['back']
    })

    return spheres


def check_vehicle_collision(pos1, angle1, model1, pos2, angle2, model2, check_sphere=None):
    """Check if two vehicles collide using their sphere-based collision system."""
    spheres1 = get_vehicle_spheres(pos1, angle1, model1)
    spheres2 = get_vehicle_spheres(pos2, angle2, model2)

    # If check_sphere is provided, only check that sphere from vehicle 1
    spheres_to_check = [check_sphere] if check_sphere else spheres1

    for sphere1 in spheres_to_check:
        for sphere2 in spheres2:
            if check_sphere_collision(sphere1['pos'], sphere1['radius'], sphere2['pos'], sphere2['radius']):
                return True
    return False


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18, scale=1.0):  # all given
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()

    # Set up an orthographic projection that matches window coordinates
    gluOrtho2D(0, 1280, 0, 720)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glTranslatef(x, y, 0)
    # Apply scaling to make the text larger
    glScalef(scale, scale, 1)
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


def draw_tutorial_text(x, y, text, font=GLUT_STROKE_ROMAN):
    """
    Draws tutorial text on the screen with a fixed scale of 0.8.
    """
    glColor3f(1, 1, 1)  # Set text color to white
    glPushMatrix()
    glTranslatef(x, y, 0)  # Move to the specified position
    glScalef(0.3, 0.3, 0.3)  # Fixed scale for tutorial text

    # Render each character in the text string
    for ch in text:
        glutStrokeCharacter(font, ord(ch))

    glPopMatrix()


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
    if current_level != 0:
        global health, max_collisions

        bar_x = 50
        bar_y = WINDOW_HEIGHT - 50
        bar_width = 200
        bar_height = 25

        # Calculate health percentage (each collision removes 1/7th)
        health_percentage = (health / max_collisions) * 100
        filled_width = (health_percentage / 100) * bar_width

        # Color based on health percentage
        if health_percentage > 50:
            bar_color = (0, 1, 0)
        elif health_percentage > 20:
            bar_color = (1, 0.5, 0)
        else:
            bar_color = (1, 0, 0)

        # Filled portion
        glColor3f(*bar_color)
        glBegin(GL_QUADS)
        glVertex2f(bar_x, bar_y)
        glVertex2f(bar_x + filled_width, bar_y)
        glVertex2f(bar_x + filled_width, bar_y - bar_height)
        glVertex2f(bar_x, bar_y - bar_height)
        glEnd()

        # Empty portion in gray
        glColor3f(0.3, 0.3, 0.3)
        glBegin(GL_QUADS)
        glVertex2f(bar_x + filled_width, bar_y)
        glVertex2f(bar_x + bar_width, bar_y)
        glVertex2f(bar_x + bar_width, bar_y - bar_height)
        glVertex2f(bar_x + filled_width, bar_y - bar_height)
        glEnd()

        # White dotted border
        glColor3f(1, 1, 1)
        glPointSize(3)
        glBegin(GL_POINTS)
        point_spacing = 2
        for i in range(0, int(bar_width), point_spacing):
            glVertex2f(bar_x + i, bar_y)
            glVertex2f(bar_x + i, bar_y - bar_height)
        for i in range(0, int(bar_height), point_spacing):
            glVertex2f(bar_x, bar_y - i)
            glVertex2f(bar_x + bar_width, bar_y - i)
        glEnd()

        # "Health" label with collision count
        glPushMatrix()
        glTranslatef(bar_x, bar_y - bar_height - 40, 0)
        glScalef(0.25, 0.3, 0.25)
        glColor3f(1, 1, 1)
        for ch in f"Health":
            glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
            glTranslatef(20, 0, 0)
        glPopMatrix()


def draw_fuel_bar():
    if current_level != 0:
        global fuel

        bar_x = 300
        bar_y = WINDOW_HEIGHT - 50
        bar_width = 200
        bar_height = 25

        # filled portion of the bar based on fuel level
        filled_width = (fuel / 100) * bar_width

        if fuel > 50:
            bar_color = (0, 1, 0)  # Green
        elif fuel > 20:
            bar_color = (1, 0.5, 0)  # Orange
        else:
            bar_color = (1, 0, 0)  # Red

        # filled portion of the fuel bar
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
                glColor3f(0.5647, 0.9333, 0.5647)  # Light green
            else:
                glColor3f(0.486, 0.804, 0.486)
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


def draw_timer():
    if current_level!=0:
        """Draws the level timer in the top right corner"""
        time_left = max(0, level_time_limit - current_level_time)
        timer_text = f"Time: {time_left}s"

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glColor3f(1, 1, 1)  # White text
        draw_text(WINDOW_WIDTH - 150, WINDOW_HEIGHT - 30, timer_text)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
def check_parking_success():
    """
    Check if the car is fully within the bounds of a designated parking spot.
    Uses AABB collision detection with stricter containment logic.
    """
    global current_level_parking_spots, player_pos, vehicle_size, player_angle

    # Car's bounding box
    car_min_x = player_pos[0] - vehicle_size / 2
    car_max_x = player_pos[0] + vehicle_size / 2
    car_min_z = player_pos[2] - vehicle_size / 2
    car_max_z = player_pos[2] + vehicle_size / 2

    for spot in current_level_parking_spots:
        if spot["occupied"]:
            continue  # Skip already occupied spots

        # Parking spot's bounding box
        spot_min_x = spot["pos"][0] - 50  # Assuming parking spot width = 100
        spot_max_x = spot["pos"][0] + 50
        spot_min_z = spot["pos"][2] - 150  # Assuming parking spot length = 300
        spot_max_z = spot["pos"][2] + 150

        # Check if the car is fully within the parking spot
        fully_inside = (
                car_min_x >= spot_min_x and car_max_x <= spot_max_x and
                car_min_z >= spot_min_z and car_max_z <= spot_max_z
        )

        if fully_inside:
            # Optional: Check if the car's orientation matches the parking spot's angle
            required_angle = spot["angle"]
            angle_tolerance = 10  # Allow a small tolerance for misalignment
            if abs(player_angle - required_angle) <= angle_tolerance:
                # Mark the spot as occupied and return success
                spot["occupied"] = True
                return True

    return False


def advance_to_next_level():
    global current_level, current_level_parking_spots, current_level_parked_cars
    global current_level_obstacles, player_pos, player_angle, current_level_road, game_state
    global current_level_time, frame_count, timer_active  # Add these

    # Reset timer for new level
    current_level_time = 0
    frame_count = 0
    if current_level!=0:
        timer_active = True

    if current_level == 0:
        current_level = 1
        player_pos = player_pos1
        player_angle = player_angle1
        current_level_parking_spots = level1_parking_spots
        current_level_parked_cars = level1_parked_cars
        current_level_obstacles = level1_obstacles
        current_level_road = road1
        game_state = "PLAY"  # Resume gameplay
    
    elif current_level == 1:
        current_level = 2
        player_pos = player_pos2
        player_angle = player_angle2
        current_level_parking_spots = level2_parking_spots
        current_level_parked_cars = level2_parked_cars
        current_level_obstacles = level2_obstacles
        current_level_road = road2
        game_state = "PLAY"
    elif current_level == 2:
        current_level = 3
        player_pos = player_pos3
        player_angle = player_angle3
        current_level_parking_spots = level3_parking_spots
        current_level_parked_cars = level3_parked_cars
        current_level_obstacles = level3_obstacles
        current_level_road = road3
        game_state = "PLAY"
    elif current_level == 3:
        game_state = "CONGRATULATIONS"
    print(f"Level advanced to {current_level}. Health remains at {health}")


def update_game_state():
    global game_state, game_over

    if game_state == "PLAY":
        if check_parking_success():
            if current_level != 3:
                game_state = "LEVEL_UP"
            else:
                game_state = "CONGRATULATIONS"
        elif current_level_time >= level_time_limit:  # Timeout check
            game_over = True


def setupCamera():
    global fovY, camera_pos, player_pos, player_angle, camera_mode

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Perspective projection
    far_clipping_plane = GRID_LENGTH * 2  # Adjust to make the scene feel closer
    gluPerspective(fovY, WINDOW_WIDTH / WINDOW_HEIGHT, 1.0, far_clipping_plane)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    if camera_mode == "third_person":
        # Dynamic camera positioning based on GRID_LENGTH
        dynamic_camera_height = GRID_LENGTH * 0.5  # Camera height relative to grid size
        dynamic_camera_distance = GRID_LENGTH * 0.3  # Camera distance behind the car

        # Camera position (above and behind the car)
        camera_x = player_pos[0]  # Stay horizontally aligned with the car
        camera_y = player_pos[1] + dynamic_camera_height  # Height above the car
        camera_z = player_pos[2] + dynamic_camera_distance  # Distance behind the car

        # Look-at target (the car's position)
        look_at_x = player_pos[0]
        look_at_y = player_pos[1] + 10  # Slightly above the car's center
        look_at_z = player_pos[2]

        # Set the camera view
        gluLookAt(
            camera_x, camera_y, camera_z,  # Camera position
            look_at_x, look_at_y, look_at_z,  # Look-at target
            0, 1, 0  # Up vector
        )
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


def update_car_position():
    """Updates the car position with immediate collision detection and frame-based cooldown."""
    global player_pos, player_angle, speed, keys_pressed, fuel, game_over, health, frames_since_last_collision, timer_active
    global fuel_depletion_active

    if game_over or game_state != "PLAY":
        speed = 0  # Ensure speed is zero when game is over
        return

    # Activate fuel depletion when Level 1 starts
    if current_level == 1 and not fuel_depletion_active:
        fuel_depletion_active = True

    # Handle acceleration/deceleration
    forward_pressed = b'w' in keys_pressed or b'W' in keys_pressed
    backward_pressed = b's' in keys_pressed or b'S' in keys_pressed

    if forward_pressed and not backward_pressed:
        speed = min(speed + acceleration * 0.1, max_speed)
    elif backward_pressed and not forward_pressed:
        speed = max(speed - acceleration * 0.1, -max_speed / 2)
    else:
        if abs(speed) < deceleration:
            speed = 0
        elif speed > 0:
            speed -= deceleration * 0.5
        elif speed < 0:
            speed += deceleration * 0.5

    # Apply steering
    if abs(speed) > 0.01:
        # Determine steering direction based on movement direction
        if speed > 0:  # Moving forward
            if b'a' in keys_pressed or b'A' in keys_pressed:
                player_angle += steering_speed  # Turn left (counterclockwise)
            if b'd' in keys_pressed or b'D' in keys_pressed:
                player_angle -= steering_speed  # Turn right (clockwise)
        else:  # Moving backward
            if b'a' in keys_pressed or b'A' in keys_pressed:
                player_angle -= steering_speed  # Turn left in reverse (clockwise)
            if b'd' in keys_pressed or b'D' in keys_pressed:
                player_angle += steering_speed  # Turn right in reverse (counterclockwise)

    # Calculate new positions and check collisions
    angle_rad = math.radians(player_angle)
    new_pos = player_pos  # Default to current position
    front_collision = False
    back_collision = False

    if forward_pressed or backward_pressed:
        # Calculate forward and backward positions
        forward_speed = max_speed if forward_pressed else 0.01  # Small speed for collision check
        new_x_forward = player_pos[0] + (forward_speed * math.sin(angle_rad))
        new_z_forward = player_pos[2] + (forward_speed * math.cos(angle_rad))
        new_pos_forward = [new_x_forward, player_pos[1], new_z_forward]

        backward_speed = -max_speed / 2 if backward_pressed else -0.01  # Small speed for collision check
        new_x_backward = player_pos[0] + (backward_speed * math.sin(angle_rad))
        new_z_backward = player_pos[2] + (backward_speed * math.cos(angle_rad))
        new_pos_backward = [new_x_backward, player_pos[1], new_z_backward]

        # Get spheres for forward and backward positions
        forward_spheres = get_vehicle_spheres(new_pos_forward, player_angle, car_model)
        backward_spheres = get_vehicle_spheres(new_pos_backward, player_angle, car_model)

        # Check collisions for forward direction (front sphere only)
        if forward_pressed:
            front_sphere = forward_spheres[0]  # Front sphere
            for car in current_level_parked_cars:
                if check_vehicle_collision(new_pos_forward, player_angle, car_model, car["pos"], car["angle"],
                                           car["model"], check_sphere=front_sphere):
                    front_collision = True
                    break
            if not front_collision:
                for obstacle in current_level_obstacles:
                    obs_pos = obstacle["pos"]
                    obs_radius = obstacle_radii[obstacle["type"]]
                    if check_sphere_collision(front_sphere['pos'], front_sphere['radius'], obs_pos, obs_radius):
                        front_collision = True
                        break
            if not front_collision:
                if check_boundary_collision(front_sphere['pos'], front_sphere['radius']):
                    front_collision = True

        # Check collisions for backward direction (back sphere only)
        if backward_pressed:
            back_sphere = backward_spheres[1]  # Back sphere
            for car in current_level_parked_cars:
                if check_vehicle_collision(new_pos_backward, player_angle, car_model, car["pos"], car["angle"],
                                           car["model"], check_sphere=back_sphere):
                    back_collision = True
                    break
            if not back_collision:
                for obstacle in current_level_obstacles:
                    obs_pos = obstacle["pos"]
                    obs_radius = obstacle_radii[obstacle["type"]]
                    if check_sphere_collision(back_sphere['pos'], back_sphere['radius'], obs_pos, obs_radius):
                        back_collision = True
                        break
            if not back_collision:
                if check_boundary_collision(back_sphere['pos'], back_sphere['radius']):
                    back_collision = True

        # Determine movement
        if forward_pressed and not front_collision:
            speed = min(speed, max_speed)  # Ensure positive speed
            new_pos = new_pos_forward
        elif backward_pressed and not back_collision:
            speed = max(speed, -max_speed / 2)  # Ensure negative speed
            new_pos = new_pos_backward
        else:
            speed = 0  # Block movement if relevant sphere collides

    # Update position and health
    if new_pos != player_pos:  # Move if direction is clear
        player_pos = new_pos
        frames_since_last_collision += 1  # Increment when moving
    else:
        # Deduct health only if pressing into a colliding direction
        if not game_over and frames_since_last_collision >= collision_cooldown_frames and current_level != 0:
            if (forward_pressed and front_collision) or (backward_pressed and back_collision):
                health = max(health - 1, 0)  # Decrease by exactly 1
                frames_since_last_collision = 0  # Reset frame counter
            else:
                frames_since_last_collision += 1
        else:
            frames_since_last_collision += 1

        if health <= 0 and current_level != 0:
            game_over = True
            timer_active = False  # Freeze timer

    # Fuel logic - only active when in a level
    if current_level != 0:
        if not game_over and fuel_depletion_active:
            # Base fuel depletion (always happens when in level)
            fuel_depletion = fuel_depletion_rate  # 0.0002 (idle rate)

            # Additional fuel consumption when moving
            if abs(speed) > 0.01:  # If car is moving
                fuel_depletion += fuel_speed_depletion_factor * abs(speed)

            fuel = max(fuel - fuel_depletion, 0)
            if fuel <= 0:
                game_over = True
                timer_active = False  # Freeze timer


def keyboard_listener(key, x, y):
    global player_pos, player_angle, camera_mode, speed, car_model, car_color, game_over, keys_pressed, game_state, timer_active

    # Reset game if needed
    if game_over:
        if key == b'r' or key == b'R':
            reset_game()
        return

    # Add key to pressed keys set
    keys_pressed.add(key)

    # Handle "LEVEL UP!" screen key press
    if game_state == "LEVEL_UP" and (key == b'\r' or key == b'\n'):  # Enter key
        advance_to_next_level()
    if game_state == "HOME" and key == b'\r':  # Enter key
        game_state = "TUTORIAL"
        timer_active = False

        # Tutorial -> Gameplay
    if game_state == "TUTORIAL" and key == b'\r':  # Enter key
        game_state = "PLAY"
        timer_active = True
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
            game_state = "TUTORIAL"
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
    # elif game_state == "PLAY" and button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
    #     # Print the game world coordinates where the mouse was clicked
    #     print(f"Mouse clicked at window coordinates: ({x}, {y})")
    #     # Convert window coordinates to normalized device coordinates (NDC)
    #     ndc_x = (2.0 * x) / WINDOW_WIDTH - 1.0
    #     ndc_y = 1.0 - (2.0 * y) / WINDOW_HEIGHT

    #     # Get the depth value at the clicked position
    #     depth = glReadPixels(x, WINDOW_HEIGHT - y, 1, 1, GL_DEPTH_COMPONENT, GL_FLOAT)

    #     # Unproject the NDC coordinates to world coordinates
    #     modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    #     projection = glGetDoublev(GL_PROJECTION_MATRIX)
    #     viewport = glGetIntegerv(GL_VIEWPORT)

    #     world_coords = gluUnProject(ndc_x, ndc_y, depth, modelview, projection, viewport)

    #     # Print the world coordinates
    #     print(f"World coordinates: {world_coords}")

    glutPostRedisplay()


def reset_game():
    global player_pos, player_angle, speed, game_over, fuel, max_fuel, camera_mode, health
    global frames_since_last_collision, fuel_depletion_active
    global current_level_time, frame_count, timer_active, game_state  # Add game_state

    if current_level == 1:
        player_pos = player_pos1
        player_angle = player_angle1
        fuel_depletion_active = False
    elif current_level == 2:
        player_pos = player_pos2
        player_angle = player_angle2
        fuel_depletion_active = True
    elif current_level == 3:
        player_pos = player_pos3
        player_angle = player_angle3
        fuel_depletion_active = True

    # Reset timer variables
    current_level_time = 0
    frame_count = 0
    timer_active = True  # Changed from False to True
    game_state = "PLAY"  # Ensure game state is set to PLAY

    speed = 0
    fuel = max_fuel
    health = max_collisions
    game_over = False
    frames_since_last_collision = 0
    camera_mode = "third_person"



def idle():
    global frame_count, current_level_time,game_over, timer_active

    update_car_position()
    update_game_state()

    # Update timer if active
    if timer_active and game_state == "PLAY":
        frame_count += 1
        if frame_count >= frames_per_second:
            current_level_time += 1
            frame_count = 0

            if current_level_time >= level_time_limit:
                game_over = True
                timer_active = False

    glutPostRedisplay()
def show_screen():
    """Handles rendering for both home screen and gameplay."""
    global game_state, game_over, fuel, current_level

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if game_state == "TUTORIAL":
        # Draw the tutorial screen
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw the tutorial instructions
        draw_tutorial_text(WINDOW_WIDTH // 2 - 290, WINDOW_HEIGHT // 2 + 150, "TUTORIAL")
        draw_tutorial_text(WINDOW_WIDTH // 2 - 450, WINDOW_HEIGHT // 2 + 50, "- Press W, A, S, D to move")
        draw_tutorial_text(WINDOW_WIDTH // 2 - 450, WINDOW_HEIGHT // 2, "- Press ESC to return to Menu")
        draw_tutorial_text(WINDOW_WIDTH // 2 - 450, WINDOW_HEIGHT // 2 - 50, "- Press C to go to first-person view")
        draw_tutorial_text(WINDOW_WIDTH // 2 - 450, WINDOW_HEIGHT // 2 - 100, "- Press 1-6 to change vehicles")
        draw_tutorial_text(WINDOW_WIDTH // 2 - 450, WINDOW_HEIGHT // 2 - 200, "Press ENTER to start the game")

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
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

        glColor3f(1, 1, 1)  # White color for the text
        if current_level == 0:
            level_text = "Tutorial"
        else:
            level_text = f"Level {current_level}"
        draw_stroke_text(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT - 100, level_text)

        # Display current time (will freeze when game_over is True)
        time_left = max(0, level_time_limit - current_level_time)
        timer_text = f"TIME: {time_left:02d}"

        if current_level > 0:
            glPushMatrix()
            glTranslatef(WINDOW_WIDTH - 200, WINDOW_HEIGHT - 90, 0)  # Right-aligned position
            glScalef(0.25, 0.3, 0.25)  # Same scale as health text
            if game_over:
                glColor3f(1, 0, 0)  # Red when game over
            else:
                glColor3f(1, 1, 1)  # White during gameplay
            for ch in timer_text:
                glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
                glTranslatef(20, 0, 0)  # Same character spacing
            glPopMatrix()


        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    elif game_state == "LEVEL_UP":
        # Draw the "LEVEL UP!" screen
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw "LEVEL UP!" text
        draw_stroke_text(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 + 50, "LEVEL UP!")
        draw_stroke_text(WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2 - 50, "Press Enter")

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    elif game_state == "CONGRATULATIONS":
        # Draw the "CONGRATULATIONS!" screen
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        # Draw "CONGRATULATIONS!" text
        draw_stroke_text(WINDOW_WIDTH // 2 - 350, WINDOW_HEIGHT // 2, " CONGRATULATIONS!")

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

    glutSwapBuffers()


def draw_parking_spot(x, y, z, angle=0, occupied=False):
    """Draws a single parking spot with marked lines on the ground"""
    width = 200
    length = 425
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
        # for ch in "P":
        #     glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
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


def draw_ingameroad(x1, z1, x2, z2, width=280, y=0.5):
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
    global current_level_road, current_level_parking_spots, current_level_parked_cars, current_level_obstacles

    for i in current_level_road:
        draw_ingameroad(i[0], i[1], i[2], i[3])

    # Draw all parking spots
    for spot in current_level_parking_spots:
        draw_parking_spot(spot["pos"][0], spot["pos"][1], spot["pos"][2],
                          spot["angle"], spot["occupied"])

    # Draw parked cars
    for car in current_level_parked_cars:
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

        vehicle_spheres = get_vehicle_spheres(car["pos"], car["angle"], car["model"])

    # Draw obstacles
    for obstacle in current_level_obstacles:
        if obstacle["type"] == "cone":
            draw_traffic_cone(obstacle["pos"][0], obstacle["pos"][1], obstacle["pos"][2])
        elif obstacle["type"] == "barrier":
            draw_barrier(obstacle["pos"][0], obstacle["pos"][1], obstacle["pos"][2], obstacle["angle"])

        obs_radius = obstacle_radii[obstacle["type"]]


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