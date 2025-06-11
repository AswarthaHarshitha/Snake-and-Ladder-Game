import numpy as np

class ValueIterationAgent:
    def __init__(self, env, gamma=0.9, theta=1e-6):
        self.env = env
        self.gamma = gamma  # discount factor
        self.theta = theta  # threshold for convergence
        self.values = np.zeros(env.board_size + 1)  # Value function
        self.policy = np.zeros(env.board_size + 1, dtype=int)  # Policy
        
        # Initialize values for terminal states
        self.values[env.board_size] = 1.0  # Win state
        for snake_start in env.snakes:
            self.values[snake_start] = -0.5  # Snake states
        for ladder_start in env.ladders:
            self.values[ladder_start] = 0.5  # Ladder states
        
        # Run value iteration
        self.value_iteration()
    
    def value_iteration(self):
        """Perform value iteration to find optimal policy"""
        while True:
            delta = 0
            # Iterate through all states
            for state in range(1, self.env.board_size):
                if state in self.env.snakes or state in self.env.ladders:
                    continue  # Skip states that lead to immediate transitions
                
                old_value = self.values[state]
                # Find best action for current state
                best_value = float('-inf')
                best_action = 1
                
                for action in range(1, 7):  # Possible dice rolls
                    # Calculate expected value for this action
                    next_state = min(state + action, self.env.board_size)
                    
                    # Handle snakes and ladders
                    if next_state in self.env.snakes:
                        next_state = self.env.snakes[next_state]
                    elif next_state in self.env.ladders:
                        next_state = self.env.ladders[next_state]
                    
                    # Calculate reward
                    if next_state == self.env.board_size:
                        reward = 1.0
                    elif next_state in self.env.snakes:
                        reward = -0.5
                    elif next_state in self.env.ladders:
                        reward = 0.5
                    else:
                        reward = 0.0
                    
                    # Calculate value
                    value = reward + self.gamma * self.values[next_state]
                    
                    if value > best_value:
                        best_value = value
                        best_action = action
                
                # Update value and policy
                self.values[state] = best_value
                self.policy[state] = best_action
                
                delta = max(delta, abs(old_value - self.values[state]))
            
            # Check for convergence
            if delta < self.theta:
                break
    
    def choose_action(self, state):
        """Choose action based on the learned policy"""
        return self.policy[state]
    
    def get_values(self):
        """Return the value function"""
        return self.values
    
    def get_policy(self):
        """Return the policy"""
        return self.policy 