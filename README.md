*This project has been created as part of the 42 curriculum by \<otqori\>, \<yelallam\>.*

---

# A-Maze-ing

## Description

A-Maze-ing is a maze generator and solver written in Python. The program reads a configuration file, generates a random maze using the **DFS Recursive Backtracker** algorithm, solves it using **BFS (Breadth-First Search)**, and displays the result in an interactive terminal interface using the `curses` library.

Key features:
- Random maze generation with optional seed for reproducibility
- Perfect maze mode (exactly one path between any two cells) or imperfect mode (loops allowed)
- Visual "42" pattern embedded in every maze
- Interactive terminal renderer with colors, animations, and a color picker
- Shortest path visualization with directional arrows
- Reusable maze generator packaged as a pip-installable Python package

---

## Instructions

### Requirements

- Python 3.10 or later
- No external dependencies required for the main program

### Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd the_maze

# Install dependencies (none required, but Makefile rule available)
make install
```

### Running the program

```bash
# Using make
make run

# Or directly
python3 a_maze_ing.py config_default.txt

# With a custom config file
python3 a_maze_ing.py my_config.txt
```

### Keyboard controls

| Key | Action |
|-----|--------|
| `r` | Regenerate a new maze |
| `p` | Show / Hide the solution path |
| `c` | Open the color picker |
| `a` | Animate maze generation (DFS) |
| `s` | Animate BFS pathfinding |
| `q` | Quit |

### Linting

```bash
make lint
make lint-strict  # optional stricter check
```

### Building the reusable package

```bash
cd mazegen_pkg
python -m build
# Output: dist/mazegen-1.0.0.tar.gz and dist/mazegen-1.0.0-py3-none-any.whl
```

---

## Configuration File

The program takes a plain text configuration file as its only argument. Each line must follow the `KEY=VALUE` format. Lines starting with `#` are treated as comments and ignored.

### Mandatory keys

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `WIDTH` | Integer | Number of columns in the maze | `WIDTH=20` |
| `HEIGHT` | Integer | Number of rows in the maze | `HEIGHT=15` |
| `ENTRY` | Tuple (x,y) | Entry cell coordinates (0-indexed) | `ENTRY=0,0` |
| `EXIT` | Tuple (x,y) | Exit cell coordinates (0-indexed) | `EXIT=19,14` |
| `OUTPUT_FILE` | String | Path to the output hex file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Boolean | If True, generates a perfect maze | `PERFECT=True` |

### Optional keys

| Key | Type | Description | Example |
|-----|------|-------------|---------|
| `SEED` | Integer | Random seed for reproducibility | `SEED=42` |

### Example configuration file

```
# Default maze configuration
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Validation rules

- `WIDTH` and `HEIGHT` must be positive integers
- `ENTRY` and `EXIT` must be within maze bounds and must be different cells
- `PERFECT` must be exactly `True` or `False`
- `SEED` is optional — if omitted, the maze is randomly generated each run

---

## Maze Generation Algorithm

### Chosen algorithm: DFS Recursive Backtracker

The maze is generated using the **Depth-First Search (DFS) Recursive Backtracker** algorithm, also known as the "recursive backtracker" or "randomized DFS".

### How it works

1. Start at cell (0, 0) and mark it as visited
2. Push it onto a stack
3. While the stack is not empty:
   - Look at the top cell — find all unvisited neighbors
   - If unvisited neighbors exist: pick one randomly, remove the wall between them, mark it visited, push it onto the stack
   - If no unvisited neighbors exist: pop the stack (backtrack)
4. When the stack is empty, every cell has been visited — the maze is complete

For **imperfect mazes** (`PERFECT=False`), a post-processing step randomly removes a percentage of walls to introduce loops, giving multiple paths between some cells.

### Why this algorithm?

- **Simple to implement** — the iterative stack-based version avoids Python recursion depth limits
- **Produces high-quality mazes** — long, winding corridors with good visual complexity
- **Directly maps to spanning tree theory** — a perfect maze is exactly a spanning tree of the grid graph
- **Efficient** — O(n) time and space where n is the number of cells
- **Easy to animate** — the step-by-step nature of DFS makes it ideal for real-time animation

---

## Reusable Module: mazegen

The maze generation logic is packaged as a standalone pip-installable Python package located in `mazegen_pkg/`.

### Installation

```bash
pip install mazegen-1.0.0.tar.gz
```

### Basic usage

```python
from mazegen.core import Maze, MazeGenerator

# Create and generate a maze
maze = Maze(width=20, height=15, entry=(0, 0), exit=(19, 14))
maze.create_grid()

gen = MazeGenerator(maze, seed=42)
gen.generate()

# Get the solution
path = gen.solve()
print(f"Path length: {len(path)} cells")
for cell in path:
    print(f"  ({cell.x}, {cell.y})")
```

### Custom parameters

```python
# Imperfect maze with seed
maze = Maze(width=30, height=20, entry=(0, 0), exit=(29, 19), perfect=False)
maze.create_grid()
gen = MazeGenerator(maze, seed=123)
gen.generate()
```

### Accessing the maze structure

```python
# Access individual cells
cell = maze.get_cell(x=5, y=3)
print(cell.north)   # True = wall closed, False = wall open
print(cell.east)
print(cell.is_42)   # True if part of the 42 pattern

# Iterate all cells
for row in maze.grid:
    for cell in row:
        print(f"({cell.x},{cell.y}): N={cell.north} E={cell.east}")
```

### Step-by-step generation (animation)

```python
gen = MazeGenerator(maze)
for _ in gen.generate_animated():
    # called after each wall removal
    # render your maze state here
    pass
```

### Rebuilding the package from source

```bash
cd mazegen_pkg
python -m venv env
source env/bin/activate
pip install build
python -m build
# creates dist/mazegen-1.0.0.tar.gz
```

---

## Resources

### Algorithm references

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker — ThinMatrix](https://www.youtube.com/watch?v=Y37-gB83HKE)
- [BFS pathfinding — redblobgames](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Spanning trees and perfect mazes — Jamis Buck's blog](http://weblog.jamisbuck.org/2011/2/7/maze-generation-algorithm-recap)

### Python references

- [Python curses documentation](https://docs.python.org/3/library/curses.html)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [flake8 documentation](https://flake8.pycqa.org/)

### AI usage

AI (Claude by Anthropic) was used during this project for the following tasks:

- **Algorithm explanation** — understanding DFS recursive backtracker, BFS pathfinding, and spanning tree theory before implementation
- **Debugging assistance** — identifying scoping issues (`nonlocal`), type annotation errors, and flake8 violations
- **curses renderer** — guidance on curses API, color pairs, Unicode box-drawing characters, and popup positioning
- **Type annotations** — adding proper mypy-compliant type hints across all files
- **Package structure** — guidance on `pyproject.toml` setup and pip-installable package creation
- **README structure** — drafting and organizing this document

All AI-generated content was reviewed, tested, and understood before being included in the project.

---

## Team and Project Management

### Team members and roles

| Member | Role |
|--------|------|
| `otqori` | Parsing configuration, Maze generation (DFS algorithm, models, generator class) |
| `yelallam` | package creation, BFS solver, curses renderer, animations |

### Planning

**Initial plan (week 1):**
- Day 1-2: Project setup, config parser, maze models
- Day 3-4: DFS generation algorithm
- Day 5-6: BFS solver, hex output writer
- Day 7: Renderer, README, packaging

**How it evolved:**
- The renderer took significantly longer than expected due to Unicode alignment issues with the curses terminal display
- The color picker and animation features were added iteratively as the renderer stabilized
- Package creation was simpler than expected thanks to Python's `build` module
- Flake8 and mypy compliance required a dedicated cleanup pass at the end

### What worked well

- The DFS and BFS algorithms were clean to implement and easy to test visually
- The curses-based renderer ended up being more feature-rich than originally planned (colors, animations, directional path arrows)
- The modular file structure (`models.py`, `generator.py`, `solver.py`, `renderer.py`) made parallel development easy
- The `mazegen` package API is clean and well-documented

### What could be improved

- The curses renderer could support resizing the terminal window dynamically
- The 42 pattern placement could be smarter — currently it can conflict with entry/exit on small mazes
- Multiple maze generation algorithms could be supported (Prim's, Kruskal's) as a bonus
- More comprehensive unit tests using `pytest` would improve reliability

### Tools used

- **VS Code** — main editor
- **Python 3.13** — runtime
- **flake8** — style linting
- **mypy** — static type checking
- **Git** — version control
- **Claude (Anthropic)** — AI assistant for guidance and debugging
- **Python `build` module** — package creation
