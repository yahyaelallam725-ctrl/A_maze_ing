from maze.config_parser import MazeConfig
from maze.models import Maze
from maze.generator import MazeGenerator
from maze.solver import bfs_solver
from maze.renderer import render_curses
from maze.writer import writer_hex
import sys
import curses
import random

file_list = sys.argv
if len(file_list) != 2:
    print("Yooo ! Enter the correct number of arguments")
    exit()

conf = MazeConfig(file_list[1])
conf.load()

if conf.seed is not None:
    random.seed(conf.seed)

maze = Maze(conf.width, conf.height, conf.entry, conf.exit, conf.perfect)
maze.create_grid()
gene = MazeGenerator(maze, seed=conf.seed)
warning_msg = None
try:
    gene.place_42_pattern()
except ValueError as e:
    warning_msg = str(e)
gene.generate()
path = bfs_solver(maze)
try:
    curses.wrapper(lambda stdscr: render_curses(stdscr, maze, gene))
except Exception as e:
    print(f"Error: terminal dimensions are not big enough: {e}")
with open(conf.output_file, "w") as file:
    file.write(writer_hex(maze))
