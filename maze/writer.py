from maze.models import Maze, Cell
from maze.solver import bfs_solver


def to_hex(number: int) -> str:
    hex_digits = "0123456789ABCDEF"
    return hex_digits[number]


def get_total(cell: Cell) -> int:
    total = 0
    if cell.north:
        total += 1
    if cell.east:
        total += 2
    if cell.south:
        total += 4
    if cell.west:
        total += 8
    return total


def different_corr(cell_a: Cell, cell_b: Cell) -> str:
    if cell_b.x == cell_a.x + 1 and cell_b.y == cell_a.y:
        return "E"
    if cell_b.x == cell_a.x - 1 and cell_b.y == cell_a.y:
        return "W"
    if cell_b.x == cell_a.x and cell_b.y == cell_a.y + 1:
        return "S"
    if cell_b.x == cell_a.x and cell_b.y == cell_a.y - 1:
        return "N"
    return ""


def writer_hex(maze: Maze) -> str:
    lines = []
    line = ""
    for i in range(maze.height):
        line = ""
        for j in range(maze.width):
            n = get_total(maze.grid[i][j])
            line += to_hex(n)
        lines.append(line)


    lines.append(f"{maze.entry[0]},{maze.entry[1]}")
    lines.append(f"{maze.exit[0]},{maze.exit[1]}")


    path = bfs_solver(maze)
    directions = ""

    for i in range(len(path) - 1):
        directions += different_corr(path[i], path[i + 1])

    lines.append(directions)
    
    return "\n".join(lines)