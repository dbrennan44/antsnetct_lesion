#antsnet ct run

sub=$1

job1_id=${sub}_2WK
bsub -J $job1_id -o /project/gugger_1/nishants/data/logs/${sub}_2WK_log.txt \
singularity run \
-B /home/danbren/templateflow:/opt/templateflow \
-B /project/gugger_1/nishants/data:/home/antspyuser/ \
~/antsnetct \
--skip-bids-validation \
--input-dataset /home/antspyuser/TRACK_phase1_BIDS/ \
--participant $sub \
--output-dataset /home/antspyuser/output_cross/ \
--thickness-iterations 1 \
--template-name none \
--session 2WK

# 6mo
job2_id=${sub}_6MO
#submit job w name
bsub -J $job2_id -o /project/gugger_1/nishants/data/logs/${sub}_6MO_log.txt \
singularity run \
-B /home/danbren/templateflow:/opt/templateflow \
-B /project/gugger_1/nishants/data:/home/antspyuser/ \
~/antsnetct \
--skip-bids-validation \
--input-dataset /home/antspyuser/TRACK_phase1_BIDS/ \
--participant $sub \
--output-dataset /home/antspyuser/output_cross/ \
--thickness-iterations 1 \
--template-name none \
--session 6MO 


# longitudinal
bsub -q bsc_long -w "done($job1_id) && done($job2_id)" -J ${sub}_longi \
-o /project/gugger_1/nishants/data/logs/${sub}_longi_log.txt \
singularity run \
-B /home/danbren/templateflow:/opt/templateflow \
-B /project/gugger_1/nishants/data:/home/antspyuser/ \
~/antsnetct --longitudinal \
--cross-sectional-dataset /home/antspyuser/output_cross/ \
--output-dataset /home/antspyuser/output_longi \
--participant $sub \
--sst-transform syn \
--sst-segmentation-method antspynet_atropos \
--template-name none \
--thickness-iterations 1 \
--sst-brain-extracted-weight 1 # try this for now
