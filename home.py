from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
game_state = "HOME"  # Keeps track of the current state of the game
health = 5  # Initial health value

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
        glVertex2f(30, y+80)
        glVertex2f(180, y+80)
        # Left vertical line
        glVertex2f(30, y)
        glVertex2f(30, y + 80)

        glEnd()
        # draw_text(100, y + 25, "P")

    # Right-side parking spots (open side toward road)
    for y in range(50, WINDOW_HEIGHT, 120):
        glLineWidth(3)
        glBegin(GL_LINES)
        # Bottom horizontal line (open toward road)
        glVertex2f(1090, y)
        glVertex2f(1250, y)
        glVertex2f(1250, y+80)
        glVertex2f(1090, y+80)
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
    glTranslatef(bar_x, bar_y - bar_height - 30, 0)  # Position the text
    glScalef(0.3, 0.2, 0.2)  # Reduce the size of the font
    glColor3f(1, 1, 1)  
    for ch in "Health Bar":
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(ch))
    glPopMatrix()
def mouseListener(button, state, x, y):
    """Handles mouse click events for the PLAY and QUIT buttons."""
    global game_state

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
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

def display():
   
    global health

    # Simulate collision (for demonstration only)
    collision = False  # Replace with actual collision detection logic
    if collision and health > 0:
        health -= 1

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    if game_state == "HOME":
        draw_roads()
        draw_parking_spots()
        draw_road_markings()
        draw_text(300, 600, "PARKING SIMULATOR")
        draw_text(550, 400, "PLAY")
        draw_text(550, 300, "QUIT")
    elif game_state == "PLAY":
        glClear(GL_COLOR_BUFFER_BIT)  # Clears the screen for the game
        draw_health_bar()

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

    glutSwapBuffers()

def main():
    """Sets up the OpenGL window."""
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutCreateWindow(b"Parking Simulator")

    glutDisplayFunc(display)
    glutMouseFunc(mouseListener)
    glutIdleFunc(display)  # Continuously update the screen

    glutMainLoop()

if __name__ == "__main__":
    main()