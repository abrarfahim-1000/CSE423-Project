from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math
from CARdraw import *

# Game state to manage screens
game_state = "HOME"  # Possible states: "HOME", "PLAY"
# Car-related variables
carselect = ''  # Used to select which car model to display
rotate_car = 0  # Tracks the car's rotation angle
# Steering and vehicle physics variables
steering_angle = 0  # Current steering angle
max_steering_angle = 20  # Maximum steering angle in degrees
current_speed = 0  # Current vehicle speed
keys_down = []  # Track which keys are currently pressed
# Camera and player variables
camera_pos = (0, 500, 500)
camera_angle = 0
third_person_view = True
player_pos = (0, 0, 0)
car_angle = 0
player_speed = 1
rotation_speed = 5
frame_counter = 0

fovY = 120
GRID_LENGTH = 1000
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720  # Define window dimensions


def start_game():
    global player_pos, car_angle, game_state
    player_pos = (0, 0, 0)
    car_angle = 0
    game_state = "PLAY"  # Update game state when starting the game

def draw_text(x, y, text, font=GLUT_STROKE_ROMAN):
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

# New function to draw rotated text for the home screen
def draw_rotated_text(x, y, text, angle, font=GLUT_STROKE_ROMAN):
    """Draws rotated text using OpenGL transformations."""
    glColor3f(1, 1, 1)  # White color for text
    glPushMatrix()
    glTranslatef(x, y, 0)  # Move text to position
    glRotatef(angle, 0, 0, 1)  # Apply rotation (angle in degrees)
    glScalef(0.3, 0.3, 0.3)  # Scale the text
    for ch in text:
        glutStrokeCharacter(font, ord(ch))
    glPopMatrix()

# New function to draw the home screen
def draw_home_screen():
    """Draws the home screen with menu options."""
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    # Setup 2D projection for the home screen
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    
    # Draw roads
    glColor3f(0.5, 0.5, 0.5)
    # Left road
    glBegin(GL_QUADS)
    glVertex2f(200, 0)
    glVertex2f(320, 0)  
    glVertex2f(320, WINDOW_HEIGHT)
    glVertex2f(200, WINDOW_HEIGHT)
    glEnd()
    
    # Right road
    glBegin(GL_QUADS)
    glVertex2f(940, 0)  
    glVertex2f(1060, 0)
    glVertex2f(1060, WINDOW_HEIGHT)
    glVertex2f(940, WINDOW_HEIGHT)
    glEnd()
    
    # Draw parking spots
    glColor3f(0.7, 0.7, 0.7)
    
    # Left-side parking spots
    for y in range(50, WINDOW_HEIGHT, 120):
        glLineWidth(3)
        glBegin(GL_LINES)
        # Bottom horizontal line
        glVertex2f(30, y)
        glVertex2f(180, y)
        # Top horizontal line
        glVertex2f(30, y+80)
        glVertex2f(180, y+80)
        # Left vertical line
        glVertex2f(30, y)
        glVertex2f(30, y + 80)
        glEnd()
        
        draw_rotated_text(100, y + 30, "P", 90)  # Left-side spots
    
    # Right-side parking spots
    for y in range(50, WINDOW_HEIGHT, 120):
        glLineWidth(3)
        glBegin(GL_LINES)
        # Bottom horizontal line
        glVertex2f(1090, y)
        glVertex2f(1250, y)
        # Top horizontal line
        glVertex2f(1250, y+80)
        glVertex2f(1090, y+80)
        # Right vertical line
        glVertex2f(1250, y)
        glVertex2f(1250, y + 80)
        glEnd()
        
        draw_rotated_text(1150, y + 50, "P", -90)  # Right-side spots
    
    # Add road markings
    glColor3f(1.0, 1.0, 0.0)  # Yellow color for road markings
    glLineWidth(3)
    
    # Left road markings
    glBegin(GL_LINES)
    for y in range(0, WINDOW_HEIGHT, 90):
        glVertex2f(260, y)
        glVertex2f(260, y + 30)
    glEnd()
    
    # Right road markings
    glBegin(GL_LINES)
    for y in range(0, WINDOW_HEIGHT, 90):
        glVertex2f(1010, y)
        glVertex2f(1010, y + 30)
    glEnd()
    
    # Draw game title and menu options
    draw_text(300, 550, "PARKING SIMULATOR")
    draw_text(550, 350, "PLAY")
    draw_text(550, 250, "QUIT")
    
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    
    glutSwapBuffers()

def draw_grid():
    glBegin(GL_QUADS)
    
    size=100
    
    for i in range(-GRID_LENGTH,GRID_LENGTH,size):
        for j in range(-GRID_LENGTH,GRID_LENGTH,size):
            if((i//size)+(j//size))%2==0:
                glColor3f(0.0,0.5,0.0)
            else:
                glColor3f(0.0,0.5,0.0);
            
            glVertex3f(i,j,0)
            glVertex3f(i+size,j,0)
            glVertex3f(i+size,j+size,0)
            glVertex3f(i,j+size,0)
    
    glEnd()
    
    wall_height=100
    
    glColor3f(0.0,1.0,0.0)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,wall_height)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,wall_height)
    glEnd()
    
    glColor3f(0.0,0.0,1.0)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,wall_height)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,wall_height)
    glEnd()
    
    glColor3f(1.0,1.0,1.0)
    glBegin(GL_QUADS)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(GRID_LENGTH,GRID_LENGTH,wall_height)
    glVertex3f(GRID_LENGTH,-GRID_LENGTH,wall_height)
    glEnd()
    
    glColor3f(0.0,1.0,1.0)
    glBegin(GL_QUADS)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,0)
    glVertex3f(-GRID_LENGTH,GRID_LENGTH,wall_height)
    glVertex3f(-GRID_LENGTH,-GRID_LENGTH,wall_height)
    glEnd()

def draw_shapes(input=''):
    draw_grid()
    
    # Get player position and rotation angle
    px, py, pz = player_pos
    
    # Draw the selected car model at the player's current position with current rotation
    if input=='':
        # Default to red car if no selection is made
        glPushMatrix()
        glTranslatef(px, py, pz)  # Position the car at player position
        glRotatef(rotate_car, 0, 0, 1)  # Rotate the car based on movement direction
        draw_car(0, 0, 50, car_color=(1.0, 0.0, 0.0))  # Draw at origin since we've already translated
        glPopMatrix()
    elif input=='j':
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(rotate_car, 0, 0, 1)
        draw_car(0, 0, 50, car_color=(1.0, 0.0, 0.0))
        glPopMatrix()
    elif input=='k':
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(rotate_car, 0, 0, 1)
        draw_truck(0, 0, 50, truck_color=(0.96, 0.96, 0.86))
        glPopMatrix()
    elif input=='l':
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(rotate_car, 0, 0, 1)
        draw_bus(0, 0, 50, bus_color=(0.9, 0.9, 0.1))
        glPopMatrix()
    elif input=='m':
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(rotate_car, 0, 0, 1)
        draw_suv(0, 0, 50, car_color=(0.0, 0.5, 0.0))
        glPopMatrix()
    elif input=='n':
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(rotate_car, 0, 0, 1)
        draw_pickup_truck(0, 0, 50, car_color=(0.7, 0.3, 0.0))
        glPopMatrix()
    elif input=='b':
        glPushMatrix()
        glTranslatef(px, py, pz)
        glRotatef(rotate_car, 0, 0, 1)
        draw_sports_car(0, 0, 50, car_color=(0.1, 0.1, 0.9))
        glPopMatrix()

def keyboardListener(key, x, y):
    global carselect, player_pos, car_angle, game_state, rotate_car, steering_angle, current_speed
    
    # Handle Escape key to return to home screen
    if key == b'\x1b':  # Escape key
        game_state = "HOME"
        return
    
    if game_state == "HOME":
        return  # Ignore other key presses on home screen
    
    px, py, pz = player_pos
    
    # Forward movement with steering
    if key == b'w':
        # Apply current steering angle when moving forward
        if key == b'w' and (b'a' in keys_down or b'd' in keys_down):
            pass  # Steering is handled in the updateVehiclePosition function
        else:
            angle_rad = math.radians(car_angle)
            new_x = px + current_speed * math.cos(angle_rad)
            new_y = py + current_speed * math.sin(angle_rad)
            
            new_x = max(min(new_x, GRID_LENGTH-50), -GRID_LENGTH+50)
            new_y = max(min(new_y, GRID_LENGTH-50), -GRID_LENGTH+50)
            
            player_pos = (new_x, new_y, pz)
            
            # Update current speed when moving forward
            # current_speed = min(current_speed + 0.5, player_speed)

    # Backward movement with steering
    if key == b's':
        # Apply current steering angle when moving backward
        if key == b's' and (b'a' in keys_down or b'd' in keys_down):
            pass  # Steering is handled in the updateVehiclePosition function
        else:
            angle_rad = math.radians(car_angle)
            new_x = px - current_speed * math.cos(angle_rad)
            new_y = py - current_speed * math.sin(angle_rad)
            
            new_x = max(min(new_x, GRID_LENGTH-50), -GRID_LENGTH+50)
            new_y = max(min(new_y, GRID_LENGTH-50), -GRID_LENGTH+50)
            
            player_pos = (new_x, new_y, pz)
            
            # Update current speed when moving backward
            # current_speed = min(current_speed + 0.5, player_speed)

    # Add keys to pressed keys list
    if key not in keys_down:
        keys_down.append(key)
    
    # Left steering - change steering angle instead of directly rotating
    if key == b'a':
        steering_angle = min(steering_angle + 1, max_steering_angle)
        
    # Right steering - change steering angle instead of directly rotating
    if key == b'd':
        steering_angle = max(steering_angle - 1, -max_steering_angle)

    if key == b'r':
        start_game()

    # Car selection keys
    if key == b'j':
        carselect='j'
    if key == b'k':
        carselect='k'
    if key == b'l':
        carselect='l'
    if key == b'm':
        carselect='m'
    if key == b'n':
        carselect='n'
    if key == b'b':
        carselect='b'

def keyboardUpListener(key, x, y):
    """Handle key release events to implement gradual steering"""
    global keys_down, steering_angle, current_speed
    
    # Remove key from pressed keys list
    if key in keys_down:
        keys_down.remove(key)
    
    # When releasing steering keys, gradually return to center
    if key == b'a' or key == b'd':
        # Steering will automatically return to 0 in updateVehiclePosition
        pass
    
    # When releasing W or S, start slowing down
    if key == b'w' or key == b's':
        # Vehicle will start slowing down in updateVehiclePosition
        pass

def specialKeyListener(key,x,y):
    global camera_pos,camera_angle
    
    x,y,z=camera_pos
    
    if key==GLUT_KEY_UP:
        y=min(y+20,800)
    
    if key==GLUT_KEY_DOWN:
        y=max(y-20,100)
    
    if key==GLUT_KEY_LEFT:
        camera_angle=(camera_angle+5)%360
    
    if key==GLUT_KEY_RIGHT:
        camera_angle=(camera_angle-5)%360
    
    camera_pos=(x,y,z)

def mouseListener(button, state, x, y):
    global third_person_view, game_state
    
    if game_state == "HOME":
        if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
            # Convert window coordinates to OpenGL coordinates
            opengl_y = WINDOW_HEIGHT - y  # Flip the y-coordinate
            
            # Check if "PLAY" is clicked
            if 550 <= x <= 700 and 350 <= opengl_y <= 400:
                start_game()
                print("Play button clicked. Starting the game...")
            # Check if "QUIT" is clicked
            elif 550 <= x <= 700 and 250 <= opengl_y <= 300:
                print("Quit button clicked. Exiting the game...")

                glutLeaveMainLoop()  # Exit the game

def setupCamera():
    global camera_pos,camera_angle,player_pos,third_person_view
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    
    gluPerspective(fovY,1.25,0.1,1500)
    
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    if not third_person_view:
        px,py,pz=player_pos
        
        offset=50
        angle_rad=math.radians(car_angle)
        
        camera_x=px-offset
        camera_y=py-offset
        camera_z=pz+100
        
        target_x=px+100
        target_y=py+100
        target_z=pz+30
        
        gluLookAt(camera_x,camera_y,camera_z,target_x,target_y,target_z,0,0,1)
        
    else:
        x,y,z=camera_pos
        
        radius=500
        angle_rad=math.radians(camera_angle)
        
        eye_x=radius*math.cos(angle_rad)
        eye_y=radius*math.sin(angle_rad)
        eye_z=y
            
        gluLookAt(eye_x,eye_y,eye_z,0,0,0,0,0,1)

def idle():
    global frame_counter
    frame_counter += 1
    
    # Update vehicle position based on steering input
    updateVehiclePosition()
    
    glutPostRedisplay()

def showScreen():
    global carselect, game_state
    
    if game_state == "HOME":
        draw_home_screen()
    else:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
        
        glEnable(GL_DEPTH_TEST)
        
        setupCamera()
        
        draw_shapes(carselect)
        
        # Display instructions
        draw_text(10, 770, "PARKING SIMULATOR")
        draw_text(10, 740, "WASD: Drive | ESC: Menu")
        draw_text(10, 710, "J-N, B keys: Change vehicle")
        
        glutSwapBuffers()

def updateVehiclePosition():
    """Update car position and orientation based on physics and steering input"""
    global player_pos, car_angle, rotate_car, steering_angle, current_speed, keys_down
    
    # Get current position
    px, py, pz = player_pos
    
    # Update steering angle (gradually return to center when not steering)
    if b'a' not in keys_down and b'd' not in keys_down:
        # Return steering wheel to center position gradually
        if steering_angle > 0:
            steering_angle = max(0, steering_angle - 0.5)
        elif steering_angle < 0:
            steering_angle = min(0, steering_angle + 0.5)
    
    # Apply vehicle movement based on key state
    if b'w' in keys_down or b's' in keys_down:
        # Determine direction (forward or reverse)
        direction = 1 if b'w' in keys_down else -1
        
        # Set constant speed instead of gradual acceleration
        current_speed = player_speed
        
        # Apply current steering to the car angle when moving
        if abs(current_speed) > 0.1:  # Only turn if we're moving
            # Steering effect is proportional to speed
            turning_factor = 1.0  # Fixed turning factor for constant speed
            car_angle += steering_angle * turning_factor * direction * 0.1
        
        # Calculate new position
        angle_rad = math.radians(car_angle)
        new_x = px + current_speed * direction * math.cos(angle_rad)
        new_y = py + current_speed * direction * math.sin(angle_rad)
        
        # Boundary checks
        new_x = max(min(new_x, GRID_LENGTH-50), -GRID_LENGTH+50)
        new_y = max(min(new_y, GRID_LENGTH-50), -GRID_LENGTH+50)
        
        # Update position
        player_pos = (new_x, new_y, pz)
    else:
        # Immediately stop when no movement keys are pressed
        current_speed = 0
    
    # FIXING SKIDDING: If steering angle is near zero but car is still turning,
    # gradually correct the car's direction back to straight
    if abs(steering_angle) < 0.1 and (b'w' in keys_down or b's' in keys_down):
        # Determine which direction to straighten (based on current angle)
        car_angle_mod = car_angle % 360
        # Find the closest cardinal direction (0, 90, 180, 270)
        closest_angle = round(car_angle_mod / 90) * 90
        # Gradually adjust toward that cardinal direction
        if car_angle_mod < closest_angle:
            car_angle += 0.1
        elif car_angle_mod > closest_angle:
            car_angle -= 0.1
    
    # Update the visual rotation of the car to match its direction
    rotate_car = car_angle

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Parking Simulator")
    
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutKeyboardUpFunc(keyboardUpListener)  # Register keyboard release handler
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    
    # Don't call start_game() here since we want to begin with the home screen
    # The game will start when the player clicks the "PLAY" button
    
    glutMainLoop()

if __name__ == "__main__": 
    main()