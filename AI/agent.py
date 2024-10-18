from collections import deque #Deque (Doubly Ended Queue)
import torch
import random
import numpy as np
from AI.helper import plot
from AI.model import Linear_QNet, QTrainer
from Game.aigame import MazeGame
from Game.utils import Direction

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 #Learning rate

class Agent():

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0 # control randomness
        self.gamma = 0 # discount rate
        #if we exceed the memory it will automatically remove element from the left => popleft()
        self.memory = deque(maxlen=MAX_MEMORY) 
        # 4 inputs, 256 hidden neurons, 4 outputs neurons
        self.model = Linear_QNet(1, 256, 4)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        state = []
        state.append(game.get_turn())
        
        return np.array(state, dtype=float)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        # More games lead to less random moves cause epsilon is getting smaller
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

    def decode_action(self, move):
        if move[0] == 1: return Direction.RIGHT
        if move[1] == 1: return Direction.LEFT
        if move[2] == 1: return Direction.UP
        if move[3] == 1: return Direction.DOWN
        
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0 #current best score  = 0
    agent = Agent()
    game = MazeGame(5,4)
    total_reward = 0
    
    while True: 
        
        state_old = agent.get_state(game)
        
        # get move
        final_move = agent.get_action(state_old)
        
        # perform move and get new state
        final_direction = agent.decode_action(final_move)
        score, lives, reward, turn, running, end = game.play_action(final_direction)
        
        state_new = agent.get_state(game)
        
        # train short memory 
        agent.train_short_memory(state_old, final_move, reward, state_new, running)
        
        # remember
        agent.remember(state_old, final_move, reward, state_new, running)
        
        total_reward += reward
        if end: 
            # train long memory
            game.reset(5,4)
            agent.n_games += 1
            agent.train_long_memory()

            record = score
            agent.model.save()
            print("=============")
            print('Game:', agent.n_games, '|Score: ', score, '|Lives: ',lives, '|Record: ', record, ' |Reward:', total_reward)
            total_reward = 0
            
            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)