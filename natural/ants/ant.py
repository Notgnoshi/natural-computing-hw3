import numpy as np

from .constants import EMPTY


class Ant:
    def __init__(self, x, y, k1, k2):
        self.x = x
        self.y = y
        self.k1 = k1
        self.k2 = k2
        self.load = EMPTY

    def update(self, kernel, k_x, k_y):
        self.update_load(kernel, k_x, k_y)
        self.update_location(kernel, k_x, k_y)

    def update_load(self, kernel, k_x, k_y):
        cell_status = kernel[k_x, k_y]
        cell_occupied = bool(cell_status)

        # Pick up
        if self.load == EMPTY and cell_occupied:
            # Calculate p based on value in grid cell
            f = self.perceived_fraction(kernel, cell_status)
            # Dermine if ant should pick up value
            if np.random.random() <= self.pickup_probability(f):
                # Pick up value
                self.load = cell_status
                kernel[k_x, k_y] = EMPTY
        # Drop off
        elif self.load != EMPTY and not cell_occupied:
            # Calculate p based on value ant is carryin
            f = self.perceived_fraction(kernel, self.load)
            # Determine if ant should drop value
            if np.random.random() <= self.dropoff_probability(f):
                # Drop value
                kernel[k_x, k_y] = self.load
                self.load = EMPTY

    def update_location(self, kernel, k_x, k_y):
        max_x, max_y = kernel.shape
        # NOTE: Ant potentially doesn't move...
        # Use the size of the kernel to make sure the ant doesn't run off the edge
        new_x = min(max(k_x + np.random.randint(-1, 1 + 1), 0), max_x)
        new_y = min(max(k_y + np.random.randint(-1, 1 + 1), 0), max_y)
        self.x = self.x - (k_x - new_x)
        self.y = self.y - (k_y - new_y)

    def perceived_fraction(self, kernel, color):
        """Determine the perceived fraction of objects of a given color around the given kernel.

        :param kernel: A sub matrix of the grid that will be considered.
        :param color: The color of the elements that will be considered.
        """
        return np.count_nonzero(kernel == color) / kernel.size

    def pickup_probability(self, f):
        """Determine the probability of an ant picking up the object in the given cell.

        :param f: The perceived fraction of objects near the given cell.
        """
        return (self.k1 / (self.k1 + f)) ** 2

    def dropoff_probability(self, f):
        """Determine the probability of an ant dropping off its load in the given cell.

        :param f: The perceived fraction of objects near the given cell.
        """
        return 2 * f if f < self.k2 else 1
