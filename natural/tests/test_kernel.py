import unittest

import numpy as np

import natural.ants

# Name mangling == private members. Didn't you know?
kernel = natural.ants.ACA._ACA__kernel


class KernelTest(unittest.TestCase):
    def test_reference(self):
        m = np.zeros((3, 3), dtype=int)
        # Get the upper left 2x2 kernel from the given matrix.
        k = kernel(m, x1=0, y1=0, x2=1, y2=1)
        k[0, 0] = 1

        # Make sure updating a kernel updates the underlying matrix.
        self.assertEqual(m[0, 0], 1)

    def test_same_size(self):
        m = np.arange(25).reshape((5, 5))
        # Get a kernel the same size as the matrix.
        k = kernel(m, x1=0, y1=0, x2=4, y2=4)
        self.assertEqual(m.shape, k.shape)
        self.assertTrue(np.all(m == k))

    def test_smallest(self):
        m = np.arange(25).reshape((5, 5))
        # Get the smallest possible kernel.
        k = kernel(m, x1=0, y1=0, x2=0, y2=0)
        self.assertEqual(k.shape, (1, 1))
        self.assertEqual(k[0, 0], m[0, 0])
        self.assertEqual(k[-1, -1], m[-1, -1])

    def test_contained(self):
        m = np.arange(25).reshape((5, 5))
        # Get a kernel fully contained within the matrix.
        k = kernel(m, x1=1, y1=1, x2=3, y2=3)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], m[1, 1])
        self.assertEqual(k[-1, -1], m[3, 3])

    def test_top(self):
        m = np.arange(25).reshape((5, 5))
        # Hang off the top of the matrix
        k = kernel(m, x1=0, y1=-2, x2=2, y2=2)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], m[0, 0])
        self.assertEqual(k[-1, -1], m[2, 2])

    def test_left(self):
        m = np.arange(25).reshape((5, 5))
        # Hang off the left of the matrix
        k = kernel(m, x1=-2, y1=0, x2=2, y2=2)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], m[0, 0])
        self.assertEqual(k[-1, -1], m[2, 2])

    def test_bottom(self):
        m = np.arange(25).reshape((5, 5))
        # Hang off the bottom of the matrix
        k = kernel(m, x1=0, y1=4, x2=1, y2=5)
        self.assertEqual(k.shape, (2, 1))
        self.assertEqual(k[0, 0], m[0, 4])
        self.assertEqual(k[-1, -1], m[1, 4])

    def test_right(self):
        m = np.arange(25).reshape((5, 5))
        # Hang off the right of the matrix
        k = kernel(m, x1=3, y1=0, x2=6, y2=2)
        self.assertEqual(k.shape, (2, 3))
        self.assertEqual(k[0, 0], m[3, 0])
        self.assertEqual(k[-1, -1], m[4, 2])

    def test_combined(self):
        m = np.arange(25).reshape((5, 5))

        # Hang off the top left of the matrix
        k = kernel(m, x1=-1, y1=-1, x2=2, y2=2)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], m[0, 0])
        self.assertEqual(k[-1, -1], m[2, 2])

        # Hang off the bottom right of the matrix
        k = kernel(m, x1=3, y1=3, x2=5, y2=5)
        self.assertEqual(k.shape, (2, 2))
        self.assertEqual(k[0, 0], m[3, 3])
        self.assertEqual(k[-1, -1], m[4, 4])
