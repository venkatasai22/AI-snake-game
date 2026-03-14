import numpy as np

# screen settings
grid_size = 20
block_size = 20
screen_width = grid_size * block_size
screen_height = grid_size * block_size

# directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 255)

# rewards
REWARD_FOOD = 10
REWARD_COLLISION = -10
REWARD_STEP = -0.1

np.random.seed(42)
