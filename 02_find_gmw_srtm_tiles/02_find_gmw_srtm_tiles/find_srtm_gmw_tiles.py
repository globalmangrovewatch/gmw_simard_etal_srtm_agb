from typing import List
import os
#import rsgislib.imageutils.imagelut
import rsgislib.tools.utils
import rsgislib.vectorutils
import rsgislib
import osgeo.ogr as ogr


def get_att_lst_select_feats_lyr_objs(
    vec_lyr_obj: ogr.Layer, att_names: list, vec_sel_lyr_obj: ogr.Layer
) -> list:
    """
    Function to get a list of attribute values from features which intersect
    with the select layer.

    :param vec_lyr_obj: the OGR layer object from which the attribute data comes from.
    :param att_names: a list of attribute names to be outputted.
    :param vec_sel_lyr_obj: the OGR layer object which will be intersected within
                            the vector file.
    :return: list of dictionaries with the output values.

    """

    att_vals = []
    try:
        if vec_lyr_obj is None:
            raise rsgislib.RSGISPyException(
                "The vector layer passed into the function was None."
            )

        if vec_sel_lyr_obj is None:
            raise rsgislib.RSGISPyException(
                "The select vector layer passed into the function was None."
            )

        lyrDefn = vec_lyr_obj.GetLayerDefn()
        feat_idxs = dict()
        feat_types = dict()
        found_atts = dict()
        for attName in att_names:
            found_atts[attName] = False

        for i in range(lyrDefn.GetFieldCount()):
            if lyrDefn.GetFieldDefn(i).GetName() in att_names:
                attName = lyrDefn.GetFieldDefn(i).GetName()
                feat_idxs[attName] = i
                feat_types[attName] = lyrDefn.GetFieldDefn(i).GetType()
                found_atts[attName] = True

        for attName in att_names:
            if not found_atts[attName]:
                raise rsgislib.RSGISPyException(
                    "Could not find the attribute ({}) specified within "
                    "the vector layer.".format(attName)
                )

        mem_driver = ogr.GetDriverByName("MEMORY")

        mem_result_ds = mem_driver.CreateDataSource("MemResultData")
        mem_result_lyr = mem_result_ds.CreateLayer(
            "MemResultLyr", geom_type=vec_lyr_obj.GetGeomType()
        )

        for attName in att_names:
            mem_result_lyr.CreateField(ogr.FieldDefn(attName, feat_types[attName]))

        vec_sel_lyr_obj.Intersection(vec_lyr_obj, mem_result_lyr)

        # loop through the input features
        reslyrDefn = mem_result_lyr.GetLayerDefn()
        inFeat = mem_result_lyr.GetNextFeature()
        outvals = []
        while inFeat:
            outdict = dict()
            for attName in att_names:
                feat_idx = reslyrDefn.GetFieldIndex(attName)
                if feat_types[attName] == ogr.OFTString:
                    outdict[attName] = inFeat.GetFieldAsString(feat_idx)
                elif feat_types[attName] == ogr.OFTReal:
                    outdict[attName] = inFeat.GetFieldAsDouble(feat_idx)
                elif feat_types[attName] == ogr.OFTInteger:
                    outdict[attName] = inFeat.GetFieldAsInteger(feat_idx)
                else:
                    outdict[attName] = inFeat.GetField(feat_idx)
            outvals.append(outdict)
            inFeat = mem_result_lyr.GetNextFeature()

        mem_result_ds = None
    except Exception as e:
        raise e
    return outvals



def query_file_lut(
    lut_db_file: str,
    lyr_name: str,
    roi_file: str,
    roi_lyr: str,
    out_dest: str,
    targz_out: bool=False,
    cp_cmds: bool=False,
) -> List[str]:
    """
    A function which allows the file LUT to be queried (intersection) and commands
    generated for completing operations. Must select (pass true) for either targz_out
    or cp_cmds not both. If both are False then the list of intersecting files will
    be returned.

    :param lut_db_file: OGR vector file with the LUT.
    :param lyr_name: name of the layer within the LUT file.
    :param roi_file: region of interest OGR vector file.
    :param roi_lyr: layer name within the ROI file.
    :param out_dest: the destination for outputs from command (e.g., where are the
                     files to be copied to or output file name for tar.gz file.
    :param targz_out: boolean which specifies that the command for generating
                      a tar.gz file should be generated.
    :param cp_cmds: boolean which specifies that the command for copying the
                    LUT files to a out_dest should be generated.

    :return: returns a list of commands to be executed.

    """
    if lyr_name is None:
        lyr_name = os.path.splitext(os.path.basename(lut_db_file))[0]

    if roi_lyr is None:
        roi_lyr = os.path.splitext(os.path.basename(roi_file))[0]

    roi_mem_ds, roi_mem_lyr = rsgislib.vectorutils.read_vec_lyr_to_mem(
        roi_file, roi_lyr
    )

    roi_bbox = roi_mem_lyr.GetExtent(True)

    lut_mem_ds, lut_mem_lyr = rsgislib.vectorutils.get_mem_vec_lyr_subset(
        lut_db_file, lyr_name, roi_bbox
    )

    file_list_dict = get_att_lst_select_feats_lyr_objs(
        lut_mem_lyr, ["path", "filename"], roi_mem_lyr
    )

    out_cmds = []
    if targz_out:
        cmd = "tar -czf {}".format(out_dest)
        for file_item in file_list_dict:
            file_path = os.path.join(file_item["path"], file_item["filename"])
            cmd = "{} {}".format(cmd, file_path)
        out_cmds.append(cmd)
    elif cp_cmds:
        for file_item in file_list_dict:
            file_path = os.path.join(file_item["path"], file_item["filename"])
            out_cmds.append("cp {0} {1}".format(file_path, out_dest))
    else:
        for file_item in file_list_dict:
            file_path = os.path.join(file_item["path"], file_item["filename"])
            out_cmds.append(file_path)

    return out_cmds





srtm_lut_file = "./srtm_tiles_lut.gpkg"
gmw_lut_file = "./gmw_union_tiles_lut.gpkg"


cp_cmds = query_file_lut(
    lut_db_file=srtm_lut_file,
    lyr_name="srtm_tiles",
    roi_file=gmw_lut_file,
    roi_lyr="gmw_tiles",
    out_dest="/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/gmw_kea",
    targz_out=False,
    cp_cmds=True,
)

cp_cmds_set = set(cp_cmds)
cp_cmds_lst = list(cp_cmds_set)

rsgislib.tools.utils.write_list_to_file(cp_cmds_lst, "cp_gmw_srtm_tiles.sh")

