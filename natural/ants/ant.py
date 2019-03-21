from constants import *

class Ant:
    def __init__(self, x, y, k1, k2):
        self.x = x
        self.y = y
        self.k1 = k1
        self.k2 = k2
        self.load = UNLOADED

    def update(self, kernel, k_x, k_y):
        # Compute percieved fraction
        # If loaded, decide if drop
        # If unloaded, decide if pickup
        # Update grid
        # Move
        raise NotImplementedError

    def perceived_fraction(self, kernel, color):
        """Determine the perceived fraction of objects around the given cell.

        :param cell: An (x, y) tuple of coordinates of the cell to consider.
        :param radius: The size of the square neighborhood around the cell.
        """
        raise NotImplementedError

    def pickup_probability(self, f):
        """Determine the probability of an ant picking up the object in the given cell.

        :param cell: An (x, y) tuple of coordinates of the cell to consider.
        :param f: The perceived fraction of objects near the given cell.
        :param k1: A tunable parameter.
        """
        raise NotImplementedError

    def dropoff_probability(self, f):
        """Determine the probability of an ant dropping off its load in the given cell.

        :param cell: An (x, y) tuple of coordinates of the cell to consider.
        :param f: The perceived fraction of objects near the given cell.
        :param k2: A tunable parameter.
        """
        raise NotImplementedError