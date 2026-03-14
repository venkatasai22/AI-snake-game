import random
from collections import deque

import numpy as np

from model import LinearQNet, QTrainer

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self, state_size=11, action_size=3):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=MAX_MEMORY)
        self.epsilon = 80
        self.gamma = 0.9
        self.model = LinearQNet(state_size, 128, action_size)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_action(self, state):
        self.epsilon = max(5, self.epsilon - 1)
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = np.array(state, dtype=float)
            prediction = self.model.predict(state0)
            move = int(np.argmax(prediction))
            final_move[move] = 1
        return final_move

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step([state], [action], [reward], [next_state], [done])
