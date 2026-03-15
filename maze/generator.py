from maze.models import Maze  
import random


class MazeGenerator:
    def __init__(self, maze) -> None:
        self.maze = maze
        self.stack = []
    #algo DFS / Recursive Backtracker
    def generate(self):
        cell = self.maze.get_cell(0,0)
        

        cell.visited = True
        self.stack.append(cell)

        while (len(self.stack) != 0):
            last_cell = self.stack[-1]

            neighbors =self.maze.get_unvisited_neighbors(last_cell)

            if len(neighbors) != 0:
                random_cell = random.choice(neighbors)
                self.maze.remove_wall_between(last_cell,random_cell)
                self.stack.append(random_cell)
                random_cell.visited = True
            else :
                self.stack.pop()
    
    def place_42_pattern(self) -> None:

    
        pattern_42 = [
            (0, 0), (2, 0),
            (0, 1), (2, 1),
            (0, 2), (1, 2), (2, 2),
            (2, 3),
            (2, 4),

            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4),
        ]

        pattern_width = 6
        pattern_height = 4

        if self.maze.width <= pattern_width or self.maze.height <= pattern_height :
            print("42 pattern cannot be placed: maze is too small")
            return

        start_x = (self.maze.width - pattern_width) // 2
        start_y = (self.maze.height - pattern_height) // 2

        for px, py in pattern_42:
            real_x = start_x + px
            real_y = start_y + py

            if (real_x, real_y) == self.maze.entry or (real_x, real_y) == self.maze.exit:
                print("please not entre cell on pattren 42")
                exit()

            cell = self.maze.get_cell(real_x, real_y)
            cell.north = True
            cell.east = True
            cell.south = True
            cell.west = True
            cell.is_42 = True