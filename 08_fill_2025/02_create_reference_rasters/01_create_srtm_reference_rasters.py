from pathlib import Path
import geopandas as gpd
import numpy as np
import rasterio
from rasterio.transform import from_origin
import tqdm

def create_srtm_reference_rasters(
    parquet_path: str = "../01_create_tiles_vec/gmw_srtm_grid_1deg.parquet",
    output_dir: str = "../00_ref_imgs",
    dtype: str = "uint8",
    nodata_val: int = 0
):
    """
    Creates blank reference GeoTIFFs aligned to the 1-arc-second SRTM grid (3601x3601)
    for each tile in the input vector parquet file.
    """
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    print(f"Reading tiles from {parquet_path}...")
    gdf = gpd.read_parquet(parquet_path)

    # SRTM 1-arc-second constants
    width, height = 3601, 3601
    pixel_size = 1.0 / 3600.0        # ~0.000277777777778 degrees
    half_pixel = pixel_size / 2.0    # ~0.000138888888889 degrees

    # Memory allocation: write zeros / nodata
    blank_band = np.full((height, width), fill_value=nodata_val, dtype=dtype)

    profile = {
        "driver": "GTiff",
        "crs": "EPSG:4326",
        "width": width,
        "height": height,
        "count": 1,
        "dtype": dtype,
        "nodata": nodata_val,
        "tiled": True,
        "blockxsize": 256,
        "blockysize": 256,
        "compress": "deflate",
        "interleave": "band"
    }

    print(f"Generating {len(gdf)} reference rasters...")

    for row in tqdm.tqdm(gdf.itertuples(), total=len(gdf), desc="Generating SRTM tiles",  unit="tile"):
        name = row.name
        geom = row.geometry
        minx, miny, maxx, maxy = geom.bounds

        # Round to integer degree boundaries to avoid floating precision drift
        tile_minx = int(np.round(minx))
        tile_maxy = int(np.round(maxy))

        # Origin is shifted outward by half a pixel to achieve the exact SRTM boundary
        origin_x = tile_minx - half_pixel
        origin_y = tile_maxy + half_pixel

        # Construct affine geotransform: from_origin(west, north, xsize, ysize)
        transform = from_origin(origin_x, origin_y, pixel_size, pixel_size)

        tile_profile = profile.copy()
        tile_profile["transform"] = transform

        out_file = out_path / f"{name}_reference.tif"
        with rasterio.open(out_file, "w", **tile_profile) as dst:
            dst.write(blank_band, 1)
            # Match the AREA_OR_POINT=Area metadata setting
            dst.update_tags(AREA_OR_POINT="Area")

    print(f"Done. Reference rasters written to {out_path.resolve()}")

if __name__ == "__main__":
    create_srtm_reference_rasters()
