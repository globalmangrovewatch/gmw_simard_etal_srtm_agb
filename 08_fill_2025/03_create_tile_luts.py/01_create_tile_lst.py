import os
import glob
import rsgislib
import rsgislib.imagecalc


def create_gmw_tile_lst(imgs_dir):
    imgs = glob.glob(os.path.join(imgs_dir, "*.tif"))
    for img in imgs:
        basename = rsgislib.tools.filetools.get_file_basename(img)
        tile_name = basename.split("_")[0]
        unq_vals = rsgislib.imagecalc.get_unique_values(input_img = img, img_band = 1)
        if len(unq_vals) > 1:
            print(tile_name)
            img_bbox = rsgislib.imageutils.get_img_bbox(img)
            cen_pt = rsgislib.tools.geometrytools.get_bbox_centre_pt(img_bbox)
            print(cen_pt)
        



tiles_2000 = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_srtm_rasters"
create_gmw_tile_lst(tiles_2000)
tiles_2025 = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2025_srtm_rasters"




