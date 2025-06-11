import numpy as np
import random

class QLearningAgent:
    def __init__(self, env, learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.env = env
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        
        # Initialize Q-table
        self.q_table = np.zeros((env.board_size + 1, 6))  # 6 possible actions (dice rolls 1-6)
    
    def choose_action(self, state):
        """Choose an action using epsilon-greedy policy"""
        if random.random() < self.exploration_rate:
            # Exploration: choose random action
            return random.choice(self.env.get_valid_actions())
        else:
            # Exploitation: choose best action from Q-table
            return np.argmax(self.q_table[state]) + 1
    
    def update_q_table(self, state, action, reward, next_state):
        """Update Q-table using Q-learning update rule"""
        current_q = self.q_table[state, action - 1]
        next_max_q = np.max(self.q_table[next_state])
        
        # Q-learning update rule
        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * next_max_q - current_q
        )
        self.q_table[state, action - 1] = new_q
    
    def train(self, num_episodes=1000):
        """Train the agent for specified number of episodes"""
        steps_per_episode = []
        
        for episode in range(num_episodes):
            state = self.env.reset()
            done = False
            steps = 0
            
            while not done:
                action = self.choose_action(state)
                next_state, reward, done, _ = self.env.step(action)
                
                self.update_q_table(state, action, reward, next_state)
                state = next_state
                steps += 1
            
            steps_per_episode.append(steps)
            
            # Decay exploration rate
            self.exploration_rate = max(0.01, self.exploration_rate * 0.995)
        
        return steps_per_episode
    
    def get_policy(self):
        """Get the learned policy"""
        return np.argmax(self.q_table, axis=1) + 1 