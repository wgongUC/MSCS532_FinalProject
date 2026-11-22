# Name: Weevern Gong
# Project Title: MSCS532_FinalProject
# Description: Checks the two searches on small inputs and boundary cases.

# Test explanation: Compare complete sets of pairs rather than just counts.
# Two different sets can contain the same number of pairs.

import random
import unittest
from neighbor_search import all_pairs, grid_pairs


class NeighborSearchTests(unittest.TestCase):
    def assert_matches(self, points, radius):
        # Use all pairs as the reference and compare the number of distance
        # checks. The two searches share the same distance test, so agreement
        # does not independently verify the cutoff rule.
        expected, checks = all_pairs(points, radius)
        actual, reduced = grid_pairs(points, radius)
        self.assertEqual(expected, actual)
        self.assertLessEqual(reduced, checks)

    def test_empty_and_single(self):
        # Neither input has two indices to compare.
        for points in ([], [(0, 0, 0)]):
            self.assert_matches(points, 1)

    def test_duplicate_coordinates(self):
        # Points with the same coordinates still have distinct input indices.
        self.assert_matches([(0, 0, 0)] * 8, 1)

    def test_cell_boundary_and_cutoff(self):
        # This input includes a close pair across a cell boundary, a pair
        # exactly one radius apart, and a pair just outside that radius.
        self.assert_matches([(0.99, 0, 0), (1.01, 0, 0), (0, 0, 0),
                             (1, 0, 0), (1.000001, 0, 0)], 1)

    def test_negative_coordinates(self):
        # The negative boundary checks that the two searches agree on pairs
        # on either side of a negative cell edge.
        self.assert_matches([(-1.01, 0, 0), (-0.99, 0, 0), (0, 0, 0)], 1)

    def test_random_clouds(self):
        # A fixed seed repeats the same cases while varying radius and size.
        rng = random.Random(532)
        for radius in (0.1, 0.5, 2.0):
            for n in (2, 17, 100):
                self.assert_matches([tuple(rng.uniform(-2, 2) for _ in range(3))
                                     for _ in range(n)], radius)

    def test_all_within_radius(self):
        # Here all points are close enough to match, so pruning cannot
        # remove those distance checks.
        self.assert_matches([(i / 100, 0, 0) for i in range(20)], 1)

    def test_invalid_input(self):
        # Both methods should reject the same invalid radii and coordinates.
        for fn in (all_pairs, grid_pairs):
            for radius in (0, -1, float('inf'), float('nan')):
                with self.assertRaises(ValueError):
                    fn([], radius)
            with self.assertRaises(ValueError):
                fn([(0, float('nan'), 0)], 1)


if __name__ == '__main__':
    unittest.main()
