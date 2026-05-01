# src/main.py
import pygame
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox
from src.config import *
from src.ui.renderer import WarehouseRenderer
from src.models.warehouse import Warehouse
from src.models.agent import Agent
from src.database.db_handler import DatabaseHandler


def get_truck_input():
    """Tkinter popup to get truck details from user"""
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    item_name = simpledialog.askstring("Truck Arrival", "What item is in the truck? (e.g. iphone, laptop)", parent=root)
    if item_name:
        quantity = simpledialog.askinteger("Truck Arrival", f"How many boxes of {item_name}?", parent=root, minvalue=1,
                                           maxvalue=500)
        root.destroy()
        return item_name.lower(), quantity  # Lowercase for color mapping
    root.destroy()
    return None, None


def main():
    # 1. Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("IntelliRoute Pro - Logistics Management System")
    clock = pygame.time.Clock()

    # 2. Database & Models
    db = DatabaseHandler()

    # Database Clean-up: Purane robots delete karein taake IDs fresh shuru hon
    try:
        db.cursor.execute("TRUNCATE TABLE robots CASCADE;")
        db.conn.commit()
    except:
        db.conn.rollback()

    warehouse = Warehouse()
    agents = []

    # 3. Register 3 Robots (Red, Green, Blue)
    robot_configs = [
        ("Bot-Red", 0, 0, (255, 50, 50)),
        ("Bot-Green", 0, 5, (50, 255, 50)),
        ("Bot-Blue", 0, 10, (50, 50, 255))
    ]
    for name, r, c, color in robot_configs:
        r_id = db.register_robot(name, r, c)
        agents.append(Agent(r_id, name, r, c, color))

    # 4. Renderer Setup
    renderer = WarehouseRenderer(screen, warehouse, agents)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # --- MOUSE INTERACTIONS ---
            # LEFT CLICK: Toggle manual black shelves (Obstacles)
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                col, row = pos[0] // GRID_SIZE, pos[1] // GRID_SIZE
                warehouse.toggle_shelf(row, col)

            # RIGHT CLICK: Create a target destination for Robots
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                pos = pygame.mouse.get_pos()
                t_col, t_row = pos[0] // GRID_SIZE, pos[1] // GRID_SIZE
                task_desc = f"{t_row},{t_col}"
                # Database mein task insert karein
                db.cursor.execute("INSERT INTO tasks (description, status) VALUES (%s, %s);", (task_desc, 'PENDING'))
                db.conn.commit()
                print(f"DEBUG: New Destination Set at ({t_row}, {t_col})")

            # --- KEYBOARD INTERACTIONS ---
            if event.type == pygame.KEYDOWN:
                # 'T' KEY: Trigger Truck Arrival
                if event.key == pygame.K_t:
                    item, qty = get_truck_input()
                    if item and qty:
                        # Truck dock location (Bottom Right area)
                        t_row, t_col = ROWS - 3, COLS - 4
                        db.add_truck(item, qty, t_row, t_col)
                        messagebox.showinfo("Logistics", f"Truck with {qty} units of {item} arrived at Dock.")

                # 'D' KEY: Drop cargo and create a permanent colored shelf
                if event.key == pygame.K_d:
                    dropped_any = False
                    for agent in agents:
                        # Sirf wahi robot drop karega jo maal uthaye hue hai aur manzil par khara hai
                        if agent.is_carrying and agent.status == "IDLE":
                            # agent.py ka drop_at_destination call karein
                            if agent.drop_at_destination(db, warehouse, agents):
                                dropped_any = True
                                break  # Ek waqt mein ek hi robot process karein
                    if not dropped_any:
                        print("DEBUG: No robot ready to drop cargo at destination.")

        # --- AI & ROBOT LOGIC ---
        for agent in agents:
            # Step 1: Smart Task Fetching (Truck > Dropped > Manual Task)
            agent.fetch_task(db, warehouse)

            # Step 2: Movement (Battery, Reversing, and Collision logic)
            agent.move(db, agents, warehouse)

        # --- DRAWING ---
        # Render pass 'db' for live truck and dropped stock visualization
        renderer.render(db)

        pygame.display.flip()
        clock.tick(10)  # 10 FPS for better visualization

    # Cleanup before exit
    db.close()
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()