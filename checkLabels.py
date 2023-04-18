import os
import pydicom
import numpy as np
import pandas as pd

parent_path = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data/'  # Replace with your actual parent folder path

# Get a list of patient folders and sort them by patient ID
patient_folders = sorted([folder for folder in os.listdir(parent_path) if folder.startswith('CA')])

# Create an empty list to store results
results = []

for patient_folder in patient_folders:
    patient_id = patient_folder
    patient_path = os.path.join(parent_path, patient_folder)
    if not os.path.isdir(patient_path):
        continue
    label_folder = os.path.join(patient_path, 'Label')
    if not os.path.isdir(label_folder):
        continue
    
    # Create a list to store the indices of slices with labels
    label_indices = []
    
    # Iterate over the dicom files in the label folder
    for dicom_file in os.listdir(label_folder):
        if not dicom_file.endswith('.dcm'):
            continue
        dicom_path = os.path.join(label_folder, dicom_file)
        dicom = pydicom.dcmread(dicom_path)
        if np.any(dicom.pixel_array == 1):
            # Add the index of this slice to the list of label indices
            label_indices.append(int(dicom.InstanceNumber))
    
    if label_indices:
        # Compute the longest continuous range of slices with labels
        ranges = []
        start = end = label_indices[0]
        for i in range(1, len(label_indices)):
            if label_indices[i] == end + 1:
                end = label_indices[i]
            else:
                ranges.append((start, end))
                start = end = label_indices[i]
        ranges.append((start, end))
        longest_range = max(ranges, key=lambda x: x[1] - x[0] + 1)
        results.append((patient_id, longest_range[0], longest_range[1]))
    else:
        # If there are no slices with labels, add a placeholder result
        results.append((patient_id, '', ''))

# Create a DataFrame to store the results and save to a csv file
df = pd.DataFrame(results, columns=['Patient ID', 'Start Slice', 'End Slice'])
df.to_csv('/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data/label_ranges.csv', index=False)