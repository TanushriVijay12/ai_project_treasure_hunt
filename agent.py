# agent.py
from utils import a_star
import random
from collections import defaultdict
class Agent:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.pos = (0, 0)
        self.visited = set()
        self.safe = {(0, 0)}
        self.frontier = set()
        self.unsafe = set()

        self.risk_map = defaultdict(lambda: 0.5)  # default risk 50% on unknowns

        # Add initial adjacent cells to frontier and safe for testing
        x, y = self.pos
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                self.frontier.add((nx, ny))
                self.safe.add((nx, ny))


    def update_knowledge(self, percepts, world):
        self.visited.add(self.pos)
        self.safe.add(self.pos)

        # Mark adjacent cells safe if no trap nearby
        for cell in percepts:
            if cell not in self.visited and cell not in self.unsafe:
                self.frontier.add(cell)
                self.safe.add(cell)

        if self.pos in world.traps:
            self.unsafe.add(self.pos)

        # Update risk map based on trap perception
        if self.pos in world.traps:
            # Increase risk around trap
            for nx, ny in world.get_adjacent(self.pos):
                if (nx, ny) not in self.safe:
                    self.risk_map[(nx, ny)] += 0.25
        else:
            # Decrease risk if no trap seen
            for nx, ny in world.get_adjacent(self.pos):
                if (nx, ny) not in self.safe:
                    self.risk_map[(nx, ny)] = max(0.0, self.risk_map[(nx, ny)] - 0.1)

    def choose_move(self):
        unexplored = self.frontier - self.visited
        if not unexplored:
            return None

        # Choose closest safe unexplored tile
        path, target = None, None
        for cell in unexplored:
            if cell in self.safe:
                result = a_star(self.pos, cell, self.grid_size, self.safe)
                if result and (path is None or len(result) < len(path)):
                    path = result
                    target = cell

         # Try safe known tile first
        if not path:
            lowest_risk = min(unexplored, key=lambda c: self.risk_map[c])
            print(f"[DEBUG] No safe path found. Picking lowest risk tile: {lowest_risk} with risk={self.risk_map[lowest_risk]:.2f}")
            result = a_star(self.pos, lowest_risk, self.grid_size, self.safe | {lowest_risk})
            if result and len(result) > 1:
                return result[1]

        if path and len(path) > 1:
            return path[1]  # next move
        return None

    def move(self, new_pos):
        self.pos = new_pos

    def plan_path(self, target):
        if target not in self.safe:
            print(f"Blocked move: {target} not in safe")
            return None
        path = a_star(self.pos, target, self.grid_size, self.safe)
        print(f"Path to {target}: {path}")
        return path