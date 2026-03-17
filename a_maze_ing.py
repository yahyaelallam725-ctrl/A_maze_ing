from maze.config_parser import MazeConfig
from maze.models import Maze
from maze.generator import MazeGenerator
from maze.solver import bfs_solver
from maze.renderer import render_curses
import sys
import curses
import locale

file_list = sys.argv
if len(file_list) != 2:
    print("Yooo ! Enter the correct number of arguments")
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
locale.setlocale(locale.LC_ALL, '')
curses.wrapper(lambda stdscr: render_curses(stdscr, maze, gene))
#render_ascii(maze, path)
print()