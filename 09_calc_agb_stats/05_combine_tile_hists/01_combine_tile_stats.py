import glob
import rsgislib.tools.utils
import numpy

country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json'
unq_cntry_vals = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)["val"].keys()

tile_stats_lut = dict()

for val in unq_cntry_vals:
    tile_stats_lut[val] = numpy.zeros((81), dtype=numpy.uint32)

stats_tiles = glob.glob('/home/pete/Documents/gmw_v3_agb_hgt/stats/hist_agb_tile_stats/*.json')

for stats_tile_file in stats_tiles:
    stats_tile_lut = rsgislib.tools.utils.read_json_to_dict(stats_tile_file)

    for val in unq_cntry_vals:
        tile_stats_lut[val] += numpy.array(stats_tile_lut[val], dtype=numpy.uint32)

rsgislib.tools.utils.write_dict_to_json(tile_stats_lut, 'country_agb_hists.json')

