#!/usr/bin/env python3
"""
Calculate project-level summary statistics (pixel count, mean, and std)
from 1x1 degree tile statistics using project lookup definitions (LUT).

Formulation:
    N_total = sum(N_i)
    mu_comb = sum(N_i * mu_i) / N_total
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

    mean_comb = sum(t["n"] * t["mean"] for t in valid_tiles) / n_tot
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


def calculate_hierarchical_stats(tile_stats_file, lut_file, prj_out_file=None, lvl1_out_file=None):
    tile_stats_path = Path(tile_stats_file)
    lut_path = Path(lut_file)

    with open(tile_stats_path, "r") as f:
        tile_stats = json.load(f)

    with open(lut_path, "r") as f:
        prj_lut = json.load(f)

    # 1. Project-level stats
    project_stats = {}
    level1_tiles = {}

    for prj_id, tile_list in prj_lut.items():
        stats_for_prj = [tile_stats[t] for t in tile_list if t in tile_stats]
        project_stats[prj_id] = combine_stats(stats_for_prj)

        # Collect unique tiles for hierarchical Level 1 (e.g., GMW-01)
        parts = prj_id.split("-")
        lvl1_id = "-".join(parts[:2]) if len(parts) >= 2 else prj_id
        if lvl1_id not in level1_tiles:
            level1_tiles[lvl1_id] = set()
        level1_tiles[lvl1_id].update(tile_list)

    # 2. Level 1 summary stats
    level1_stats = {}
    for lvl1_id, tiles_set in sorted(level1_tiles.items()):
        stats_for_lvl1 = [tile_stats[t] for t in tiles_set if t in tile_stats]
        level1_stats[lvl1_id] = combine_stats(stats_for_lvl1)

    # Save outputs if specified
    if prj_out_file:
        with open(prj_out_file, "w") as f:
            json.dump(project_stats, f, indent=4)
        print(f"Saved project stats to '{prj_out_file}'")

    if lvl1_out_file:
        with open(lvl1_out_file, "w") as f:
            json.dump(level1_stats, f, indent=4)
        print(f"Saved Level 1 summary stats to '{lvl1_out_file}'")

    return project_stats, level1_stats

tile_stats_file = "agb_tile_stats_v4112.json"
lut_file = "../01_create_tiles_vec/gmw_srtm_tiles_prj_def_lut.json"
prj_out_file = "agb_project_lv2_stats_v4112.json"
lvl1_out_file = "agb_project_lv1_stats_v4112.json"

calculate_hierarchical_stats(tile_stats_file, lut_file, prj_out_file, lvl1_out_file)
