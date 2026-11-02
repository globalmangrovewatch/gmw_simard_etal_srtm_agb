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
        data_dfs = list()
        for data_file in self.params["pxl_smpl_files"]:
            if os.path.exists(data_file):
                data_df = pandas.read_parquet(data_file)
                if len(data_df) > 0:
                    data_dfs.append(data_df)
        data_df = pandas.concat(data_dfs, ignore_index=True)
        agb_vals = data_df['agb'].values
        agb_vals = agb_vals[numpy.isfinite(agb_vals)]

        # Fit a distribution (e.g. lognormal or bounded kernel density estimate)
        # If samples are clustered/constant, calculate summary stats:
        #p_min = numpy.min(agb_vals)
        p_max = numpy.max(agb_vals)
        p_mean = numpy.mean(agb_vals)
        p_std = numpy.std(agb_vals) if numpy.std(agb_vals) > 0 else (p_mean * 0.15)

        agb_arr = rsgislib.imageutils.get_img_data_as_arr(self.params["gmw_agb_img"],  img_bands=[1])
        gmw_2025_arr = rsgislib.imageutils.get_img_data_as_arr(self.params["gmw_2025_img"], img_bands=[1])
        gmw_diff_arr = rsgislib.imageutils.get_img_data_as_arr(self.params["gmw_diff_img"], img_bands=[1])

        gmw_diff_flat = gmw_diff_arr.flatten()
        agb_flat = agb_arr.flatten()
        pxl_id = numpy.arange(gmw_diff_flat.shape[0])

        pxl_id_sub = pxl_id[gmw_diff_flat == 1]

        agb_samples = numpy.random.normal(loc=p_mean, scale=p_std, size=len(pxl_id_sub))
        agb_samples = numpy.clip(agb_samples, 0.1, p_max)
        agb_flat[pxl_id_sub] = agb_samples

        out_agb_arr = agb_flat.reshape((agb_arr.shape[1], agb_arr.shape[2]))
        out_agb_arr[gmw_2025_arr == 0] = 0

        rsgislib.imageutils.create_img_from_array_ref_img(
            data_arr = out_agb_arr, output_img = self.params["out_img"], ref_img = self.params["gmw_2025_img"], gdalformat = "GTIFF", datatype = rsgislib.TYPE_16INT, options = ["TILED=YES", "INTERLEAVE=PIXEL", "COMPRESS=DEFLATE"], no_data_val = 0.0)
        rsgislib.imageutils.pop_img_stats(self.params["out_img"], use_no_data=True, no_data_val=0,
                                          calc_pyramids=True)

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "tilename",
            "gmw_2025_img",
            "gmw_diff_img",
            "gmw_agb_img",
            "pxl_smpl_files",
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
