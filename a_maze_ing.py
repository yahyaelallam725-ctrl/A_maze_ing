from maze.config_parser import MazeConfig
from maze.models import Maze
from maze.generator import MazeGenerator
from maze.renderer import render_ascii
from maze.solver import bfs_solver
import sys


file_list = sys.argv
if len(file_list) != 2:
    print("entre correcte argc")
    exit()
conf = MazeConfig(file_list[1])
conf.load()
# print(conf.width)
# print(conf.height)
# print(conf.entry)
# print(conf.exit)
# print(conf.output_file)
# print(conf.perfect)
maze = Maze(conf.width, conf.height, conf.entry, conf.exit)
maze.create_grid()
gene = MazeGenerator(maze)
gene.place_42_pattern()
gene.generate()
path = bfs_solver(maze)

render_ascii(maze, path)
