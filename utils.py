# utils.py
import heapq

def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def get_neighbors(pos, grid_size):
    x, y = pos
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < grid_size and 0 <= ny < grid_size:
            yield (nx, ny)

def a_star(start, goal, grid_size, allowed):
    queue = []
    heapq.heappush(queue, (0, [start]))
    visited = set()

    while queue:
        cost, path = heapq.heappop(queue)
        current = path[-1]
        if current == goal:
            return path
        if current in visited:
            continue
        visited.add(current)

        for neighbor in get_neighbors(current, grid_size):
            if neighbor in allowed:
                new_cost = cost + 1 + heuristic(neighbor, goal)
                heapq.heappush(queue, (new_cost, path + [neighbor]))
    return None
