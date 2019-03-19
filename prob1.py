#!/usr/bin/env python3
from natural.ants import init_grid, plot_grid
from natural.ants import AntClustering


GRID_SIZE = (200, 200)  # (width, height)
REDS = 100
BLUES = 100
ANTS = 500


def main():
    grid = init_grid(GRID_SIZE, colors=(REDS, BLUES))
    plot_grid(grid, blocking=True)

    alg = AntClustering(grid)
    clustering = alg.cluster(iters=100, ants=ANTS, neighborhood_size=4, k1=0.1, k2=0.1)
    plot_grid(clustering, blocking=True)


if __name__ == "__main__":
    main()
