import numpy as np

from natural.ants.constants import BLUE, RED, X_COORD, Y_COORD


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


def perceived_fraction(grid, cell, neighborhood):
    """Get the perceived fraction of objects around the given cell.

    :param grid: The grid to search through
    :param cell: An (x, y) tuple of coordinates of the cell to consider
    :param neighborhood: The size of the square neighborhood around the cell.
    """
    raise NotImplementedError


def pickup_probability(grid, cell, f, k1):
    """Determine the probability of an ant picking up the object in the given cell.

    :param grid: The grid of objects.
    :param cell: An (x, y) tuple of coordinates of the cell to consider.
    :param f: The perceived fraction of objects near the given cell.
    :param k1: A tunable parameter.
    """
    raise NotImplementedError


def dropoff_probability(grid, cell, f, k2):
    """Determine the probability of an ant dropping off its load in the given cell.

    :param grid: The grid of objects.
    :param cell: An (x, y) tuple of coordinates of the cell to consider.
    :param f: The perceived fraction of objects near the given cell.
    :param k2: A tunable parameter.
    """
    raise NotImplementedError


def cluster(grid, iters, ants, neighborhood, k1, k2):
    """Use the Ant Clustering Algorithm to cluster the given grid.

    :param grid: The grid to cluster.
    :type grid: A 2D array of RED, BLUE, or UNLOADED values.
    :param iters: The number of iterations to the the ACA for.
    :param ants: The number of ants to use.
    :param neighborhood: The size of the square neighborhood around the cell.
    :type neighborhood: int
    :param k1: The tunable parameter for the pickup probability.
    :param k2: The tunable parameter for the dropoff probability.
    """
    raise NotImplementedError
