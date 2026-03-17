from collections import deque
from maze.models import Maze, Cell


def bfs_solver(maze: Maze) -> list[Cell]:
    #the setup
    entry = maze.get_cell(*maze.entry)
    exit_ = maze.get_cell(*maze.exit)
    #step 1: we need to make the bfs algo decide on which cell to visit next
    #by storing each unvisited neighbor in a fifo queue
    queue = deque()
    queue.append(entry)
    #step2:now we need to make sure we only visit unvisited cells
    visited = set()
    visited.add(entry)
    #step3:now we need to make sure that it remembers the path it took
    #by saving the child cell that we found  along with it's parent cell
    came_from = {}
    came_from[entry] = None   #as that the entry cell has no parent
    while queue:
        current = queue.popleft()   # take from front — which deque method?
        if current == exit_:
            break
        for neighbor in maze.get_open_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    #step4: reconstrunt the path: since now we are on the exit cell we need to trace back to the entry
    path = []
    current = exit_
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path
