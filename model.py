import numpy as np
try:
    import torch
    import torch.nn as nn
    import torch.optim as optim
except Exception:
    torch = None

class LinearQNet:
    def __init__(self, input_size, hidden_size, output_size):
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.output_size = output_size
        if torch:
            self.model = nn.Sequential(
                nn.Linear(input_size, hidden_size),
                nn.ReLU(),
                nn.Linear(hidden_size, output_size)
            )
        else:
            self.model = None

    def predict(self, state):
        if torch:
            with torch.no_grad():
                x = torch.tensor(state, dtype=torch.float)
                return self.model(x).numpy()
        return np.zeros(self.output_size)

    def save(self, file_name='model.pth'):
        if torch:
            torch.save(self.model.state_dict(), file_name)

    def load(self, file_name='model.pth'):
        if torch:
            self.model.load_state_dict(torch.load(file_name))

class QTrainer:
    def __init__(self, model, lr=0.001, gamma=0.9):
        self.model = model
        self.gamma = gamma
        if torch:
            self.optimizer = optim.Adam(self.model.model.parameters(), lr=lr)
            self.criterion = nn.MSELoss()

    def train_step(self, states, actions, rewards, next_states, dones):
        if not torch:
            return
        states = torch.tensor(np.array(states), dtype=torch.float)
        actions = torch.tensor(np.array(actions), dtype=torch.long)
        rewards = torch.tensor(np.array(rewards), dtype=torch.float)
        next_states = torch.tensor(np.array(next_states), dtype=torch.float)

        pred = self.model.model(states)
        target = pred.clone()

        with torch.no_grad():
            next_pred = self.model.model(next_states)

        for idx in range(len(states)):
            q_new = rewards[idx]
            if not dones[idx]:
                q_new = rewards[idx] + self.gamma * torch.max(next_pred[idx])
            action_index = torch.argmax(actions[idx]).item()
            target[idx][action_index] = q_new

        self.optimizer.zero_grad()
        loss = self.criterion(pred, target)
        loss.backward()
        self.optimizer.step()
