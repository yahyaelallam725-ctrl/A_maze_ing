from maze.config_parser import MazeConfig
from maze.models import Maze
from maze.generator import MazeGenerator


def render_ascii(maze, path) -> None:
    top_line = "+"
    path_coords = set((cell.x, cell.y) for cell in path)
    for _ in range(maze.width):
        top_line += "---+"
    print(top_line)
    for y in range(maze.height):
        middle_line = ""
        bottom_line = "+"
        for x in range(maze.width):
            cell = maze.get_cell(x, y)

            if cell.west:
                middle_line += "|"
            else:
                middle_line += " "
            if (x, y) == maze.entry:
                middle_line += " E "
            elif (x, y) == maze.exit:
                middle_line += " X "
            elif (x, y) in path_coords:
                middle_line += " * "
            elif getattr(cell, "is_42", False):
                middle_line += " # "
            else:
                middle_line += "   "
            if cell.south:
                bottom_line += "---+"
            else:
                bottom_line += "   +"
        last_cell = maze.get_cell(maze.width - 1, y)
        if last_cell.east:
            middle_line += "|"
        else:
            middle_line += " "
        print(middle_line)
        print(bottom_line)

# conf = MazeConfig("config_default.txt")
# conf.load()

# maze = Maze(conf.width, conf.height, conf.entry, conf.exit)
# maze.create_grid()

# gene = MazeGenerator(maze)
# gene.generate()

# render_ascii(maze)


