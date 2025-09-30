# 🐍 Snake and Ladder Game with Value Iteration 🎲

## Description

This project simulates the classic Snake and Ladder game using the **Value Iteration** algorithm, a dynamic programming technique to find the optimal strategy for winning the game. It includes a graphical user interface (GUI) for visualization and interactive play, allowing users to watch the agent learn and play optimally or play manually.

## Features

- 🎯 **Value Iteration Agent**: Learns the optimal policy using dynamic programming.
- 🎮 **Game Simulation**: Runs multiple game simulations to analyze performance statistics.
- 📊 **Visualization**: Generates plots for value functions, optimal policies, and steps distribution.
- 🕹️ **Interactive GUI**: Pygame-based interface with dice rolling animation for manual play.
- 🤖 **Auto Play Mode**: Watch the agent play the game optimally.
- 📈 **Statistics Analysis**: Calculates minimum, maximum, average steps to win, and path diversity.

## Prerequisites

- Python 3.7 or higher

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd snake-and-ladder-game-idp
   ```

2. (Optional but recommended) Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the simulation and GUI:
```bash
python main.py
```

The program will:
1. Train the Value Iteration agent.
2. Simulate 1000 games and display statistics including min, max, average steps to win.
3. Generate plots:
   - `steps_distribution.png`: Histogram of steps to win.
   - `value_iteration_results.png`: Value function and optimal policy visualization.
4. Launch the GUI for interactive or auto play.

### GUI Controls

- **Start**: Begin auto-play mode where the agent plays optimally.
- **Roll**: Manual play mode; click to roll the dice.
- **Reset**: Reset the game to the initial state.

## How It Works

The project uses the Value Iteration algorithm to solve the Snake and Ladder game:

1. **Environment** (`environment.py`): Defines the board layout with snakes and ladders.
2. **Agent** (`value_iteration_agent.py`): Learns the optimal policy using dynamic programming.
3. **Value Iteration**: Iteratively computes the value of each state until convergence.
4. **Policy**: Determines the best dice roll for each position on the board.
5. **Visualization** (`visualization.py`): Handles the Pygame GUI and animations.

## Dependencies

- `numpy`: Numerical computations
- `matplotlib`: Plotting and visualization
- `pygame`: GUI and game rendering
- `tqdm`: Progress bars (optional)

## Project Structure

- `main.py`: Main entry point and GUI loop
- `environment.py`: Game environment definition
- `value_iteration_agent.py`: Value Iteration agent implementation
- `visualization.py`: Pygame GUI components and animations
- `requirements.txt`: Python dependencies

## Screenshots
- `steps_distribution`
- <img width="1000" height="600" alt="steps_distribution" src="https://github.com/user-attachments/assets/ca9b1193-79ca-4531-951e-7e4459a8a95f" />
    Histogram of steps to win across simulations.
- `value_iteration_results'
- <img width="1200" height="800" alt="value_iteration_results" src="https://github.com/user-attachments/assets/a90d2dc2-9ef5-443c-a41a-a82919cde96c" />
     Value function and optimal policy visualization.
- `learning_curve'
- <img width="1000" height="600" alt="learning_curve" src="https://github.com/user-attachments/assets/8f07a417-8bc5-45d0-ad4d-4ef716e25c24" />
     Learning progress over iterations.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements or bug fixes.
