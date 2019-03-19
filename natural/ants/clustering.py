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
