import numpy as np
from natural.ants.constants import X_COORD, Y_COORD


def init_grid(grid_size, colors):
    """Return a randomly initialized grid of objects.

    The grid is a 2D array of integers, where
    0 - unoccupied by an object
    1 - occupied by a red object
    2 - occupied by a blue object
    3 - occupied by the next color in the list
    ...

    The colors list contains the number of each color to use. The number of colors
    is taken from the length of the list.
    """
    width, height = grid_size
    num_objects = sum(colors)
    assert num_objects <= width * height, "Too many colored objects to fit in the grid."
    # Use 1D arrays because that's all I can generate random indices for.
    object_grid = np.zeros(height * width, dtype=int)
    random_indices = np.random.choice(height * width, num_objects, replace=False)

    start = 0
    # 0 represents unoccupied, so start color indexing at 1.
    for color, num_color in enumerate(colors, start=1):
        object_grid[random_indices[start : start + num_color]] = color
        start += num_color

    return object_grid.reshape(grid_size)


def init_ants(grid_size, num_ants):
    """Return a randomly initialized array of ants.

    Each ant is a (x, y, load) tuple, where the load is one of
    0 - unloaded
    1 - red
    2 - blue
    3 - green
    ...
    """
    width, height = grid_size
    ants = np.zeros((num_ants, 3), dtype=int)
    # This is an array of indices into the grid as if it were 1D.
    ant_indices = np.random.choice(height * width, num_ants, replace=False)
    for ant, index in zip(ants, ant_indices):
        ant[X_COORD] = index % width
        ant[Y_COORD] = index // width
    return ants
