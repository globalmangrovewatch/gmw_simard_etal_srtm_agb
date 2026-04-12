from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os
import glob

import rsgislib.tools.filetools

logger = logging.getLogger(__name__)

class GenCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_path']):
            os.mkdir(kwargs['out_path'])

        srtm_tiles = glob.glob(kwargs['srtm_tiles'])
        for srtm_tile in srtm_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(srtm_tile)
            gmw_img = os.path.join(kwargs['gmw_path'], "{}_gmw_v4109_2000.tif".format(tile_base_name))
            out_img = os.path.join(kwargs['out_path'], "{}_srtm_gmw.tif".format(tile_base_name))
            cmp_file = os.path.join(kwargs['out_path'], "{}_cmp.txt".format(tile_base_name))
            if (not os.path.exists(cmp_file)) and (not os.path.exists(out_img)):
                c_dict = dict()
                c_dict['srtm_tile'] = srtm_tile
                c_dict['gmw_img'] = gmw_img
                c_dict['out_img'] = out_img
                c_dict['cmp_file'] = cmp_file
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(srtm_tiles='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/srtm/gmw_srtm_tiles/*.tif',
                              gmw_path='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw/gmw_v4109_2000_srtm_rasters',
                              out_path='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/srtm/gmw_v4109_2000_srtm_tiles')

        self.pop_params_db()

        self.create_shell_exe(
                run_script="run_exe_analysis.sh",  # The file to call to run analysis
                cmds_sh_file="pbpt_cmds_lst.sh",  # The list of commands to be run.
                n_cores=40,  # The number of cores to use for analysis.
                db_info_file="pbpt_lcl_db_info.json",
        )


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = f"python {py_script}"

    process_tools_mod = "perform_analysis"
    process_tools_cls = "PerformAnalysis"

    create_tools = GenCmds(
            cmd=script_cmd,
            db_conn_file="/home/pete/.pbpt_db_conn.txt",
            lock_file_path="./pbpt_lock_file.txt",
            process_tools_mod=process_tools_mod,
            process_tools_cls=process_tools_cls,
    )
    create_tools.parse_cmds()
