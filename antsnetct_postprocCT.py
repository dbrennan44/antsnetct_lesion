# usage:
# python3 antsnetct_postprocCT.py {subject} {session}

import ants
import glob
import sys
sub=sys.argv[1]
ses=sys.argv[2]

basedir="/project/gugger_1/nishants/data/output_longi/{}/{}/anat/".format(sub,ses)

l=glob.glob("/project/gugger_1/nishants/data/TRACK_phase1_BIDS/{}/{}/anat/*_label-lesion_roi.nii.gz".format(sub,ses))

def subtract_lesion(img,lesion=[]):
    if lesion:
        return img - (img*lesion)
    else:
        return img


#posterior_files = [ants.image_read(i) for i in glob.glob(basedir+"*_probseg.nii.gz")]
kk_seg=ants.image_read(basedir+"{}_{}_acq-3D_seg-antsnetct_dseg.nii.gz".format(sub,ses))

# grab lesion and resample
if l:
    lesion=ants.resample_image_to_target(ants.threshold_image(ants.image_read(l[0]),low_thresh=0.1),
                                         kk_seg,interp_type="nearestNeighbor")
else:
    lesion=l



gm_lab=8
wm_lab=2
sgm_lab=9

kk_seg[kk_seg == sgm_lab] = wm_lab
kk_seg=subtract_lesion(kk_seg,lesion)


wm_posterior = ants.image_read(basedir+"{}_{}_acq-3D_seg-antsnetct_label-WM_probseg.nii.gz".format(sub,ses))
sgm_posterior = ants.image_read(basedir+"{}_{}_acq-3D_seg-antsnetct_label-SGM_probseg.nii.gz".format(sub,ses))
kk_wm_posterior = subtract_lesion((wm_posterior + sgm_posterior),lesion)
kk_gm_posterior= subtract_lesion(
    ants.image_read(basedir+"{}_{}_acq-3D_seg-antsnetct_label-CGM_probseg.nii.gz".format(sub,ses)),lesion)




kk=ants.kelly_kapowski(s=kk_seg,g=kk_gm_posterior,w=kk_wm_posterior,
                       gm_label=gm_lab,wm_label=wm_lab)

ants.image_write(kk,filename=basedir+"kk_thickness.nii.gz")
