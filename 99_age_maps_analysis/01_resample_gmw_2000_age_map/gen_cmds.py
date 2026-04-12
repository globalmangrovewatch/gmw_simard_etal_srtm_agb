import logging
import os
import glob
import rsgislib.tools.filetools

from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

logger = logging.getLogger(__name__)


class GenCmds(PBPTGenQProcessToolCmds):
    def gen_command_info(self, **kwargs):
        print("** This function needs implementing! **")

        # Create output directory if it doesn't exist.
        if not os.path.exists(kwargs["out_dir"]):
            os.mkdir(kwargs["out_dir"])

        # Get the list of input images
        ref_imgs = glob.glob(kwargs["ref_imgs"])

        # Loop through the reference images to create the jobs
        for ref_img in ref_imgs:
            # Get the basename of the input file to make the output file name
            basename = rsgislib.tools.filetools.get_file_basename(ref_img)

            # Create the output file name
            output_file = os.path.join(kwargs["out_dir"], f"{basename}.tif")
            # Check if the output file exists.
            if not os.path.exists(output_file):
                # You will probably have a loop here:
                # Within the loop create a dict with the parameters for each
                # job which will be added to the self.params list.
                c_dict = dict()
                c_dict["input1"] = ""
                c_dict["input2"] = ""
                c_dict["input3"] = ""
                c_dict["output1"] = ""
                self.params.append(c_dict)

    def run_gen_commands(self):
        # Could Pass info to gen_command_info function
        # (e.g., input / output directories)
        self.gen_command_info(
            ref_imgs="path/to/inputs/*.kea", out_dir="/path/to/outputs"
        )

        self.pop_params_db()

        self.create_shell_exe(
            run_script="run_exe_analysis.sh",  # The file to call to run analysis
            cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
            n_cores=10,  # The number of cores to use for analysis.
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

