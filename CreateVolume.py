import os
import numpy as np
import pydicom
import SimpleITK as sitk

# define path to data folders
data_path = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data"

# loop through each patient folder
for patient_folder in os.listdir(data_path):
    if patient_folder.startswith("CA"):
        # create path to image and label folders
        image_folder = os.path.join(data_path, patient_folder, "Image")
        label_folder = os.path.join(data_path, patient_folder, "Label")
        
        # get list of all image filenames in image folder
        image_filenames = sorted([os.path.join(image_folder, filename) for filename in os.listdir(image_folder)])
        
        # get list of all label filenames in label folder
        label_filenames = sorted([os.path.join(label_folder, filename) for filename in os.listdir(label_folder)])
        
        # loop through each slice and bisect
        for i in range(len(image_filenames)):
            # load the image and label slices
            image_slice = pydicom.read_file(image_filenames[i]).pixel_array
            label_slice = pydicom.read_file(label_filenames[i]).pixel_array
            
            # apply HU windowing
            image_slice = np.clip(image_slice, -300, 600)
            image_slice = (image_slice - (-300)) / (600 - (-300))
            
            # bisect the image and label slices
            if i < len(image_filenames) // 2:
                # bottom half of heart, sequence from bottom-to-middle
                image_slice = image_slice[::-1]
                label_slice = label_slice[::-1]
                output_name = os.path.join(data_path, patient_folder + "_bottom", f"{patient_folder}_bottom_{i:03d}.mha")
            else:
                # top half of heart, sequence from top-to-middle
                output_name = os.path.join(data_path, patient_folder + "_top", f"{patient_folder}_top_{i:03d}.mha")
            
            # save the image and label slices as a 3D volume
            if not os.path.exists(os.path.dirname(output_name)):
                os.makedirs(os.path.dirname(output_name))
            sitk_image_slice = sitk.GetImageFromArray(image_slice)
            sitk_label_slice = sitk.GetImageFromArray(label_slice)
            sitk_image_slice.CopyInformation(sitk_label_slice)
            sitk.WriteImage(sitk_image_slice, output_name)
            print(f"Patient {patient_folder} bisected!")
