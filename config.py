TILE_SIZE = 80
GRID_SIZE = 5
WINDOW_PADDING = 50

# Add a sidebar of 300px for status/info panel
STATUS_PANEL_WIDTH = 300

SCREEN_WIDTH = GRID_SIZE * TILE_SIZE + STATUS_PANEL_WIDTH
SCREEN_HEIGHT = GRID_SIZE * TILE_SIZE

COLORS = {
    'fog': (30, 30, 30),
    'safe': (200, 200, 200),
    'agent': (0, 128, 255),
    'trap': (255, 0, 0),
    'treasure': (255, 215, 0),
    'grid': (50, 50, 50),
    'panel_bg': (20, 20, 20),       # status panel background
    'text': (255, 255, 255),        # white text
    'win': (0, 255, 0),
    'lose': (255, 0, 0),
}
