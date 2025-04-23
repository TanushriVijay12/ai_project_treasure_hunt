import pygame
from game import GridWorld
from agent import Agent
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, TILE_SIZE

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Treasure Hunt in Foggy Grid")
font = pygame.font.SysFont(None, 36)

def draw_grid(world, agent):
    for x in range(world.size):
        for y in range(world.size):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if (x, y) in world.revealed:
                pygame.draw.rect(screen, COLORS['safe'], rect)
                if (x, y) == world.treasure:
                    pygame.draw.circle(screen, COLORS['treasure'], rect.center, TILE_SIZE//4)
                elif (x, y) in world.traps:
                    pygame.draw.circle(screen, COLORS['trap'], rect.center, TILE_SIZE//4)
            else:
                pygame.draw.rect(screen, COLORS['fog'], rect)

            pygame.draw.rect(screen, COLORS['grid'], rect, 1)

    # draw agent
    ax, ay = agent.pos
    agent_rect = pygame.Rect(ax*TILE_SIZE, ay*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, COLORS['agent'], agent_rect)

def main():
    clock = pygame.time.Clock()
    grid_size = 5
    world = GridWorld(grid_size)
    agent = Agent(grid_size)

    running = True
    while running:
        screen.fill((0,0,0))
        draw_grid(world, agent)
        pygame.display.flip()

        pygame.time.wait(200)

        if world.status == "running":
            percepts = world.get_adjacent(agent.pos)
            agent.update_knowledge(percepts, world)
            move = agent.choose_move()
            if move:
                agent.move(move)
                world.move_agent_to(agent.pos)

        elif world.status == "won":
            pygame.display.set_caption("🎉 You found the treasure! Increasing grid size...")
            pygame.time.wait(1500)
            grid_size += 1
            world = GridWorld(grid_size)
            agent = Agent(grid_size)

        elif world.status == "lost":
            pygame.display.set_caption("💀 You hit a trap! Restarting...")
            pygame.time.wait(1500)
            world = GridWorld(grid_size)
            agent = Agent(grid_size)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(10)

if __name__ == '__main__':
    main()
