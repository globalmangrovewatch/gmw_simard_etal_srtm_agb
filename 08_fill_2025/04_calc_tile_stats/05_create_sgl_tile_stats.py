import rsgislib.tools.utils
import glob
import rsgislib.tools.filetools

tile_stats_lut = rsgislib.tools.utils.read_json_to_dict("agb_tile_stats_v4112.json")
near_tile_stats_lut = rsgislib.tools.utils.read_json_to_dict("agb_tile_nearest_stats_v4112.json")
gmw_prj_lv1_stats_lut = rsgislib.tools.utils.read_json_to_dict("agb_project_lv1_stats_v4112.json")
gmw_prj_lv2_stats_lut = rsgislib.tools.utils.read_json_to_dict("agb_project_lv2_stats_v4112.json")

gmw_prj_lv2_lut = rsgislib.tools.utils.read_json_to_dict("../01_create_tiles_vec/gmw_srtm_tile_key_prj_def_lut.json")


print(len(tile_stats_lut))

ref_imgs = glob.glob("../00_ref_imgs/*.tif")

for ref_img in ref_imgs:
    tile = rsgislib.tools.filetools.get_file_basename(ref_img).split("_")[0]
    if tile not in tile_stats_lut:
        tile_stats_lut[tile] = dict()
        tile_stats_lut[tile]["n"] = 0
        tile_stats_lut[tile]["mean"] = 0.0
        tile_stats_lut[tile]["std"] = 0.0

    if tile_stats_lut[tile]["n"] < 1000:
        if tile in near_tile_stats_lut and near_tile_stats_lut[tile]["n"] > 1000:
            tile_stats_lut[tile]["n"] = near_tile_stats_lut[tile]["n"]
            tile_stats_lut[tile]["mean"] = near_tile_stats_lut[tile]["mean"]
            tile_stats_lut[tile]["std"] = near_tile_stats_lut[tile]["std"]
        else:
            gmw_prj_lv2 = gmw_prj_lv2_lut[tile]
            if gmw_prj_lv2_stats_lut[gmw_prj_lv2]["n"] > 0:
                tile_stats_lut[tile]["n"] = gmw_prj_lv2_stats_lut[gmw_prj_lv2]["n"]
                tile_stats_lut[tile]["mean"] = gmw_prj_lv2_stats_lut[gmw_prj_lv2]["mean"]
                tile_stats_lut[tile]["std"] = gmw_prj_lv2_stats_lut[gmw_prj_lv2]["std"]
            else:
                prj_comps = gmw_prj_lv2.split("-")
                gmw_prj_lv1 = f"{prj_comps[0]}-{prj_comps[1]}"

                if gmw_prj_lv1_stats_lut[gmw_prj_lv1]["n"] > 0:
                    tile_stats_lut[tile]["n"] = gmw_prj_lv1_stats_lut[gmw_prj_lv1]["n"]
                    tile_stats_lut[tile]["mean"] = gmw_prj_lv1_stats_lut[gmw_prj_lv1]["mean"]
                    tile_stats_lut[tile]["std"] = gmw_prj_lv1_stats_lut[gmw_prj_lv1]["std"]
                else:
                    raise Exception(f"NO STATS - {tile}")


print(len(tile_stats_lut))
rsgislib.tools.utils.write_dict_to_json(tile_stats_lut, out_file = "agb_tile_stats_gmw_v4112_fnl_combined.json")
