import pygame
import numpy as np
from utils import grid_size, block_size, screen_width, screen_height, RED, GREEN, BLACK, WHITE, REWARD_FOOD, REWARD_COLLISION, REWARD_STEP, UP, DOWN, LEFT, RIGHT
from snake import Snake
from food import place_food


def _is_collision(head, grid_size, snake_body):
    x, y = head
    if x < 0 or x >= grid_size or y < 0 or y >= grid_size:
        return True
    # collision with body
    return head in list(snake_body)[1:]


def _direction_to_vector(direction):
    if direction == 0:
        return LEFT
    if direction == 1:
        return RIGHT
    if direction == 2:
        return UP
    return DOWN

class SnakeGame:
    def __init__(self, human_mode=True):
        self.human_mode = human_mode
        if self.human_mode:
            pygame.init()
            self.screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("AI Snake Game")
            self.clock = pygame.time.Clock()
            self.font = pygame.font.SysFont("arial", 18)
        else:
            # Training mode doesn't need rendering or event handling
            self.screen = None
            self.clock = None
            self.font = None
        self.reset()

    def reset(self):
        start_x = grid_size // 2
        start_y = grid_size // 2
        self.snake = Snake(start_x, start_y)
        self.food = place_food(grid_size, self.snake.body)
        self.score = 0
        self.game_over = False
        self.frame_iteration = 0
        self.direction = RIGHT

    def _get_state(self):
        head = self.snake.head
        x, y = head
        point_l = (x - 1, y)
        point_r = (x + 1, y)
        point_u = (x, y - 1)
        point_d = (x, y + 1)

        dir_l = self.snake.direction == LEFT
        dir_r = self.snake.direction == RIGHT
        dir_u = self.snake.direction == UP
        dir_d = self.snake.direction == DOWN

        danger_straight = _is_collision((x + self.snake.direction[0], y + self.snake.direction[1]), grid_size, self.snake.body)
        left_turn = (-self.snake.direction[1], self.snake.direction[0])
        right_turn = (self.snake.direction[1], -self.snake.direction[0])
        danger_left = _is_collision((x + left_turn[0], y + left_turn[1]), grid_size, self.snake.body)
        danger_right = _is_collision((x + right_turn[0], y + right_turn[1]), grid_size, self.snake.body)

        food_left = self.food[0] < x
        food_right = self.food[0] > x
        food_up = self.food[1] < y
        food_down = self.food[1] > y

        state = [
            danger_straight,
            danger_left,
            danger_right,
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            food_left,
            food_right,
            food_up,
            food_down,
        ]
        return np.array(state, dtype=int)

    def play_step(self, action):
        self.frame_iteration += 1

        # action is [straight, right, left]
        clock_wise = [RIGHT, DOWN, LEFT, UP]
        idx = clock_wise.index(self.snake.direction)

        if np.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0, 1, 0]):
            new_dir = clock_wise[(idx + 1) % 4]
        else:
            new_dir = clock_wise[(idx - 1) % 4]
        self.snake.set_direction(new_dir)

        self.snake.move()

        reward = 0
        if _is_collision(self.snake.head, grid_size, self.snake.body):
            self.game_over = True
            reward = REWARD_COLLISION
            return reward, self.game_over, self.score

        if self.snake.head == self.food:
            self.score += 1
            reward = REWARD_FOOD
            self.snake.grow()
            self.food = place_food(grid_size, self.snake.body)

        reward += REWARD_STEP

        if self.frame_iteration > 100 * len(self.snake.body):
            self.game_over = True
            reward = REWARD_COLLISION

        return reward, self.game_over, self.score

    def human_move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.snake.set_direction(LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.snake.set_direction(RIGHT)
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    self.snake.set_direction(UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    self.snake.set_direction(DOWN)
        return True

    def draw(self):
        if not self.human_mode or self.screen is None:
            return
        self.screen.fill(BLACK)
        for pt in self.snake.body:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(pt[0] * block_size, pt[1] * block_size, block_size, block_size))
        pygame.draw.rect(self.screen, RED, pygame.Rect(self.food[0] * block_size, self.food[1] * block_size, block_size, block_size))
        text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(text, (10, 10))
        pygame.display.flip()

    def close(self):
        if self.human_mode:
            pygame.quit()
