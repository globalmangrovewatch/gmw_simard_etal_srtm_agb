from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os
import glob

import rsgislib.tools.filetools
import rsgislib.vectorutils

logger = logging.getLogger(__name__)

class GenTaskCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_path']):
            os.mkdir(kwargs['out_path'])

        agb_tiles = glob.glob(kwargs['agb_tiles'])
        for agb_tile in agb_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(agb_tile).replace("_agb_gmw_v314_mng_mjr_2020", "")
            cntry_img = os.path.join(kwargs['cntry_uid_dir'], "{}_cnty.kea".format(tile_base_name))

            out_file = os.path.join(kwargs['out_path'], "{}_gmw_v314_agb_stats.json".format(tile_base_name))
            if not os.path.exists(out_file):
                c_dict = dict()
                c_dict['agb_tile'] = agb_tile
                c_dict['country_ids_lut_file'] = kwargs['country_ids_lut_file']
                c_dict['cntry_img'] = cntry_img
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        self.gen_command_info(agb_tiles='/home/pete/Documents/gmw_v3_agb_hgt/gmw_srtm_mangrove_agb/agb_mng_mjr_2020_tif/*.tif',
                              cntry_uid_dir='/home/pete/Documents/gmw_v3_agb_hgt/countries/srtm_rasters',
                              country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json',
                              gmw_extent_dirs='/home/pete/Documents/gmw_v3_agb_hgt/gmw/mng_mjr_2020',
                              out_path='/home/pete/Documents/gmw_v3_agb_hgt/stats/hist_tile_stats')

        self.pop_params_db()

        self.create_shell_exe(run_script="run_exe_analysis.sh", cmds_sh_file="cmds_lst.sh", n_cores=20, db_info_file=None)


if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = "python {}".format(py_script)

    process_tools_mod = 'perform_analysis'
    process_tools_cls = 'PerformAnalysis'

    create_tools = GenTaskCmds(cmd=script_cmd, db_conn_file="/home/pete/.pbpt_db_conn.txt",
                                         lock_file_path="./gmw_agb_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
