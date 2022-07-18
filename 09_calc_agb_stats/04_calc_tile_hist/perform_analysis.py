from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import numpy
import osgeo.gdal as gdal
import rsgislib.tools.utils

logger = logging.getLogger(__name__)


def calc_unq_val_pxl_areas(vals_img, uid_img, unq_val_area_lut):
    img_vals_ds = gdal.Open(vals_img)
    if img_vals_ds is None:
        raise Exception("Could not open the values input image: '{}'".format(uid_img))
    img_vals_band = img_vals_ds.GetRasterBand(1)
    if img_vals_band is None:
        raise Exception("Failed to read the values image band: '{}'".format(uid_img))
    vals_arr = img_vals_band.ReadAsArray()
    img_vals_ds = None

    img_uid_ds = gdal.Open(uid_img)
    if img_uid_ds is None:
        raise Exception("Could not open the UID input image: '{}'".format(uid_img))
    img_uid_band = img_uid_ds.GetRasterBand(1)
    if img_uid_band is None:
        raise Exception("Failed to read the UID image band: '{}'".format(uid_img))
    uid_arr = img_uid_band.ReadAsArray()
    img_uid_ds = None

    unq_pix_vals = numpy.unique(uid_arr)

    for unq_val in unq_pix_vals:
        if unq_val != 0:
            msk = numpy.zeros_like(uid_arr, dtype=bool)
            msk[(uid_arr == unq_val) & (uid_arr > 0) & (vals_arr > 0)] = True

            if numpy.sum(msk) > 0:
                vals_unq_val_arr = vals_arr[msk].flatten()
                print(vals_unq_val_arr.shape)
                vals_hist, bin_edges = numpy.histogram(vals_unq_val_arr, bins=71, range=(0, 71))
                print(bin_edges)
                print(vals_hist.shape)
                print(unq_val_area_lut[unq_val].shape)
                unq_val_area_lut[unq_val] = unq_val_area_lut[unq_val] + vals_hist


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        unq_vals = rsgislib.tools.utils.read_json_to_dict(self.params['country_ids_lut_file'])["val"].keys()

        tile_stats_lut = dict()

        lut_vals = dict()
        for val in unq_vals:
            val = int(val)
            lut_vals[val] = numpy.zeros((100), dtype=numpy.uint32)

        calc_unq_val_pxl_areas(self.params["agb_tile"], self.params["cntry_img"], lut_vals)

        rsgislib.tools.utils.write_dict_to_json(lut_vals, self.params["out_file"])


    def required_fields(self, **kwargs):
        return ["agb_tile", "country_ids_lut_file", "cntry_img", "out_file"]

    def outputs_present(self, **kwargs):
        files_dict = dict()
        files_dict[self.params["out_file"]] = {"type": "file"}
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        if os.path.exists(self.params["out_file"]):
            os.remove(self.params["out_file"])


if __name__ == "__main__":
    PerformAnalysis().std_run()
