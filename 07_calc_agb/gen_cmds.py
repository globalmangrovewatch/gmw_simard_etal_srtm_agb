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
            tile_base_name = tile_base_name.replace("_95thp_thresholded", "")
            tile_name = tile_base_name.replace("_srtm_gmw", "")

            agb_lut_img = os.path.join(kwargs['agb_lut_path'], "{}_allom.tif".format(tile_name))
            hba_img = os.path.join(kwargs['hba_path'], "{}_hba.tif".format(tile_base_name))
            hchm_img = os.path.join(kwargs['hchm_path'], "{}_hchm.tif".format(tile_base_name))
            hmax_img = os.path.join(kwargs['hmax_path'], "{}_hmax.tif".format(tile_base_name))

            out_img = os.path.join(kwargs['out_path'], "{}_agb.tif".format(tile_base_name))
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict['srtm_tile'] = srtm_tile
                c_dict['agb_lut_img'] = agb_lut_img
                c_dict['hba_img'] = hba_img
                c_dict['hchm_img'] = hchm_img
                c_dict['hmax_img'] = hmax_img
                c_dict['agb_lut'] = kwargs['agb_lut']
                c_dict['out_img'] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(srtm_tiles='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/srtm/srtm_95th_percent_thresholded/*.tif',
                              agb_lut_path='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/countries/agb_allom_rasters',
                              hba_path='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4109_2000_hba',
                              hchm_path='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4109_2000_hchm',
                              hmax_path='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_v4109_2000_hmax',
                              agb_lut='../03_define_country_extents/01_define_country_ids/allom_id_lut.json',
                              out_path='/bigdata/petebunting/GlobalMangroveWatch/gmw_blue_carbon_v4_ext/simard_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_v4109_2000_agb')

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
