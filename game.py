# game.py
import random
from config import GRID_SIZE

class GridWorld:
    def __init__(self, size=GRID_SIZE):
        self.size = size
        self.agent_pos = (0, 0)
        self.visited = set()
        self.revealed = set()
        self.traps = self.generate_traps()
        self.treasure = self.generate_treasure()
        self.status = "running"

    def generate_traps(self, count=3):
        traps = set()
        while len(traps) < count:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x, y) != (0, 0):
                traps.add((x, y))
        return traps

    def generate_treasure(self):
        while True:
            x, y = random.randint(0, self.size-1), random.randint(0, self.size-1)
            if (x, y) != (0, 0) and (x, y) not in self.traps:
                return (x, y)

    def move_agent(self, dx, dy):
        if self.status != "running":
            return
        x, y = self.agent_pos
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.size and 0 <= ny < self.size:
            self.agent_pos = (nx, ny)
            self.revealed.add((nx, ny))
            self.revealed.update(self.get_adjacent((nx, ny)))
            self.visited.add((nx, ny))

            if (nx, ny) in self.traps:
                self.status = "lost"
            elif (nx, ny) == self.treasure:
                self.status = "won"

    def get_adjacent(self, pos):
        x, y = pos
        adj = [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]
        return [(a,b) for a,b in adj if 0 <= a < self.size and 0 <= b < self.size]
