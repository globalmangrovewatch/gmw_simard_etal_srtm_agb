import glob
import os
import rsgislib.tools.filetools

out_base_dir = '/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/hgt'
input_files = glob.glob('/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/srtm/raw/*.zip')
for in_file in input_files:
    tile = os.path.basename(in_file).split('.')[0]
    print(tile)
    out_dir = os.path.join(out_base_dir, tile)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    rsgislib.tools.filetools.unzip_file(in_file, out_dir)


