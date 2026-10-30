import glob
import rsgislib.imageutils.imagelut

srtm_tiles = glob.glob("/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/srtm/SRTM_GL1_srtm/*.tif")
srtm_lut_file = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/srtm/srtm_tiles_lut.gpkg"
rsgislib.imageutils.imagelut.create_img_extent_lut(srtm_tiles, vec_file=srtm_lut_file, vec_lyr="srtm_tiles", out_format="GPKG", ignore_none_imgs=False, out_proj_wgs84=False, overwrite_lut_file=False)

gmw_union_tiles = glob.glob("/bigdata/GlobalMangroveWatch/gmw_ext_lyrs/gmw_v4112_timeseries/mng_union_intersection/raster/gmw_mng_ext_v4112_union/*.tif")
gmw_lut_file = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_v4112_union_tiles_lut.gpkg"
rsgislib.imageutils.imagelut.create_img_extent_lut(gmw_union_tiles, vec_file=gmw_lut_file, vec_lyr="gmw_tiles", out_format="GPKG", ignore_none_imgs=False, out_proj_wgs84=False, overwrite_lut_file=False)
