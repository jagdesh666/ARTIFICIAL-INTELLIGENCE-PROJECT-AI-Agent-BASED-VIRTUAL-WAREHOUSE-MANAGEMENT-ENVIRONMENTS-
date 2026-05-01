# src/models/agent.py
import pygame
import random
import tkinter as tk
from tkinter import messagebox
from src.config import GRID_SIZE, CHARGING_STATIONS


class Agent:
    def __init__(self, agent_id, name, row, col, color):
        self.id = agent_id
        self.name = name
        self.row = row
        self.col = col
        self.battery = 100.0
        self.status = "IDLE"
        self.path = []
        self.color = color
        self.current_task_id = None
        self.current_task_type = None
        self.wait_count = 0
        self.priority = agent_id

        # Stock Management
        self.is_carrying = False
        self.cargo = None

    def fetch_task(self, db, warehouse):
        """Battery check pehle, naya task baad mein"""
        # Agar battery 25% se kam hai, to naya task kabhi mat uthao
        if self.battery <= 25:
            return

        if self.status != "IDLE":
            return

        from src.algorithms.a_star import get_a_star_path

        # 1. Truck
        truck = db.get_active_truck()
        if truck and not self.is_carrying:
            t_id, item, _, _, t_row, t_col = truck
            self.path = get_a_star_path(warehouse.grid, (self.row, self.col), (t_row, t_col))
            if self.path:
                self.status, self.current_task_type, self.current_task_id = "GOING_TO_TRUCK", "TRUCK", t_id
                return

        # 2. Dropped Stock
        dropped_list = db.get_dropped_stocks()
        if dropped_list and not self.is_carrying:
            d_id, item, qty, d_row, d_col = dropped_list[0]
            self.path = get_a_star_path(warehouse.grid, (self.row, self.col), (d_row, d_col))
            if self.path:
                self.status, self.current_task_type, self.current_task_id = "GOING_TO_DROPPED", "DROPPED", d_id
                return

        # 3. Normal Tasks
        task = db.fetch_nearest_task(self.id, self.row, self.col)
        if task:
            task_id, description = task
            self.current_task_id, self.current_task_type = task_id, "NORMAL"
            try:
                target_row, target_col = map(int, description.split(','))
                self.path = get_a_star_path(warehouse.grid, (self.row, self.col), (target_row, target_col))
                self.status = "MOVING" if self.path else "IDLE"
            except:
                db.update_task_status(task_id, self.id, 'FAILED')

    def show_confirmation(self, title, message):
        root = tk.Tk()
        root.withdraw()
        root.attributes("-topmost", True)
        response = messagebox.askyesno(title, message)
        root.destroy()
        return response

    def drop_at_destination(self, db, warehouse, all_agents):
        """Manual storage at destination"""
        if self.is_carrying and self.status == "IDLE":
            item = self.cargo['item']
            warehouse.add_item_shelf(self.row, self.col, item)
            db.add_inventory(self.row, self.col, item, self.cargo['qty'])
            self.is_carrying, self.cargo = False, None
            # Safety step away
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = self.row + dr, self.col + dc
                if warehouse.is_walkable(nr, nc) and not any((o.row, o.col) == (nr, nc) for o in all_agents):
                    self.row, self.col = nr, nc
                    db.update_robot_pos(self.id, self.row, self.col, self.battery)
                    break
            return True
        return False

    def move(self, db, all_agents, warehouse):
        # --- 1. EMERGENCY BATTERY TRIGGER (FORCED ACTION) ---
        # Agar battery 25% se kam ho, to foran sab roko
        if self.battery < 25:
            if self.is_carrying:
                print(f"DEBUG: {self.name} emergency drop due to low battery.")
                db.add_dropped_stock(self.cargo['item'], self.cargo['qty'], self.row, self.col)
                self.is_carrying, self.cargo, self.path = False, None, []

            if self.status not in ["CHARGING", "GOING_TO_CHARGE"]:
                from src.algorithms.a_star import get_a_star_path
                # Nearest station dhoondo bajaye random ke
                nearest_station = min(CHARGING_STATIONS, key=lambda s: abs(s[0] - self.row) + abs(s[1] - self.col))
                self.path = get_a_star_path(warehouse.grid, (self.row, self.col), nearest_station)
                if self.path:
                    self.status = "GOING_TO_CHARGE"
                    print(f"DEBUG: {self.name} force heading to charge.")

        # --- 2. CHARGING PROCESS ---
        if self.status == "CHARGING":
            self.battery = min(100, self.battery + 1.0)  # Faster charging
            db.update_robot_pos(self.id, self.row, self.col, round(self.battery, 2))
            if self.battery >= 100:
                self.status = "IDLE"
            return

        # --- 3. ACTIVE YIELDING (Dhaka Logic) ---
        for other in all_agents:
            if other.id != self.id and other.path:
                if other.path[0] == (self.row, self.col):
                    if self.status == "IDLE" or self.id > other.id:
                        neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                        random.shuffle(neighbors)
                        for dr, dc in neighbors:
                            nr, nc = self.row + dr, self.col + dc
                            if warehouse.is_walkable(nr, nc) and not any(
                                    (o.row, o.col) == (nr, nc) for o in all_agents):
                                self.row, self.col = nr, nc
                                self.path = []
                                db.update_robot_pos(self.id, self.row, self.col, round(self.battery, 2))
                                return

        # --- 4. MOVEMENT ---
        if self.path:
            next_step = self.path[0]
            other = next((o for o in all_agents if o.id != self.id and (o.row, o.col) == next_step), None)

            if not other:
                self.path.pop(0)
                self.row, self.col = next_step
                warehouse.record_usage(self.row, self.col)
                self.battery -= 0.12  # Move consumption
                db.update_robot_pos(self.id, self.row, self.col, round(self.battery, 2))

                if not self.path:
                    if self.status == "GOING_TO_CHARGE":
                        self.status = "CHARGING"
                    elif self.status == "GOING_TO_TRUCK":
                        truck = db.get_active_truck()
                        if truck and self.show_confirmation("Truck", f"Pick 10x {truck[1]}?"):
                            self.is_carrying, self.cargo = True, {"item": truck[1], "qty": 10}
                            db.update_truck_quantity(truck[0], 10)
                        self.status = "IDLE"
                    elif self.status == "GOING_TO_DROPPED":
                        dropped = db.get_dropped_stocks()
                        d_item = next((d for d in dropped if d[3] == self.row and d[4] == self.col), None)
                        if d_item and self.show_confirmation("Recover", f"Pick dropped {d_item[1]}?"):
                            self.is_carrying, self.cargo = True, {"item": d_item[1], "qty": d_item[2]}
                            db.remove_dropped_stock(d_item[0])
                        self.status = "IDLE"
                    else:
                        db.update_task_status(self.current_task_id, self.id, 'COMPLETED')
                        self.status = "IDLE"
            else:
                self.status = "WAITING"
                self.wait_count += 1
                if self.wait_count > 10:
                    from src.algorithms.a_star import get_a_star_path
                    new_path = get_a_star_path(warehouse.grid, (self.row, self.col), self.path[-1],
                                               [(o.row, o.col) for o in all_agents if o.id != self.id])
                    if new_path: self.path = new_path
                    self.wait_count = 0
        else:
            self.status = "IDLE"
            self.battery -= 0.02  # Passive drain while idle
            db.update_robot_pos(self.id, self.row, self.col, round(self.battery, 2))

    def draw(self, screen):
        x, y = self.col * GRID_SIZE + GRID_SIZE // 4, self.row * GRID_SIZE + GRID_SIZE // 4
        size = GRID_SIZE // 2
        pygame.draw.rect(screen, self.color, (x, y, size, size))
        if self.is_carrying:
            pygame.draw.rect(screen, (139, 69, 19), (x + 2, y + 2, size - 4, size - 4))
        pygame.draw.circle(screen, (255, 255, 255), (x + size // 2, y + size // 2), 3)