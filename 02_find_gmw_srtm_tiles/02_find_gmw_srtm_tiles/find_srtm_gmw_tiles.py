import rsgislib.imageutils.imagelut
import rsgislib.tools.utils

srtm_lut_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/srtm_tiles_lut.gpkg"
gmw_lut_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/gmw_union_tiles_lut.gpkg"


cp_cmds = rsgislib.imageutils.imagelut.query_file_lut(
    lut_db_file=srtm_lut_file,
    lyr_name="srtm_tiles",
    roi_file=gmw_lut_file,
    roi_lyr="gmw_tiles",
    out_dest="/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/gmw_kea",
    targz_out=False,
    cp_cmds=True,
)

rsgislib.tools.utils.write_list_to_file(cp_cmds, "cp_gmw_srtm_tiles.sh")

