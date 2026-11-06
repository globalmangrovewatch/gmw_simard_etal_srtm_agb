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
        gmw_ext_imgs = glob.glob(kwargs["gmw_ext_imgs"])
        agb_type_name = kwargs['agb_type_name']

        tile_stats_lut = rsgislib.tools.utils.read_json_to_dict(kwargs["tile_stats_lut_file"])

        # Loop through the reference images to create the jobs
        for gmw_ext_img in gmw_ext_imgs:
            tilename = rsgislib.tools.filetools.get_file_basename(gmw_ext_img).split("_")[0]

            gmw_agb_img = os.path.join(kwargs["gmw_agb_img_dir"], f"{tilename}_{agb_type_name}.tif")

            # Create the output file name
            out_img = os.path.join(kwargs["out_dir"], f"{tilename}{agb_type_name}_gmw_2025.tif")
            # Check if the output file exists.
            if not os.path.exists(out_img):
                # You will probably have a loop here:
                # Within the loop create a dict with the parameters for each
                # job which will be added to the self.params list.
                c_dict = dict()
                c_dict["tilename"] = tilename
                c_dict["gmw_ext_img"] = gmw_ext_img
                c_dict["gmw_agb_img"] = gmw_agb_img
                c_dict["tile_stats"] = tile_stats_lut["tilename"]
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
                gmw_ext_imgs="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_all_ref_tiles_rasters/*.tif",
                gmw_agb_img_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_v4112_2000_agb",
                agb_type_name="srtm_gmw_agb",
                tile_stats_lut_file = "../04_calc_tile_stats/agb_tile_stats_gmw_v4112_fnl_combined.json",
                out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_v4112_2000_agb_filled"
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
