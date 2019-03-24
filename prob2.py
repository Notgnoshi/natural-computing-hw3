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
        "--vmin", type=float, default=0.01, help="The particle velocity lower bound."
    )
    parser.add_argument(
        "--vmax", type=float, default=1.0, help="The particle velocity upper bound."
    )

    parser.add_argument(
        "--particles", "-p", type=int, default=100, help="The number of particles in the swarm."
    )
    parser.add_argument(
        "--iterations", "-i", type=int, default=100, help="The number of iterations to use."
    )

    parser.add_argument(
        "--headless", action="store_true", default=False, help="A headless mode for profiling."
    )

    return parser.parse_args()


def func(x):
    return 2 ** (-2 * ((x - 0.1) / 0.9) ** 2) * np.sin(5 * np.pi * x) ** 6


def main(args):
    print(args)

    swarm = Swarm(
        particles=args.particles,
        AC1=args.ac1,
        AC2=args.ac2,
        xmin=args.xmin,
        xmax=args.xmax,
        vmin=args.vmin,
        vmax=args.vmax,
    )
    opt = swarm.optimize(func, iters=args.iterations)
    print("optimum:", opt)

    if not args.headless:
        x = np.linspace(args.xmin, args.xmax, 200)

        plt.plot(x, func(x), label="$f(x)$")
        plt.plot(opt, func(opt), ".", label=r"$\hat x$")

        plt.title("Particle Swarm Results")
        plt.xlabel("$x$")
        plt.ylabel("$f(x)$")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    main(parse_args())
