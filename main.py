import numpy as np
import matplotlib.pyplot as plt
import pygame
from environment import SnakeAndLadderEnv
from value_iteration_agent import ValueIterationAgent
from visualization import SnakeAndLadderVisualizer
import time
import random

def simulate_games(env, agent, num_games=100):
    """Simulate multiple games to find min/max steps with path tracking"""
    steps_list = []
    paths = []  # Store the paths taken
    
    for _ in range(num_games):
        state = env.reset()
        steps = 0
        done = False
        path = [state]  # Track the path taken
        
        while not done:
            # Add some randomness to the policy
            if random.random() < 0.1:  # 10% chance of random action
                action = random.randint(1, 6)
            else:
                action = agent.choose_action(state)
            
            next_state, _, done, _ = env.step(action)
            path.append(next_state)
            state = next_state
            steps += 1
        
        steps_list.append(steps)
        paths.append(path)
    
    # Find unique paths
    unique_paths = []
    for path in paths:
        if path not in unique_paths:
            unique_paths.append(path)
    
    # Print path statistics
    print("\nPath Statistics:")
    print(f"Total unique paths found: {len(unique_paths)}")
    if len(unique_paths) > 0:
        print("\nExample paths:")
        for i, path in enumerate(unique_paths[:3]):  # Show first 3 unique paths
            print(f"Path {i+1}: {' -> '.join(map(str, path))}")
            print(f"Steps: {len(path)-1}\n")
    
    return steps_list

def visualize_values(agent, env):
    """Visualize the learned value function"""
    values = agent.get_values()
    policy = agent.get_policy()
    
    # Create a heatmap of the value function
    plt.figure(figsize=(12, 8))
    
    # Plot value function
    plt.subplot(2, 1, 1)
    plt.plot(range(1, env.board_size + 1), values[1:])
    plt.title('Value Function')
    plt.xlabel('Position')
    plt.ylabel('Value')
    
    # Plot policy
    plt.subplot(2, 1, 2)
    plt.bar(range(1, env.board_size + 1), policy[1:])
    plt.title('Optimal Policy')
    plt.xlabel('Position')
    plt.ylabel('Dice Roll')
    
    plt.tight_layout()
    plt.savefig('value_iteration_results.png')
    plt.close()

def animate_movement(visualizer, start_pos, end_pos, snakes, ladders, steps, dice, game_state):
    """Animate smooth movement between positions"""
    start_x, start_y = visualizer.get_cell_center(start_pos)
    end_x, end_y = visualizer.get_cell_center(end_pos)
    
    frames = 20
    for i in range(frames + 1):
        t = i / frames
        current_x = start_x + (end_x - start_x) * t
        current_y = start_y + (end_y - start_y) * t
        
        # Draw board with current position
        visualizer.draw_board(
            start_pos if i < frames else end_pos,
            snakes,
            ladders,
            steps,
            dice,
            game_state
        )
        
        # Draw moving player
        pygame.draw.circle(visualizer.screen, (100, 100, 100),
                         (int(current_x) + 2, int(current_y) + 2),
                         visualizer.cell_size/4)
        pygame.draw.circle(visualizer.screen, visualizer.PLAYER_COLOR,
                         (int(current_x), int(current_y)),
                         visualizer.cell_size/4)
        
        pygame.display.flip()
        time.sleep(0.05)

def animate_dice_roll(visualizer, state, snakes, ladders, steps, game_state):
    """Animate the dice rolling"""
    # Show multiple random dice faces with increasing delay
    delays = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
    for delay in delays:
        current_dice = random.randint(1, 6)
        visualizer.draw_board(state, snakes, ladders, steps, current_dice, game_state)
        time.sleep(delay)
    return current_dice

def play_game(env, agent, visualizer, roll_mode=False):
    """Play a single game with visualization"""
    state = env.reset()
    done = False
    steps = 0
    game_state = "roll" if roll_mode else "auto"
    current_dice = 0
    
    while not done:
        # Draw current state
        visualizer.draw_board(state, env.snakes, env.ladders, steps, current_dice, game_state)
        
        # Get action
        if roll_mode:
            # Wait for roll button click
            action = None
            while action is None:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        return "quit", steps
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        button = visualizer.check_button_click(event.pos)
                        if button == "roll":
                            # Animate dice roll
                            current_dice = animate_dice_roll(visualizer, state, env.snakes, env.ladders, steps, game_state)
                            action = current_dice
                            time.sleep(0.5)  # Pause to show final dice roll
                        elif button == "reset":
                            return "reset", steps
        else:
            # Get action from agent
            action = agent.choose_action(state)
            current_dice = action
        
        # Take step
        next_state, reward, done, info = env.step(action)
        
        # Animate movement
        animate_movement(visualizer, state, next_state, env.snakes, env.ladders, steps, current_dice, game_state)
        
        # Update state
        state = next_state
        steps += 1
        
        # Check for quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", steps
    
    # Show final position for a moment
    time.sleep(1.0)
    return "done", steps

def main():
    # Initialize environment and agent
    env = SnakeAndLadderEnv()
    agent = ValueIterationAgent(env)
    visualizer = SnakeAndLadderVisualizer()
    
    # Simulate games to find min/max steps
    print("Simulating games to find optimal path statistics...")
    steps_list = simulate_games(env, agent, num_games=1000)
    
    # Calculate statistics
    min_steps = min(steps_list)
    max_steps = max(steps_list)
    avg_steps = np.mean(steps_list)
    std_steps = np.std(steps_list)
    
    print("\nGame Statistics:")
    print(f"Minimum steps to win: {min_steps}")
    print(f"Maximum steps to win: {max_steps}")
    print(f"Average steps to win: {avg_steps:.2f}")
    print(f"Standard deviation: {std_steps:.2f}")
    
    # Plot steps distribution
    plt.figure(figsize=(10, 6))
    plt.hist(steps_list, bins=20, edgecolor='black')
    plt.title('Distribution of Steps to Win')
    plt.xlabel('Number of Steps')
    plt.ylabel('Frequency')
    plt.savefig('steps_distribution.png')
    plt.close()
    
    # Visualize the learned value function and policy
    print("\nVisualizing value function and policy...")
    visualize_values(agent, env)
    
    # Main game loop
    running = True
    game_state = "idle"
    current_steps = 0
    
    while running:
        # Draw initial state
        visualizer.draw_board(1, env.snakes, env.ladders, current_steps, 0, game_state)
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                button = visualizer.check_button_click(event.pos)
                if button == "start":
                    game_state = "auto"
                    result, steps = play_game(env, agent, visualizer)
                    current_steps = steps
                    if result == "reset":
                        env.reset()
                        game_state = "idle"
                    elif result == "quit":
                        running = False
                elif button == "reset":
                    env.reset()
                    game_state = "idle"
                    current_steps = 0
                elif button == "roll":
                    game_state = "roll"
                    result, steps = play_game(env, agent, visualizer, roll_mode=True)
                    current_steps = steps
                    if result == "reset":
                        env.reset()
                        game_state = "idle"
                    elif result == "quit":
                        running = False
        
        # Reset button pressed state if mouse button is released
        if event.type == pygame.MOUSEBUTTONUP:
            visualizer.button_pressed = None
    
    # Close visualization
    visualizer.close()

if __name__ == "__main__":
    main() 