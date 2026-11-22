# MSCS532_FinalProject by Weevern Gong

## Description

This project compares two ways of finding pairs of 3D points within a fixed radius. The baseline checks every unordered pair. The spatial grid assigns points to cells one radius wide and checks the current cell and its 26 neighbors. Both implementations return the same kind of result: a set of matching index pairs and the number of distance checks.

The grid adapts the idea of ruling out unnecessary collision comparisons from the assigned HPC study. It does not reproduce OpenFOAM's collision rules or run in parallel.

## Requirements

- Python 3.14 to match the original Windows benchmark.
- No third-party packages.

## Instructions

From the source folder, run the seven unit tests:

```text
python -m unittest -v
```

To produce a fresh run, copy the repository to a separate folder, open a terminal in that copy, and run:

```text
python benchmark.py
```

Running the benchmark overwrites `results/raw_timings.csv` and `results/environment.json` in the current folder. It does not update `results/summary_verified.csv`, which summarizes the Windows measurements collected on November 22, 2026. Keep the original and any new run separate. Runtimes vary by machine.

## Files

| File | Purpose |
| --- | --- |
| `neighbor_search.py` | Implements both searches and their shared distance check. |
| `test_neighbor_search.py` | Checks pair-set agreement on valid inputs and rejection of invalid inputs. |
| `benchmark.py` | Times both searches on identical inputs over five trials per input. |
| `results/raw_timings.csv` | Stores the 80 Windows timing observations used in the report. |
| `results/summary_verified.csv` | Summarizes the report run’s median timings and pair counts. |
| `results/environment.json` | Records the report run’s benchmark environment. |
| `results/test_output.txt` | Records the seven Windows unit tests. |
| `.gitignore` | Excludes generated Python cache files. |

## Summary of findings

At 2,000 points, the grid was 51.52 times as fast at fixed density and 1.47 times as fast in the crowded cube. At 100 points in the crowded cube, the grid took about 9% longer. The benchmark timed each search as a whole, including index construction for the grid. It did not measure the time spent building the index separately.

The benchmark checks both methods before timing. After each timed call, it verifies the returned pairs against the baseline before keeping the result.
