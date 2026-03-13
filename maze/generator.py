from maze.models import Maze  

class MazeGenerator:
    def __init__(self) -> None:
        self.maze = None
        self.stack = []

    def generate(self):
        cell = self.maze.get_cell(0,0)
        cell.visitide = True
        self.stack.append(cell)



        while (self.stack is not None):
            last_cell = self.stack[-1]

            neighbors =self.maze.get_unvisited_neighbors(last_cell)


            for neigh in neighbors:
                self.remove_wall_between(last_cell,neigh) 


