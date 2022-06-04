from pbprocesstools.pbpt_q_process import PBPTQProcessTool
import logging
import os
import numpy
import rsgislib
import rsgislib.tools.utils
import rsgislib.imageutils
import rsgislib.imagecalc

from rios import applier
from rios import cuiprogress

logger = logging.getLogger(__name__)


def calc_mangrove_agb(info, inputs, outputs, otherargs):
    outputs.outimage = numpy.zeros_like(inputs.hba, dtype=float)

    uniq_agb_reg = numpy.unique(inputs.agbregion)
    for agb_reg in uniq_agb_reg:
        if agb_reg > 0:
            agb_equ = otherargs.agb_lut["id"][str(agb_reg)]
            # CREATE MASK FOR AGB REGION AND NON-ZERO VALUES.
            msk = numpy.zeros_like(inputs.hba, dtype=bool)

            if (agb_equ == 'Global generic power') or (
                    agb_equ == 'East Africa generic power') or (
                    agb_equ == 'Americas generic power') or (
                    agb_equ == 'Middle East Asia generic power'):
                msk[
                    numpy.logical_and(inputs.agbregion == agb_reg, numpy.logical_not(inputs.hba == 0))] = True
            elif (agb_equ == 'Global Hmax power') or (
                    agb_equ == 'East Africa Hmax power') or (
                    agb_equ == 'Americas Hmax power'):
                msk[
                    numpy.logical_and(inputs.agbregion == agb_reg, numpy.logical_not(inputs.hmax == 0))] = True
            else:
                msk[
                    numpy.logical_and(inputs.agbregion == agb_reg, numpy.logical_not(inputs.hchm == 0))] = True

            if agb_equ == 'Global generic power':
                outputs.outimage[msk] = 3.254 * numpy.power(inputs.hba[msk], 1.5295)
            elif agb_equ == 'East Africa generic power':
                outputs.outimage[msk] = 1.066 * numpy.power(inputs.hba[msk], 2.1295)
            elif agb_equ == 'Americas generic power':
                outputs.outimage[msk] = 1.418 * numpy.power(inputs.hba[msk], 1.6038)
            elif agb_equ == 'Middle East Asia generic power':
                outputs.outimage[msk] = 1.589 * numpy.power(inputs.hba[msk], 2.0067)
            elif agb_equ == 'South East Asia generic power':
                outputs.outimage[msk] = numpy.exp(3.9042 + 0.0858 * inputs.hchm[msk])
            elif agb_equ == 'Global Hmax power':
                outputs.outimage[msk] = 2.572 * numpy.power(inputs.hmax[msk], 1.5191)
            elif agb_equ == 'East Africa Hmax power':
                outputs.outimage[msk] = 0.440 * numpy.power(inputs.hmax[msk], 2.1578)
            elif agb_equ == 'Americas Hmax power':
                outputs.outimage[msk] = 0.745 * numpy.power(inputs.hmax[msk], 1.6228)
            else:
                raise Exception("Do not recognise '{}'".format(agb_equ))

            msk = None




class PerformAnalysis(PBPTQProcessTool):
    def __init__(self):
        super().__init__(cmd_name="perform_analysis.py", descript=None)

    def do_processing(self, **kwargs):
        agb_lut = rsgislib.tools.utils.read_json_to_dict(self.params['agb_lut'])

        infiles = applier.FilenameAssociations()
        infiles.agbregion = self.params['agb_lut_img']
        infiles.hba = self.params['hba_img']
        infiles.hmax = self.params['hmax_img']
        infiles.hchm = self.params['hchm_img']
        outfiles = applier.FilenameAssociations()
        outfiles.outimage = self.params['out_img']
        otherargs = applier.OtherInputs()
        otherargs.agb_lut = agb_lut
        aControls = applier.ApplierControls()
        aControls.progress = cuiprogress.CUIProgressBar()
        aControls.drivername = 'KEA'
        aControls.omitPyramids = False
        aControls.calcStats = False

        applier.apply(calc_mangrove_agb, infiles, outfiles, otherargs, controls=aControls)
        rsgislib.imageutils.pop_img_stats(self.params['out_img'], use_no_data=True, no_data_val=0, calc_pyramids=True)

    def required_fields(self, **kwargs):
        return ["srtm_tile", "agb_lut_img", "hba_img", "hchm_img", "hmax_img", "agb_lut", "out_img"]

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
