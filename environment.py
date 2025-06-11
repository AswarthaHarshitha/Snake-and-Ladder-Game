import numpy as np

class SnakeAndLadderEnv:
    def __init__(self, board_size=100):
        self.board_size = board_size
        self.current_position = 1
        
        # Define snakes (start: end)
        self.snakes = {
            16: 6,
            47: 26,
            49: 11,
            56: 53,
            62: 19,
            64: 60,
            87: 24,
            93: 73,
            95: 75,
            98: 78
        }
        
        # Define ladders (start: end)
        self.ladders = {
            4: 14,
            9: 31,
            21: 42,
            28: 84,
            36: 44,
            51: 67,
            71: 91,
            80: 100
        }
    
    def reset(self):
        """Reset the environment to initial state"""
        self.current_position = 1
        return self.current_position
    
    def step(self, action):
        """Take a step in the environment"""
        # Move the player
        new_position = self.current_position + action
        
        # Check if the new position is beyond the board
        if new_position > self.board_size:
            new_position = self.board_size - (new_position - self.board_size)
        
        # Check for snakes and ladders
        if new_position in self.snakes:
            new_position = self.snakes[new_position]
            reward = -0.5  # Negative reward for landing on a snake
        elif new_position in self.ladders:
            new_position = self.ladders[new_position]
            reward = 0.5  # Positive reward for landing on a ladder
        else:
            reward = 0.0  # Neutral reward for normal move
        
        # Check if the game is over
        done = new_position == self.board_size
        if done:
            reward = 1.0  # Positive reward for winning
        
        # Update current position
        self.current_position = new_position
        
        return new_position, reward, done, {}
    
    def get_valid_actions(self):
        """Get valid actions (dice rolls) from current state"""
        return list(range(1, 7))
    
    def get_state(self):
        """Get current state"""
        return self.current_position 