# AI Snake Game

The AI Snake Game is a classic grid-based snake simulation where an RL agent learns to play autonomously while also supporting human play with keyboard controls.

## 1. Project Overview

This project includes two modes:

- **Human Play Mode** — user controls the snake with arrow keys or WASD.
- **Training Mode** — an AI agent learns to collect food and avoid collisions with reinforcement learning.

Objective: demonstrate modular game design, environment-agent RL interaction, and simulation-based training.

## 2. Core Technologies

- Python
- Pygame
- NumPy
- PyTorch (optional, used in `model.py`)

## 3. Game Mechanics

The game uses a 2D grid. Each step updates the snake and food state.

- Snake moves in four directions (up/down/left/right)
- Eating food grows the snake and increases score
- Game ends on wall or self collision

### Collision detection

```
if head in snake_body[1:]:
    game_over = True
```

## 4. Game Loop Architecture

Main loop:
1. Process input (keyboard or AI action)
2. Update near-end state (move snake)
3. Check collisions
4. Render output (human mode)

## 5. Reinforcement Learning Integration

### State representation

State includes danger straight/left/right, direction, and food relative location.

### Action space

The agent selects one of three actions:
- `[1,0,0]` straight
- `[0,1,0]` right
- `[0,0,1]` left

### Reward system

- +10 for eating food
- -10 for collisions
- -0.1 per step to encourage shorter solutions

## 6. Training Process

1. Initialize agent and game
2. For each episode:
   - Reset environment
   - While not done:
     - Choose action
     - Execute action
     - Observe reward and next state
     - Store experience
     - Train model
3. Track best score and mean score

## 7. Neural Network Model (Optional)

A small feed-forward network can map state to action values.

## 8. Experience Replay

Training uses memory to sample experiences for stable learning.

## 9. Visualization and Evaluation

The project tracks and prints:
- episode number
- score
- best score
- mean score

## 10. Project Architecture

```
ai-snake-game/
  main.py
  game.py
  snake.py
  food.py
  agent.py
  model.py
  trainer.py
  utils.py
```

Responsibilities:
- `game.py` — environment and step logic
- `snake.py` — snake body behavior
- `agent.py` — action selection and memory
- `model.py` — neural network and trainer
- `trainer.py` — training loop

## 11. Key Learning Outcomes

- Real-time game loop
- Collision detection and grid movement
- RL concepts: state/action/reward
- Modular software architecture

## 12. Run Instructions

Install requirements:

```bash
python -m pip install pygame numpy torch
```

Run human mode:

```bash
python main.py --mode human
```

Run training mode:

```bash
python main.py --mode train --episodes 500
```

## 13. Future Improvements

- Evolutionary algorithms
- Multiple AI agents
- Procedural environments
- Leaderboards and web deployment
>>>>>>> 044507b (Add AI Snake Game project)
