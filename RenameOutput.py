import os

parent_folder = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data"

patient_dirs = sorted([os.path.join(parent_folder, f"CA{i:03}") for i in range(46, 47)])
for patient_dir in patient_dirs:
    # Get patient label from directory name
    patient_label = os.path.basename(patient_dir)

    # Get path to NifTI file in Output folder and construct new filename
    output_folder = os.path.join(patient_dir, "Output")
    nifti_file = os.path.join(output_folder, "volume.nii.gz")
    new_filename = f"{patient_label}_image_volume.nii.gz"

    # Rename file
    os.rename(nifti_file, os.path.join(output_folder, new_filename))
