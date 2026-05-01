# src/config.py

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Grid Settings
GRID_SIZE = 20  # Ek cell kitne pixels ka hoga
ROWS = 25       # Warehouse mein kitni rows hongi
COLS = 30       # Warehouse mein kitne columns honge

# Colors (RGB)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRID = (200, 200, 200) # Halki gray lines grid ke liye
COLOR_BG = (240, 240, 240)   # Background color


# Isay src/config.py mein add karein
COLOR_SHELF = (50, 50, 50)  # Dark Gray/Black for shelves


# src/config.py mein add karein
COLOR_CHARGING = (255, 255, 0) # Yellow for charging stations
CHARGING_STATIONS = [(1, 1), (1, COLS-2), (ROWS-2, 1)] # Corners mein charging stations


# src/config.py mein add karein
COLOR_TRUCK = (255, 165, 0) # Orange for Truck
COLOR_DROPPED = (139, 69, 19) # Brown for Dropped Boxes
MAX_CAPACITY = 10
TRUCK_LOCATION = (ROWS-2, COLS-5) # Truck khara hone ki jagah


# src/config.py mein add karein
ITEM_COLORS = {
    "iphone": (255, 100, 100),   # Light Red
    "laptop": (100, 255, 100),   # Light Green
    "tablet": (100, 100, 255),   # Light Blue
    "default": (150, 150, 150)   # Gray
}