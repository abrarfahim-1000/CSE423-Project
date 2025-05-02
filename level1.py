player_pos1 = [850, 30, 850]
player_angle1 = 270
road1=[(-850, -640, -850, 990),(-750, 850, 1000, 850)]

level1_parked_cars = [
    {"model": "suv", "color": (0.0, 0.5, 0.0), "pos": [-650, 0, -850], "angle": 90},
    {"model": "car", "color": (1.0, 0.0, 0.0), "pos": [-450, 0, -850], "angle": 90},
    {"model": "bus", "color": (0.0, 0.0, 0.5), "pos": [-250, 0, 500], "angle": 90},
    {"model": "truck", "color": (0.5, 0.5, 0.0), "pos": [-500, 0, 0], "angle": 180}
]

level1_obstacles = [
    {"type": "cone", "pos": [-1000, 0, -600]},
    {"type": "cone", "pos": [-1000, 0, -350]},
    {"type": "cone", "pos": [-1000, 0, -100]},
    {"type": "cone", "pos": [-1000, 0, 150]},
    {"type": "cone", "pos": [-1000, 0, 400]},
    {"type": "cone", "pos": [-1000, 0, 650]},
    {"type": "cone", "pos": [-1000, 0, 900]},
    
    {"type": "barrier", "pos": [-700, 0, -550], "angle": 90},
    {"type": "barrier", "pos": [-700, 0, -200], "angle": 90},
    {"type": "barrier", "pos": [-700, 0, 150], "angle": 90},
    {"type": "barrier", "pos": [-700, 0, 500], "angle": 90},
    
    {"type": "cone", "pos": [-700, 0, 690]},
    {"type": "cone", "pos": [-350, 0, 690]},
    {"type": "cone", "pos": [0, 0, 690]},
    {"type": "cone", "pos": [350, 0, 690]},
    {"type": "cone", "pos": [700, 0, 690]},
    
    {"type": "barrier", "pos": [-600, 0, 1000], "angle": 0},
    {"type": "barrier", "pos": [-150, 0, 1000], "angle": 0},
    {"type": "barrier", "pos": [300, 0, 1000], "angle": 0},
    {"type": "barrier", "pos": [750, 0, 1000], "angle": 0},
    
    {"type": "barrier", "pos": [-950, 0, -850], "angle": 90},
    {"type": "barrier", "pos": [-750, 0, -850], "angle": 90}
]

level1_parking_spots = [
    {"pos": [-850, 0, -850], "angle": 180, "occupied": False},
]