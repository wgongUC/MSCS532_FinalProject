# Name: Weevern Gong
# Project Title: MSCS532_FinalProject
# Description: Measures all-pairs search and spatial grid search on the same
# point clouds and records runtime, distance checks, and matching pairs.

# Performance comparison explanation: Compare five-run medians for each
# search. Use two distributions to see how crowding changes the number of
# distance checks the grid can avoid.
# Running this script replaces the raw CSV and environment file in results.

"""Reproducible single-process experiment; no external packages required."""
import csv
import json
import platform
import random
import statistics
import sys
import time
from pathlib import Path
from neighbor_search import all_pairs, grid_pairs


def main():
    out = Path('results')
    out.mkdir(exist_ok=True)
    rows = []
    for distribution in ('fixed_density', 'clustered'):
        for n in (100, 500, 1000, 2000):
            # Fixed-density inputs grow in volume as n grows. The crowded
            # inputs use the same small cube at every size. Each method and
            # every timing trial uses the same points for a given case.
            rng = random.Random(532 + n)
            side = (n / 10) ** (1 / 3) if distribution == 'fixed_density' else 0.5
            points = [tuple(rng.uniform(0, side) for _ in range(3)) for _ in range(n)]
            radius = 0.2
            # Check agreement before timing and keep the baseline answer for
            # the check after each measured call.
            expected, base_checks = all_pairs(points, radius)
            actual, grid_checks = grid_pairs(points, radius)
            assert expected == actual, 'Correctness failure'
            times = {'all_pairs': [], 'grid': []}
            for trial in range(5):
                # Reverse the order on alternate trials so one method does
                # not always run first.
                order = [('all_pairs', all_pairs), ('grid', grid_pairs)]
                if trial % 2:
                    order.reverse()
                for name, fn in order:
                    # Time only the search call. This includes validation
                    # and, for the grid, building the index. It excludes
                    # generating points and checking the returned pairs.
                    start = time.perf_counter()
                    result, checks = fn(points, radius)
                    elapsed = time.perf_counter() - start
                    assert result == expected
                    times[name].append(elapsed)
                    rows.append(dict(distribution=distribution, n=n, radius=radius,
                                     algorithm=name, trial=trial + 1,
                                     seconds=elapsed, distance_checks=checks,
                                     matching_pairs=len(result)))
            # Report baseline time divided by grid time. A value below one
            # means the grid took longer for this case.
            b, g = (statistics.median(times[k]) for k in ('all_pairs', 'grid'))
            print(f'{distribution:14} n={n:4} baseline={b:.6f}s grid={g:.6f}s '
                  f'speedup={b/g:.2f}x checks={base_checks}/{grid_checks}')
    # Save each timing so readers can check the medians and run-to-run
    # variation. Record the environment separately for context.
    with (out / 'raw_timings.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    (out / 'environment.json').write_text(json.dumps(dict(
        python=sys.version, platform=platform.platform(), processor=platform.processor(),
        repeats=5, seed_rule='532 + n', measured_at_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
        notes='Single process; grid build included; output materialized; no CPU affinity or isolation; no peak-memory measurements.'
    ), indent=2))


if __name__ == '__main__':
    main()
