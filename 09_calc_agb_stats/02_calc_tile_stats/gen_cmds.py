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
            tile_base_name = rsgislib.tools.filetools.get_file_basename(agb_tile).replace("_srtm_gmw_agb", "")
            cntry_img = os.path.join(kwargs['cntry_uid_dir'], "{}_cnty.kea".format(tile_base_name))
            pxl_area_img = os.path.join(kwargs['pxl_area_dir'], "{}_pxl_area.kea".format(tile_base_name))
            gmw_ext_imgs = dict()
            for gmw_ext in kwargs['gmw_extent_dirs']:
                year = gmw_ext.split("_")[-1]
                gmw_ext_img = os.path.join(kwargs['gmw_extent_dirs'][gmw_ext], "{}_gmw_v314_{}.kea".format(tile_base_name, gmw_ext))
                gmw_ext_imgs[year] = gmw_ext_img

            out_file = os.path.join(kwargs['out_path'], "{}_gmw_v314_agb_stats.json".format(tile_base_name))
            if not os.path.exists(out_file):
                c_dict = dict()
                c_dict['agb_tile'] = agb_tile
                c_dict['country_ids_lut_file'] = kwargs['country_ids_lut_file']
                c_dict['cntry_img'] = cntry_img
                c_dict['pxl_area_img'] = pxl_area_img
                c_dict['gmw_ext_imgs'] = gmw_ext_imgs
                c_dict['out_file'] = out_file
                self.params.append(c_dict)

    def run_gen_commands(self):
        vec_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/gmw_v3_fnl_mjr_v314.gpkg"

        vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_file)
        gmw_extent_dirs = dict()
        for vec_lyr in vec_lyrs:
            gmw_extent_dirs[vec_lyr] = '/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/{}'.format(vec_lyr)

        self.gen_command_info(agb_tiles='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_union_agb/*.kea',
                              cntry_uid_dir='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/countries/srtm_rasters',
                              country_ids_lut_file='../../03_define_country_extents/01_define_country_ids/country_ids_lut.json',
                              pxl_area_dir='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/stats/pxl_area',
                              gmw_extent_dirs=gmw_extent_dirs,
                              out_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/stats/tile_stats')

        self.pop_params_db()
        self.create_slurm_sub_sh("calc_agb_stats", 8224, '/scratch/a.pfb/gmw_simard_etal_srtm_agb/logs',
                                 run_script='run_exe_analysis.sh', job_dir="job_scripts",
                                 db_info_file="db_info_run_file.txt", account_name='scw1376',
                                 n_cores_per_job=10, n_jobs=10, job_time_limit='2-23:59',
                                 module_load='module load parallel singularity\n\nexport http_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\nexport https_proxy="http://a.pfb:proxy101019@10.212.63.246:3128"\n')

if __name__ == "__main__":
    py_script = os.path.abspath("perform_analysis.py")
    script_cmd = "singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python {}".format(py_script)

    process_tools_mod = 'perform_analysis'
    process_tools_cls = 'PerformAnalysis'

    create_tools = GenTaskCmds(cmd=script_cmd, db_conn_file="/home/a.pfb/gmw_gap_fill_db/pbpt_db_conn.txt",
                                         lock_file_path="./gmw_agb_lock_file.txt",
                                         process_tools_mod=process_tools_mod, process_tools_cls=process_tools_cls)
    create_tools.parse_cmds()
