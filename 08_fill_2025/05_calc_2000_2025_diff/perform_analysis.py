import logging
import os
import rsgislib
import rsgislib.imagecalc
import rsgislib.imageutils

from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        band_defns = list()
        band_defns.append(
            rsgislib.imagecalc.BandDefn(
                band_name="y2000", input_img=self.params["gmw_2000_img"], img_band=1
            )
        )
        band_defns.append(
            rsgislib.imagecalc.BandDefn(
                band_name="y2025", input_img=self.params["gmw_2025_img"], img_band=1
            )
        )
        rsgislib.imagecalc.band_math(
            output_img=self.params["out_img"],
            exp="(y2000==0) && (y2025==1)?1:0",
            gdalformat="GTIFF",
            datatype=rsgislib.TYPE_8UINT,
            band_defs=band_defns,
        )
        rsgislib.imageutils.pop_thmt_img_stats(self.params["out_img"], add_clr_tab = True, calc_pyramids = True, ignore_zero = True)

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "gmw_2000_img",
            "gmw_2025_img",
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
