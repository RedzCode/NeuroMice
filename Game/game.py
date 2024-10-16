import sys
import pygame
import random

# Initialize Pygame
pygame.init()
font = pygame.font.Font('freesansbold.ttf', 20)

# Constants
CELL_SIZE = 60  # Size of each grid cell
MOUSE_SIZE = 30  # Size of the mouse
GRID_WIDTH = 5  # Number of cells in width
GRID_HEIGHT = 4  # Number of cells in height
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)

# Maze layout (1 for walls, 0 for paths)
maze = [
    [2, 0, 0, 0, 2],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
    [1, 1, 0, 1, 1],
]


won = False
running = True

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("T-Maze")



def draw_maze():
    for row in range(GRID_HEIGHT):
        for col in range(GRID_WIDTH):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if maze[row][col] == 1:
                pygame.draw.rect(screen, BLACK, rect)  # Draw wall
            elif maze[row][col] == 0:
                pygame.draw.rect(screen, WHITE, rect)  # Draw path
            elif maze[row][col] == 2:
                pygame.draw.rect(screen, RED, rect)  # Draw escape
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Draw grid lines

# Player class
class Player:
    def __init__(self):
        self.x = 2
        self.y = 3
    def move(self, dx, dy, maze):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_x < GRID_WIDTH and 0 <= new_y < GRID_HEIGHT and maze[new_y][new_x] != 1:
            self.x = new_x
            self.y = new_y
    def draw(self, screen):
        pygame.draw.rect(screen, GRAY, (self.x * CELL_SIZE + ( CELL_SIZE / 4), self.y * CELL_SIZE + (CELL_SIZE / 4), MOUSE_SIZE, MOUSE_SIZE))

def Move():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player.move(0, -1, maze)
        elif event.key == pygame.K_DOWN:
            player.move(0, 1, maze)
        elif event.key == pygame.K_LEFT:
            player.move(-1, 0, maze)
        elif event.key == pygame.K_RIGHT:
            player.move(1, 0, maze)

def HasWon():
    if maze[player.y][player.x] == 2:
        won = True
        running = False

player = Player()
while running:
    for event in pygame.event.get():
        Move()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw the maze
    draw_maze()
 
    player.draw(screen)

    #HasWon()
    if maze[player.y][player.x] == 2:
        won = True
        running = False

    # Update the display
    pygame.display.flip()

