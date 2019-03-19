class AntClustering:
    """Implements the Ant Clustering Algorithm."""

    def __init__(self, grid, animate=False):
        """Initialize the algorithm to cluster the given grid.

        :param grid: The grid to cluster.
        :type grid: A 2D array of integers.
        :param animated: Whether or not to animate each run of the algorithm.
        """
        # Perform a copy so that we can modify the given grid willy-nilly.
        self.grid = grid.copy()
        self.animate = animate

    def perceived_fraction(self, cell, neighborhood):
        """Determine the perceived fraction of objects around the given cell.

        :param cell: An (x, y) tuple of coordinates of the cell to consider.
        :param neighborhood: The size of the square neighborhood around the cell.
        """
        raise NotImplementedError

    def pickup_probability(self, cell, f, k1):
        """Determine the probability of an ant picking up the object in the given cell.

        :param cell: An (x, y) tuple of coordinates of the cell to consider.
        :param f: The perceived fraction of objects near the given cell.
        :param k1: A tunable parameter.
        """
        raise NotImplementedError

    def dropoff_probability(self, cell, f, k2):
        """Determine the probability of an ant dropping off its load in the given cell.

        :param cell: An (x, y) tuple of coordinates of the cell to consider.
        :param f: The perceived fraction of objects near the given cell.
        :param k2: A tunable parameter.
        """
        raise NotImplementedError

    def cluster(self, iters, ants, neighborhood_size, k1, k2):
        """Cluster the grid with the given tunable parameters.

        Provide the tunable parameters here, so different tunable parameters can
        be attempted on the same grid.

        :param iters: The number of iterations to the the ACA for.
        :param ants: The number of ants to use.
        :param neighborhood: The size of the square neighborhood around the cell.
        :type neighborhood: int
        :param k1: The tunable parameter for the pickup probability.
        :param k2: The tunable parameter for the dropoff probability.
        :returns: The clustered grid.
        """
        raise NotImplementedError
