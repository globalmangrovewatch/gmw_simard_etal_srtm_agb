import os
import glob
import rsgislib
import rsgislib.imagecalc


def create_gmw_tile_lst(imgs_dir):
    imgs = glob.glob(os.path.join(imgs_dir, "*.tif"))
    for img in imgs:
        unq_vals = rsgislib.imagecalc.get_unique_values(input_img = img, img_band = 1)
        print(unq_vals)
        if len(unq_vals) > 1:
            print(img)
        



tiles_2000 = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_srtm_rasters"
create_gmw_tile_lst(tiles_2000)
tiles_2025 = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2025_srtm_rasters"




