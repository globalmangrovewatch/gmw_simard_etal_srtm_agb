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

        rsgislib.imagecalc.band_math(self.params["out_hba_img"], 'srtm<0.5?0:1.0754*srtm', 'KEA', rsgislib.TYPE_32FLOAT, band_defns)
        rsgislib.imageutils.pop_img_stats(self.params['out_hba_img'], use_no_data=True, no_data_val=0, calc_pyramids=True)

        rsgislib.imagecalc.band_math(self.params["out_hchm_img"], 'srtm<0.5?0:2.7191*srtm^0.676', 'KEA', rsgislib.TYPE_32FLOAT, band_defns)
        rsgislib.imageutils.pop_img_stats(self.params['out_hchm_img'], use_no_data=True, no_data_val=0, calc_pyramids=True)

        rsgislib.imagecalc.band_math(self.params["out_hmax_img"], 'srtm<0.5?0:1.697*srtm', 'KEA', rsgislib.TYPE_32FLOAT, band_defns)
        rsgislib.imageutils.pop_img_stats(self.params['out_hmax_img'], use_no_data=True, no_data_val=0, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["srtm_tile", "out_hba_img", "out_hchm_img", "out_hmax_img"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_hba_img"]] = {
            "type": "gdal_image",
            "n_bands": 1,
            "chk_proj": True,
            "epsg_code": 4326,
            "read_img": True,
            "calc_chk_sum": True,
        }
        files_dict[self.params["out_hchm_img"]] = {
            "type": "gdal_image",
            "n_bands": 1,
            "chk_proj": True,
            "epsg_code": 4326,
            "read_img": True,
            "calc_chk_sum": True,
        }
        files_dict[self.params["out_hmax_img"]] = {
            "type": "gdal_image",
            "n_bands": 1,
            "chk_proj": True,
            "epsg_code": 4326,
            "read_img": True,
            "calc_chk_sum": True,
        }
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_hba_img"]):
            os.remove(self.params["out_hba_img"])

        if os.path.exists(self.params["out_hchm_img"]):
            os.remove(self.params["out_hchm_img"])

        if os.path.exists(self.params["out_hmax_img"]):
            os.remove(self.params["out_hmax_img"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
