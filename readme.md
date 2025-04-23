# Treasure Hunt in Foggy Grid

An AI-powered puzzle game where an agent navigates through a fog-covered grid to find a hidden treasure while avoiding deadly traps. Inspired by Wumpus World and pathfinding under uncertainty, this project features manual control, logical inference, and visual simulation using Python and Pygame.


## Features

- 5x5 grid world with fog-of-war and expanding difficulty
- Randomly placed traps and hidden treasure
- A* Search algorithm to find paths through revealed safe tiles
- Partial observability: agent sees only adjacent tiles
- Movement logging to `log.txt` for analysis
- Press `T` to toggle full map (debug mode)
- Manual controls and replayable simulations
- Grid increases in size after each win!



## Getting Started

### Requirements
- Python 3.10+
- [`pygame`](https://www.pygame.org/)

```bash
pip install pygame