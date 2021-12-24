from aoc_helper import read_and_clean_file
import numpy as np

lines, line_count = read_and_clean_file(".\data\day_13_data.txt")
points = [x.split(',') for x in lines if not x.startswith('fold along') and x != '']
instructions = [x.removeprefix('fold along ').split('=') for x in lines if x.rfind(',') == -1 and x != '']

max_x = max(int(x[0]) for x in points) + 1
max_y = max(int(y[1]) for y in points) + 1

grid = [[0 for x in range(max_x)] for i in range(max_y)]

for p in points:
    x = int(p[0])
    y = int(p[1])
    grid[y][x] = 1

for i in instructions:
    fold_point = int(i[1])

    if i[0] == 'x':
        new_grid = [[0 for x in range(fold_point + 1)] for i in range(max_y)]

        for y in range(max_y):
            for x in range(max_x):
                v = grid[y][x]
                if v == 1:
                    if x < fold_point:
                        new_grid[y][x] = grid[y][x]
                    else:
                        x_diff = fold_point - (x - fold_point)
                        new_grid[y][x_diff] = grid[y][x]
                
        grid = new_grid
    else:
        new_grid = [[0 for x in range(max_x)] for i in range(fold_point + 1)]

        for y in range(max_y):
            for x in range(max_x):
                v = grid[y][x]
                if v == 1:
                    if y < fold_point:
                        new_grid[y][x] = grid[y][x]
                    else:
                        y_diff = fold_point - (y - fold_point)
                        new_grid[y_diff][x] = grid[y][x]
                
        grid = new_grid
    
    max_x = len(grid[0])
    max_y = len(grid)

print(np.array(grid))