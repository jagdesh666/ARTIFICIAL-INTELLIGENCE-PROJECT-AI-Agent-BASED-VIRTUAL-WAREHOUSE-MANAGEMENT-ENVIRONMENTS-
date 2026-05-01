# src/database/db_handler.py
import psycopg2
import os
from dotenv import load_dotenv

# .env file se details load karna
load_dotenv()


class DatabaseHandler:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT")
            )
            self.cursor = self.conn.cursor()
            print("PostgreSQL connected successfully!")
        except Exception as e:
            print(f"Error connecting to database: {e}")

    def execute_script(self, script_path):
        """SQL file run karne ke liye"""
        try:
            with open(script_path, 'r') as f:
                self.cursor.execute(f.read())
            self.conn.commit()
            print("Database schema created successfully!")
        except Exception as e:
            print(f"Error executing script: {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()

    # --- ROBOT MANAGEMENT ---
    def register_robot(self, name, row, col):
        query = "INSERT INTO robots (name, current_x, current_y) VALUES (%s, %s, %s) RETURNING id;"
        self.cursor.execute(query, (name, row, col))
        robot_id = self.cursor.fetchone()[0]
        self.conn.commit()
        return robot_id

    def update_robot_pos(self, robot_id, row, col, battery):
        query = "UPDATE robots SET current_x = %s, current_y = %s, battery = %s WHERE id = %s;"
        self.cursor.execute(query, (row, col, battery, robot_id))
        self.conn.commit()

    # --- INVENTORY & SHELF MANAGEMENT ---
    def add_inventory(self, row, col, item_name, quantity):
        """Permanent storage: Shelf par saman ka record DB mein save karna"""
        try:
            query = "INSERT INTO inventory (shelf_row, shelf_col, item_name, quantity) VALUES (%s, %s, %s, %s);"
            self.cursor.execute(query, (row, col, item_name, quantity))
            self.conn.commit()
            print(f"DEBUG: Inventory logged in DB - {quantity} units of {item_name}")
        except Exception as e:
            print(f"Error adding inventory: {e}")
            self.conn.rollback()

    # --- TRUCK MANAGEMENT ---
    def add_truck(self, item, qty, r, c):
        try:
            query = "INSERT INTO inbound_stock (item_name, total_quantity, remaining_quantity, truck_row, truck_col) VALUES (%s, %s, %s, %s, %s);"
            self.cursor.execute(query, (item, qty, qty, r, c))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def get_active_truck(self):
        self.cursor.execute(
            "SELECT id, item_name, total_quantity, remaining_quantity, truck_row, truck_col FROM inbound_stock WHERE status = 'ARRIVED' AND remaining_quantity > 0 LIMIT 1;")
        return self.cursor.fetchone()

    def update_truck_quantity(self, truck_id, amount_picked):
        try:
            query = "UPDATE inbound_stock SET remaining_quantity = remaining_quantity - %s WHERE id = %s RETURNING remaining_quantity;"
            self.cursor.execute(query, (amount_picked, truck_id))
            rem = self.cursor.fetchone()[0]
            if rem <= 0:
                self.cursor.execute("UPDATE inbound_stock SET status = 'EMPTY' WHERE id = %s", (truck_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    # --- DROPPED STOCK MANAGEMENT ---
    def add_dropped_stock(self, item, qty, r, c):
        try:
            query = "INSERT INTO dropped_stock (item_name, quantity, row, col) VALUES (%s, %s, %s, %s);"
            self.cursor.execute(query, (item, qty, r, c))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    def get_dropped_stocks(self):
        self.cursor.execute("SELECT id, item_name, quantity, row, col FROM dropped_stock;")
        return self.cursor.fetchall()

    def remove_dropped_stock(self, stock_id):
        try:
            self.cursor.execute("DELETE FROM dropped_stock WHERE id = %s", (stock_id,))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()

    # --- TASK MANAGEMENT ---
    def fetch_nearest_task(self, robot_id, r_row, r_col):
        try:
            query = "SELECT id, description FROM tasks WHERE status = 'PENDING' FOR UPDATE SKIP LOCKED;"
            self.cursor.execute(query)
            tasks = self.cursor.fetchall()
            if not tasks: return None

            best_task, min_dist = None, float('inf')
            for t_id, desc in tasks:
                t_row, t_col = map(int, desc.split(','))
                dist = abs(r_row - t_row) + abs(r_col - t_col)
                if dist < min_dist:
                    min_dist, best_task = dist, (t_id, desc)

            if best_task:
                self.cursor.execute("UPDATE tasks SET status = 'IN_PROGRESS', assigned_robot_id = %s WHERE id = %s;",
                                    (robot_id, best_task[0]))
                self.conn.commit()
                return best_task
            return None
        except Exception as e:
            self.conn.rollback()
            return None

    def update_task_status(self, task_id, robot_id, status):
        query = "UPDATE tasks SET assigned_robot_id = %s, status = %s WHERE id = %s;"
        self.cursor.execute(query, (robot_id, status, task_id))
        self.conn.commit()