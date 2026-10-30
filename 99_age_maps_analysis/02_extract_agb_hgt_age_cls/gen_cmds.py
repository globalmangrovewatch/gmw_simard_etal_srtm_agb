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
            basename = rsgislib.tools.filetools.get_file_basename(agb_img).replace("_srtm_gmw_agb", "")

            gmw_msk_img = os.path.join(kwargs["gmw_ext_imgs"], f"{basename}_gmw_v4109_2000.tif")
            hgt_img = os.path.join(kwargs['hgt_imgs'], f"{basename}_srtm_gmw_hmax.tif")
            age_img = os.path.join(kwargs['age_imgs'], f"{basename}_srtm_gmw_v4019_2000_age_map.tif")

            # Create the output file name
            out_h5_file = os.path.join(kwargs["out_dir"], f"{basename}_gmw_v4109_agb_hgt_age.h5")
            # Check if the output file exists.
            if not os.path.exists(out_h5_file):
                # You will probably have a loop here:
                # Within the loop create a dict with the parameters for each
                # job which will be added to the self.params list.
                c_dict = dict()
                c_dict["gmw_msk_img"] = gmw_msk_img
                c_dict["agb_img"] = agb_img
                c_dict["hgt_img"] = hgt_img
                c_dict["age_img"] = age_img
                c_dict["out_h5_file"] = out_h5_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            agb_imgs="/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_v4109_2000_agb/*.tif",
            gmw_ext_imgs='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4109_2000_srtm_rasters',
            age_imgs="/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/age_maps/gmw_v4109_2000_age",
            hgt_imgs='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4109_2000_hmax',
            out_dir="/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_v4109_2000_extracted"
        )

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=30,  # The number of cores to use for analysis.
            db_info_file="pbpt_lcl_db_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = f"python {py_script}"

    process_tools_mod = "perform_analysis"
    process_tools_cls = "ProcessCmd"

    create_tools = GenCmds(
        cmd=script_cmd,
        db_conn_file="/home/pete/.pbpt_db_conn.txt",
        lock_file_path="./pbpt_lock_file.txt",
        process_tools_mod=process_tools_mod,
        process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()
