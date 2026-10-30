import geopandas
import rsgislib.vectorattrs
import rsgislib.tools.utils

vec_file="gmw_openstreetmap_country_boundaries_20250320_agb.gpkg"
vec_lyr="gmw_openstreetmap_country_boundaries_20250320"

base_gdf = geopandas.read_file(vec_file, layer=vec_lyr)

agb_eq_vals = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, "agb_eq")
cntry_vals = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, "gmw_cntry_name")

lut = dict()

for agb_val, cntry_val in zip(agb_eq_vals, cntry_vals):
    lut[cntry_val] = agb_val

rsgislib.tools.utils.write_dict_to_json(lut, "countries_abg_lut.json")
