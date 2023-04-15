import os
import nibabel as nib
import numpy as np

parent_path = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data/"  # replace with your parent folder path
patient_folders = [f"CA{i+1:03}" for i in range(46)]

for patient_folder in patient_folders:
    print(f"Converting {patient_folder}...")

    # Load the axial image and label volumes
    image_path = os.path.join(parent_path, patient_folder, "Output", f"{patient_folder}_image_volume.nii.gz")
    label_path = os.path.join(parent_path, patient_folder, "Output", f"{patient_folder}_label_volume.nii.gz")
    axial_image = nib.load(image_path)
    axial_label = nib.load(label_path)

    # Get the image and label data from the loaded volumes
    axial_image_data = axial_image.get_fdata()
    axial_label_data = axial_label.get_fdata()

    # Transpose the image and label data so that the sagittal axis becomes the first axis
    sagittal_image_data = np.transpose(axial_image_data, (2, 1, 0))
    sagittal_label_data = np.transpose(axial_label_data, (2, 1, 0))

    # Create new NIfTI image and label objects with the transposed data
    sagittal_image = nib.Nifti1Image(sagittal_image_data, affine=axial_image.affine)
    sagittal_label = nib.Nifti1Image(sagittal_label_data, affine=axial_label.affine)

    # Save the new NIfTI image and label objects as .nii.gz files
    output_folder = os.path.join(parent_path, patient_folder, "Output")
    nib.save(sagittal_image, os.path.join(output_folder, f"{patient_folder}_image_volume_sagittal.nii.gz"))
    nib.save(sagittal_label, os.path.join(output_folder, f"{patient_folder}_label_volume_sagittal.nii.gz"))

print("Done!")
