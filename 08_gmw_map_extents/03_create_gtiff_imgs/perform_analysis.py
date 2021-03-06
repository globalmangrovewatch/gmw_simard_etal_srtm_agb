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
        options = (
            "-co TILED=YES -co INTERLEAVE=PIXEL -co BLOCKXSIZE=256 "
            "-co BLOCKYSIZE=256 -co COMPRESS=LZW -co BIGTIFF=YES "
            "-co COPY_SRC_OVERVIEWS=YES"
        )
        rsgislib.imageutils.gdal_translate(self.params["img_tile"], self.params["out_img"], gdalformat='GTIFF', options=options)

    def required_fields(self, **kwargs):
        return ["img_tile", "out_img"]

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
