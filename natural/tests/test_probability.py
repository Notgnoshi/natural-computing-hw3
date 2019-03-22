import unittest

import numpy as np

import natural.ants
from natural.ants import Ant

# Name mangling == private members. Didn't you know?
perceived_fraction = natural.ants.Ant.perceived_fraction
k1 = 0.5
k2 = 0.5
ant = Ant(5, 5, k1, k2)

class ProbabilityFunctionTest(unittest.TestCase):
    def test_all_colors(self):
        # Kernel with no colors
        kernel = np.zeros((5,5), dtype=int)

        kernel[0,:] = 2
        kernel[:,4] = 3
        kernel[4,:] = 3
        kernel[1,:] = 4

        self.assertEqual(ant.perceived_fraction(kernel, 1), 0)
        self.assertEqual(ant.perceived_fraction(kernel, 2), (4/25))
        self.assertEqual(ant.perceived_fraction(kernel, 3), (8/25))
        self.assertEqual(ant.perceived_fraction(kernel, 4), (5/25))

    def test_pickup_probability_high(self):
        kernel = np.zeros((5,5), dtype=int)
        kernel[0, 0] = 1

        f = ant.perceived_fraction(kernel, 1)
        self.assertAlmostEqual(ant.pickup_probability(f), 0.8573388203017831)

    def test_pickup_probability_low(self):
        kernel = np.ones((5,5), dtype=int)
        kernel[0, 0] = 0

        f = ant.perceived_fraction(kernel, 1)
        self.assertAlmostEqual(ant.pickup_probability(f), 0.11728279226871832)

    def test_dropoff_probabilty_low(self):
        kernel = np.zeros((5,5), dtype=int)
        kernel[0, 0] = 1
        
        f = ant.perceived_fraction(kernel, 1)
        self.assertAlmostEqual(ant.dropoff_probability(f), (1/25)*2)

    def test_dropoff_probabilty_high(self):
        kernel = np.ones((5,5), dtype=int)
        kernel[0, 0] = 0
        
        f = ant.perceived_fraction(kernel, 1)
        self.assertAlmostEqual(ant.dropoff_probability(f), 1)

