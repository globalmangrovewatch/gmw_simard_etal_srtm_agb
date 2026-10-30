import logging
import os
import glob
import rsgislib.tools.filetools

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        # Get the list of input images
        srtm_tiles = glob.glob(kwargs["srtm_tiles"])

        # Loop through the reference images to create the jobs
        for srtm_tile in srtm_tiles:
            # Get the basename of the input file to make the output file name
            tile_base_name = rsgislib.tools.filetools.get_file_basename(srtm_tile)

            gmw_2000_img = os.path.join(
                kwargs["out_path"], f"{tile_base_name}_gmw_v4112_2000.tif"
            )
            gmw_2025_img = os.path.join(
                kwargs["out_path"], f"{tile_base_name}_gmw_v4112_2025.tif"
            )

            # Create the output file name
            out_img = os.path.join(
                kwargs["out_path"], f"{tile_base_name}_gmw_v4112_2000_2025_diff.tif"
            )
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict["gmw_2000_img"] = gmw_2000_img
                c_dict["gmw_2025_img"] = gmw_2025_img
                c_dict["out_img"] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            srtm_tiles="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/srtm/gmw_srtm_tiles/*.tif",
            gmw_2000_imgs="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_srtm_rasters",
            gmw_2025_imgs="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2025_srtm_rasters",
            out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4112_2000_2025_diff_srtm_rasters",
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
