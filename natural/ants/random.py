import numpy as np
from natural.ants.constants import X_COORD, Y_COORD, RED, BLUE


def init_grid(grid_size, num_reds, num_blues):
    """Return a randomly initialized grid of objects.

    The grid is a 2D array of integers, where
    0 - unoccupied by an object
    1 - occupied by a blue object
    2 - occupied by a red object
    """
    width, height = grid_size
    # Use 1D arrays because that's all I can generate random indices for.
    object_grid = np.zeros(height * width, dtype=int)
    # Create REDS+BLUES random indices for an array of size height*width.
    random_indices = np.random.choice(height * width, num_reds + num_blues, replace=False)
    object_grid[random_indices[:num_reds]] = RED
    object_grid[random_indices[num_reds:]] = BLUE
    return object_grid.reshape(grid_size)


def init_ants(grid_size, num_ants):
    """Return a randomly initialized array of ants.

    Each ant is a (x, y, load) tuple, where the load is one of
    0 - unloaded
    1 - blue
    2 - red
    """
    width, height = grid_size
    ants = np.zeros((num_ants, 3), dtype=int)
    # This is an array of indices into the grid as if it were 1D.
    ant_indices = np.random.choice(height * width, num_ants, replace=False)
    for ant, index in zip(ants, ant_indices):
        ant[X_COORD] = index % width
        ant[Y_COORD] = index // width
    return ants
