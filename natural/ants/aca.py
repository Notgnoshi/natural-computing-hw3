import matplotlib.pyplot as plt
import numba
import numpy as np
from matplotlib.colors import ListedColormap

from .ant import Ant


@numba.jit(nopython=True, cache=True)
def __kernel(matrix, x1, y1, x2, y2):
    """Get the kernel from (x1, y1) to (x2, y2) from the given matrix."""
    # Only get the first two dimensions of the matrix if more exist.
    width, height = matrix.shape[:2]
    x1 = max(0, min(x1, width))
    x2 = max(0, min(x2, width))
    y1 = max(0, min(y1, height))
    y2 = max(0, min(y2, height))
    return matrix[x1 : x2 + 1, y1 : y2 + 1]


@numba.jit(nopython=True, cache=True)
def kernel_center(matrix, x, y, r):
    """Get the kernel centered at (x, y) with radius `r` from the given matrix."""
    x1, x2 = x - r, x + r
    y1, y2 = y - r, y + r
    return __kernel(matrix, x1, y1, x2, y2)


@numba.jit(nopython=True, cache=True)
def kernel_coords(coords, radius):
    """Given a set of matrix coordinates and a kernel radius, get the local kernel coordinates.

    In most cases the kernel coordinates will be (r, r) -- the center of the kernel. That is,
    unless the kernel overlaps the edge of the matrix. In this edge case (it's a pun, get it?)
    the local coordinates shift by however much the kernel goes off the edge of the matrix.

    For our use cases, the given coordinates will always be contained inside the matrix, so
    the bottom and right most coordinates will remain unchanged. The relative coordinates will
    only change if the kernel overlaps the top or left boundary, because the coordinates are
    relative to the upper left corner of the kernel.

    :param coords: The absolute matrix (x, y) coordinates.
    :param r: The kernel square radius.
    """
    x, y = coords
    return min(radius, x), min(radius, y)


class ACA:
    """An implementation of the Ant Clustering Algorithm (ACA).

    The ACA clusters objects on a 2D grid.

    The grid stores colored objects in cells indexed via (x, y) coordinates. The
    objects' colors are stored as a positive integer, with 0 representing an
    empty cell.

    The grid also maintains a list of Ants which can pick up objects in the cells
    and move them to another cell.

    ACA implements an ACA.update() function, which runs one iteration of the ACA
    algorithm and yields the wrapped numpy grid object. It is important that this
    object not be modified between iterations, as it is a reference (to avoid
    copies with every iteration) to the wrapped grid object.

    ACA also implements an ACA.run(iters) function, which runs the given number
    of iterations, and optionally animates the clustering progress.
    """

    def __init__(self, grid_size, colors, num_ants, radius, k1, k2):
        """Initialize a random Grid and set up for proceding with the ACA algorithm.

        :param grid_size: A (width, height) tuple specifying the grid size.
        :param colors: A list containing the number of objects of each color to
        initialize the grid with. E.g., using [10, 20] will initialize 10 objects
        of the first color, and 20 of the second.
        :param num_ants: The number of ants to use.
        :param radius: Each ant's sight distance.
        :param k1: A tunable parameter for the pickup probability.
        :param k2: A tunable parameter for the dropoff probability.
        """
        self.width, self.height = grid_size
        self.num_ants = num_ants
        self.radius = radius
        self.k1 = k1
        self.k2 = k2
        self.colors = colors
        self.grid = None
        self.init_grid()
        self.ants = None
        self.init_ants()

    def init_grid(self):
        """Get a randomly initialized grid of objects.

        The grid is a 2D array of (color, ant) tuples, where color is
        0 - unoccupied by an object
        1 - occupied by a red object
        2 - occupied by a blue object
        and so on.

        The ant value is either 0 or 1 to indicate the presence of an ant in the
        cell. The corresponding Ant object in the self.ants list is responsible
        for indicating whether or not the Ant is carrying the colored item or not.

        The Ant object is also responsible for managing the ant value when it
        moves from cell to cell.
        """
        num_objects = sum(self.colors)
        assert (
            num_objects <= self.width * self.height
        ), "Too many colored objects to fit in the grid."
        # Use 1D arrays because that's all I can generate random indices for.
        object_grid = np.zeros((self.height * self.width, 2), dtype=int)
        random_indices = np.random.choice(self.height * self.width, num_objects, replace=False)

        start = 0
        # 0 represents unoccupied, so start color indexing at 1.
        for color, num_color in enumerate(self.colors, start=1):
            object_grid[random_indices[start : start + num_color], 0] = color
            start += num_color

        self.grid = object_grid.reshape((self.width, self.height, 2))

    def init_ants(self):
        """Get a randomly initialized array of ants.

        Each ant is a (x, y, load) tuple, where the load is an integer representing
        the color of the object the ant is carrying. 0 represents an unloaded ant,
        and 1, 2, 3, ... represent different colors of objects.
        """
        assert self.num_ants <= self.width * self.height, "Too many ants to fit in the grid."
        # This is an array of indices into the grid as if it were 1D.
        indices = np.random.choice(self.height * self.width, self.num_ants, replace=False)
        ants = []
        for i in indices:
            x = i % self.width
            y = i // self.width
            ant = Ant(x, y, self.k1, self.k2)
            ants.append(ant)
            self.grid[x, y, 1] = 1

        self.ants = ants

    def update(self):
        """Perform one iteration of the ACA."""
        for ant in self.ants:
            kernel = kernel_center(self.grid, ant.x, ant.y, self.radius)
            ant.update(kernel, *kernel_coords((ant.x, ant.y), self.radius))

    def drop_items(self):
        """Force every ant to drop their items."""
        for ant in self.ants:
            k = kernel_center(self.grid, ant.x, ant.y, self.radius)
            k_x, k_y = kernel_coords((ant.x, ant.y), self.radius)
            ant.dropoff(k, k_x, k_y)
            ant.update_location(k, k_x, k_y)

    def run(self, iters, period=None, animate=False):
        """Run the specified number of iterations of the ACA.

        :param iters: The number of iterations to run the ACA.
        :param period: How often to force the ants to drop all of their items.
        :param animate: Whether or not to plot the progress of the ACA, defaults to False
        :returns: The grid after the final iteration.
        """
        for i in range(iters):
            self.update()

            if animate and i % 50 == 0:
                self.plot(blocking=False)

            # Every so often, drop every load and make a position update without a load update.
            if period is not None and i % period == 0:
                self.drop_items()

        self.drop_items()

    def plot(self, blocking=False):
        """Plot the grid.

        :param blocking: If blocking is True, display the plot GUI, and wait for
        the user to exit. Otherwise, update the existing plot without waiting.
        """
        colors = ["white", "red", "blue", "green", "orange", "purple", "brown", "pink"]
        cmap = ListedColormap(colors)

        if not blocking:
            plt.ion()

        # Start a new figure each iteration, because in live plotting mode, it takes
        # exponentially longer for each frame because it's adding a new image to an
        # existing figure. I think.
        plt.clf()
        # Don't be an idiot. Set the largest value to the most amount of colors supported.
        # If more colors are provided, then fail silently (shame on me).
        plt.imshow(self.grid[:, :, 0], cmap=cmap, vmin=0, vmax=len(colors) - 1)
        plt.title("Ant Clustering Results")
        plt.axis("off")

        if blocking:
            plt.ioff()
            title = f"aca-w{self.width}-h{self.height}-o{sum(self.colors)}-c{len(self.colors)}-a{self.num_ants}-r{self.radius}-k1{self.k1}-k2{self.k2}".replace(
                ".", "_"
            )
            plt.savefig(title + ".eps")
            plt.show()
        else:
            plt.pause(0.00000001)
