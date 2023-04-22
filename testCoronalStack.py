import os
import pydicom
import numpy as np

data_dir = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data"
output_dir = "Coronal_Test"

# Loop through each patient's folder
for patient_folder in os.listdir(data_dir):
    # Check if the folder name contains "CA"
    if "CA" not in patient_folder:
        continue
        
    patient_dir = os.path.join(data_dir, patient_folder)
    
    # Create a new output folder for the coronal DICOM stack
    output_folder = os.path.join(data_dir, patient_folder, output_dir)
    os.makedirs(os.path.join(output_folder, "Image"), exist_ok=True)
    os.makedirs(os.path.join(output_folder, "Label"), exist_ok=True)

    print(f"Processing {patient_folder}...")
    
    # Load the axial DICOM stack for this patient
    axial_stack = []
    for i in range(1, 1000): # Assuming that there are fewer than 1000 slices in each stack
        filename = os.path.join(patient_dir, "Image", f"IMG{str(i).zfill(4)}.dcm")
        if not os.path.exists(filename):
            break
        slice = pydicom.dcmread(filename)
        axial_stack.append(slice.pixel_array)

    # Convert the axial stack to a NumPy array
    axial_array = np.array(axial_stack)

    # Flip the array along the y-axis to create a coronal view
    coronal_array = np.flip(axial_array, axis=1)

    # Save the coronal DICOM stack for this patient
    for i in range(coronal_array.shape[0]):
        filename = os.path.join(output_folder, "Image", f"IMG{str(i+1).zfill(4)}.dcm")
        slice = pydicom.dcmread(os.path.join(patient_dir, "Image", f"IMG{str(i+1).zfill(4)}.dcm"), force=True)
        slice.PixelData = coronal_array[i].tobytes()
        slice.save_as(filename)
        
        filename = os.path.join(output_folder, "Label", f"IMG{str(i+1).zfill(4)}.dcm")
        slice = pydicom.dcmread(os.path.join(patient_dir, "Label", f"IMG{str(i+1).zfill(4)}.dcm"), force=True)
        slice.PixelData = coronal_array[i].tobytes()
        slice.save_as(filename)