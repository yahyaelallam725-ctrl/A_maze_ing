PYTHON = python3
MAIN_SCRIPT = a_maze_ing.py
ARGS =  config_default.txt

.PHONY: install run debug clean lint lint-strict

install:
	pip install flake8 mypy

run:
	$(PYTHON) $(MAIN_SCRIPT) $(ARGS)

debug:
	$(PYTHON) -m pdb $(MAIN_SCRIPT) $(ARGS)

clean:
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +

lint:
	python3 -m flake8 .
	python3 -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .
	mypy . --strict



# def make_imperfect(self, extra_walls_to_remove: int = 5) -> None:
#         """
#         تكسير بعض الجدران عشوائياً لخلق مسارات متعددة (في حال كان PERFECT = False).
#         """
#         removed = 0
#         while removed < extra_walls_to_remove:
#             # اختيار إحداثيات عشوائية (تجنب الحواف)
#             x = random.randint(1, self.maze.width - 2)
#             y = random.randint(1, self.maze.height - 2)
#             cell = self.maze.get_cell(x, y)
            
#             # اختيار جدار عشوائي لفتحه
#             wall = random.choice(['north', 'east', 'south', 'west'])
            
#             # التأكد أننا لا نفتح جداراً لخلية "42"
#             neighbor = None
#             if wall == 'north': neighbor = self.maze.get_cell(x, y - 1)
#             elif wall == 'south': neighbor = self.maze.get_cell(x, y + 1)
#             elif wall == 'east': neighbor = self.maze.get_cell(x + 1, y)
#             elif wall == 'west': neighbor = self.maze.get_cell(x - 1, y)

#             if neighbor and not cell.is_42 and not neighbor.is_42:
#                 # نفتح الجدار بين الخلية وجارها
#                 self.maze.remove_wall_between(cell, neighbor)
#                 removed += 1