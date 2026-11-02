import logging
import os
import glob
import rsgislib.tools.filetools
import rsgislib.tools.utils

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        # Get the list of input images
        tiles_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["tiles_lut"])
        agb_type_name = kwargs['agb_type_name']

        # Loop through the reference images to create the jobs
        for tilename in tiles_lut:
            gmw_2025_img = os.path.join(kwargs["gmw_2025_dir"], f"{tilename}_gmw_v4112_2025.tif")
            gmw_diff_img = os.path.join(kwargs["gmw_diff_img_dir"], f"{tilename}_gmw_v4112_2000_2025_diff.tif")
            gmw_agb_img = os.path.join(kwargs["gmw_diff_img_dir"], f"{tilename}{agb_type_name}.tif")

            pxl_smpl_files = list()
            pxl_smpl_files.append(os.path.join(kwargs["gmw_pxl_smpls_dir"], f"{tilename}{agb_type_name}_pxl_vals.parquet.gz"))
            near_tiles = tiles_lut[tilename]
            for near_tile in near_tiles:
                pxl_smpl_files.append(os.path.join(kwargs["gmw_pxl_smpls_dir"], f"{near_tile}{agb_type_name}_pxl_vals.parquet.gz"))

            # Create the output file name
            out_img = os.path.join(kwargs["out_dir"], f"{tilename}{agb_type_name}_gmw_2025.tif")
            # Check if the output file exists.
            if not os.path.exists(out_img):
                # You will probably have a loop here:
                # Within the loop create a dict with the parameters for each
                # job which will be added to the self.params list.
                c_dict = dict()
                c_dict["tilename"] = tilename
                c_dict["gmw_2025_img"] = gmw_2025_img
                c_dict["gmw_diff_img"] = gmw_diff_img
                c_dict["gmw_agb_img"] = gmw_agb_img
                c_dict["pxl_smpl_files"] = pxl_smpl_files
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
                tiles_lut = "../03_create_tile_luts/gmw_nearest_tiles.json",
                gmw_2025_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2025_srtm_rasters",
                gmw_agb_img_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hba",
                gmw_diff_img_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_2025_diff_srtm_rasters",
                gmw_pxl_smpls_dir = "/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hba_pxl_vals",
                agb_type_name = "_srtm_gmw_hba",
                out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2025_hba"
        )

        self.gen_command_info(
                tiles_lut="../03_create_tile_luts/gmw_nearest_tiles.json",
                gmw_2025_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2025_srtm_rasters",
                gmw_agb_img_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hchm",
                gmw_diff_img_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_2025_diff_srtm_rasters",
                gmw_pxl_smpls_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hchm_pxl_vals",
                agb_type_name="_srtm_gmw_hchm",
                out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2025_hchm"
        )

        self.gen_command_info(
                tiles_lut="../03_create_tile_luts/gmw_nearest_tiles.json",
                gmw_2025_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2025_srtm_rasters",
                gmw_agb_img_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hmax",
                gmw_diff_img_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_2025_diff_srtm_rasters",
                gmw_pxl_smpls_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hmax_pxl_vals",
                agb_type_name="_srtm_gmw_hmax",
                out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2025_hmax"
        )

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=60,  # The number of cores to use for analysis.
            db_info_file="pbpt_lcl_db_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = f"python {py_script}"

    process_tools_mod = "perform_analysis"
    process_tools_cls = "ProcessCmd"

    create_tools = GenCmds(
        cmd=script_cmd,
        db_conn_file="/home/pfb/.pbpt_db_conn.txt",
        lock_file_path="./pbpt_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()
