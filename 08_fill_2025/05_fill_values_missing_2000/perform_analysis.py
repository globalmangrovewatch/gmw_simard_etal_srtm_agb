import logging
import os
import pandas
import numpy
import rsgislib.imageutils
import numpy.random

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        tile_stats = self.params["tile_stats"]

        p_mean = tile_stats["mean"]
        p_std = tile_stats["std"]
        p_max = p_mean * (2 * p_std)

        gmw_ext_arr = rsgislib.imageutils.get_img_data_as_arr(self.params["gmw_ext_img"], img_bands=[1])
        if os.path.exists(self.params["gmw_agb_img"]):
            agb_arr = rsgislib.imageutils.get_img_data_as_arr(self.params["gmw_agb_img"],  img_bands=[1])
        else:
            agb_arr = numpy.zeros_like(gmw_ext_arr)


        gmw_ext_flat = gmw_ext_arr.flatten()
        agb_flat = agb_arr.flatten()
        pxl_id = numpy.arange(gmw_ext_flat.shape[0])

        pxl_id_sub = pxl_id[numpy.logical_and(gmw_ext_flat == 1, agb_flat < 1)]

        agb_samples = numpy.random.normal(loc=p_mean, scale=p_std, size=len(pxl_id_sub))
        agb_samples = numpy.clip(agb_samples, 5, p_max)
        agb_flat[pxl_id_sub] = agb_samples

        out_agb_arr = numpy.expand_dims(agb_flat.reshape((agb_arr.shape[1], agb_arr.shape[2])), axis=0)
        out_agb_arr[gmw_ext_arr == 0] = 0

        rsgislib.imageutils.create_img_from_array_ref_img(
            data_arr = out_agb_arr, output_img = self.params["out_img"], ref_img = self.params["gmw_ext_img"], gdalformat = "GTIFF", datatype = rsgislib.TYPE_16INT, options = ["TILED=YES", "INTERLEAVE=PIXEL", "COMPRESS=DEFLATE"], no_data_val = 0.0)
        rsgislib.imageutils.pop_img_stats(self.params["out_img"], use_no_data=True, no_data_val=0,
                                          calc_pyramids=True)

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "tilename",
            "gmw_ext_img",
            "gmw_agb_img",
            "tile_stats",
            "out_img",
        ]

    def outputs_present(self, **kwargs):
        # Check the output files are as expected - called with --check option
        # the function expects a tuple with the first item a list of booleans
        # specifying whether the file is OK and secondly a dict with outputs
        # as keys and any error message as the value

        # A function (self.check_files) has been provided to do the work for
        # you which takes a dict of inputs which will do the work for you in
        # most cases. The supported file types are: gdal_image, gdal_vector,
        # hdf5, file (checks present) and filesize (checks present and size > 0)

        files_dict = dict()
        files_dict[self.params["out_img"]] = "gdal_image"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["out_img"]):
            os.remove(self.params["out_img"])


if __name__ == "__main__":
    ProcessCmd().std_run()
