import json
import math
from typing import Dict, List, Tuple


def haversine_distance(
    coord1: Tuple[float, float], coord2: Tuple[float, float]
) -> float:
    """Calculates the great-circle angular distance (in radians) between two points

    on a sphere using the Haversine formula.

    Note: coord format is [lon, lat] as given in the dataset.
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

    # Clamp to avoid numerical floating-point inaccuracies outside [-1, 1]
    a = min(1.0, max(0.0, a))
    return 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))


def find_nearest_tiles(
    tiles: Dict[str, List[float]], k: int = 4
) -> Dict[str, List[str]]:
    """For each tile, finds the identifiers of the k nearest neighboring tiles."""
    tile_names = list(tiles.keys())
    nearest_neighbors = {}

    for tile, coord in tiles.items():
        # Compute distances to all other tiles
        distances = []
        for other_tile in tile_names:
            if other_tile == tile:
                continue
            dist = haversine_distance(coord, tiles[other_tile])
            distances.append((dist, other_tile))

        # Sort by distance and extract top k tile keys
        distances.sort(key=lambda item: item[0])
        nearest_neighbors[tile] = [name for _, name in distances[:k]]

    return nearest_neighbors


def main():
    input_file = "gmw_data_tiles.json"
    output_file = "gmw_nearest_tiles.json"

    with open(input_file, "r") as f:
        tiles = json.load(f)

    nearest = find_nearest_tiles(tiles, k=4)

    with open(output_file, "w") as f:
        json.dump(nearest, f, indent=4)

    # Example display: check a Fiji-region tile across the antimeridian
    sample_key = "S17W180" if "S17W180" in nearest else next(iter(nearest))
    print(f"Sample output for '{sample_key}': {nearest[sample_key]}")
    print(f"Nearest neighbors saved to '{output_file}'.")


if __name__ == "__main__":
    main()