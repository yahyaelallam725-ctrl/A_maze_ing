class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.north = True
        self.east = True
        self.south = True
        self.west = True
        self.visited = False


class Maze:
    def __init__(self, width: int, height: int, entry: tuple[int, int], exit: tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.grid = []

    def create_grid(self) -> None:
        self.grid = []
        for i in range(self.height):
            rows = []
            for j in range(self.width):
                rows.append(Cell(j, i))
            self.grid.append(rows)

    def is_inside(self, x, y) -> bool:
        if x < 0 or y < 0:
            return False
        if x >= self.width or y >= self.height:
            return False
        return True

    def get_cell(self, x: int, y: int):
        return self.grid[y][x]

    def get_neighbors(self, cell: Cell) -> list:
        x = cell.x
        y = cell.y
        neighbors = []

        if self.is_inside(x, y + 1):
            neighbors.append(self.get_cell(x, y + 1))

        if self.is_inside(x, y - 1):
            neighbors.append(self.get_cell(x, y - 1))

        if self.is_inside(x + 1, y):
            neighbors.append(self.get_cell(x + 1, y))

        if self.is_inside(x - 1, y):
            neighbors.append(self.get_cell(x - 1, y))

        return neighbors

    def get_unvisited_neighbors(self, cell) -> list:
        unvisited_neighbors = []
        neighbors = self.get_neighbors(cell)
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



# def create_grid(self):


# MazeConfig
#    ↓
# Maze(width, height, entry, exit)
#    ↓
# Maze creates grid
#    ↓
# grid contains Cell objects
#    ↓
# Maze ready for generation 


# grid[0][0]  grid[0][1]  grid[0][2]  grid[0][3]
# grid[1][0]  grid[1][1]  grid[1][2]  grid[1][3]
# grid[2][0]  grid[2][1]  grid[2][2]  grid[2][3]

# conf = MazeConfig("../config_default.txt")
# conf.load()

# maze = Maze(conf.width, conf.height, conf.entry, conf.exit)

# maze.create_grid()