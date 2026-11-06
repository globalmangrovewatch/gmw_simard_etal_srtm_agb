import json
import math
import re
from typing import Any, Dict, List, Tuple, Union


def parse_tile_centre(tile_name: str) -> Tuple[float, float]:
    """Parses a 1x1 degree tile name representing its bottom-left corner

    and returns the tile centre coordinates as (lon, lat).

    Examples:
        'N00E006' -> bottom-left: (0, 6)      -> centre: (6.5, 0.5)
        'S17W180' -> bottom-left: (-17, -180) -> centre: (-179.5, -16.5)
    """
    match = re.match(r"^([NS])(\d{2})([EW])(\d{3})$", tile_name.strip())
    if not match:
        raise ValueError(f"Invalid tile identifier format: '{tile_name}'")

    lat_hemi, lat_str, lon_hemi, lon_str = match.groups()

    lat_bl = float(lat_str) if lat_hemi == "N" else -float(lat_str)
    lon_bl = float(lon_str) if lon_hemi == "E" else -float(lon_str)

    # Offset by +0.5 degree to get the centre of the 1x1 degree cell
    centre_lat = lat_bl + 0.5
    centre_lon = lon_bl + 0.5

    return centre_lon, centre_lat


def haversine_distance(
    coord1: Tuple[float, float], coord2: Tuple[float, float]
) -> float:
    """Calculates the great-circle angular distance (in radians) between two points

    on a sphere using the Haversine formula.

    Note: coord format is (lon, lat).
    """
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)

    # Longitude difference handling world wrap-around (-180 to 180 degrees)
    dlambda = math.radians((lon2 - lon1 + 180.0) % 360.0 - 180.0)

    a = (
        math.sin(dphi / 2.0) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2.0) ** 2
    )

    # Clamp to avoid numerical floating-point inaccuracies outside [0, 1]
    a = min(1.0, max(0.0, a))
    return 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def find_nearest_tiles(
    tiles: Union[Dict[str, Any], List[str]], k: int = 4
) -> Dict[str, List[str]]:
    """For each tile, determines its centre coordinate from its name and finds

    the identifiers of the k nearest neighboring tiles.
    """
    tile_names = list(tiles.keys()) if isinstance(tiles, dict) else list(tiles)

    # Pre-calculate centre coordinates for all tiles once
    coords = {tile: parse_tile_centre(tile) for tile in tile_names}
    nearest_neighbors = {}

    for tile in tile_names:
        tile_coord = coords[tile]
        distances = []
        for other_tile in tile_names:
            if other_tile == tile:
                continue
            dist = haversine_distance(tile_coord, coords[other_tile])
            distances.append((dist, other_tile))

        distances.sort(key=lambda item: item[0])
        nearest_neighbors[tile] = [name for _, name in distances[:k]]

    return nearest_neighbors


def main():
    input_file = "../01_create_tiles_vec/gmw_srtm_tile_key_prj_def_lut.json"
    output_file = "gmw_srtm_tile_nearest_tiles.json"

    with open(input_file, "r") as f:
        tiles = json.load(f)

    nearest = find_nearest_tiles(tiles, k=4)

    with open(output_file, "w") as f:
        json.dump(nearest, f, indent=4)

    # Example display: check a Fiji-region tile across the antimeridian
    sample_key = "S17W180" if "S17W180" in nearest else next(iter(nearest))
    sample_centre = parse_tile_centre(sample_key)
    print(f"Sample tile: '{sample_key}' -> centre: {sample_centre}")
    print(f"Nearest neighbors for '{sample_key}': {nearest[sample_key]}")
    print(f"Nearest neighbors saved to '{output_file}'.")

if __name__ == "__main__":
    main()
