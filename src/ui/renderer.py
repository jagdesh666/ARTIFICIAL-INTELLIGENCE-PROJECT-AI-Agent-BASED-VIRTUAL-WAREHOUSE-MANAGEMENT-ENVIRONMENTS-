# src/ui/renderer.py
import pygame
from src.config import *


class WarehouseRenderer:
    def __init__(self, screen, warehouse, agents):
        self.screen = screen
        self.warehouse = warehouse
        self.agents = agents
        # Professional Fonts
        self.font = pygame.font.SysFont("Arial", 13, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 11)

    def draw_grid(self):
        for x in range(0, COLS * GRID_SIZE + 1, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (x, 0), (x, ROWS * GRID_SIZE))
        for y in range(0, ROWS * GRID_SIZE + 1, GRID_SIZE):
            pygame.draw.line(self.screen, COLOR_GRID, (0, y), (COLS * GRID_SIZE, y))

    def draw_heatmap(self):
        for r in range(ROWS):
            for c in range(COLS):
                usage = self.warehouse.heatmap[r][c]
                if usage > 0:
                    alpha = min(usage * 15, 160)
                    s = pygame.Surface((GRID_SIZE, GRID_SIZE))
                    s.set_alpha(alpha)
                    s.fill((255, 0, 0))
                    self.screen.blit(s, (c * GRID_SIZE, r * GRID_SIZE))

    def draw_truck_and_dropped(self, db):
        truck = db.get_active_truck()
        if truck:
            r, c = truck[4], truck[5]
            pygame.draw.rect(self.screen, (255, 165, 0), (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE * 2, GRID_SIZE * 2))
            label = self.small_font.render(f"TRUCK: {truck[1]} ({truck[3]} left)", True, (200, 100, 0))
            self.screen.blit(label, (c * GRID_SIZE, r * GRID_SIZE - 15))

        dropped_stocks = db.get_dropped_stocks()
        for d in dropped_stocks:
            dr, dc = d[3], d[4]
            pygame.draw.rect(self.screen, (139, 69, 19),
                             (dc * GRID_SIZE + 4, dr * GRID_SIZE + 4, GRID_SIZE - 8, GRID_SIZE - 8))
            cap = self.small_font.render(f"DROPPED: {d[1]}", True, (139, 69, 19))
            self.screen.blit(cap, (dc * GRID_SIZE, dr * GRID_SIZE + GRID_SIZE))

    def draw_stations(self):
        for r, c in CHARGING_STATIONS:
            rect = pygame.Rect(c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(self.screen, COLOR_CHARGING, rect, 3)
            label = self.small_font.render("C", True, COLOR_CHARGING)
            self.screen.blit(label, (c * GRID_SIZE + 5, r * GRID_SIZE + 2))

    def draw_shelves(self):
        from src.config import ITEM_COLORS, COLOR_SHELF
        for r in range(ROWS):
            for c in range(COLS):
                if self.warehouse.grid[r][c] == 1:
                    rect = pygame.Rect(c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                    if (r, c) in self.warehouse.item_shelves:
                        item_name = self.warehouse.item_shelves[(r, c)]
                        color = ITEM_COLORS.get(item_name, ITEM_COLORS.get("default", (150, 150, 150)))
                        pygame.draw.rect(self.screen, color, rect)
                        pygame.draw.rect(self.screen, (255, 255, 255), rect, 1)
                    else:
                        pygame.draw.rect(self.screen, COLOR_SHELF, rect)

    def draw_dashboard(self):
        """Side Panel with Live Telemetry and Numeric Battery Percentage"""
        start_x = COLS * GRID_SIZE + 10
        y_offset = 60
        # Dark Background for Dashboard
        pygame.draw.rect(self.screen, (40, 44, 52),
                         (COLS * GRID_SIZE, 0, WINDOW_WIDTH - (COLS * GRID_SIZE), WINDOW_HEIGHT))

        title = self.font.render("--- INTELLIROUTE DASHBOARD ---", True, (255, 255, 255))
        self.screen.blit(title, (start_x, 20))

        for agent in self.agents:
            # Robot Color Indicator
            pygame.draw.rect(self.screen, agent.color, (start_x, y_offset, 12, 12))

            # Name and Cargo Info
            cargo_info = f" | [{agent.cargo['item'].upper()}]" if agent.is_carrying else ""
            name_text = self.font.render(f"{agent.name}{cargo_info}", True, (255, 255, 255))
            self.screen.blit(name_text, (start_x + 20, y_offset - 3))

            # Status Text
            status_text = self.small_font.render(f"Status: {agent.status}", True, (200, 200, 200))
            self.screen.blit(status_text, (start_x + 20, y_offset + 15))

            # --- BATTERY SECTION ---
            # 1. Numeric Percentage Text (NEW FIX)
            batt_percent = int(agent.battery)
            batt_text = self.small_font.render(f"Battery: {batt_percent}%", True, (255, 255, 255))
            self.screen.blit(batt_text, (start_x + 20, y_offset + 30))

            # 2. Visual Battery Bar
            bar_color = (0, 255, 0) if batt_percent > 30 else (255, 50, 50)  # Red if low
            pygame.draw.rect(self.screen, (100, 100, 100), (start_x + 20, y_offset + 45, 100, 8))  # Background
            pygame.draw.rect(self.screen, bar_color, (start_x + 20, y_offset + 45, batt_percent, 8))  # Filled bar

            y_offset += 75  # Space between robots

        # Legend for Items
        legend_y = WINDOW_HEIGHT - 100
        from src.config import ITEM_COLORS
        l_title = self.small_font.render("ITEM STORAGE COLORS:", True, (255, 255, 255))
        self.screen.blit(l_title, (start_x, legend_y))
        ly = legend_y + 20
        for item, color in ITEM_COLORS.items():
            if item != "default":
                pygame.draw.rect(self.screen, color, (start_x, ly, 10, 10))
                l_txt = self.small_font.render(item.capitalize(), True, (200, 200, 200))
                self.screen.blit(l_txt, (start_x + 15, ly - 2))
                ly += 15

    def render(self, db):
        self.screen.fill(COLOR_BG)
        self.draw_heatmap()
        self.draw_stations()
        self.draw_shelves()
        self.draw_truck_and_dropped(db)
        for agent in self.agents:
            if agent.path:
                points = [(c * GRID_SIZE + GRID_SIZE // 2, r * GRID_SIZE + GRID_SIZE // 2) for (r, c) in agent.path]
                if len(points) > 1:
                    pygame.draw.lines(self.screen, agent.color, False, points, 2)
            agent.draw(self.screen)
        self.draw_grid()
        self.draw_dashboard()