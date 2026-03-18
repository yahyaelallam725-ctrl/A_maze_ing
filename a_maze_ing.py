from maze.config_parser import MazeConfig
from maze.models import Maze
from maze.generator import MazeGenerator
from maze.solver import bfs_solver


from maze.writer import writer_hex
from maze.renderer import render_curses
import sys
import curses
import locale

file_list = sys.argv

if len(file_list) != 2:
    print("entre correcte argc")
    exit()

conf = MazeConfig(file_list[1])
conf.load()


if conf.seed is not None:
    random.seed(conf.seed)

maze = Maze(conf.width, conf.height, conf.entry, conf.exit)
maze.create_grid()

gene = MazeGenerator(maze)
gene.place_42_pattern()
gene.generate()

if not conf.perfect :
    gene.make_imperfect(5)

path = bfs_solver(maze)
locale.setlocale(locale.LC_ALL, '')
curses.wrapper(lambda stdscr: render_curses(stdscr, maze, gene))


with   open(conf.output_file,"w") as file:
    file.write(writer_hex(maze))


