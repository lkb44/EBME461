import numpy as np
import os
import nibabel as nib
import pydicom
from skimage import exposure

def apply_preprocessing(img):
    # Apply 350 HU/40 HU window/level operation
    img = exposure.rescale_intensity(img, in_range=(40, 390), out_range=(0, 1))
    img = exposure.adjust_gamma(img, gamma=0.8)
    img = np.uint8(img * 255)
    return img

def process_patient(patient_dir):
    # Get list of DICOM files for Image folder
    img_folder = os.path.join(patient_dir, "Image")
    img_files = sorted([f for f in os.listdir(img_folder) if f.endswith(".dcm")])

    # Divide heart slices into two equal halves
    img_files_lower = img_files[:len(img_files)//2]
    img_files_upper = img_files[len(img_files)//2:]

    # Process slices for lower half of heart
    img_slices_lower = []
    for f in img_files_lower:
        dicom_file = pydicom.dcmread(os.path.join(img_folder, f))
        img_slice = apply_preprocessing(dicom_file.pixel_array)
        img_slices_lower.append(img_slice)

    # Process slices for upper half of heart
    img_slices_upper = []
    for f in img_files_upper:
        dicom_file = pydicom.dcmread(os.path.join(img_folder, f))
        img_slice = apply_preprocessing(dicom_file.pixel_array)
        img_slices_upper.append(img_slice)

    # Generate input voxel slabs by concatenating 3 consecutive slices
    slabs = []
    for i in range(len(img_slices_lower)-2):
        slab = np.zeros((512, 512, 3), dtype=np.uint8)
        slab[..., 0] = img_slices_lower[i]
        slab[..., 1] = img_slices_lower[i+1]
        slab[..., 2] = img_slices_lower[i+2]
        slabs.append(slab)
    for i in range(len(img_slices_upper)-2):
        slab = np.zeros((512, 512, 3), dtype=np.uint8)
        slab[..., 0] = img_slices_upper[i]
        slab[..., 1] = img_slices_upper[i+1]
        slab[..., 2] = img_slices_upper[i+2]
        slabs.append(slab)

    # Concatenate slabs to form 3D volume
    volume = np.concatenate(slabs, axis=2)

    # Save volume in NifTI format
    output_dir = os.path.join(patient_dir, "Output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "volume.nii.gz")
    nib.save(nib.Nifti1Image(volume, np.eye(4)), output_file)

# Process all patients
parent_dir = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data/"
patient_dirs = sorted([os.path.join(parent_dir, f"CA{i:03}") for i in range(1, 47)])
for patient_dir in patient_dirs:
    process_patient(patient_dir)
