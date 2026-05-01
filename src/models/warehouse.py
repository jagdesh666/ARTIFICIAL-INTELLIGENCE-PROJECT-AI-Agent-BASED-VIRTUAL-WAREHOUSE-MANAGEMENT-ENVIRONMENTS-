# src/models/warehouse.py
from src.config import ROWS, COLS

class Warehouse:
    def __init__(self):
        from src.config import ROWS, COLS
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.heatmap = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        # NEW: Store item info for specific shelves
        self.item_shelves = {} # Key: (row, col), Value: "item_name"

    def add_item_shelf(self, row, col, item_name):
        """Destination par box drop karke usay shelf banane ke liye"""
        self.grid[row][col] = 1 # Block the path
        self.item_shelves[(row, col)] = item_name.lower()


    def record_usage(self, row, col):
        """Jab bhi koi robot kisi cell par jaye, uski value barha do"""
        if 0 <= row < len(self.grid) and 0 <= col < len(self.grid[0]):
            self.heatmap[row][col] += 1

    def toggle_shelf(self, row, col):
        """Click karne par rasta shelf ban jaye, aur shelf rasta ban jaye."""
        if 0 <= row < ROWS and 0 <= col < COLS:
            if self.grid[row][col] == 0:
                self.grid[row][col] = 1
            else:
                self.grid[row][col] = 0

    def is_walkable(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.grid[row][col] == 0
        return False