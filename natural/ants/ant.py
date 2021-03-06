import numba
import numpy as np

from .constants import EMPTY

spec = [
    ("x", numba.int32),
    ("y", numba.int32),
    ("k1", numba.float32),
    ("k2", numba.float32),
    ("load", numba.int32),
]


@numba.jitclass(spec)
class Ant:
    """An ant entity that moves around and picks up and puts down objects."""

    def __init__(self, x, y, k1, k2):
        """Initialize an Ant with its location and tunable parameters.

        :param x: The x coordinate of the Ant in the grid.
        :param y: The y coordinate of the Ant in the grid.
        :param k1: The pickup probability tunable parameter.
        :param k2: The dropoff probability tunable parameter.
        """
        self.x = x
        self.y = y
        self.k1 = k1
        self.k2 = k2
        self.load = EMPTY

    def update(self, kernel, k_x, k_y):
        """Attempt to pick up or drop off an item at the current location, then make a random step.

        Note that the ant modifies the given kernel by removing items or putting them back in
        different locations. This works because the kernel should be a view of an underlying numpy
        array.

        Also note that the given local coordinates may be something other than the center of the
        kernel if the kernel is near the edge of the grid and is thus not square.

        :param kernel: The Ant's visible neighborhood.
        :param k_x: The local x coordinate of the Ant in the kernel.
        :param k_y: The local y coordinate of the Ant in the kernel.
        """
        self.update_load(kernel, k_x, k_y)
        self.update_location(kernel, k_x, k_y)

    def pickup(self, kernel, k_x, k_y):
        self.load = kernel[k_x, k_y, 0]
        kernel[k_x, k_y, 0] = EMPTY

    def dropoff(self, kernel, k_x, k_y):
        kernel[k_x, k_y, 0] = self.load
        self.load = EMPTY

    def update_load(self, kernel, k_x, k_y):
        """Randomly pick up or drop off an object.

        The ant randomly decides to pick up an object if the cell it's residing in is occupied. It
        does so with some probability influenced by how many other objects of the same type the Ant
        can see. If it can see many like objects, the probability of picking up the object is low.

        Likewise, the ant randomly decides to drop off an object in an unoccupied cell if it is
        loaded. It does so with some probability similarly influenced by the number of like objects
        the Ant can see. If the are many like objects, the probability of dropping off the object
        is high.

        :param kernel: The Ant's visible neighborhood.
        :param k_x: The local x coordinate of the Ant in the kernel
        :param k_y: The local y coordinate of the Ant in the kernel
        """
        color = kernel[k_x, k_y, 0]
        cell_occupied = bool(color)

        # Pick up
        if self.load == EMPTY and cell_occupied:
            # Calculate p based on value in grid cell
            f = self.perceived_fraction(kernel[:, :, 0], color)
            # Dermine if ant should pick up value
            if np.random.random() <= self.pickup_probability(f):
                # NOTE: Removing the item from the grid makes it impossible to use the item in the
                # perceived fraction calculation. However, from our tests, it appears this works
                # best.
                self.pickup(kernel, k_x, k_y)
        # Drop off
        elif self.load != EMPTY and not cell_occupied:
            # Calculate p based on value ant is carryin
            f = self.perceived_fraction(kernel[:, :, 0], self.load)
            # Determine if ant should drop value
            if np.random.random() <= self.dropoff_probability(f):
                self.dropoff(kernel, k_x, k_y)

    def update_location(self, kernel, k_x, k_y):
        """Randomly take a step in one of the neighboring cells.

        :param kernel: The Ant's visible neighborhood.
        :param k_x: The Ant's local x coordinate in the neighborhood.
        :param k_y: The Ant's local y coordinate in the neighborhood.
        """
        # TODO: This randomly selects *any* cell in the entire neighborhood. Pick a random
        # unoccupied cell only one cell away from (k_x, k_y).
        unoccupied_by_ants = kernel[:, :, 1] == EMPTY
        unoccupied_by_items = kernel[:, :, 0] == EMPTY

        # Find unoccupied indices.
        x, y = np.where(unoccupied_by_ants)
        if self.load != EMPTY:
            x, y = np.where(np.logical_and(unoccupied_by_ants, unoccupied_by_items))

        i = np.random.randint(len(x))
        new_x, new_y = x[i], y[i]

        # Update the ant's position in the ant layer.
        kernel[k_x, k_y, 1] = 0
        kernel[new_x, new_y, 1] = 1

        self.x = self.x - (k_x - new_x)
        self.y = self.y - (k_y - new_y)

    def perceived_fraction(self, kernel, color):
        """Determine the perceived fraction of objects of a given color around the given kernel.

        :param kernel: A sub matrix of the grid that will be considered.
        :param color: The color of the elements that will be considered.
        """
        return np.sum(kernel == color) / (kernel.size - 1)

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
