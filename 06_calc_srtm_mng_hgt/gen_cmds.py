from pbprocesstools.pbpt_q_process import PBPTGenQProcessToolCmds

import logging
import os
import glob

import rsgislib.tools.filetools

logger = logging.getLogger(__name__)

class GenTaskCmds(PBPTGenQProcessToolCmds):

    def gen_command_info(self, **kwargs):
        if not os.path.exists(kwargs['out_path']):
            os.mkdir(kwargs['out_path'])

        srtm_tiles = glob.glob(kwargs['srtm_tiles'])
        for srtm_tile in srtm_tiles:
            tile_base_name = rsgislib.tools.filetools.get_file_basename(srtm_tile)
            tile_base_name = tile_base_name.replace("_95thp_thresholded", "")
            out_hba_img = os.path.join(kwargs['out_hba_path'], "{}_hba.kea".format(tile_base_name))
            out_hchm_img = os.path.join(kwargs['out_hchm_path'], "{}_hchm.kea".format(tile_base_name))
            out_hmax_img = os.path.join(kwargs['out_hmax_path'], "{}_hmax.kea".format(tile_base_name))
            if (not os.path.exists(out_hba_img)) or (not os.path.exists(out_hchm_img)) or (not os.path.exists(out_hmax_img)):
                c_dict = dict()
                c_dict['srtm_tile'] = srtm_tile
                c_dict['out_hba_img'] = out_hba_img
                c_dict['out_hchm_img'] = out_hchm_img
                c_dict['out_hmax_img'] = out_hmax_img
                self.params.append(c_dict)

    def run_gen_commands(self):

        self.gen_command_info(srtm_tiles='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/srtm_95thpercent/*.kea',
                              out_hba_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_union_hba',
                              out_hchm_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_union_hchm',
                              out_hmax_path='/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/gmw_union_hmax')


        self.pop_params_db()
        self.create_slurm_sub_sh("apply_95th_percent", 8224, '/scratch/a.pfb/gmw_simard_etal_srtm_agb/logs',
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
