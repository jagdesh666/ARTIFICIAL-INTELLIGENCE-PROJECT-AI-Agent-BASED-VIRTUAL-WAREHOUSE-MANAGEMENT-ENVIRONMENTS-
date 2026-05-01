ARTIFICIAL INTELLIGENCE PROJECT (AI-Agent BASED VIRTUAL WAREHOUSE MANAGEMENT ENVIRONMENTS)
📌 Project Overview
IntelliRoute Pro is an advanced Multi-Agent Pathfinding (MAPF) and Logistics Simulation designed to mimic real-world automated warehouses (like Amazon or Alibaba). The project focuses on autonomous decision-making, dynamic conflict resolution, and persistent data management using PostgreSQL.
The system features intelligent agents (robots) that perceive their environment, manage their own battery levels, coordinate with other agents to avoid deadlocks, and handle complex logistics tasks like truck unloading and inventory storage.
🚀 Key Features in Detail
1. Intelligent Multi-Agent Pathfinding (MAPF)
A (A-Star) Search Algorithm:* Each agent calculates the most efficient route using Manhattan Distance heuristics.
Conflict Resolution (Push & Yield Logic):
If an agent is blocked by another robot in a narrow corridor, it uses a Priority-Based Reversing Logic.
Higher priority agents (smaller IDs) are given the right of way.
IDLE agents will actively move out of the way if they detect another agent needs their current cell.
Dynamic Obstacle Handling: Users can place or remove "Shelves" (obstacles) in real-time, forcing all active agents to recalculate their paths instantly.
2. Autonomous Logistics & Stock Management
Truck Inbound System ('T' Key): Users can simulate a truck arrival at the loading dock. Agents will prioritize truck tasks over normal tasks to unload inventory.
Smart Task Allocation (Nearest-Neighbor): Instead of simple FIFO, agents scan the database to find the task closest to their current coordinates to minimize travel time and energy.
Permanent Item Storage ('D' Key): Once an agent reaches its destination with cargo, pressing 'D' stores the item. The cell transforms into a permanent, color-coded shelf based on the item category (e.g., iPhone = Red, Laptop = Green).
Inventory Database: Every item moved, stored, or dropped is logged into PostgreSQL in real-time.
3. Energy & Battery Intelligence
Self-Preservation: Agents monitor battery levels. If the battery drops below 25%, the agent aborts its mission and heads to the nearest charging station.
Emergency Cargo Drop: If a robot's battery becomes critical while carrying goods, it will "Emergency Drop" the cargo at its current location (creating a brown spot on the grid) before heading to charge.
Stock Recovery: Other idle robots with sufficient battery will autonomously detect dropped stock and attempt to recover and deliver it.
4. Real-Time Data Analytics
Traffic Heatmaps: The system tracks the usage frequency of every grid cell. Highly congested areas turn a deeper shade of Red, allowing warehouse managers to identify "bottlenecks."
Live Telemetry Dashboard: A dark-themed side panel displaying:
Agent Status (Moving, Waiting, Charging, Yielding).
Numeric Battery Percentage & Visual Progress Bars.
Current Cargo Information.
Item Color Legend.
🛠 Technical Stack
Language: Python 3.12+
Graphics: Pygame (High-performance 2D rendering)
Database: PostgreSQL (Relational storage with ACID compliance)
GUI Input: Tkinter (Integrated for user-driven data input)
Algorithms: A* Search, Finite State Machines (FSM), Manhattan Heuristics, Greedy Task Allocation.
📂 Project Structure
code
Text
IntelliRoute_Pro/
│
├── src/
│   ├── algorithms/    # Core AI: A* Implementation & Heuristics
│   ├── database/      # DB Handlers: PostgreSQL connections & CRUD operations
│   ├── models/        # Objects: Agent logic, Warehouse Grid, Task structures
│   ├── ui/            # Visualization: Renderer, Dashboard, Heatmaps
│   ├── config.py      # System Constants: Colors, Grid size, Item categories
│   └── main.py        # Entry Point: Event loop and logic orchestration
│
├── sql_scripts/       # Database Schema: schema.sql
├── .env               # Secrets: DB Credentials (Ignored by Git)
├── .gitignore         # Security: Prevents sensitive data upload
└── README.md          # Documentation
🎮 Controls & Interaction
Key/Action	Function
Left Click	Place or remove a black "Wall/Shelf" obstacle.
Right Click	Set a target destination for the nearest available robot.
'T' Key	Trigger a Truck Arrival popup (Item Name & Quantity).
'D' Key	Command a robot at its destination to store its cargo permanently.
Automatic	Robots will auto-charge, avoid collisions, and fetch tasks.
⚙️ Installation & Setup
1. Database Configuration
Install PostgreSQL and create a database named intelliroute_db.
Run the provided script in sql_scripts/schema.sql via DBeaver or pgAdmin.
2. Environment Setup
Create a .env file in the root directory:
code
Text
DB_NAME=intelliroute_db
DB_USER=postgres
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=5432
3. Dependencies
Install the required libraries:
code
Bash
python -m pip install pygame psycopg2-binary python-dotenv
4. Running the Project
code
Bash
python -m src.main
👥 Group Members
23k-0543 - Jagdesh
23k-0873 - Rana Mokshkumar
23k-0884 - Ahsan Raza
This project was developed for the 6th-semester Artificial Intelligence Course.
