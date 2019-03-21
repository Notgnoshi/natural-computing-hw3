from natural.abc import ABCMeta, abstractattribute, abstractmethod


class Grid(metaclass=ABCMeta):
    """Abstract base class for a Grid object.

    The Grid stores colored objects in cells indexed via (x, y) coordinates. The
    objects' colors are stored as a positive integer, with 0 representing an
    empty cell.

    The Grid also maintains a list of Ants which can pick up objects in the cells
    and move them to another cell.
    """

    @abstractattribute
    def grid_size(self):
        """The (width, height) tuple describing the grid dimensions."""

    @abstractattribute
    def num_ants(self):
        """The number of ants stored in the Grid."""

    @abstractattribute
    def radius(self):
        """The distance each ant can see."""

    @abstractattribute
    def k1(self):
        """The tunable parameter for the object pickup."""

    @abstractattribute
    def k2(self):
        """The tunable parameter for the object dropoff."""

    @abstractattribute
    def colors(self):
        """The list containing the number of each color to use.

        E.g. The list [20, 50] means to use two colors, with 20 objects of the
        first color, and 50 objects of the second color.
        """

    @abstractattribute
    def ants(self):
        """The array of ants on the grid."""

    @abstractmethod
    def init_grid(self):
        """Initialize the wrapped internal grid object."""

    @abstractmethod
    def init_ants(self):
        """Initialize the Ant array."""

    @abstractmethod
    def getkernel(self, x, y):
        """Get the kernel centered at the given coordinates."""

    @abstractmethod
    def update(self):
        """Perform one iteration of the ACA.

        TODO: Our original thought was to yield the grid with every iteration.
        However, we have abstracted away the wrapped grid object so that it could
        be a matrix *or* a hash table. Thus we cannot yield the grid with each
        iteration.
        """

    @abstractmethod
    def plot(self, blocking=False):
        """Plot the grid.

        :param blocking: If blocking is True, display the plot GUI, and wait for
        the user to exit. Otherwise, update the existing plot without waiting.
        """
