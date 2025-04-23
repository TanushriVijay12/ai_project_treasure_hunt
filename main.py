# treasure_hunt_ai/main.py
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

def draw_status(world):
    if world.status == "won":
        text = font.render("🎉 You won! Press R to retry with larger grid.", True, (255, 255, 255))
        screen.blit(text, (20, 10))
    elif world.status == "lost":
        text = font.render("💀 You lost! Press R to retry.", True, (255, 255, 255))
        screen.blit(text, (20, 10))

def main():
    clock = pygame.time.Clock()
    grid_size = 5
    world = GridWorld(grid_size)
    agent = Agent(grid_size)

    running = True
    while running:
        screen.fill((0,0,0))
        draw_grid(world, agent)
        draw_status(world)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if world.status == "running":
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP: dy = -1
                    elif event.key == pygame.K_DOWN: dy = 1
                    elif event.key == pygame.K_LEFT: dx = -1
                    elif event.key == pygame.K_RIGHT: dx = 1

                    target = (agent.pos[0] + dx, agent.pos[1] + dy)
                    path = agent.plan_path(target)
                    if path and len(path) > 1:
                        agent.move(path[1])
                        world.move_agent_to(agent.pos)
                        percepts = world.get_adjacent(agent.pos)
                        agent.update_knowledge(percepts, world)
                    else:
                        print(f"Blocked move: {target} not in safe")

                elif world.status in ["won", "lost"] and event.key == pygame.K_r:
                    if world.status == "won":
                        grid_size += 1
                    world = GridWorld(grid_size)
                    agent = Agent(grid_size)

        clock.tick(10)

if __name__ == '__main__':
    main()
