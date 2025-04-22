# main.py
import pygame
from config import *
from game import GridWorld

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Treasure Hunt in Foggy Grid")
font = pygame.font.SysFont(None, 36)

def draw_grid(world):
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
    ax, ay = world.agent_pos
    agent_rect = pygame.Rect(ax*TILE_SIZE, ay*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, COLORS['agent'], agent_rect)

def main():
    clock = pygame.time.Clock()
    world = GridWorld()

    running = True
    while running:
        screen.fill((0,0,0))
        draw_grid(world)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN and world.status == "running":
                if event.key == pygame.K_UP: world.move_agent(0, -1)
                if event.key == pygame.K_DOWN: world.move_agent(0, 1)
                if event.key == pygame.K_LEFT: world.move_agent(-1, 0)
                if event.key == pygame.K_RIGHT: world.move_agent(1, 0)

        if world.status == "won":
            pygame.display.set_caption("🎉 You found the treasure! Grid size will increase!")
            pygame.time.wait(1500)
            # increase grid
            GRID_SIZE_NEXT = world.size + 1
            world = GridWorld(size=GRID_SIZE_NEXT)
        elif world.status == "lost":
            pygame.display.set_caption("💀 You hit a trap! Game Over.")
            pygame.time.wait(1500)
            world = GridWorld(size=world.size)

        clock.tick(10)

if __name__ == '__main__':
    main()
