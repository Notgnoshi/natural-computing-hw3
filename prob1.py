#!/usr/bin/env python3
import argparse

from natural.ants import ACA

# The default values given by the homework assignment.
GRID_SIZE = (200, 200)  # (width, height)
REDS = 100
BLUES = 100
ANTS = 500


def parse_args():
    parser = argparse.ArgumentParser(description="Cluster objects with Ants.")
    parser.add_argument(
        "--width", "-x", type=int, default=GRID_SIZE[0], help="The width of the grid to cluster."
    )
    parser.add_argument(
        "--height", "-y", type=int, default=GRID_SIZE[1], help="The height of the grid to cluster."
    )
    parser.add_argument("--ants", "-s", type=int, default=ANTS, help="The number of ants to use.")
    parser.add_argument(
        "--iterations", "-i", type=int, default=100, help="The number of iterations to run."
    )
    parser.add_argument("--radius", type=int, default=1, help="The ant's perceiveable radius.")
    parser.add_argument("--k1", type=float, default=0.1, help="The k1 tunable parameter")
    parser.add_argument("--k2", type=float, default=0.1, help="The k2 tunable parameter")
    parser.add_argument("--reset-period", "-p", type=int, default=-1, help="Force ants to drop off their items every P iterations. -1 to disable.")
    parser.add_argument(
        "--animate",
        "-a",
        action="store_true",
        default=False,
        help="Animate the clustering progress.",
    )
    parser.add_argument(
        "--colors",
        nargs="+",
        type=int,
        default=[REDS, BLUES],
        help="The number of objects to use for each color.",
    )
    # Enable a headless mode so a profiler doesn't profile matplotlib (eww)
    parser.add_argument(
        "--headless", action="store_true", default=False, help="Run in headless mode for profiling."
    )

    return parser.parse_args()


def main(args):
    print(args)
    if args.reset_period < 0:
        args.reset_period = None
    elif args.reset_period > args.iterations:
        print("Reset period must be less than the number of iterations.")
        args.reset_period = None

    alg = ACA((args.width, args.height), args.colors, args.ants, args.radius, args.k1, args.k2)
    # Only animate when the flag is set, and not running in headless mode.
    alg.run(args.iterations, period=args.reset_period, animate=args.animate and not args.headless)

    if not args.headless:
        # TODO: Plot the initial and end grid on the same window.
        alg.plot(blocking=True)


if __name__ == "__main__":
    main(parse_args())
