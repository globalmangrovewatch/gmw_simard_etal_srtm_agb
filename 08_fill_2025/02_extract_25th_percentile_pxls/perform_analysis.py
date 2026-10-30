import logging
import os

import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils

import numpy

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        percent25th = rsgislib.imagecalc.calc_band_percentile(self.params["agb_img"], percentile=0.25, no_data_val=0.0)[0]
        print(percent25th)

        img_bbox = rsgislib.imageutils.get_img_bbox(self.params["agb_img"])
        tlX = img_bbox[0]
        tlY = img_bbox[3]
        x_res, y_res = rsgislib.imageutils.get_img_res(self.params["agb_img"], abs_vals = True)
        agb_arr = rsgislib.imageutils.get_img_data_as_arr(self.params["agb_img"], img_bands = [1])
        agb_arr_shp = agb_arr.shape
        print(agb_arr_shp)

        ncols = agb_arr_shp[1]
        nrows = agb_arr_shp[2]

        print(f"ncols = {ncols}")
        print(f"nrows = {nrows}")

        x_coords = tlX + numpy.arange(ncols) * x_res
        y_coords = tlY - numpy.arange(nrows) * y_res

        # Create 2D coordinate grids
        x_grid, y_grid = numpy.meshgrid(x_coords, y_coords)

        # Resulting shapes: (1500, 1000)
        print(x_grid.shape)  # (1500, 1000)
        print(y_grid.shape)  # (1500, 1000)

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "agb_img",
            "out_pd_file",
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
        files_dict[self.params["out_pd_file"]] = "filesize"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["out_pd_file"]):
            os.remove(self.params["out_pd_file"])


if __name__ == "__main__":
    ProcessCmd().std_run()
