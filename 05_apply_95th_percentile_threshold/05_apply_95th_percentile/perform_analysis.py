from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imageutils
import rsgislib.imagecalc

logger = logging.getLogger(__name__)


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        band_defns = list()
        band_defns.append(rsgislib.imagecalc.BandDefn('srtm', self.params["srtm_tile"], 1))
        band_defns.append(rsgislib.imagecalc.BandDefn('thres', self.params["percent95th_img"], 1))
        rsgislib.imagecalc.band_math(self.params["out_img"], 'srtm>thres?thres:srtm', 'KEA', rsgislib.TYPE_16INT, band_defns)

        rsgislib.imageutils.pop_img_stats(self.params['out_img'], use_no_data=True, no_data_val=-32768, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["srtm_tile", "percent95th_img", "out_img"]

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
