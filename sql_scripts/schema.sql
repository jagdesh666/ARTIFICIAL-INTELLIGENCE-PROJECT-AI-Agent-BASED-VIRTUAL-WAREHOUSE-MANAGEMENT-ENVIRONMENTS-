-- Purani tables delete karna (agar exist karti hain)
DROP TABLE IF EXISTS tasks;
DROP TABLE IF EXISTS robots;
DROP TABLE IF EXISTS inventory;

-- 1. Robots ki Table
CREATE TABLE robots (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    current_x INTEGER,
    current_y INTEGER,
    battery FLOAT DEFAULT 100.0,
    status VARCHAR(20) DEFAULT 'IDLE' -- IDLE, MOVING, CHARGING
);

-- 2. Inventory (Shelves) ki Table
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    shelf_row INTEGER,
    shelf_col INTEGER,
    item_name VARCHAR(100),
    quantity INTEGER
);

-- 3. Tasks ki Table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    description TEXT,
    assigned_robot_id INTEGER REFERENCES robots(id),
    status VARCHAR(20) DEFAULT 'PENDING', -- PENDING, COMPLETED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Truck/Inbound Stock ki table
CREATE TABLE inbound_stock (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    total_quantity INTEGER,
    remaining_quantity INTEGER,
    truck_row INTEGER,
    truck_col INTEGER,
    status VARCHAR(20) DEFAULT 'ARRIVED' -- ARRIVED, EMPTY
);

-- Raste mein chhote hue stock ki table
CREATE TABLE dropped_stock (
    id SERIAL PRIMARY KEY,
    item_name VARCHAR(100),
    quantity INTEGER,
    row INTEGER,
    col INTEGER
);