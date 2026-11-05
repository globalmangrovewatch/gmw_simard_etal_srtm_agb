#!/usr/bin/env python3
"""
Inverts a project-to-tiles lookup table (LUT) so that tile names
become the primary keys.

Input structure:
    {
        "GMW-01-001": ["N34W122", "N34W121", ...],
        ...
    }

Output structure:
    {
        "N34W122": "GMW-01-001",
        "N34W121": "GMW-01-001",
        ...
    }
"""

import argparse
import json
from pathlib import Path


def invert_lut(input_lut_file, output_lut_file, include_lvl1=False, as_list=False):
    input_path = Path(input_lut_file)
    output_path = Path(output_lut_file)

    with open(input_path, "r") as f:
        prj_lut = json.load(f)

    inverted_lut = {}

    for prj_id, tile_list in prj_lut.items():
        parts = prj_id.split("-")
        lvl1_id = "-".join(parts[:2]) if len(parts) >= 2 else prj_id

        for tile in tile_list:
            if include_lvl1:
                val = {"project": prj_id, "level1": lvl1_id}
            else:
                val = prj_id

            if as_list:
                if tile not in inverted_lut:
                    inverted_lut[tile] = []
                inverted_lut[tile].append(val)
            else:
                # Direct 1-to-1 mapping (safely handles any overlap if present)
                if tile in inverted_lut and inverted_lut[tile] != val:
                    if isinstance(inverted_lut[tile], list):
                        inverted_lut[tile].append(val)
                    else:
                        inverted_lut[tile] = [inverted_lut[tile], val]
                else:
                    inverted_lut[tile] = val

    # Sort keys alphabetically for clean, deterministic JSON output
    sorted_inverted_lut = {k: inverted_lut[k] for k in sorted(inverted_lut.keys())}

    with open(output_path, "w") as f:
        json.dump(sorted_inverted_lut, f, indent=4)

    print(f"Inverted {len(prj_lut)} projects across {len(sorted_inverted_lut)} unique tiles.")
    print(f"Saved inverted LUT to '{output_path}'")


invert_lut("gmw_srtm_tiles_prj_def_lut.json", "gmw_srtm_tile_key_prj_def_lut.json", include_lvl1=False, as_list=False)
