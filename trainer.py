import numpy as np
from game import SnakeGame
from agent import Agent


def train(episodes=2000, max_steps=1000):
    agent = Agent()
    game = SnakeGame(human_mode=False)

    best_score = 0
    mean_score = 0

    for episode in range(1, episodes + 1):
        game.reset()
        state_old = game._get_state()
        total_reward = 0

        while True:
            action = agent.get_action(state_old)
            reward, done, score = game.play_step(action)
            state_new = game._get_state()

            agent.train_short_memory(state_old, action, reward, state_new, done)
            agent.remember(state_old, action, reward, state_new, done)

            state_old = state_new
            total_reward += reward

            if done:
                agent.train_long_memory()
                if score > best_score:
                    best_score = score
                    agent.model.save('best_model.pth')
                mean_score = (mean_score * (episode - 1) + score) / episode
                print(f"Episode {episode}/{episodes} - Score: {score} - Best: {best_score} - Mean: {mean_score:.2f}")
                break

    print("Training complete")


def play_human():
    game = SnakeGame(human_mode=True)
    running = True
    while running:
        if game.human_move() is None:
            running = False
            break
        reward, done, score = game.play_step([1, 0, 0])
        if done:
            print(f"Game over! Score: {score}")
            game.reset()
        game.draw()
        game.clock.tick(10)

    game.close()
