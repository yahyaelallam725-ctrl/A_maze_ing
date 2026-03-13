from maze.config_parser import MazeConfig
from maze.models import Maze 


conf = MazeConfig("config_default.txt")
conf.load()

maze = Maze(conf.width, conf.height, conf.entry, conf.exit)

maze.create_grid()


print("*****")

print(maze.get_cell(0,2))


