import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


def plot_grid(grid, blocking=False):
    """Plot the given grid of objects.

    :param grid: The grid to plot.
    :param blocking: Whether or not to plot in interactive mode, optional.
    """
    width, height = grid.shape
    colors = ["white", "red", "blue", "green", "orange", "purple", "brown", "pink"]
    cmap = ListedColormap(colors)

    # Start a new figure each iteration, because in live plotting mode, it takes
    # exponentially longer for each frame because it's adding a new image to an
    # existing figure. I think.
    plt.clf()
    # Don't be an idiot. Set the largest value to the most amount of colors supported.
    # If more colors are provided, then fail silently (shame on me).
    plt.imshow(grid, cmap=cmap, vmin=0, vmax=len(colors) - 1)
    plt.title("")
    plt.axis("off")

    if blocking:
        plt.show()
    else:
        # TODO: Figure out how to implement nonblocking plotting from not a
        # Jupyter notebook.
        raise NotImplementedError
