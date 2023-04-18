import os
import nibabel as nib
import numpy as np
from nilearn.image import resample_img

# Define the input and output directories
input_dir = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Axial Output/Label'
output_dir = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Axial Output/Label_resampled/'

# Define the desired output shape
output_shape = (512, 512, 56)

# Create the output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Loop over all the files in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith('_label_volume.nii.gz'):
        # Load the volume
        input_path = os.path.join(input_dir, filename)
        volume = nib.load(input_path)

        # Resample the volume to the desired shape
        target_affine = np.eye(4)
        target_affine[:3, :3] = np.diag((1, 1, 1))
        target_affine[:3, 3] = volume.affine[:3, 3]
        resampled_volume = resample_img(volume, target_affine=target_affine, target_shape=output_shape)

        # Save the resampled volume to the output directory
        output_path = os.path.join(output_dir, filename)
        nib.save(resampled_volume, output_path)