import geopandas as gpd
import numpy as np
from shapely.geometry import box

def format_grid_name(lat: int, lon: int) -> str:
    """
    Formats the bottom-left coordinate into a standard tile identifier.
    e.g., lat=0, lon=117 -> N00E117
          lat=-34, lon=-58 -> S34W058
    """
    ns = "N" if lat >= 0 else "S"
    ew = "E" if lon >= 0 else "W"
    return f"{ns}{abs(lat):02d}{ew}{abs(lon):03d}"

def generate_degree_grid(
    min_lat: int = -45,
    max_lat: int = 45,
    min_lon: int = -180,
    max_lon: int = 180,
    step: int = 1
) -> gpd.GeoDataFrame:
    names = []
    geometries = []

    # Iterate over bottom-left origins
    for lat in range(min_lat, max_lat, step):
        for lon in range(min_lon, max_lon, step):
            # Polygon bounds: (minx, miny, maxx, maxy)
            poly = box(lon, lat, lon + step, lat + step)
            names.append(format_grid_name(lat, lon))
            geometries.append(poly)

    gdf = gpd.GeoDataFrame(
        {"name": names, "geometry": geometries},
        crs="EPSG:4326"
    )
    return gdf

if __name__ == "__main__":
    # Generate the global 1x1 degree grid
    grid_gdf = generate_degree_grid()

    # View sample records
    print(grid_gdf.head())

    # Example: filter or look up N00E117 specifically
    sample_tile = grid_gdf[grid_gdf["name"] == "N00E117"]
    print("\nLookup N00E117:")
    print(sample_tile)

    # Optional: Save to file (GeoPackage or Parquet recommended for speed/size)
    #grid_gdf.to_file("grid_1deg.gpkg", layer="grid", driver="GPKG")
    grid_gdf.to_parquet("grid_1deg.parquet")
