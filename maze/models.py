from typing import List, Tuple


class Cell:

    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True
        self.visited: bool = False
        self.is_42: bool = False

class Maze:

    def __init__(
        self,
        width: int,
        height: int,
        entry: Tuple[int, int],
        exit_coords: Tuple[int, int]
    ) -> None:
        self.width: int = width
        self.height: int = height
        self.entry: Tuple[int, int] = entry
        self.exit: Tuple[int, int] = exit_coords
        self.grid: List[List[Cell]] = []

    def create_grid(self) -> None:
        self.grid = []
        for i in range(self.height):
            rows: List[Cell] = []
            for j in range(self.width):
                rows.append(Cell(j, i))
            self.grid.append(rows)

    def is_inside(self, x: int, y: int) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        return True

    def get_cell(self, x: int, y: int) -> Cell:
        return self.grid[y][x]

    def get_neighbors(self, cell: Cell) -> List[Cell]:
 
        x: int = cell.x
        y: int = cell.y
        neighbors: List[Cell] = []

        if self.is_inside(x, y + 1) and not self.get_cell(x, y + 1).is_42:
            neighbors.append(self.get_cell(x, y + 1))

        if self.is_inside(x, y - 1) and not self.get_cell(x, y - 1).is_42:
            neighbors.append(self.get_cell(x, y - 1))

        if self.is_inside(x + 1, y) and not self.get_cell(x + 1, y).is_42:
            neighbors.append(self.get_cell(x + 1, y))

        if self.is_inside(x - 1, y) and not self.get_cell(x - 1, y).is_42:
            neighbors.append(self.get_cell(x - 1, y))

        return neighbors

    def get_unvisited_neighbors(self, cell: Cell) -> List[Cell]:
        unvisited_neighbors: List[Cell] = []
        neighbors: List[Cell] = self.get_neighbors(cell)
        for neighbor in neighbors:
            if neighbor.visited is False:
                unvisited_neighbors.append(neighbor)
        return unvisited_neighbors

    def remove_wall_between(self, cell_a: Cell, cell_b: Cell) -> None:
        if cell_a.x == cell_b.x:
            if cell_a.y > cell_b.y:
                cell_a.north = False
                cell_b.south = False
            else:
                cell_a.south = False
                cell_b.north = False

        if cell_a.y == cell_b.y:
            if cell_a.x > cell_b.x:
                cell_a.west = False
                cell_b.east = False
            else:
                cell_a.east = False
                cell_b.west = False

    def get_open_neighbors(self, cell: Cell) -> List[Cell]:
        neighbors: List[Cell] = []
        x, y = cell.x, cell.y
        if not cell.north and self.is_inside(x, y - 1):
            neighbors.append(self.get_cell(x, y - 1))
        if not cell.east and self.is_inside(x + 1, y):
            neighbors.append(self.get_cell(x + 1, y))
        if not cell.south and self.is_inside(x, y + 1):
            neighbors.append(self.get_cell(x, y + 1))
        if not cell.west and self.is_inside(x - 1, y):
            neighbors.append(self.get_cell(x - 1, y))
        return neighbors