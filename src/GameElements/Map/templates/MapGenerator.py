import random
import json


width_cells = 30
height_cells = 30
cells = ['-'] * width_cells
for i in range(0, width_cells):
    cells[i] = [0] * height_cells
    for j in range(0, height_cells):
        cells[i][j] = '-'

ind_x = 0
ind_y = 0
for ind_x, row in enumerate(cells):
    for ind_y, cell in enumerate(row):
        if ind_x == 0 or ind_y == 0:
            cells[ind_x][ind_y] = 'w'
        if ind_x == width_cells - 1 or ind_y == height_cells - 1:
            cells[ind_x][ind_y] = 'w'

f = open('test_map_3.txt', 'w')
for row in cells:
    for cell in row:
        f.write(str(cell))
    f.write('\n')
f.close()
