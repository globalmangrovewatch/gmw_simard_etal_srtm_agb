import rsgislib.tools.filetools
import rsgislib.vectorutils

def rm_files_size_gt(file_path:str, file_srch:str, min_size:int, rm_file:bool=False, rm_use_basename:bool=False):
    """
    A function which removes all the files from the search path which are
    greater than the specified size.

    Note, the file_path and file_srch will be merged with os.path.join.
    e.g., file_path="/hello/world", file_srch="*.txt" would result in
    "/hello/world/*.txt". Wild characters can get put in both parts if
    needed.

    :param file_path: The directory within which the files will be search for.
    :param file_srch: The search string (must have a wild card '*' for glob).
    :param min_size: the minimum valid size, above this size the files will
                     be deleted. In bytes.
    :param rm_file: If True then files will be deleted if False then a list of
                    'rm file' commands will be produced rather than the files
                    actually being deleted. (default: False)
    :param rm_use_basename: If True then all files with the same base name (i.e.,
                            same name but different file extension) within the same
                            directory will also be deleted. Useful if you have file
                            formats which have multiple files. (default: False)

    """
    file_lst = rsgislib.tools.filetools.find_files_size_limits(file_path, file_srch, min_size=min_size)
    if len(file_lst) > 0:
        for in_file in file_lst:
            if rm_file:
                if rm_use_basename:
                    rsgislib.tools.filetools.delete_file_with_basename(in_file)
                else:
                    rsgislib.tools.filetools.delete_file_silent(in_file)
            else:
                print("rm {}".format(in_file))


vec_file = "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/gmw_v3_fnl_mjr_v314.gpkg"

size_thres = 10000000


vec_lyrs = rsgislib.vectorutils.get_vec_lyrs_lst(vec_file)
for vec_lyr in vec_lyrs:
    print(vec_lyr)
    rm_files_size_gt('/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_{}_tif'.format(vec_lyr), '*.tif', size_thres, rm_file=True, rm_use_basename=True)
print("")

for vec_lyr in vec_lyrs:
    print(vec_lyr)
    rm_files_size_gt('/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/hmax_{}_tif'.format(vec_lyr), '*.tif', size_thres, rm_file=True, rm_use_basename=True)
print("")

for vec_lyr in vec_lyrs:
    print(vec_lyr)
    rm_files_size_gt('/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/hba_{}_tif'.format(vec_lyr), '*.tif', size_thres, rm_file=True, rm_use_basename=True)
print("")

for vec_lyr in vec_lyrs:
    print(vec_lyr)
    rm_files_size_gt('/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_hgt/hchm_{}_tif'.format(vec_lyr), '*.tif', size_thres, rm_file=True, rm_use_basename=True)
print("")

