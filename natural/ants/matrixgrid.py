from .grid import Grid


class MatrixGrid(Grid):
    def __init__(self, grid_size, num_ants, radius, k1, k2, colors):
        self.width, self.height = grid_size
        self.num_ants = num_ants
        self.radius = radius
        self.k1 = k1
        self.k2 = k2
        self.colors = colors
        self.grid = self.init_grid()
        self.ants = self.init_ants()

    def init_grid(self):
        raise NotImplementedError

    def init_ants(self):
        raise NotImplementedError

    def getkernel(self, x, y):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError

    def plot(self, blocking=False):
        raise NotImplementedError
