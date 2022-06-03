from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import rsgislib
import rsgislib.imageutils
import rsgislib.vectorutils
import rsgislib.vectorutils.createrasters
import rsgislib.tools.geometrytools

logger = logging.getLogger(__name__)


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):

        img_bbox = rsgislib.imageutils.get_img_bbox(self.params["srtm_tile"])
        img_buf_bbox = rsgislib.tools.geometrytools.buffer_bbox(img_bbox, 1)

        vec_ds_obj, vec_lyr_obj = rsgislib.vectorutils.open_gdal_vec_lyr(vec_file=self.params["vec_file"], vec_lyr=self.params["vec_lyr"], readonly=True)
        vec_ds_sub_obj, vec_lyr_sub_obj = rsgislib.vectorutils.subset_envs_vec_lyr_obj(vec_lyr_obj=vec_lyr_obj, bbox=img_buf_bbox)
        vec_ds_obj = None

        rsgislib.imageutils.create_copy_img(self.params["srtm_tile"], self.params["out_img"], n_bands=1, pxl_val=0, gdalformat="KEA", datatype=rsgislib.TYPE_16INT)

        rsgislib.vectorutils.createrasters.rasterise_vec_lyr_obj(
            vec_lyr_obj=vec_lyr_sub_obj,
            output_img=self.params["out_img"],
            burn_val=1,
            att_column=self.params["vec_col"],
            thematic=False,
            no_data_val=0,
        )
        vec_ds_sub_obj = None

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
