from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imageutils

logger = logging.getLogger(__name__)


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imageutils.mask_img(self.params["agb_tile"], self.params["gmw_msk"], self.params["out_img"], "KEA", rsgislib.TYPE_32FLOAT, 0, 0)
        rsgislib.imageutils.pop_img_stats(self.params["out_img"], use_no_data=True, no_data_val=0, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["val_tile", "gmw_msk", "out_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_img"]] = {
            "type": "gdal_image",
            "n_bands": 1,
            "chk_proj": True,
            "epsg_code": 4326,
            "read_img": True,
            "calc_chk_sum": True,
        }
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_img"]):
            os.remove(self.params["out_img"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
