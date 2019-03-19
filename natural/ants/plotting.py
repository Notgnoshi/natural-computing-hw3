import matplotlib.pyplot as plt
from matplotlib import colors


def plot_grid(grid, blocking=False):
    """Plot the given grid of objects.

    :param grid: The grid to plot.
    :param blocking: Whether or not to plot in interactive mode, optional.
    """
    width, height = grid.shape
    cmap = colors.ListedColormap(["white", "blue", "red"])

    # Start a new figure each iteration, because in live plotting mode, it takes
    # exponentially longer for each frame because it's adding a new image to an
    # existing figure. I think.
    plt.clf()
    plt.imshow(grid, cmap=cmap)
    plt.title("")
    plt.axis("off")

    if blocking:
        plt.show()
    else:
        # TODO: Figure out how to implement nonblocking plotting from not a
        # Jupyter notebook.
        raise NotImplementedError
