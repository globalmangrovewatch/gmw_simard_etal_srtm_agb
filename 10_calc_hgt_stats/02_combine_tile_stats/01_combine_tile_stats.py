import glob
import rsgislib.tools.utils


country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json'
unq_cntry_vals = rsgislib.tools.utils.read_json_to_dict(country_ids_lut_file)["val"].keys()

gmw_years = [1996, 2007, 2008, 2009, 2010, 2015, 2015, 2016, 2017, 2018, 2019, 2020]

tile_stats_lut = dict()
for year in gmw_years:
    lut_vals = dict()
    for val in unq_cntry_vals:
        lut_vals[val] = dict()
        lut_vals[val]['count'] = 0
        lut_vals[val]['vals'] = 0.0
    year_str = f"{year}"
    tile_stats_lut[year_str] = lut_vals

stats_tiles = glob.glob('/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/stats/tile_hchm_stats/*.json')

for stats_tile_file in stats_tiles:
    stats_tile_lut = rsgislib.tools.utils.read_json_to_dict(stats_tile_file)

    for year in gmw_years:
        year_str = f"{year}"
        for val in unq_cntry_vals:
            tile_stats_lut[year_str][val]['count'] += stats_tile_lut[year_str][val]['count']
            tile_stats_lut[year_str][val]['vals'] += stats_tile_lut[year_str][val]['vals']

rsgislib.tools.utils.write_dict_to_json(tile_stats_lut, '/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/stats/country_hchm_stats.json')

