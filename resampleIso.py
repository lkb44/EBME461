import os
import numpy as np
import nibabel as nib
import pandas as pd

# Define the parent path for the NifTI files
parent_path = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project'

# Define the output voxel size
output_voxel_size = [1, 1, 1]  # in mm

# Loop over each patient folder that contains "Output"
for patient_folder in pd.Series(os.listdir(parent_path)).loc[lambda s: s.str.contains("Output")]:
    if not os.path.isdir(os.path.join(parent_path, patient_folder)):
        continue  # Skip non-directory files
    # Loop over each output folder (axial, sagittal, coronal)
    for output_folder in os.listdir(os.path.join(parent_path, patient_folder)):
        if not os.path.isdir(os.path.join(parent_path, patient_folder, output_folder)):
            continue  # Skip non-directory files
        # Load the Image and Label volumes for the current output folder
        image_path = os.path.join(parent_path, patient_folder, output_folder, 'Image')
        label_path = os.path.join(parent_path, patient_folder, output_folder, 'Label')
        image_volume = nib.load(os.path.join(image_path, os.listdir(image_path)[0])).get_fdata()
        label_volume = nib.load(os.path.join(label_path, os.listdir(label_path)[0])).get_fdata()
        # Get the current voxel size
        current_voxel_size = nib.load(os.path.join(image_path, os.listdir(image_path)[0])).header.get_zooms()[:3]
        # Calculate the resampling factor
        resampling_factor = [current_voxel_size[i] / output_voxel_size[i] for i in range(3)]
        # Resample the Image and Label volumes
        image_volume_resampled = np.zeros([int(image_volume.shape[0] * resampling_factor[0]),
                                           int(image_volume.shape[1] * resampling_factor[1]),
                                           int(image_volume.shape[2] * resampling_factor[2])])
        label_volume_resampled = np.zeros([int(label_volume.shape[0] * resampling_factor[0]),
                                           int(label_volume.shape[1] * resampling_factor[1]),
                                           int(label_volume.shape[2] * resampling_factor[2])])
        for i in range(image_volume_resampled.shape[0]):
            for j in range(image_volume_resampled.shape[1]):
                for k in range(image_volume_resampled.shape[2]):
                    image_volume_resampled[i, j, k] = image_volume[int(i / resampling_factor[0]),
                                                                    int(j / resampling_factor[1]),
                                                                    int(k / resampling_factor[2])]
                    label_volume_resampled[i, j, k] = label_volume[int(i / resampling_factor[0]),
                                                                    int(j / resampling_factor[1]),
                                                                    int(k / resampling_factor[2])]
        # Save the resampled Image and Label volumes
        image_volume_resampled = nib.Nifti1Image(image_volume_resampled, np.eye(4))
        label_volume_resampled = nib.Nifti1Image(label_volume_resampled, np.eye(4))
        nib.save(image_volume_resampled, os.path.join(image_path, 'Image_resampled.nii.gz'))
        nib.save(label_volume_resampled, os.path.join(label_path, 'Label_resampled.nii.gz'))
