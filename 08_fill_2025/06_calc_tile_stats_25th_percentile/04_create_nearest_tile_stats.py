#!/usr/bin/env python3
"""
Calculate summary statistics (pixel count, mean, and std) from 1x1 degree
tile statistics across local spatial neighborhoods (target tile + 4 nearest neighbors)
and optionally project / hierarchical Level 1 definitions.

Formulation:
    N_total  = sum(N_i)
    mu_comb  = sum(N_i * mu_i) / N_total
    var_comb = sum(N_i * (sigma_i^2 + (mu_i - mu_comb)^2)) / N_total
    std_comb = sqrt(var_comb)
"""

import json
import math
import sys
from pathlib import Path


def combine_stats(tile_stats_list):
    """
    Combines a list of dicts with keys ('n', 'mean', 'std').
    Filters out missing, empty (n=0), or NaN tiles.
    """
    valid_tiles = [
        t for t in tile_stats_list
        if t is not None
        and t.get("n", 0) > 0
        and not math.isnan(t.get("mean", float("nan")))
        and not math.isnan(t.get("std", float("nan")))
    ]

    if not valid_tiles:
        return {"n": 0, "mean": None, "std": None}

    n_tot = sum(t["n"] for t in valid_tiles)
    if n_tot == 0:
        return {"n": 0, "mean": None, "std": None}

    # Combined mean (weighted average)
    mean_comb = sum(t["n"] * t["mean"] for t in valid_tiles) / n_tot

    # Combined variance = within-tile variance + between-tile variance
    sum_sq_diff = sum(
        t["n"] * ((t["std"] ** 2) + ((t["mean"] - mean_comb) ** 2))
        for t in valid_tiles
    )
    var_comb = sum_sq_diff / n_tot
    std_comb = math.sqrt(max(0.0, var_comb))

    return {
        "n": int(n_tot),
        "mean": float(mean_comb),
        "std": float(std_comb),
    }


def calculate_nearest_tiles_stats(tile_stats_file, nearest_lut_file, output_file=None):
    """
    Calculates combined statistics across each tile and its 4 nearest neighbors
    (5 tiles total per group).
    """
    tile_stats_path = Path(tile_stats_file)
    nearest_lut_path = Path(nearest_lut_file)

    with open(tile_stats_path, "r") as f:
        tile_stats = json.load(f)

    with open(nearest_lut_path, "r") as f:
        nearest_lut = json.load(f)

    nearest_combined_stats = {}

    for tile_id, neighbors in nearest_lut.items():
        # Include the target tile itself alongside the 4 nearest neighbors
        tile_group = [tile_id] + list(neighbors)

        # Collect stats for tiles present in tile_stats
        stats_list = [tile_stats[t] for t in tile_group if t in tile_stats]
        nearest_combined_stats[tile_id] = combine_stats(stats_list)

    if output_file:
        out_path = Path(output_file)
        with open(out_path, "w") as f:
            json.dump(nearest_combined_stats, f, indent=4)
        print(f"Saved nearest combined tile stats ({len(nearest_combined_stats)} tiles) to '{out_path}'")

    return nearest_combined_stats


if __name__ == "__main__":
    tile_stats_file = "agb_tile_stats_v4112_2000_lt_25th_percentile.json"
    nearest_lut_file = "gmw_srtm_tile_nearest_tiles.json"
    nearest_out_file = "agb_tile_nearest_stats_v4112_2000_lt_25th_percentile.json"

    # 1. Calculate combined stats for target tile + 4 nearest neighbors
    calculate_nearest_tiles_stats(tile_stats_file, nearest_lut_file, nearest_out_file)
