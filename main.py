# treasure_hunt_ai/main.py
import pygame
from game import GridWorld
from agent import Agent
from config import get_screen_dimensions, COLORS, STATUS_PANEL_WIDTH

pygame.init()
grid_size = 5
SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE = get_screen_dimensions(grid_size)
#=screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Treasure Hunt in Foggy Grid")
font = pygame.font.SysFont(None, 36)

open("log.txt", "w").close()  # clear log at start

def risk_to_color(risk):
    # Clamp between 0 and 1
    risk = max(0.0, min(1.0, risk))
    r = int(255 * risk)
    g = int(255 * (1 - risk))
    b = 0
    return (r, g, b)


def draw_grid(screen, world, agent, reveal_all, visualize_a_star):
    for x in range(world.size):
        for y in range(world.size):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            tile = (x, y)

            # Decide color priority
            color = COLORS['fog']  # Default

            if tile == agent.pos:
                color = COLORS['agent']
            elif visualize_a_star and tile in agent.last_path:
                color = COLORS['path']
            elif visualize_a_star and tile in agent.last_open_set:
                color = COLORS['open']
            elif visualize_a_star and tile in agent.last_closed_set:
                color = COLORS['closed']
            elif reveal_all or tile in world.revealed:
                if tile in agent.suspected_traps:
                    color = COLORS['suspected_trap']
                elif tile in agent.suspected_pits:
                    color = COLORS['suspected_pit']
                elif tile in agent.safe:
                    color = COLORS['safe']
                else:
                    color = COLORS['safe_inferred']
            else:
                # Unrevealed: apply risk heatmap
                if tile in agent.risk_map:
                    color = risk_to_color(agent.risk_map[tile])
                else:
                    color = COLORS['fog']

            # Draw the cell
            pygame.draw.rect(screen, color, rect)

            # Draw grid border
            pygame.draw.rect(screen, COLORS['grid'], rect, 1)

            # Draw treasure or trap if revealed
            if reveal_all or tile in world.revealed:
                if tile == world.treasure:
                    pygame.draw.circle(screen, COLORS['treasure'], rect.center, TILE_SIZE // 4)
                elif tile in world.traps:
                    pygame.draw.circle(screen, COLORS['trap'], rect.center, TILE_SIZE // 4)


def draw_status(screen, world, agent, grid_size):
    status_x = grid_size * TILE_SIZE + 20  # right panel start

    info = f"Grid: {grid_size}x{grid_size}"
    moves = f"Moves: {len(agent.visited)}"
    info_text = font.render(info, True, COLORS['text'])
    moves_text = font.render(moves, True, COLORS['text'])
    screen.blit(info_text, (status_x, 40))
    screen.blit(moves_text, (status_x, 80))

    if world.status == "won":
        win_text = font.render("You won!", True, COLORS['win'])
        prompt = font.render("Press R to retry", True, COLORS['text'])
        screen.blit(win_text, (status_x, 120))
        screen.blit(prompt, (status_x, 160))
    elif world.status == "lost":
        lose_text = font.render("You lost!", True, COLORS['lose'])
        prompt = font.render("Press R to retry", True, COLORS['text'])
        screen.blit(lose_text, (status_x, 120))
        screen.blit(prompt, (status_x, 160))

def main():
    clock = pygame.time.Clock()
    grid_size = 5
    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE = get_screen_dimensions(grid_size)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    world = GridWorld(grid_size)
    agent = Agent(grid_size)


    # Reveal starting cell and adjacent cells
    world.revealed.add(agent.pos)
    world.revealed.update(world.get_adjacent(agent.pos))
    # Provide initial percepts
    initial_percepts = world.get_adjacent(agent.pos)
    agent.update_knowledge(initial_percepts, world)

    reveal_all = False
    visualize_a_star = True  # NEW TOGGLE FOR VISUALIZATION

    running = True
    while running:
        screen.fill((0, 0, 0))  # full window clear
        pygame.draw.rect(screen, COLORS['panel_bg'], (grid_size * TILE_SIZE, 0, STATUS_PANEL_WIDTH, SCREEN_HEIGHT))

        draw_grid(screen, world, agent, reveal_all, visualize_a_star)
        draw_status(screen, world, agent, grid_size)
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
                        percepts = world.get_percepts_at(agent.pos)
                        agent.update_knowledge(percepts, world)

                        if world.status == "running":
                            agent.infer_knowledge(world)  # Keep inferring!

                        with open("log.txt", "a") as f:
                            f.write(f"Moved to {agent.pos}\n")
                    else:
                        # If no path found, declare loss
                        print("[GAME OVER] No safe move possible. Declaring loss.")
                        world.status = "lost"
                        
                elif event.key == pygame.K_t:
                    reveal_all = not reveal_all
                    print(f"[DEBUG] reveal_all is now {reveal_all}")

                elif world.status in ["won", "lost"] and event.key == pygame.K_r:
                    if world.status == "won":
                        grid_size += 1
                    SCREEN_WIDTH, SCREEN_HEIGHT, TILE_SIZE = get_screen_dimensions(grid_size)
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                    world = GridWorld(grid_size)
                    agent = Agent(grid_size)
                    # Restore perception and knowledge
                    world.revealed.add(agent.pos)
                    world.revealed.update(world.get_adjacent(agent.pos))
                    initial_percepts = world.get_adjacent(agent.pos)
                    agent.update_knowledge(initial_percepts, world)

        clock.tick(10)

if __name__ == '__main__':
    main()
