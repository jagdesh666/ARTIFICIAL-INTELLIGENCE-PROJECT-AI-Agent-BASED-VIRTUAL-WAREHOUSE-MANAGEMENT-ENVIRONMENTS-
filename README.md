# 🤖 ARTIFICIAL INTELLIGENCE PROJECT  
## AI-Agent Based Virtual Warehouse Management Environment

---

## 📌 Project Overview

**IntelliRoute Pro** is an advanced **Multi-Agent Pathfinding (MAPF)** and logistics simulation designed to mimic real-world automated warehouses (like Amazon or Alibaba).

The project focuses on:
- Autonomous decision-making  
- Dynamic conflict resolution  
- Persistent data management using PostgreSQL  

The system features intelligent agents (robots) that:
- Perceive their environment  
- Manage battery levels  
- Coordinate with other agents to avoid deadlocks  
- Handle logistics tasks like truck unloading and inventory storage  

---

## 🚀 Key Features

### 1. 🧠 Intelligent Multi-Agent Pathfinding (MAPF)

- **A* (A-Star) Search Algorithm**  
  Agents calculate optimal routes using Manhattan Distance heuristics.

- **Conflict Resolution (Push & Yield Logic)**  
  - Priority-based reversing logic  
  - Lower ID = higher priority  
  - Idle agents move out of the way  

- **Dynamic Obstacle Handling**  
  Users can place/remove shelves in real-time → agents instantly recalculate paths.

---

### 2. 📦 Autonomous Logistics & Stock Management

- **Truck Inbound System (`T` Key)**  
  Simulates truck arrival → agents prioritize unloading tasks.

- **Smart Task Allocation (Nearest Neighbor)**  
  Agents pick the closest task instead of FIFO → faster + efficient.

- **Permanent Storage (`D` Key)**  
  - Items stored as color-coded shelves  
  - Example:  
    - iPhone → 🔴 Red  
    - Laptop → 🟢 Green  

- **Inventory Database**  
  All operations are logged in PostgreSQL in real-time.

---

### 3. 🔋 Energy & Battery Intelligence

- **Self-Preservation Mode**  
  Battery < 25% → agent moves to charging station.

- **Emergency Cargo Drop**  
  Critical battery → drops cargo (brown cell) before charging.

- **Stock Recovery System**  
  Idle robots detect dropped items and recover them automatically.

---

### 4. 📊 Real-Time Data Analytics

- **Traffic Heatmaps**  
  Frequently used paths turn darker red → helps identify bottlenecks.

- **Live Dashboard Includes:**  
  - Agent Status (Moving, Waiting, Charging, Yielding)  
  - Battery % with progress bars  
  - Current cargo  
  - Item color legend  

---

## 🛠 Technical Stack

- **Language:** Python 3.12+  
- **Graphics:** Pygame  
- **Database:** PostgreSQL  
- **GUI Input:** Tkinter  
- **Algorithms:**  
  - A* Search  
  - Finite State Machines (FSM)  
  - Manhattan Heuristics  
  - Greedy Task Allocation  

---

## 📂 Project Structure


IntelliRoute_Pro/
│
├── src/
│ ├── algorithms/ # A* & heuristics
│ ├── database/ # PostgreSQL handlers (CRUD)
│ ├── models/ # Agent, grid, task logic
│ ├── ui/ # Renderer, dashboard, heatmaps
│ ├── config.py # Constants (colors, grid, items)
│ └── main.py # Entry point
│
├── sql_scripts/ # schema.sql
├── .env # DB credentials (ignored)
├── .gitignore # security config
└── README.md


---

## 🎮 Controls & Interaction

| Key / Action  | Function |
|--------------|---------|
| Left Click   | Place/remove obstacle (wall/shelf) |
| Right Click  | Set destination for nearest robot |
| `T` Key      | Trigger truck arrival |
| `D` Key      | Store cargo permanently |
| Automatic    | Charging, collision avoidance, task execution |

---

## ⚙️ Installation & Setup

### 1. Database Setup

- Install PostgreSQL  
- Create database:


intelliroute_db


- Run:


sql_scripts/schema.sql


(using pgAdmin or DBeaver)

---

### 2. Environment Setup

Create a `.env` file:


DB_NAME=intelliroute_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432


---

### 3. Install Dependencies

```bash
python -m pip install pygame psycopg2-binary python-dotenv
4. Run the Project
python -m src.main
🎓 Academic Context

This project was developed for the 6th Semester Artificial Intelligence Course.
