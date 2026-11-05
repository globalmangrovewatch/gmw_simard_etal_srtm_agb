import os
import glob
import tqdm
import rsgislib.tools.filetools
import rsgislib.tools.utils

def calc_tile_stats(ref_imgs, agb_img_dir, agb_img_str, out_json_file):
    tile_stats = dict()
    for img in ref_imgs:
        tile_name = rsgislib.tools.filetools.get_file_basename(img).replace("_reference", "")
        agb_img = os.path.join(agb_img_dir, f"{tile_name}_{agb_img_str}.tif")
        if not os.path.exists(agb_img):
            print(agb_img)

            tile_stats[tile_name] = dict()
    rsgislib.tools.utils.write_dict_to_json(data_dict = tile_stats, out_file = out_json_file)

ref_imgs = glob.glob("../00_ref_imgs/*.tif")
agb_img_dir = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_v4112_2000_agb"
agb_img_str = "srtm_gmw_agb"
out_json_file = "agb_tile_stats_v4112.json"
calc_tile_stats(ref_imgs, agb_img_dir, agb_img_str, out_json_file)
