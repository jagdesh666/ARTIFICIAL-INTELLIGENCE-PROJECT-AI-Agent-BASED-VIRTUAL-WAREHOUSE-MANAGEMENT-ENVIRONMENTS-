# src/algorithms/a_star.py
import heapq


def manhattan_distance(p1, p2):
    """Heuristic function for A*: Manhattan Distance"""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_a_star_path(grid, start, goal, dynamic_obstacles=None):
    """
    Finds the shortest path from start to goal.
    grid: 2D list (0 = path, 1 = shelf)
    start: (row, col)
    goal: (row, col)
    dynamic_obstacles: List of (row, col) representing other robots
    """
    rows = len(grid)
    cols = len(grid[0])

    # Priority Queue: (priority, (row, col))
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}

    # g_score: Cost from start to current node
    g_score = {start: 0}

    # f_score: Estimated total cost (g_score + heuristic)
    f_score = {start: manhattan_distance(start, goal)}

    while open_set:
        # Get node with the lowest f_score
        current = heapq.heappop(open_set)[1]

        # Check if we reached the goal
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Return path in correct order (start to goal)

        # Check neighbors (Up, Down, Left, Right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dr, current[1] + dc)

            # 1. Bounds check
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:

                # 2. Permanent Obstacles (Shelves) check
                if grid[neighbor[0]][neighbor[1]] == 1:
                    continue

                # 3. Dynamic Obstacles (Other Robots) check
                # We skip this check if the neighbor is the goal (to allow reaching the target)
                if dynamic_obstacles and neighbor in dynamic_obstacles and neighbor != goal:
                    continue

                # Calculate tentative g_score
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    # This is the best path found so far
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + manhattan_distance(neighbor, goal)

                    # Add neighbor to queue if not already there
                    if neighbor not in [i[1] for i in open_set]:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None  # No path found