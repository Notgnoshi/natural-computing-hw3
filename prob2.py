#!/usr/bin/env python3
import argparse

import matplotlib.pyplot as plt
import numpy as np

from natural.particles import Swarm

XMIN = 0
XMAX = 1
AC1 = AC2 = 2.05


def parse_args():
    parser = argparse.ArgumentParser(description="Optimize a function with a particle swarm.")

    parser.add_argument("--xmin", type=float, default=XMIN, help="The lower domain boundary.")
    parser.add_argument("--xmax", type=float, default=XMAX, help="The upper domain boundary.")

    parser.add_argument(
        "--ac1",
        type=float,
        default=AC1,
        help="Acceleration constant for the particle history component.",
    )
    parser.add_argument(
        "--ac2",
        type=float,
        default=AC2,
        help="Acceleration constant for the swarm history component.",
    )

    parser.add_argument(
        "--vmin", type=float, default=-0.1, help="The particle velocity lower bound."
    )
    parser.add_argument(
        "--vmax", type=float, default=+0.1, help="The particle velocity upper bound."
    )

    parser.add_argument(
        "--particles", "-p", type=int, default=100, help="The number of particles in the swarm."
    )
    parser.add_argument(
        "--iterations", "-i", type=int, default=100, help="The number of iterations to use."
    )

    parser.add_argument(
        "--animate", action="store_true", default=False, help="Animate the swarm's progress."
    )
    parser.add_argument(
        "--headless", action="store_true", default=False, help="A headless mode for profiling."
    )

    return parser.parse_args()


def func(x):
    return 2 ** (-2 * ((x - 0.1) / 0.9) ** 2) * np.sin(5 * np.pi * x) ** 6


def main(args):
    print(args)


    rows = 3
    _, axes = plt.subplots(rows, 2, figsize=(8, 8))
    axes = iter(axes.flatten())
    for _ in range(rows):
        swarm = Swarm(
            particles=args.particles,
            AC1=args.ac1,
            AC2=args.ac2,
            xmin=args.xmin,
            xmax=args.xmax,
            vmin=args.vmin,
            vmax=args.vmax,
        )
        # NOTE: Repeated calls to optimize does not reset the swarm.
        opt, bests, means = swarm.optimize(
            func, iters=args.iterations, animate=args.animate and not args.headless
        )
        print("optimum:", opt)

        # TODO: Animation and results summary don't play well together.
        if not args.headless and not args.animate:
            ax = next(axes)
            ax.plot(bests, label="Swarm Best")
            ax.plot(means, label="Swarm Mean")
            ax.set_title("Swarm Behavior Over Time")
            ax.set_xlabel("iteration")
            ax.set_ylabel("$x$")
            ax.set_ylim(args.xmin-0.1, args.xmax+0.1)
            ax.legend()

            ax = next(axes)
            x = np.linspace(args.xmin, args.xmax, 500)
            ax.plot(x, func(x), label="$f(x)$")
            ax.plot(opt, func(opt), "r.", label=r"$\hat x$")
            ax.plot(swarm.particles, func(swarm.particles), ".", markersize=3, label="$swarm$")
            ax.set_title("Particle Swarm Results")
            ax.set_xlabel("$x$")
            ax.set_ylabel("$f(x)$")
            ax.legend()

    if not args.headless and not args.animate:
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main(parse_args())
