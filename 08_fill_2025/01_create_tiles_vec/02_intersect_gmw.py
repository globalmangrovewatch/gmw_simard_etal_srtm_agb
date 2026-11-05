import geopandas as gpd
from shapely.geometry import box


def filter_intersecting_tiles(
        grid_parquet_path: str = "grid_1deg.parquet",
        gpkg_path: str = "gmw_mng_ext_v4112_union_vec.gpkg",
) -> gpd.GeoDataFrame:
    # 1. Read the 1x1 degree grid (small memory footprint: 64,800 rows)
    print("Loading grid...")
    grid_gdf = gpd.read_parquet(grid_parquet_path)

    # 2. Extract the overall extent of the mangrove dataset without reading all records
    # pyogrio uses GDAL to read file metadata directly from the header/R-Tree
    import pyogrio
    info = pyogrio.read_info(gpkg_path)
    total_bounds = info["total_bounds"]  # [minx, miny, maxx, maxy]

    # Pre-filter grid to the global bounding box of the dataset
    print(f"Filtering grid to global dataset envelope: {total_bounds}")
    coarse_grid = grid_gdf.cx[
        total_bounds[0]:total_bounds[2], total_bounds[1]:total_bounds[3]].copy()

    # 3. Read only geometries that fall within the coarse envelope
    # Specifying 'engine="pyogrio"' uses fast C-level spatial indexing (R*Tree built into GPKG)
    print("Reading target geometries using spatial bounds...")
    gmw_gdf = gpd.read_file(
            gpkg_path,
            engine="pyogrio",
            bbox=tuple(total_bounds),
            columns=[]  # Do not load attribute columns to conserve RAM; geometries only
    )

    # Ensure identical CRS
    if gmw_gdf.crs != coarse_grid.crs:
        print("Re-projecting dataset to match grid CRS...")
        gmw_gdf = gmw_gdf.to_crs(coarse_grid.crs)

    # 4. Use PyGEOS / GEOS STRtree spatial indexing
    # In modern GeoPandas (>=0.10+), .sindex builds an STRtree automatically.
    print("Building spatial index and running sjoin...")

    # We use predicate='intersects'. Because GMW polygons can be dense,
    # spatial joining the candidate grid cells against the dataset is fast.
    intersecting_tiles_idx = coarse_grid.sindex.query(
            gmw_gdf.geometry,
            predicate="intersects"
    )[1]

    # Extract unique matching tile indices
    unique_indices = coarse_grid.iloc[intersecting_tiles_idx].index.unique()
    selected_tiles = coarse_grid.loc[unique_indices].copy()

    print(f"Matched {len(selected_tiles)} intersecting 1x1 degree tiles.")

    return selected_tiles


if __name__ == "__main__":
    matching_tiles_gdf = filter_intersecting_tiles(
        grid_parquet_path = "grid_1deg.parquet",
        gpkg_path = "/Users/pfb/Library/CloudStorage/Dropbox/University/Research/Projects/GlobalMangroveWatch/GMW_v4_Development/gmw_v4_full_timeseries/v4112/mng_union_intersection/vector/gmw_mng_ext_v4112_union_vec.gpkg",
    )

    matching_tiles_gdf.to_file("gmw_srtm_grid_1deg.gpkg", layer="gmw_srtm_grid_1deg", driver="GPKG")
    matching_tiles_gdf.to_parquet("gmw_srtm_grid_1deg.parquet")
    print("Done.")
