from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.tools.utils
import rsgislib.tools.filetools

logger = logging.getLogger(__name__)


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        if os.path.exists(self.params['tif_img']):
            match, prop_diff = rsgislib.imagecalc.are_imgs_equal(self.params['img_tile'], self.params['tif_img'], prop_eql=1.0, flt_dif=0.01)
            if not match:
                rsgislib.tools.filetools.delete_file_with_basename(self.params['tif_img'])
            else:
                match_info = dict()
                match_info['match'] = match
                match_info['prop_diff'] = float(prop_diff)
                rsgislib.tools.utils.write_dict_to_json(match_info, self.params['out_file'])

    def required_fields(self, **kwargs):
        return ["img_tile", "tif_img", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_file"]] = 'file'
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_file"]):
            os.remove(self.params["out_file"])

if __name__ == "__main__":
    PerformAnalysis().std_run()
