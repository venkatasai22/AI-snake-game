import random


def place_food(grid_size, snake_body):
    choices = [(x, y) for x in range(grid_size) for y in range(grid_size) if (x, y) not in snake_body]
    if not choices:
        return None
    return random.choice(choices)
