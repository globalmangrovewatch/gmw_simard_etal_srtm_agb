import rsgislib.vectorutils
import rsgislib.vectorattrs
import rsgislib.tools.utils
import numpy
import osgeo.ogr as ogr
import os

vec_file="/bigdata/petebunting/Dropbox/University/Research/Data/Mangroves/OpenStreetMap_Boundaries/20260412/gmw_openstreetmap_country_boundaries_20250320.gpkg"
vec_lyr="gmw_openstreetmap_country_boundaries_20250320"


ref_vals = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, "gmw_allocation")
cntry_vals = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, "gmw_cntry_name")
unq_vals = rsgislib.vectorattrs.read_vec_column(vec_file, vec_lyr, "gmw_cntry_id")

lut = dict()
lut['ref'] = dict()
lut['val'] = dict()
for ref_val, unq_val in zip(ref_vals, unq_vals):
    lut['ref'][ref_val] = unq_val
    lut['val'][unq_val] = ref_val

rsgislib.tools.utils.write_dict_to_json(lut, "country_ids_lut.json")


cntry_names = numpy.empty(len(ref_vals), dtype=numpy.dtype('U255'))
agb_allom_rgns = numpy.empty(len(ref_vals), dtype=numpy.dtype('U255'))
agb_allom_rgns_idx = numpy.zeros(len(ref_vals), dtype=numpy.dtype('int'))
agb_allom_rgns[...] = 'Global Hmax power'

country_names_lut = dict()
country_names_lut['ctry'] = dict()
country_names_lut['gid'] = dict()
for ref_val, unq_val in zip(ref_vals, cntry_vals):
    lut['gid'][ref_val] = cntry_vals
    lut['ctry'][cntry_vals] = ref_val

rsgislib.tools.utils.write_dict_to_json(lut, "country_names_lut.json")


agb_allom_lut = rsgislib.tools.utils.read_json_to_dict("countries_abg_lut.json")

agb_allom_id_lut = dict()
agb_allom_id_lut["id"] = dict()
agb_allom_id_lut["allom"] = dict()
id = 1
for cntry in agb_allom_lut:
    if agb_allom_lut[cntry] not in agb_allom_id_lut["allom"]:
        agb_allom_id_lut["allom"][agb_allom_lut[cntry]] = id
        agb_allom_id_lut["id"][id] = agb_allom_lut[cntry]
        id = id + 1

for i, cntry_id in enumerate(ref_vals):
    if cntry_id in country_names_lut["gid"]:
        country_name = country_names_lut["gid"][cntry_id]
        cntry_names[i] = country_name
        if country_name in agb_allom_lut:
            agb_allom = agb_allom_lut[country_name]
            agb_allom_rgns[i] = agb_allom
            agb_allom_rgns_idx[i] = agb_allom_id_lut["allom"][agb_allom]


out_vec_file="/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_openstreetmap_country_boundaries_20250320_agb_alloc.gpkg"
out_vec_lyr="gmw_openstreetmap_country_boundaries_20250320_agb_alloc"


rsgislib.vectorattrs.write_vec_column(out_vec_file, out_vec_lyr, "country_names", ogr.OFTString, cntry_names.tolist())
rsgislib.vectorattrs.write_vec_column(out_vec_file, out_vec_lyr, "agb_allom", ogr.OFTString, agb_allom_rgns.tolist())
rsgislib.vectorattrs.write_vec_column(out_vec_file, out_vec_lyr, "agb_allom_idx", ogr.OFTInteger, agb_allom_rgns_idx.tolist())

rsgislib.tools.utils.write_dict_to_json(agb_allom_id_lut, "allom_id_lut.json")
