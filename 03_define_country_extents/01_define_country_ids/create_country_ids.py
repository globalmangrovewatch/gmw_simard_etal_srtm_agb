import rsgislib.vectorattrs
import rsgislib.tools.utils

out_vec_file="/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/countries/GADM_EEZ_WCMC_UnqID.gpkg"
out_vec_lyr="National"

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

rsgislib.tools.utils.write_dict_to_json(lut, )