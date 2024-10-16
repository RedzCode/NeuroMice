from collections import deque #Deque (Doubly Ended Queue)
import torch
import random
import numpy as np
from AI.helper import plot, plot_vic
from AI.model import Linear_QNet, QTrainer
from Game.aigame import PacmanGame, Pos
from Game.utils import Direction

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001 #Learning rate

class Agent():

    def get_action(self, state):
              print("decode")

    def decode_action(self, move):
        print("decode")
        
def train():
    print("train")