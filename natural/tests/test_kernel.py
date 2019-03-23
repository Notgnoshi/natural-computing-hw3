import unittest

import numpy as np

import natural.ants

# Name mangling == private members. Didn't you know?
kernel = natural.ants.ACA._ACA__kernel
kernel_center = natural.ants.ACA._ACA__kernel_center


class KernelTest(unittest.TestCase):
    def setUp(self):
        self.m = np.arange(25).reshape((5, 5))

    def test_reference(self):
        m = np.zeros((3, 3), dtype=int)
        # Get the upper left 2x2 kernel from the given matrix.
        k = kernel(m, x1=0, y1=0, x2=1, y2=1)
        k[0, 0] = 1

        # Make sure updating a kernel updates the underlying matrix.
        self.assertEqual(m[0, 0], 1)

    def test_same_size(self):
        # Get a kernel the same size as the matrix.
        k = kernel(self.m, x1=0, y1=0, x2=4, y2=4)
        self.assertEqual(self.m.shape, k.shape)
        self.assertTrue(np.all(self.m == k))

    def test_smallest(self):
        # Get the smallest possible kernel.
        k = kernel(self.m, x1=0, y1=0, x2=0, y2=0)
        self.assertEqual(k.shape, (1, 1))
        self.assertEqual(k[0, 0], self.m[0, 0])
        self.assertEqual(k[-1, -1], self.m[0, 0])

    def test_contained(self):
        # Get a kernel fully contained within the matrix.
        k = kernel(self.m, x1=1, y1=1, x2=3, y2=3)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], self.m[1, 1])
        self.assertEqual(k[-1, -1], self.m[3, 3])

    def test_top(self):
        # Hang off the top of the matrix
        k = kernel(self.m, x1=0, y1=-2, x2=2, y2=2)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], self.m[0, 0])
        self.assertEqual(k[-1, -1], self.m[2, 2])

    def test_left(self):
        # Hang off the left of the matrix
        k = kernel(self.m, x1=-2, y1=0, x2=2, y2=2)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], self.m[0, 0])
        self.assertEqual(k[-1, -1], self.m[2, 2])

    def test_bottom(self):
        # Hang off the bottom of the matrix
        k = kernel(self.m, x1=0, y1=4, x2=1, y2=5)
        self.assertEqual(k.shape, (2, 1))
        self.assertEqual(k[0, 0], self.m[0, 4])
        self.assertEqual(k[-1, -1], self.m[1, 4])

    def test_right(self):
        # Hang off the right of the matrix
        k = kernel(self.m, x1=3, y1=0, x2=6, y2=2)
        self.assertEqual(k.shape, (2, 3))
        self.assertEqual(k[0, 0], self.m[3, 0])
        self.assertEqual(k[-1, -1], self.m[4, 2])

    def test_combined(self):
        # Hang off the top left of the matrix
        k = kernel(self.m, x1=-1, y1=-1, x2=2, y2=2)
        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], self.m[0, 0])
        self.assertEqual(k[-1, -1], self.m[2, 2])

        # Hang off the bottom right of the matrix
        k = kernel(self.m, x1=3, y1=3, x2=5, y2=5)
        self.assertEqual(k.shape, (2, 2))
        self.assertEqual(k[0, 0], self.m[3, 3])
        self.assertEqual(k[-1, -1], self.m[4, 4])


class KernelCenterTest(unittest.TestCase):
    def setUp(self):
        self.m = np.arange(25).reshape((5, 5))

    def test_contained(self):
        k = kernel_center(self.m, x=2, y=2, r=1)

        self.assertEqual(k.shape, (3, 3))
        self.assertEqual(k[0, 0], self.m[1, 1])
        self.assertEqual(k[-1, -1], self.m[3, 3])

    def test_contains(self):
        k = kernel_center(self.m, x=2, y=2, r=3)
        self.assertEqual(k.shape, self.m.shape)
        self.assertTrue(np.all(k == self.m))

        k = kernel_center(self.m, x=2, y=2, r=4)
        self.assertEqual(k.shape, self.m.shape)
        self.assertTrue(np.all(k == self.m))

    def test_left(self):
        k = kernel_center(self.m, x=0, y=0, r=1)
        self.assertEqual(k.shape, (2, 2))
        self.assertEqual(k[0, 0], self.m[0, 0])
        self.assertEqual(k[-1, -1], self.m[1, 1])

    def test_right(self):
        k = kernel_center(self.m, x=4, y=4, r=1)
        self.assertEqual(k.shape, (2, 2))
        self.assertEqual(k[0, 0], self.m[3, 3])
        self.assertEqual(k[-1, -1], self.m[4, 4])

    def test_smallest(self):
        k = kernel_center(self.m, x=2, y=2, r=0)
        self.assertEqual(k.shape, (1, 1))
        self.assertEqual(k[0, 0], self.m[2, 2])
