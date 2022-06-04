#singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb /scratch/a.pfb/sw_imgs/au-eoed-dev.sif python gen_cmds.py --check

singularity exec --bind /scratch/a.pfb:/scratch/a.pfb --bind /home/a.pfb:/home/a.pfb \
/scratch/a.pfb/sw_imgs/au-eoed-dev.sif \
rsgischkgdalfile.py -i "/scratch/a.pfb/gmw_simard_etal_srtm_agb/data/gmw_srtm_mangrove_agb/gmw_union_agb/*.kea" \
--nbands 1 --epsg 4326 --chkproj --readimg --chksum --rmerr



