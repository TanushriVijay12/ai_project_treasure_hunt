WINDOW_PADDING = 50
GRID_SIZE = 5
STATUS_PANEL_WIDTH = 300
MAX_WINDOW_HEIGHT = 800
MAX_WINDOW_WIDTH = 1000

def get_tile_size(grid_size):
    return min((MAX_WINDOW_HEIGHT // grid_size), 60)  # upper limit to prevent overly large tiles

def get_screen_dimensions(grid_size):
    tile_size = get_tile_size(grid_size)
    width = grid_size * tile_size + STATUS_PANEL_WIDTH
    height = grid_size * tile_size
    return width, height, tile_size


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
