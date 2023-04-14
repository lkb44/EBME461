import numpy as np
import os
import pydicom
import cv2

# Define HU window/level
WINDOW_WIDTH = 350
WINDOW_LEVEL = 40

# Define the number of slices to bisect
SLICES_TO_BISECT = 3

# Define the output image size
IMG_SIZE = 512

input_path = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data"

output_path = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Output"

def preprocess_images(input_path, output_path):
    # Create output folder if it doesn't exist
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Loop through all patient folders
    for patient_folder in os.listdir(input_path):
        patient_path = os.path.join(input_path, patient_folder)

        # Loop through all image slices for the current patient
        for i in range(len(os.listdir(os.path.join(patient_path, "Image")))):
            # Read image slice and apply HU window/level
            img_path = os.path.join(patient_path, "Image", "IMG{:03d}.dcm".format(i+1))
            ds = pydicom.dcmread(img_path)
            img = ds.pixel_array.astype(np.float32)
            img = np.clip(img, WINDOW_LEVEL-WINDOW_WIDTH/2, WINDOW_LEVEL+WINDOW_WIDTH/2)
            img = (img - (WINDOW_LEVEL-WINDOW_WIDTH/2)) / (WINDOW_WIDTH)
            img = np.uint8(img * 255)

            # Bisection
            if i < SLICES_TO_BISECT:
                continue
            img_slices = []
            for j in range(i-SLICES_TO_BISECT, i+1):
                img_path = os.path.join(patient_path, "Image", "IMG{:03d}.dcm".format(j+1))
                ds = pydicom.dcmread(img_path)
                img_slice = ds.pixel_array.astype(np.float32)
                img_slice = np.clip(img_slice, WINDOW_LEVEL-WINDOW_WIDTH/2, WINDOW_LEVEL+WINDOW_WIDTH/2)
                img_slice = (img_slice - (WINDOW_LEVEL-WINDOW_WIDTH/2)) / (WINDOW_WIDTH)
                img_slice = np.uint8(img_slice * 255)
                img_slices.append(img_slice)

            # Concatenate images
            img_concat = cv2.hconcat(img_slices)

            # Resize image to IMG_SIZE x IMG_SIZE
            img_resized = cv2.resize(img_concat, (IMG_SIZE, IMG_SIZE), interpolation = cv2.INTER_AREA)

            # Save image to output folder
            output_filename = "IMG{:03d}.png".format(i+1)
            output_filepath = os.path.join(output_path, patient_folder, output_filename)
            if not os.path.exists(os.path.dirname(output_filepath)):
                os.makedirs(os.path.dirname(output_filepath))
            cv2.imwrite(output_filepath, img_resized)

preprocess_images(input_path, output_path)