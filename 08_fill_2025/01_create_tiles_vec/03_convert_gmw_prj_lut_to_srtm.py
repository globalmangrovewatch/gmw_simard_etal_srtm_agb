import geopandas
import re
from collections import defaultdict
import json
import os

def jaxa_tr_to_srtm_bl(tile_name: str) -> str:
    """
    Converts a 1x1 degree JAXA tile name (top-right corner)
    to an SRTM tile name (bottom-left corner).
    """
    match = re.search(r"([NS])(\d{2})_?([EW])(\d{2,3})", tile_name, re.IGNORECASE)
    if not match:
        raise ValueError(f"Unable to parse tile identifier from: {tile_name}")

    lat_hemi, lat_str, lon_hemi, lon_str = match.groups()
    lat = int(lat_str) if lat_hemi.upper() == "N" else -int(lat_str)
    lon = int(lon_str) if lon_hemi.upper() == "E" else -int(lon_str)

    # Shift from top-right to bottom-left
    srtm_lat = lat - 1
    srtm_lon = lon# - 1

    out_lat_hemi = "N" if srtm_lat >= 0 else "S"
    out_lon_hemi = "E" if srtm_lon >= 0 else "W"

    return f"{out_lat_hemi}{abs(srtm_lat):02d}{out_lon_hemi}{abs(srtm_lon):03d}"


def create_project_to_tiles_lut(input_json_path: str, output_lut_path: str, output_srtm_lut_path: str):
    """Reads a GeoJSON FeatureCollection and creates a LUT mapping

    gmw_prj to a list of tile_names, saving the result as a JSON file.
    """
    # 1. Load the GeoJSON data
    with open(input_json_path, "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    # 2. Build the LUT: { "gmw_prj": ["tile_name_1", "tile_name_2", ...] }
    prj_tile_lut = defaultdict(list)
    prj_srtm_tile_lut = defaultdict(list)
    features = geojson_data.get("features", [])

    for feature in features:
        props = feature.get("properties", {})
        tile_name = props.get("tile_name")
        tile_srtm_name = jaxa_tr_to_srtm_bl(tile_name)
        gmw_prj = props.get("gmw_prj")

        if gmw_prj and tile_name:
            prj_tile_lut[gmw_prj].append(tile_name)
            prj_srtm_tile_lut[gmw_prj].append(tile_srtm_name)

    # Convert defaultdict back to standard dict
    prj_tile_lut = dict(prj_tile_lut)
    prj_srtm_tile_lut = dict(prj_srtm_tile_lut)

    # 3. Export to JSON
    os.makedirs(os.path.dirname(output_lut_path) or ".", exist_ok=True)
    with open(output_lut_path, "w", encoding="utf-8") as f:
        json.dump(prj_tile_lut, f, indent=4)

    with open(output_srtm_lut_path, "w", encoding="utf-8") as f:
        json.dump(prj_srtm_tile_lut, f, indent=4)

    print(
        f"LUT successfully created with {len(prj_tile_lut)} distinct projects."
    )
    print(f"Exported to: {output_lut_path}")

    return prj_tile_lut


create_project_to_tiles_lut(input_json_path = "gmw_tiles_prj_def.geojson", output_lut_path = "gmw_tiles_prj_def_lut.json", output_srtm_lut_path = "gmw_srtm_tiles_prj_def_lut.json")
