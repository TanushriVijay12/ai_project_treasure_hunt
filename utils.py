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
    def heuristic(a, b):
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    queue = []
    heapq.heappush(queue, (0 + heuristic(start, goal), [start]))
    visited = set()

    open_set_log = set()
    closed_set_log = set()

    while queue:
        cost, path = heapq.heappop(queue)
        current = path[-1]

        if current == goal:
            return path, open_set_log, closed_set_log

        if current in visited:
            continue
        visited.add(current)
        closed_set_log.add(current)

        for neighbor in get_neighbors(current, grid_size):
            if neighbor in allowed and neighbor not in visited:
                new_cost = cost + 1 + heuristic(neighbor, goal)
                heapq.heappush(queue, (new_cost, path + [neighbor]))
                open_set_log.add(neighbor)

    return None, open_set_log, closed_set_log
