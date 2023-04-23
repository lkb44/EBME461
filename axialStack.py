import os
import numpy as np
import nibabel as nib
import pydicom
from skimage import exposure

def apply_preprocessing_img(img):
    # Apply 350 HU/40 HU window/level operation
    img = exposure.rescale_intensity(img, in_range=(-135, 215), out_range=(0, 1))
    img = exposure.adjust_gamma(img, gamma=0.8)
    img = np.uint8(img * 255)
    return img

def apply_preprocessing_lbl(img):
    img = img
    return img

def process_patient(patient_dir):
    # Get list of DICOM files for Image folder
    img_folder = os.path.join(patient_dir, "Image")
    img_files = sorted([f for f in os.listdir(img_folder) if f.endswith(".dcm")])

    # Get list of DICOM files for Label folder
    lbl_folder = os.path.join(patient_dir, "Label")
    lbl_files = sorted([f for f in os.listdir(lbl_folder) if f.endswith(".dcm")])

    # Process slices for the heart
    img_slices = []
    for f in img_files:
        dicom_file = pydicom.dcmread(os.path.join(img_folder, f))
        img_slice = apply_preprocessing_img(dicom_file.pixel_array)
        img_slices.append(img_slice)

    lbl_slices = []
    for l in lbl_files:
        dicom_file = pydicom.dcmread(os.path.join(lbl_folder, l))
        lbl_slice = apply_preprocessing_lbl(dicom_file.pixel_array)
        lbl_slices.append(lbl_slice)

    image_slabs = []
    label_slabs = []
    for i in range(len(img_slices) - 2):
        slab = np.zeros((512, 512, 3), dtype=np.uint8)
        slab[..., 0] = img_slices[i]
        slab[..., 1] = img_slices[i+1]
        slab[..., 2] = img_slices[i+2]
        image_slabs.append(slab)
    for i in range(len(lbl_files) - 2):
        slab = np.zeros((512, 512, 3), dtype=np.uint8)
        slab[..., 0] = lbl_slices[i]
        slab[..., 1] = lbl_slices[i+1]
        slab[..., 2] = lbl_slices[i+2]
        label_slabs.append(slab)

    # Save slabs in NifTI format
    patient_id = os.path.basename(patient_dir)
    output_dir = os.path.join(patient_dir, "Output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, image in enumerate(image_slabs):
        image_output_file = os.path.join(output_dir, f"{patient_id}_Slab{i:03}_axial_image.nii.gz")
        nib.save(nib.Nifti1Image(image, np.eye(4)), image_output_file)
    for i, label in enumerate(label_slabs):
        label_output_file = os.path.join(output_dir, f"{patient_id}_Slab{i:03}_axial_label.nii.gz")
        nib.save(nib.Nifti1Image(label, np.eye(4)), label_output_file)

# Process all patients
parent_dir = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data/"
patient_dirs = sorted([os.path.join(parent_dir, f"CA{i:03}") for i in range(1, 47)])
for patient_dir in patient_dirs:
    process_patient(patient_dir)