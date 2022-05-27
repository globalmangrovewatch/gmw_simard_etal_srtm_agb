import glob
import rsgislib.imageutils.imagelut

srtm_tiles = glob.glob("/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/kea/*.kea")
srtm_lut_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/srtm_tiles_lut.gpkg"
rsgislib.imageutils.imagelut.create_img_extent_lut(srtm_tiles, vec_file=srtm_lut_file, vec_lyr="srtm_tiles", out_format="GPKG", ignore_none_imgs=False, out_proj_wgs84=False, overwrite_lut_file=False)

gmw_union_tiles = glob.glob("/scratch/a.pfb/gmw_v3_change/data/fnl_v3_prods/gmw_summaries/gmw_v3_union_v314_kea/*.kea")
gwm_lut_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/srtm_tiles_lut.gpkg"
rsgislib.imageutils.imagelut.create_img_extent_lut(gmw_union_tiles, vec_file=gwm_lut_file, vec_lyr="gmw_tiles", out_format="GPKG", ignore_none_imgs=False, out_proj_wgs84=False, overwrite_lut_file=False)


