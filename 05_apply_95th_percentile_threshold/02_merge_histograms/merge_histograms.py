import rsgislib.tools.utils
import numpy
import pickle
import glob

countries_lut_file = "../../03_define_country_extents/01_define_country_ids/country_ids_lut.json"
countries_lut = rsgislib.tools.utils.read_json_to_dict(countries_lut_file)

countries_idxs = list(countries_lut.keys())
print(countries_idxs)

countries_hists = dict()
for country_idx in countries_idxs:
    countries_hists[country_idx] = numpy.zeros(70, dtype=int)

tile_hist_files = glob.glob('/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/cnty_tile_hists/*.pkl')

for tile_hist in tile_hist_files:
    hist_pklobj = pickle.load(open(tile_hist, 'rb'))
    for country_idx in hist_pklobj.keys():
        country_idx_str = str(country_idx)
        if country_idx_str in countries_idxs:
            countries_hists[country_idx_str] = countries_hists[country_idx_str] + hist_pklobj[country_idx]
        else:
            print("{} is not in countries_idxs.".format(country_idx))

countries_hist_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/country_srtm_histograms.pkl"

with open(countries_hist_file, 'wb') as out_pkl_obj:
    pickle.dump(countries_hists, out_pkl_obj, protocol=pickle.HIGHEST_PROTOCOL)

