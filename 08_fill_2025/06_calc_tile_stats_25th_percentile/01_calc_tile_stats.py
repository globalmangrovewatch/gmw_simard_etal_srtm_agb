import os
import glob
import tqdm
import rsgislib.tools.filetools
import rsgislib.tools.utils
import rsgislib.imageutils
import numpy

def calc_tile_stats(ref_imgs, agb_img_dir, agb_img_str, out_json_file):
    tile_stats = dict()
    for img in tqdm.tqdm(ref_imgs):
        tile_name = rsgislib.tools.filetools.get_file_basename(img).replace("_reference", "")
        agb_img = os.path.join(agb_img_dir, f"{tile_name}_{agb_img_str}.tif")
        if os.path.exists(agb_img):
            agb_arr = rsgislib.imageutils.get_img_data_as_arr(agb_img, img_bands = [1])
            agb_flat_arr = agb_arr.flatten()
            agb_flat_arr = agb_flat_arr[numpy.isfinite(agb_flat_arr)]
            agb_flat_arr = agb_flat_arr[agb_flat_arr > 0]
            if agb_flat_arr.shape[0] > 0:
                agb_25th_percent = numpy.percentile(agb_flat_arr, 25)
                agb_flat_arr = agb_flat_arr[agb_flat_arr < agb_25th_percent]

                n_pxl = int(agb_flat_arr.shape[0])
                mean_agb = float(numpy.mean(agb_flat_arr))
                std_agb = float(numpy.std(agb_flat_arr))
            else:
                n_pxl = 0
                mean_agb = 0.0
                std_agb = 0.0
        else:
            n_pxl = 0
            mean_agb = 0.0
            std_agb = 0.0

        tile_stats[tile_name] = dict()
        tile_stats[tile_name]["n"] = n_pxl
        tile_stats[tile_name]["mean"] = mean_agb
        tile_stats[tile_name]["std"] = std_agb

    rsgislib.tools.utils.write_dict_to_json(data_dict = tile_stats, out_file = out_json_file)

ref_imgs = glob.glob("../00_ref_imgs/*.tif")
agb_img_dir = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_v4112_2000_agb_filled"
agb_img_str = "srtm_gmw_agb_2000_filled"
out_json_file = "agb_tile_stats_v4112_2000_lt_25th_percentile.json"
calc_tile_stats(ref_imgs, agb_img_dir, agb_img_str, out_json_file)
