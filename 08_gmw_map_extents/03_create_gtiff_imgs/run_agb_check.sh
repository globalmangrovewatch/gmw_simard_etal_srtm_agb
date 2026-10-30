#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_1996_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2007_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2008_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2009_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2010_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2015_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2016_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2017_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2018_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2019_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/agb_mng_mjr_2020_tif/*.tif" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr


