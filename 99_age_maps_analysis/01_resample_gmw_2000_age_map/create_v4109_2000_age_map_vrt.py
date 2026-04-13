import rsgislib.imageutils
import rsgislib.tools.filetools
import glob
import os

tmp_dir = "/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/tmp/age_maps"
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

age_imgs = glob.glob("/bigdata/petebunting/GlobalMangroveWatch/gmw_v4_baseline/gmw_v4_30m_change_analysis/data/gmw_v4_timeseries/v4109/gmw_mng_ext_v4109_ages/*.tif")

age_2000_imgs = list()
for age_img in age_imgs:
    basename = rsgislib.tools.filetools.get_file_basename(age_img)
    out_vrt_img = os.path.join(tmp_dir, f"{basename}_2000.vrt")
    rsgislib.imageutils.create_vrt_band_subset(input_img = age_img, img_bands = [16], out_vrt_img = out_vrt_img)
    age_2000_imgs.append(out_vrt_img)

rsgislib.imageutils.create_mosaic_images_vrt(input_imgs = age_2000_imgs, out_vrt_file = "gmw_v4109_age_map.vrt")
