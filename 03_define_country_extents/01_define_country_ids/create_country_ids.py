import rsgislib.vectorutils
import rsgislib.vectorattrs
import rsgislib.tools.utils
import numpy
import osgeo.ogr as ogr
import os

out_vec_file="/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/countries/GADM_EEZ_WCMC_UnqID.gpkg"
out_vec_lyr="National"

if os.path.exists(out_vec_file):
    rsgislib.vectorutils.delete_vector_file(out_vec_file)

rsgislib.vectorattrs.add_unq_numeric_col(
    vec_file="/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/countries/GADM_EEZ_WCMC.gpkg",
    vec_lyr="National",
    unq_col="gid_0",
    out_col="unqid",
    out_vec_file=out_vec_file,
    out_vec_lyr=out_vec_lyr,
    out_format="GPKG",
)

ref_vals = rsgislib.vectorattrs.read_vec_column(out_vec_file, out_vec_lyr, "gid_0")
unq_vals = rsgislib.vectorattrs.read_vec_column(out_vec_file, out_vec_lyr, "unqid")

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

country_names_lut = rsgislib.tools.utils.read_json_to_dict("gadm_lut.json")
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


rsgislib.vectorattrs.write_vec_column(out_vec_file, out_vec_lyr, "country_names", ogr.OFTString, cntry_names.tolist())
rsgislib.vectorattrs.write_vec_column(out_vec_file, out_vec_lyr, "agb_allom", ogr.OFTString, agb_allom_rgns.tolist())
rsgislib.vectorattrs.write_vec_column(out_vec_file, out_vec_lyr, "agb_allom", ogr.OFTInteger, agb_allom_rgns_idx.tolist())

rsgislib.tools.utils.write_dict_to_json("allom_id_lut.json", agb_allom_id_lut)

