#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_1996/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2007/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2008/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2009/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2010/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2015/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2016/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2017/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2018/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2019/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw/mng_mjr_2020/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr


