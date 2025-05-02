player_pos2 = [300, 30, 850]
player_angle2 = 180
road2=[(300, 1000, 300, 300),(440, 160, -850, 160),(-710, 20, -710, -500),(-850, -500, 550, -500)]
level2_parked_cars = [
    {"model": "suv", "color": (0.0, 0.5, 0.0), "pos": [-300, 30, -250], "angle": 90},
    {"model": "car", "color": (1.0, 0.0, 0.0), "pos": [50, 30, -250], "angle": 90}
]

level2_obstacles = [
    {"type": "cone", "pos": [150, 0, 950]},
    {"type": "cone", "pos": [150, 0, 700]},
    {"type": "cone", "pos": [150, 0, 450]},
    
    {"type": "barrier", "pos": [450, 0, 900], "angle": 90},
    {"type": "barrier", "pos": [450, 0, 550], "angle": 90},
    
    {"type": "cone", "pos": [350, 0, 0]},
    {"type": "cone", "pos": [50, 0, 0]},
    {"type": "cone", "pos": [-350, 0, 0]},
    
    {"type": "barrier", "pos": [-250, 0, 300], "angle": 0},
    {"type": "barrier", "pos": [-750, 0, 300], "angle": 0},
    
    {"type": "cone", "pos": [-860, 0, 0]},
    {"type": "cone", "pos": [-860, 0, -250]},
    {"type": "cone", "pos": [-860, 0, -500]},
    
    {"type": "barrier", "pos": [-560, 0, -50], "angle": 90},
    {"type": "barrier", "pos": [-560, 0, -300], "angle": 90},
    
    {"type": "cone", "pos": [-800, 0, -700]},
    {"type": "cone", "pos": [-450, 0, -700]},
    {"type": "cone", "pos": [-100, 0, -700]},
    {"type": "cone", "pos": [250, 0, -700]},
    
    {"type": "barrier", "pos": [-150, 0, -350], "angle": 0},
    {"type": "barrier", "pos": [300, 0, -350], "angle": 0},
    
    {"type": "barrier", "pos": [750, 0, -600], "angle": 0},
    {"type": "barrier", "pos": [750, 0, -400], "angle": 0}
]

level2_parking_spots = [
    {"pos": [750,0,-500], "angle": 90, "occupied": False},
]

# x is horizontal
# -1000 to 1000

# z is vertical
# -1000
# to
# 1000
