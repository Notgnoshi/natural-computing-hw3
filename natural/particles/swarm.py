import numpy as np


class Swarm:
    def __init__(self, particles, AC1, AC2, xmin, xmax, vmin, vmax):
        self.num_particles = particles
        self.AC1, self.AC2 = AC1, AC2
        self.xmin, self.xmax = xmin, xmax
        self.vmin, self.vmax = vmin, vmax

    def optimize(self, func, iters):
        return self.xmin
