# Snake and Ladder Game with AI

## Description

This project implements a Snake and Ladder game simulation using reinforcement learning techniques. It features a Value Iteration agent that learns the optimal policy for playing the game, along with a graphical user interface for visualization and interactive play.

## Features

- **Reinforcement Learning Agent**: Uses Value Iteration to learn the optimal strategy for Snake and Ladder.
- **Game Simulation**: Simulates multiple games to analyze performance statistics.
- **Visualization**: Plots value function, policy, and steps distribution.
- **Interactive GUI**: Pygame-based interface for manual play with dice rolling animation.
- **Auto Play Mode**: Watch the AI agent play optimally.
- **Statistics Analysis**: Calculates min, max, average steps to win, and path diversity.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd snake-and-ladder-game-idp
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script:
```bash
python main.py
```

The program will:
1. Train the Value Iteration agent.
2. Simulate 1000 games and display statistics.
3. Generate plots (steps_distribution.png, value_iteration_results.png).
4. Launch the GUI for interactive play.

### GUI Controls
- **Start**: Begin auto-play mode with the AI agent.
- **Roll**: Manual play mode - click to roll dice.
- **Reset**: Reset the game to initial state.

## Screenshots

- `steps_distribution.png`: Histogram of steps to win across simulations.
- `value_iteration_results.png`: Value function and optimal policy visualization.
- `learning_curve.png`: (If available) Learning progress over iterations.

## How It Works

The project uses reinforcement learning to solve the Snake and Ladder game:

1. **Environment**: Defined in `environment.py`, includes board layout with snakes and ladders.
2. **Agent**: `ValueIterationAgent` learns the optimal policy using dynamic programming.
3. **Value Iteration**: Iteratively computes the value of each state until convergence.
4. **Policy**: Determines the best dice roll for each position on the board.

## Dependencies

- numpy: Numerical computations
- matplotlib: Plotting and visualization
- pygame: GUI and game rendering
- tqdm: Progress bars (if used)

## Project Structure

- `main.py`: Main entry point and GUI loop
- `environment.py`: Game environment definition
- `value_iteration_agent.py`: Reinforcement learning agent
- `visualization.py`: Pygame GUI components
- `requirements.txt`: Python dependencies
