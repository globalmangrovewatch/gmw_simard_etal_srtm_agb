from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import pathlib
import rsgislib
import rsgislib.imageutils
import rsgislib.imagecalc

logger = logging.getLogger(__name__)


class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        rsgislib.imageutils.set_env_vars_lzw_gtiff_outs()

        gmw_count = rsgislib.imagecalc.count_pxls_of_val(input_img=self.params["gmw_img"], vals=[1])[0]
        print(f"gmw_count: {gmw_count}")
        if gmw_count > 0:
            band_defns = list()
            band_defns.append(rsgislib.imagecalc.BandDefn(band_name='gmw', input_img=self.params["gmw_img"], img_band=1))
            band_defns.append(rsgislib.imagecalc.BandDefn(band_name='srtm', input_img=self.params["srtm_tile"], img_band=1))
            rsgislib.imagecalc.band_math(output_img=self.params['out_img'], exp='(gmw == 1) && (srtm > 0) && (srtm < 80)?srtm:-32768', gdalformat='GTIFF', datatype=rsgislib.TYPE_16INT, band_defs=band_defns)
            rsgislib.imageutils.pop_img_stats(self.params['out_img'], use_no_data=True, no_data_val=-32768, calc_pyramids=True)

        pathlib.Path(self.params['cmp_file']).touch()

    def required_fields(self, **kwargs):
        return ["srtm_tile", "gmw_img", "out_img", "cmp_file"]

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
