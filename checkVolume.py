import os
import nibabel as nib
import csv

path = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Axial Output/Image_resampled'
output_file = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/patient_dimensions_resampled.csv'

with open(output_file, 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Patient ID', 'Dimensions'])

    for filename in os.listdir(path):
        if filename.endswith('_image_volume.nii.gz'):
            patient_id = filename.split('_')[0]
            volume_path = os.path.join(path, filename)
            volume = nib.load(volume_path)
            dimensions = ' x '.join([str(dim) for dim in volume.shape])
            writer.writerow([patient_id, dimensions])