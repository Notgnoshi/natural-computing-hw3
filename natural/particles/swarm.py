import matplotlib.pyplot as plt
import numpy as np


class Swarm:
    """Optimize a function of one variable using a particle swarm."""

    def __init__(self, particles, AC1, AC2, xmin, xmax, vmin, vmax):
        """Construct a particle swarm with a number of tunable parameters.

        :param particles: The number of particles in the swarm.
        :param AC1: The acceleration constant for the particle's best position component.
        :param AC2: The acceleration constant for the swarm's best position component.
        :param xmin, xmax: The domain bounds to optimize over.
        :param vmin, vmax: The velocity bounds on each particle.
        """
        self.num_particles = particles
        self.AC1, self.AC2 = AC1, AC2
        self.xmin, self.xmax = xmin, xmax
        self.vmin, self.vmax = vmin, vmax

        self.particles = np.random.uniform(low=xmin, high=xmax, size=particles)
        self.velocities = np.random.uniform(low=vmin, high=vmax, size=particles)
        # Each particle's best historical position.
        self.history = self.particles.copy()
        # The entire swarm's best historical position.
        self.best = None

    def update(self, func):
        """Perform one iteration of optimization."""
        for i, x in enumerate(self.particles):
            if func(x) > func(self.history[i]):
                self.history[i] = x
            if func(x) > func(self.best):
                self.best = x

            # NOTE: The size is the number of dimensions of a single particle.
            phi1 = np.random.uniform(low=0, high=self.AC1, size=1)
            phi2 = np.random.uniform(low=0, high=self.AC2, size=1)

            # Update the particle's velocity.
            self.velocities[i] += phi1 * (self.history[i] - x) + phi2 * (self.best - x)
            # Clip the velocity between the allowable bounds.
            # NOTE: Must be done elementwise if x is more than one dimension.
            self.velocities[i] = min(self.vmax, max(self.vmin, self.velocities[i]))
            self.particles[i] += self.velocities[i]
            self.particles[i] = min(self.xmax, max(self.xmin, self.particles[i]))

    def optimize(self, func, iters, animate=False):
        """Optimize the given function for `iters` iterations."""
        b = np.argmax(func(self.particles))
        self.best = self.particles[b]

        for i in range(iters):
            print("\rf({:.04f}) = {:.04f}".format(self.best, func(self.best)), end="")
            self.update(func)

            if animate and i % 5 == 0:
                self.plot(func, blocking=False)

        print()
        return self.best

    def plot(self, func, blocking=False):
        """Plot the swarm's progress on the given function.

        :param func: The function to plot
        :param blocking: Whether or not to plot in interactive mode, defaults to False
        :param blocking: bool, optional
        """
        if not blocking:
            plt.ion()

        # Start a new figure each iteration, because in live plotting mode, it takes
        # exponentially longer for each frame because it's adding a new image to an
        # existing figure. I think.
        plt.clf()
        x = np.linspace(self.xmin, self.xmax, 500)
        plt.plot(x, func(x), label="$f(x)$")
        plt.plot(self.best, func(self.best), "r.", label=r"$\hat x$")
        plt.plot(self.particles, func(self.particles), ".", markersize=3, label=r"$swarm$")

        plt.title("Particle Swarm Results")
        plt.xlabel("$x$")
        plt.ylabel("$f(x)$")
        plt.legend()
        plt.show()

        if blocking:
            plt.ioff()
            plt.show()
        else:
            # WTF. Why does black add the number separators here, but not in the other class?
            plt.pause(0.00000001)
