import sys
import pygame
import random
from utils import Direction

pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)

class Player:
    def __init__(self):
        self.x = 2
        self.y = 3
    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < maze.GRID_WIDTH and 0 <= new_y < maze.GRID_HEIGHT  and maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y
    def draw(self, screen,maze):
        pygame.draw.rect(screen, GRAY, (self.x * maze.CELL_SIZE + ( maze.CELL_SIZE / 4), self.y * maze.CELL_SIZE  + (maze.CELL_SIZE  / 4), maze.MOUSE_SIZE, maze.MOUSE_SIZE))


class MazeGame : 


    #TODO : change the param for maze and get the width and height
    def __init__(self, width, height):
        self.CELLSIZE = 60
        self.GRID_WIDTH = width
        self.GRID_HEIGHT = height

        self.maze = [
            [2, 0, 0, 0, 2],
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
        ]

        self.reset()

    def reset(self):

        #init display
        self.screen = pygame.display.set_mode([self.GRID_WIDTH, self.GRID_HEIGHT])
        pygame.display.set_caption("T-Maze")
        
        #init game state
        self.score = 0
        self.lives = 3
        self.turn = 0
        self.running = True
        self.game_over = False
        self.player = Player()
        self.max_turn = 50

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.player.move(0, -1, self)
                elif event.key == pygame.K_DOWN:
                    self.player.player.move(0, 1, self)
                elif event.key == pygame.K_LEFT:
                    self.player.player.move(-1, 0, self)
                elif event.key == pygame.K_RIGHT:
                    self.player.player.move(1, 0, self)

    def set_direction(self, action):
        if action == Direction.RIGHT:
            self.player.move(0, -1, self)
        if action == Direction.LEFT:
            self.player.move(0, 1, self)
        if action  == Direction.UP:
            self.player.move(-1, 0, self)
        if action == Direction.DOWN:
            self.player.move(1, 0, self)

    def draw_maze(self):
        for row in range(self.GRID_HEIGHT):
            for col in range(self.GRID_WIDTH):
                rect = pygame.Rect(col * self.CELL_SIZE, row * self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE)
                if self.maze[row][col] == 1:
                    pygame.draw.rect(self.screen, BLACK, rect)  # Draw wall
                elif self.maze[row][col] == 0:
                    pygame.draw.rect(self.screen, WHITE, rect)  # Draw path
                elif self.maze[row][col] == 2:
                    pygame.draw.rect(self.screen, RED, rect)  # Draw escape
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)  # Draw grid lines

    def display_states(self):
        print("===========")
        print("vous avez ",self.lives, " vies")
        print("votre score est de ",self.score)
        print("new turn ",self.turn)

    def play_action(self, action):
        self.reward = 0
        
        self.input()
        self.set_direction(action)

        # Fill the screen with white
        self.screen.fill(WHITE)

        # Draw the maze and the player
        self.draw_maze()
        self.player.draw(self.screen)

        #HasWon()
        if self.maze[self.player.y][self.player.x] == 2:
            # 1er tour, peu importe quel coté
            if(self.score == 0):
                if self.player.x == 0 :
                    turn = 0
                elif self.player.x == self.GRID_WIDTH-1:
                    turn = 1

            # Si la souris est à droite pendant un tour pair
            # Ou si la souris est à gauche pendant un tour impaire
            # Augmentation du score
            if(turn%2 == 0 and self.player.x == 0) or (turn%2 == 1 and self.player.x == self.GRID_WIDTH-1) :
                self.score += 1
                self.reward += 20
            else :
                self.lives -= 1
                self.reward += -10
            
            # Si la souris n'a plus de vie, fin de jeu
            if(self.lives == 0):
                self.running = False
                self.game_over = True
            else :
                turn += 1
                self.player = Player()

            self.display_states()

        # Update the display
        pygame.display.flip()
        return self.score, self.game_over, self.lives, self.reward, self.turn


       