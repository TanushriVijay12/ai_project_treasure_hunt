# agent.py
from utils import a_star
import random

class Agent:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.pos = (0, 0)
        self.visited = set()
        self.safe = {(0, 0)}
        self.frontier = set()
        self.unsafe = set()

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

    def choose_move(self):
        unexplored = self.frontier - self.visited
        if not unexplored:
            return None

        # Choose closest safe unexplored tile
        path, target = None, None
        for cell in unexplored:
            result = a_star(self.pos, cell, self.grid_size, self.safe)
            if result:
                if path is None or len(result) < len(path):
                    path = result
                    target = cell

        if path and len(path) > 1:
            return path[1]  # next move
        return None

    def move(self, new_pos):
        self.pos = new_pos
