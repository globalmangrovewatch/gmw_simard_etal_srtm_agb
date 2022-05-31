from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.vectorutils.createrasters

logger = logging.getLogger(__name__)


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        rsgislib.vectorutils.createrasters.rasterise_vec_lyr(
            vec_file=self.params["vec_file"],
            vec_lyr=self.params["vec_lyr"],
            input_img=self.params["srtm_tile"],
            output_img=self.params["out_img"],
            gdalformat="KEA",
            burn_val=1,
            datatype=rsgislib.TYPE_8UINT,
            att_column=self.params["vec_col"],
            thematic=True,
            no_data_val=0,
        )

    def required_fields(self, **kwargs):
        return ["srtm_tile", "vec_file", "vec_lyr", "vec_col", "out_img"]

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
