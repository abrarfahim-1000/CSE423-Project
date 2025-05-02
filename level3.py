player_pos3 = [800, 30, 825]
player_angle3 = 180
road3=[
    (800, 980, 800, 500),
    (940, 500, -340, 500),
    (-200, 500, -200, -200),
    (-340, -200, 640, -200),
    (500, -340, 500, -640),
    (500, -500, -950, -500),
]

level3_parked_cars = [
    {"model": "suv", "color": (0.0, 0.5, 0.0), "pos": [300, 30, 700], "angle": 0},
    {"model": "car", "color": (1.0, 0.0, 0.0), "pos": [-400, 30, 700], "angle": 90},
    {"model": "bus", "color": (0.6, 0.0, 0.5), "pos": [-600, 30, 200], "angle": 0},
    {"model": "truck", "color": (0.5, 0.5, 0.0), "pos": [700, 30, -350], "angle": 270},
    {"model": "suv", "color": (0.3, 0.3, 0.3), "pos": [-400, 30, -700], "angle": 0}
]

level3_obstacles = [
    {"type": "cone", "pos": [650, 0, 930]},
    {"type": "cone", "pos": [650, 0, 630]},

    {"type": "barrier", "pos": [950, 0, 880], "angle": 90},
    {"type": "barrier", "pos": [950, 0, 580], "angle": 90},
    
    {"type": "cone", "pos": [600, 0, 330]},
    {"type": "cone", "pos": [200, 0, 330]},
    
    {"type": "barrier", "pos": [500, 0, 650], "angle": 0},
    {"type": "barrier", "pos": [100, 0, 650], "angle": 0},
    {"type": "barrier", "pos": [-150, 0, 650], "angle": 0},
    
    {"type": "cone", "pos": [-350, 0, 400]},
    {"type": "cone", "pos": [-350, 0, 100]},
    {"type": "cone", "pos": [-350, 0, -150]},
    
    {"type": "barrier", "pos": [-50, 0, 200], "angle": 90},
    
    {"type": "cone", "pos": [-600, 0, -370]},
    {"type": "cone", "pos": [-300, 0, -370]},
    {"type": "cone", "pos": [100, 0, -370]},
    
    {"type": "barrier", "pos": [100, 0, -50], "angle": 0},
    {"type": "barrier", "pos": [400, 0, -50], "angle": 0},
    
    {"type": "barrier", "pos": [650, 0, -100], "angle": 90},
    {"type": "barrier", "pos": [650, 0, -550], "angle": 90},
    
    {"type": "barrier", "pos": [300, 0, -650], "angle": 0},
    {"type": "barrier", "pos": [-150, 0, -650], "angle": 0},
    {"type": "barrier", "pos": [-600, 0, -650], "angle": 0},
    
    {"type": "barrier", "pos": [-950, 0, -850], "angle": 90},
    {"type": "barrier", "pos": [-750, 0, -850], "angle": 90}
]

level3_parking_spots = [
    {"pos": [-850, 0, -850], "angle": 180, "occupied": False}
]

# x is horizontal
# -1000 to 1000

# z is vertical
# -1000
# to
# 1000
