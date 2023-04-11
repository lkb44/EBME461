import os
import numpy as np
import SimpleITK as sitk

# Set the input and output directories
input_dir = '/path/to/input/directory'
output_dir = '/path/to/output/directory'

# Loop over each patient directory
for patient_dir in os.listdir(input_dir):
    # Create a list to store the concatenated volumes for each patient
    patient_volumes = []
    
    # Loop over each slice in the Image folder for this patient
    image_dir = os.path.join(input_dir, patient_dir, 'Image')
    slice_files = sorted(os.listdir(image_dir))
    for i in range(1, len(slice_files)-1):
        # Load the three consecutive slices
        slice1 = sitk.ReadImage(os.path.join(image_dir, slice_files[i-1]))
        slice2 = sitk.ReadImage(os.path.join(image_dir, slice_files[i]))
        slice3 = sitk.ReadImage(os.path.join(image_dir, slice_files[i+1]))
        
        # Concatenate the slices into a 3D volume
        volume = np.stack([sitk.GetArrayFromImage(slice1),
                           sitk.GetArrayFromImage(slice2),
                           sitk.GetArrayFromImage(slice3)],
                          axis=-1)
        
        # Add the volume to the list of volumes for this patient
        patient_volumes.append(volume)
    
    # Save the concatenated volumes as an .mha file
    output_file = os.path.join(output_dir, f'{patient_dir}.mha')
    sitk.WriteImage(sitk.GetImageFromArray(np.array(patient_volumes)), output_file)
