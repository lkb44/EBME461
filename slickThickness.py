import pydicom
import os

# Change this to the path where your patient folders are stored
base_path = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data/'


for patient_folder in sorted(os.listdir(base_path)):
    # Skip over non-directory files (e.g. .DS_Store)
    if not os.path.isdir(os.path.join(base_path, patient_folder)):
        continue

    patient_path = os.path.join(base_path, patient_folder)
    image_path = os.path.join(patient_path, 'Image')

    # Get the first DICOM file in the folder
    first_file_path = os.path.join(image_path, os.listdir(image_path)[0])

    # Load the DICOM file and extract the slice thickness
    ds = pydicom.dcmread(first_file_path)
    slice_thickness = ds.SliceThickness

    print(f"Patient {patient_folder} has slice thickness of {slice_thickness} mm")
