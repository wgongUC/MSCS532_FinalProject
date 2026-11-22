# Name: Weevern Gong
# Project Title: MSCS532_FinalProject
# Description: Finds nearby point pairs using two different search methods.

# Spatial indexing explanation: A spatial grid lets the search skip points in cells
# that are too far apart to hold a match. Use the all-pairs search as the
# baseline for matching pairs and distance-check counts.

"""Exact fixed-radius pair search using all pairs or a spatial hash grid.

This educational prototype adapts the study's unnecessary-comparison idea.
It is not a reproduction of OpenFOAM physics or a parallel HPC application.
"""
from itertools import product
from math import floor, isfinite


def validate(points, radius):
    # Both methods check the same input so the comparison uses the same rules.
    if not isfinite(radius) or radius <= 0:
        raise ValueError("radius must be finite and positive")
    if any(len(p) != 3 or not all(isfinite(x) for x in p) for p in points):
        raise ValueError("points must contain three finite coordinates")


def close(a, b, r2):
    # Comparing squared distances removes the need for a square root.
    # Using <= keeps a pair whose distance is exactly the radius.
    return sum((x - y) ** 2 for x, y in zip(a, b)) <= r2


def all_pairs(points, radius):
    """Return exact unordered index pairs and number of distance evaluations."""
    validate(points, radius)
    pairs, checks = set(), 0
    r2 = radius * radius
    # Only compare each point with later points. This counts each unordered
    # pair once and avoids comparing a point with itself.
    for i, a in enumerate(points):
        for j in range(i + 1, len(points)):
            checks += 1
            if close(a, points[j], r2):
                pairs.add((i, j))
    return pairs, checks


def grid_pairs(points, radius):
    """Build a fresh radius-width grid and inspect 27 surrounding cells.

    Negative coordinates use floor, not truncation. j > i prevents duplicate
    pair evaluation. Neighbor cells are essential for cross-boundary pairs.
    Grid construction is included in this function and therefore in timings.
    """
    validate(points, radius)
    grid, cells = {}, []
    # A cell is one radius wide. Floor places negative and positive
    # coordinates in consistent intervals. Only occupied cells get entries.
    # The cells list keeps each point's cell key in input order.
    for i, point in enumerate(points):
        key = tuple(floor(x / radius) for x in point)
        cells.append(key)
        grid.setdefault(key, []).append(i)
    pairs, checks = set(), 0
    r2 = radius * radius
    # A possible match can lie one cell away along each axis, including
    # diagonally. Trying -1, 0, and 1 in three dimensions visits 27 cells.
    # Checking j > i keeps the lower index first, as in the all-pairs method.
    for i, cell in enumerate(cells):
        for delta in product((-1, 0, 1), repeat=3):
            key = tuple(c + d for c, d in zip(cell, delta))
            for j in grid.get(key, ()):
                if j > i:
                    # The grid finds candidates; the distance test decides
                    # whether a candidate is close enough to be a match.
                    checks += 1
                    if close(points[i], points[j], r2):
                        pairs.add((i, j))
    return pairs, checks
