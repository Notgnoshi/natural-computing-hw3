# natural-computing-hw3

Ant clustering and particle optimization

---

The paper can be built with the given [makefile](paper/Makefile).

## Ant Clustering

The [`prob1.py`](prob1.py) script has the following usage

```shell
$ ./prob1.py --help
usage: prob1.py [-h] [--width WIDTH] [--height HEIGHT] [--ants ANTS]
                [--iterations ITERATIONS] [--radius RADIUS] [--k1 K1]
                [--k2 K2] [--reset-period RESET_PERIOD] [--animate]
                [--colors COLORS [COLORS ...]] [--headless]

Cluster objects with Ants.

optional arguments:
  -h, --help            show this help message and exit
  --width WIDTH, -x WIDTH
                        The width of the grid to cluster.
  --height HEIGHT, -y HEIGHT
                        The height of the grid to cluster.
  --ants ANTS, -s ANTS  The number of ants to use.
  --iterations ITERATIONS, -i ITERATIONS
                        The number of iterations to run.
  --radius RADIUS       The ant's perceiveable radius.
  --k1 K1               The k1 tunable parameter
  --k2 K2               The k2 tunable parameter
  --reset-period RESET_PERIOD, -p RESET_PERIOD
                        Force ants to drop off their items every P iterations.
                        -1 to disable.
  --animate, -a         Animate the clustering progress.
  --colors COLORS [COLORS ...]
                        The number of objects to use for each color.
  --headless            Run in headless mode for profiling.
```

An example usage is given below

```shell
$ ./prob1.py -x 100 -y 100 --colors 50 50 -i 1000 --ants 100 --radius 3 --animate
Namespace(animate=True, ants=100, colors=[50, 50], headless=False, height=100, iterations=1000, k1=0.1, k2=0.1, radius=3, reset_period=-1, width=100)
```

## Particle Swarm Optimization

The [`prob2.py`](prob2.py) script has the following usage.

```shell
$ ./prob2.py --help
usage: prob2.py [-h] [--xmin XMIN] [--xmax XMAX] [--ac1 AC1] [--ac2 AC2]
                [--vmin VMIN] [--vmax VMAX] [--particles PARTICLES]
                [--iterations ITERATIONS] [--animate] [--headless]

Optimize a function with a particle swarm.

optional arguments:
  -h, --help            show this help message and exit
  --xmin XMIN           The lower domain boundary.
  --xmax XMAX           The upper domain boundary.
  --ac1 AC1             Acceleration constant for the particle history
                        component.
  --ac2 AC2             Acceleration constant for the swarm history component.
  --vmin VMIN           The particle velocity lower bound.
  --vmax VMAX           The particle velocity upper bound.
  --particles PARTICLES, -p PARTICLES
                        The number of particles in the swarm.
  --iterations ITERATIONS, -i ITERATIONS
                        The number of iterations to use.
  --animate             Animate the swarm's progress.
  --headless            A headless mode for profiling.
```

An example usage is shown below

```shell
$ ./prob2.py --particles 5 --ac1 0.1 --ac2 0.1 -i 100
Namespace(ac1=0.1, ac2=0.1, animate=False, headless=False, iterations=100, particles=5, vmax=0.1, vmin=-0.1, xmax=1, xmin=0)
f(0.1008) = 0.9995
optimum: 0.1007805032995858
f(0.0999) = 1.0000
optimum: 0.09989047564149028
f(0.1000) = 1.0000
optimum: 0.09999808547123037
```
