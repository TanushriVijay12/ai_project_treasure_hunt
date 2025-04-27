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
        self.suspected_pits = set()
        self.suspected_traps = set()
        self.unsafe = set()
        self.last_open_set = set()
        self.last_closed_set = set()
        self.last_path = []


        self.risk_map = defaultdict(lambda: 0.5)  # default risk 50% on unknowns

        # Add initial adjacent cells to frontier and safe for testing
        x, y = self.pos
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < grid_size and 0 <= ny < grid_size:
                self.frontier.add((nx, ny))
                self.safe.add((nx, ny))

        self.last_open_set = set()
        self.last_closed_set = set()
        self.last_path = []
        
    def update_knowledge(self, percepts, world):
        self.visited.add(self.pos)
        self.safe.add(self.pos)

        if "breeze" in percepts:
            for cell in world.get_adjacent(self.pos):
                if cell not in self.safe and cell not in self.visited:
                    self.suspected_pits.add(cell)

        if "stench" in percepts:
            for cell in world.get_adjacent(self.pos):
                if cell not in self.safe and cell not in self.visited:
                    self.suspected_traps.add(cell)

        if not percepts:
            # No danger nearby → mark adjacent cells as safe!
            for cell in world.get_adjacent(self.pos):
                if cell not in self.visited:
                    self.safe.add(cell)
                    if cell in self.suspected_pits:
                        self.suspected_pits.discard(cell)
                    if cell in self.suspected_traps:
                        self.suspected_traps.discard(cell)

        # Update frontier as usual
        for cell in world.get_adjacent(self.pos):
            if cell not in self.visited and cell not in self.safe and cell not in self.unsafe:
                self.frontier.add(cell)

        # Check if we stepped into real danger
        if self.pos in world.traps or self.pos in world.pits:
            self.unsafe.add(self.pos)


    def choose_move(self):
        # Avoid suspected danger tiles
        unexplored = unexplored - self.suspected_pits - self.suspected_traps
        if not unexplored:
            return None

        # Choose closest safe unexplored tile
        path, target = None, None
        for cell in unexplored:
            if cell in self.safe:
                result, open_set, closed_set = a_star(self.pos, cell, self.grid_size, self.safe)
                self.last_open_set = open_set
                self.last_closed_set = closed_set
                self.last_path = result

                if result and (path is None or len(result) < len(path)):
                    path = result
                    target = cell

         # Try safe known tile first
        if not path:
            lowest_risk = min(unexplored, key=lambda c: self.risk_map[c])
            print(f"[DEBUG] No safe path found. Picking lowest risk tile: {lowest_risk} with risk={self.risk_map[lowest_risk]:.2f}")
            result, open_set, closed_set = a_star(self.pos, lowest_risk, self.grid_size, self.safe | {lowest_risk})
            self.last_open_set = open_set
            self.last_closed_set = closed_set
            self.last_path = result

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
        path, open_set, closed_set = a_star(self.pos, target, self.grid_size, self.safe)
        print(f"Path to {target}: {path}")
        self.last_open_set = open_set
        self.last_closed_set = closed_set
        self.last_path = path
        return path
    
    def infer_knowledge(self, world):
        """
        Use rule-based inference to deduce safe and unsafe (trap) tiles based on visited knowledge.
         """
        for cell in self.visited:
            if cell in world.traps:
                # If it's a trap, look at its unrevealed neighbors
                neighbors = world.get_adjacent(cell)
                unknowns = [n for n in neighbors if n not in self.safe and n not in self.unsafe]
                if len(unknowns) == 1:
                    self.unsafe.add(unknowns[0])
                    print(f"[INFER] Marking {unknowns[0]} as TRAP based on single unknown near trap {cell}")
            else:
                # If it's safe, mark unrevealed neighbors as likely safe
                neighbors = world.get_adjacent(cell)
                for n in neighbors:
                    if n not in self.unsafe and n not in self.safe:
                        self.safe.add(n)
                        print(f"[INFER] Marking {n} as SAFE based on safe cell {cell}")

    