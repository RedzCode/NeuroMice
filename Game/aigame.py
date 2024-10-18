import sys
import pygame
import random
from Game.utils import Direction

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
    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        self.x = new_x
        self.y = new_y

class MazeGame : 


    #TODO : change the param for maze and get the width and height
    def __init__(self, width, height):
        self.CELL_SIZE = 60
        self.MOUSE_SIZE = 30
        self.grid_width = width
        self.grid_height = height

        self.maze = [
            [2, 0, 0, 0, 2],
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
            [1, 1, 0, 1, 1],
        ]

        self.reset(width, height)

    def reset(self,width, height):
        self.grid_width = width
        self.grid_height = height
        #init display
        SCREEN_WIDTH = self.CELL_SIZE * self.grid_width
        SCREEN_HEIGHT = self.CELL_SIZE * self.grid_height
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("T-Maze")
        
        #init game state
        self.score = 0
        self.lives = 3
        self.turn = 0
        self.running = True
        self.player = Player()
        self.max_turn = 50
        self.end = False

    def get_turn(self):
        return self.turn

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
            if self.can_move(self.player.x, self.player.y, 0,-1) :
                self.player.move(0, -1)
        if action == Direction.LEFT:
            if self.can_move(self.player.x, self.player.y, 0,1) :
                self.player.move(0, 1)
        if action  == Direction.UP:
            if self.can_move(self.player.x, self.player.y, -1,0) :
                self.player.move(-1, 0)
        if action == Direction.DOWN:
            if self.can_move(self.player.x, self.player.y, 1,0) :
               self.player.move(1, 0)

    def can_move(self, x, y, dx, dy):
        new_x = x + dx
        new_y = y + dy
        if 0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height and self.maze[new_y][new_x] != 1:
            return True
        return False
    

    def draw_maze(self):
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                rect = pygame.Rect(col * self.CELL_SIZE, row *  self.CELL_SIZE,  self.CELL_SIZE,  self.CELL_SIZE)
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
        #self.player.draw(self.screen)
        pygame.draw.rect(self.screen, GRAY, (self.player.x * self.CELL_SIZE + ( self.CELL_SIZE / 4), self.player.y * self.CELL_SIZE  + (self.CELL_SIZE  / 4), self.MOUSE_SIZE, self.MOUSE_SIZE))

        #HasWon()
        if self.maze[self.player.y][self.player.x] == 2:
            # 1er tour, peu importe quel coté
            if(self.score == 0):
                if self.player.x == 0 :
                    self.turn = 0
                elif self.player.x == self.grid_width-1:
                    self.turn = 1

            # Si la souris est à droite pendant un tour pair
            # Ou si la souris est à gauche pendant un tour impaire
            # Augmentation du score
            if(self.turn%2 == 0 and self.player.x == 0) or (self.turn%2 == 1 and self.player.x == self.grid_width-1) :
                self.score += 1
                self.reward += 20
            else :
                self.lives -= 1
                self.reward += -10
            
            # Si la souris n'a plus de vie, fin de jeu
            if(self.lives == 0):
                self.running = False
                self.end = True
            else :
                self.turn += 1
                self.player = Player()

            self.display_states()

            if self.max_turn == self.turn:
                self.running = False
                self.end = True

        # Update the display
        pygame.display.flip()
        pygame.time.wait(50)
        return self.score, self.lives, self.reward, self.turn, self.running, self.end


       