from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pickle
import rsgislib
import rsgislib.imagecalc

logger = logging.getLogger(__name__)


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        hist_dict = rsgislib.imagecalc.calc_histograms_for_msk_vals(self.params["srtm_tile"], 1, self.params["cnty_img"], 1, 0.5, 70, 1, msk_vals=None)

        with open(self.params["out_file"], 'wb') as out_pkl_obj:
            pickle.dump(hist_dict, out_pkl_obj, protocol=pickle.HIGHEST_PROTOCOL)

    def required_fields(self, **kwargs):
        return ["srtm_tile", "cnty_img", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_file"]] = {"type": "file"}
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_file"]):
            os.remove(self.params["out_file"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
