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

        val_tiles = glob.glob(kwargs['val_tiles'])
        for val_tile in val_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(val_tile).replace(kwargs['rplc_val'], "")
            gmw_msk = os.path.join(kwargs['gmw_msk_dir'], "{}_gmw_v314_{}.kea".format(tile_base_name, kwargs['gmw_vec_lyr']))
            out_img = os.path.join(kwargs['out_path'], "{}_agb_gmw_v314_{}.kea".format(tile_base_name, kwargs['gmw_vec_lyr']))
            if not os.path.exists(out_img):
                c_dict = dict()
                c_dict['val_tile'] = val_tile
                c_dict['gmw_msk'] = gmw_msk
                c_dict['out_img'] = out_img
                self.params.append(c_dict)

    def run_gen_commands(self):
        vec_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/gmw_v3_fnl_mjr_v314.gpkg"

        vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_file)
        for vec_lyr in vec_lyrs:
            self.gen_command_info(val_tiles='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_union_agb/*.kea',
                                  gmw_msk_dir='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/{}'.format(vec_lyr),
                                  gmw_vec_lyr=vec_lyr,
                                  rplc_val="_srtm_gmw_agb",
                                  out_name="_agb_gmw_v314_",
                                  out_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_{}'.format(vec_lyr))

        for vec_lyr in vec_lyrs:
            self.gen_command_info(val_tiles='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_union_hmax/*.kea',
                                  gmw_msk_dir='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/{}'.format(vec_lyr),
                                  gmw_vec_lyr=vec_lyr,
                                  rplc_val="_srtm_gmw_hmax",
                                  out_name="_hmax_gmw_v314_",
                                  out_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/hmax_{}'.format(vec_lyr))

        for vec_lyr in vec_lyrs:
            self.gen_command_info(val_tiles='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_union_hba/*.kea',
                                  gmw_msk_dir='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/{}'.format(vec_lyr),
                                  gmw_vec_lyr=vec_lyr,
                                  rplc_val="_srtm_gmw_hba",
                                  out_name="_hba_gmw_v314_",
                                  out_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/hba_{}'.format(vec_lyr))

        for vec_lyr in vec_lyrs:
            self.gen_command_info(val_tiles='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_union_hchm/*.kea',
                                  gmw_msk_dir='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/{}'.format(vec_lyr),
                                  gmw_vec_lyr=vec_lyr,
                                  rplc_val="_srtm_gmw_hchm",
                                  out_name="_hchm_gmw_v314_",
                                  out_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/hchm_{}'.format(vec_lyr))

        self.pop_params_db()
        self.create_slurm_sub_sh("msk_to_gmw_prods", 8224, '/scratch/a.pfb/gmw_simard_etal_srtm_agb/logs',
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
