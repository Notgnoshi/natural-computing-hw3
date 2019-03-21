from .grid import Grid


class ACA:
    def __init__(self, grid_size, num_ants, iters, radius, k1, k2, animate, colors):
        self.grid = Grid(grid_size, num_ants, radius, k1, k2, colors)
        self.animate = animate
        self.iters = iters

    def runAlgorithm(self):
        raise NotImplementedError
