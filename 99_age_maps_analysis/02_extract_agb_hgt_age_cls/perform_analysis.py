import logging
import os

import rsgislib.imageutils
import rsgislib.zonalstats
from pbprocesstools.pbpt_q_process import PBPTQProcessTool

logger = logging.getLogger(__name__)


class ProcessCmd(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        in_img_info = list()
        in_img_info.append(
                rsgislib.imageutils.ImageBandInfo(
                        file_name=self.params["age_img"],
                        name="age",
                        bands=[1],
                )
        )
        in_img_info.append(
                rsgislib.imageutils.ImageBandInfo(
                        file_name=self.params["agb_img"],
                        name="agb",
                        bands=[1],
                )
        )
        in_img_info.append(
                rsgislib.imageutils.ImageBandInfo(
                        file_name=self.params["hgt_img"],
                        name="hgt",
                        bands=[1],
                )
        )

        rsgislib.zonalstats.extract_zone_img_band_values_to_hdf(
                in_img_info=in_img_info,
                in_msk_img=self.params["gmw_msk_img"],
                out_h5_file=self.params["out_h5_file"],
                mask_val=1,
                datatype=rsgislib.TYPE_32FLOAT,
        )

    def required_fields(self, **kwargs):
        # Return a list of the required fields which will be checked
        return [
            "gmw_msk_img",
            "agb_img",
            "hgt_img",
            "age_img",
            "out_h5_file",
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
        files_dict[self.params["out_h5_file"]] = "hdf5"
        return self.check_files(files_dict)

    def remove_outputs(self, **kwargs):
        # Remove the output files and reset anything
        # else which might need to be reset if re-running the job.
        if os.path.exists(self.params["out_h5_file"]):
            os.remove(self.params["out_h5_file"])


if __name__ == "__main__":
    ProcessCmd().std_run()
