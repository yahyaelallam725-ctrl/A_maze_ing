from maze.solver import bfs_solver
import curses
import locale


def render_curses(stdscr, maze, generator):
    locale.setlocale(locale.LC_ALL, '')
    curses.start_color()
    curses.start_color()
    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_RED, 0)
    curses.init_pair(2, curses.COLOR_GREEN, 0)
    curses.init_pair(3, curses.COLOR_CYAN, 0)
    curses.init_pair(4, curses.COLOR_RED, 0)
    curses.init_pair(5, curses.COLOR_YELLOW, 0)
    path = bfs_solver(maze)
    show_path = True
    def color_picker():
        colors = [
            (curses.COLOR_WHITE,   "White"),
            (curses.COLOR_CYAN,    "Cyan"),
            (curses.COLOR_GREEN,   "Green"),
            (curses.COLOR_RED,     "Red"),
            (curses.COLOR_YELLOW,  "Yellow"),
            (curses.COLOR_MAGENTA, "Magenta"),
            (curses.COLOR_BLUE,    "Blue"),
            (curses.COLOR_BLACK,   "Black"),
        ]
        targets = [
            (1, "42 pattern color"),
            (2, "Wall color"),
            (3, "Entry color"),
            (4, "Exit color"),
            (5, "Path color"),
        ]
        target_idx = 0
        selected = 0
        popup_h = 16
        popup_w = 32
        start_y = maze.height * 2 // 2 - popup_h // 2
        start_x = maze.width * 4 // 2 - popup_w // 2
        while True:
            # draw popup
            stdscr.addstr(start_y,     start_x, "┌──────────────────────────────┐", curses.color_pair(1))
            stdscr.addstr(start_y + 1, start_x, "│        Color Picker          │", curses.color_pair(1))
            stdscr.addstr(start_y + 2, start_x, "├──────────────────────────────┤", curses.color_pair(1))
            # targets row
            for i, (pair, name) in enumerate(targets):
                prefix = "►" if i == target_idx else " "
                stdscr.addstr(start_y + 3 + i, start_x, f"│ {prefix} {name:<28}│", curses.color_pair(pair))
            stdscr.addstr(start_y + 3 + len(targets), start_x, "├──────────────────────────────┤", curses.color_pair(1))
            # colors row
            for i, (color_val, color_name) in enumerate(colors):
                curses.init_pair(20 + i, color_val, -1)
                prefix = "►" if i == selected else " "
                stdscr.addstr(start_y + 4 + len(targets) + i, start_x, f"│ {prefix} {color_name:<28}│", curses.color_pair(20 + i))
            stdscr.addstr(start_y + 4 + len(targets) + len(colors), start_x, "└──────────────────────────────┘", curses.color_pair(1))
            stdscr.addstr(start_y + 5 + len(targets) + len(colors), start_x, " TAB: switch target  ↑↓: color", curses.color_pair(1))
            stdscr.addstr(start_y + 6 + len(targets) + len(colors), start_x, " ENTER: apply  ESC: close", curses.color_pair(1))
            stdscr.refresh()
            key = stdscr.getch()
            if key == curses.KEY_UP:
                selected = (selected - 1) % len(colors)
            elif key == curses.KEY_DOWN:
                selected = (selected + 1) % len(colors)
            elif key == ord('\t'):  # TAB switches target
                target_idx = (target_idx + 1) % len(targets)
            elif key == ord('\n'):
                # apply selected color to selected target pair
                pair_id = targets[target_idx][0]
                curses.init_pair(pair_id, colors[selected][0], -1)
            elif key == 27:  # ESC closes
                break
    def draw():
        nonlocal path, show_path
        curses.curs_set(0)
        stdscr.clear()
        path_coords = set((cell.x, cell.y) for cell in path) if show_path else set()
        path_symbols = {}
        if show_path:
            for i in range(len(path) - 1):
                a = path[i]
                b = path[i + 1]
                if b.x > a.x:
                    path_symbols[(a.x, a.y)] = " ▶ "
                elif b.x < a.x:
                    path_symbols[(a.x, a.y)] = " ◀ "
                elif b.y > a.y:
                    path_symbols[(a.x, a.y)] = " ▼ "
                elif b.y < a.y:
                    path_symbols[(a.x, a.y)] = " ▲ "
            # last cell points to exit
            last = path[-1]
            path_symbols[(last.x, last.y)] = " ✦ "
        W = curses.color_pair(2)  # wall color shortcut
        # top border
        stdscr.addstr(0, 0, "┌", W)
        stdscr.addstr(0, 1, "───", W)
        for x in range(1, maze.width):
            stdscr.addstr(0, x * 4, "─", W)
            stdscr.addstr(0, x * 4 + 1, "───", W)
        stdscr.addstr(0, maze.width * 4, "┐", W)
        for y in range(maze.height):
            for x in range(maze.width):
                cell = maze.get_cell(x, y)
                # body color
                if (x, y) == maze.entry:
                    body = " E "
                    color = curses.color_pair(3)
                elif (x, y) == maze.exit:
                    body = " X "
                    color = curses.color_pair(4)
                elif (x, y) in path_coords:
                    body = path_symbols.get((x, y), " • ")
                    color = curses.color_pair(5)
                elif getattr(cell, 'is_42', False):
                    body = " █ "
                    color = curses.color_pair(1)
                else:
                    body = "   "
                    color = curses.color_pair(2)
                # west wall
                if x == 0:
                    stdscr.addstr((y * 2) + 1, x * 4, "│", W)
                else:
                    stdscr.addstr((y * 2) + 1, x * 4, "│" if cell.west else " ", W)
                # body
                stdscr.addstr((y * 2) + 1, x * 4 + 1, body, color)
                # bottom wall
                if y + 1 == maze.height and x == 0:
                    stdscr.addstr((y * 2) + 2, x * 4, "└", W)
                    stdscr.addstr((y * 2) + 2, x * 4 + 1, "───", W)
                elif x == 0:
                    stdscr.addstr((y * 2) + 2, x * 4, "│", W)
                    stdscr.addstr((y * 2) + 2, x * 4 + 1, "───" if cell.south else "   ", W)
                elif y + 1 == maze.height:
                    stdscr.addstr((y * 2) + 2, x * 4, "─", W)
                    stdscr.addstr((y * 2) + 2, x * 4 + 1, "───", W)
                else:
                    has_h = cell.south
                    has_v = (maze.is_inside(x - 1, y) and maze.get_cell(x - 1, y).east) or \
                            (maze.is_inside(x, y) and maze.get_cell(x, y).west)
                    if has_h and has_v:
                        j = "┼"
                        h = "───"
                    elif has_h:
                        j = "─"
                        h = "───"
                    elif has_v:
                        j = "│"
                        h = "   "
                    else:
                        j = " "
                        h = "   "
                    stdscr.addstr((y * 2) + 2, x * 4, j, W)
                    stdscr.addstr((y * 2) + 2, x * 4 + 1, h, W)
            # east wall
            stdscr.addstr((y * 2) + 1, maze.width * 4, "│", W)
            if y + 1 < maze.height:
                stdscr.addstr((y * 2) + 2, maze.width * 4, "│", W)
            else:
                stdscr.addstr((y * 2) + 2, maze.width * 4, "┘", W)
        # menu bar below maze
        menu_row = maze.height * 2 + 1
        stdscr.addstr(
            menu_row, 0,
            "The Magic Maze Menu:\n"
            "[r] Regenerate\n[p] Path on/off]\n[c] Colors\n[q] Quit ", curses.color_pair(6) | curses.A_BOLD
        )
        stdscr.refresh()
    draw()
    while True:
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('r'):
            maze.create_grid()
            generator.place_42_pattern()
            generator.generate()
            path = bfs_solver(maze)
            draw()
        elif key == ord('p'):
            show_path = not show_path
            draw()
        elif key == ord('c'):
            color_picker()
            draw()
        elif key == ord('\n'):
            pair_id = targets[target_idx][0]  # ← this should be 1,2,3,4, or 5
            color_val = colors[selected][0]   # ← the chosen color value
            curses.init_pair(pair_id, color_val, -1)  # ← reinitialize the correct pair
