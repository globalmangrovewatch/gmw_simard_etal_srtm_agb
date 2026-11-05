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
        agb_imgs = glob.glob(kwargs["agb_imgs"])

        # Loop through the reference images to create the jobs
        for agb_img in agb_imgs:
            # Get the basename of the input file to make the output file name
            basename = rsgislib.tools.filetools.get_file_basename(agb_img)

            # Create the output file name
            out_pd_file = os.path.join(kwargs["out_dir"], f"{basename}_pxl_vals.parquet.gz")
            # Check if the output file exists.
            if not os.path.exists(out_pd_file):
                # You will probably have a loop here:
                # Within the loop create a dict with the parameters for each
                # job which will be added to the self.params list.
                c_dict = dict()
                c_dict["agb_img"] = agb_img
                c_dict["out_pd_file"] = out_pd_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            agb_imgs='/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hba/*.tif',
            out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hba_pxl_vals"
        )

        self.gen_command_info(
                agb_imgs='/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hchm/*.tif',
                out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hchm_pxl_vals"
        )

        self.gen_command_info(
                agb_imgs='/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hmax/*.tif',
                out_dir="/bigdata/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4112_2000_hmax_pxl_vals"
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
