import random
from typing import List, Tuple, Any
from maze.models import Maze


class MazeGenerator:

    def __init__(self, maze: Maze) -> None:
        self.maze: Maze = maze
        self.stack: List[Any] = []

    # DFS / Recursive Backtracker

    def generate(self) -> None:
        cell = self.maze.get_cell(0, 0)

        cell.visited = True
        self.stack.append(cell)

        while len(self.stack) != 0:
            last_cell = self.stack[-1]

            neighbors = self.maze.get_unvisited_neighbors(last_cell)

            if len(neighbors) != 0:
                random_cell = random.choice(neighbors)
                self.maze.remove_wall_between(last_cell, random_cell)
                self.stack.append(random_cell)
                random_cell.visited = True
            else:
                self.stack.pop()


    def make_imperfect(self, extra_walls_to_remove: int = 5) -> None:

        removed = 0
        while removed < extra_walls_to_remove:
  
            x = random.randint(1, self.maze.width - 2)
            y = random.randint(1, self.maze.height - 2)
            cell = self.maze.get_cell(x, y)
            
            wall = random.choice(['north', 'east', 'south', 'west'])
        
            neighbor = None
            if wall == 'north': neighbor = self.maze.get_cell(x, y - 1)
            elif wall == 'south': neighbor = self.maze.get_cell(x, y + 1)
            elif wall == 'east': neighbor = self.maze.get_cell(x + 1, y)
            elif wall == 'west': neighbor = self.maze.get_cell(x - 1, y)

            if neighbor and not cell.is_42 and not neighbor.is_42:
                self.maze.remove_wall_between(cell, neighbor)
                removed += 1

    def place_42_pattern(self) -> None:
        pattern_42: List[Tuple[int, int]] = [
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

        pattern_width: int = 7
        pattern_height: int = 5

        if self.maze.width < pattern_width or self.maze.height < pattern_height:
            print("42 pattern cannot be placed: maze is too small")
            return

        start_x: int = (self.maze.width - pattern_width) // 2
        start_y: int = (self.maze.height - pattern_height) // 2

        for px, py in pattern_42:
            real_x: int = start_x + px
            real_y: int = start_y + py

            current_pos: Tuple[int, int] = (real_x, real_y)
            if current_pos == self.maze.entry or current_pos == self.maze.exit:
                print("Error: 42 pattern overlaps with entry or exit points.")
                exit()

            cell = self.maze.get_cell(real_x, real_y)
            cell.north = True
            cell.east = True
            cell.south = True
            cell.west = True
            cell.is_42 = True