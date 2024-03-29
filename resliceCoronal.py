import os
import SimpleITK as sitk

# define the parent path where patient folders are stored
parent_path = '/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data/'

# define the order of the patient folders
patient_order = [f"CA{i:03}" for i in range(1, 47)]

# loop through each patient folder in order
for patient_folder in patient_order:
    print(f"Processing {patient_folder}...")
        
    # define the path to the patient's label and image volumes
    label_volume_path = os.path.join(parent_path, patient_folder, 'Output_2', f"{patient_folder}_label_volume.nii.gz")
    image_volume_path = os.path.join(parent_path, patient_folder, 'Output_2', f"{patient_folder}_image_volume.nii.gz")
        
    # load the label and image volumes as SimpleITK images
    label_volume = sitk.ReadImage(label_volume_path)
    image_volume = sitk.ReadImage(image_volume_path)
        
    # reslice the volumes to the coronal plane
    reslice_filter = sitk.ResampleImageFilter()
    reslice_filter.SetOutputDirection((-1,0,0,0,0,1,0,1,0))
    reslice_filter.SetOutputSpacing((1,1,1))
    reslice_filter.SetOutputOrigin(image_volume.GetOrigin())
    reslice_filter.SetSize((512, 512, image_volume.GetDepth()))
    coronal_label_volume = reslice_filter.Execute(label_volume)
    coronal_image_volume = reslice_filter.Execute(image_volume)
        
    # save the coronal slices as DICOM files
    coronal_images_path = os.path.join(parent_path, patient_folder, 'Output_2', 'Coronal_Images')
    coronal_labels_path = os.path.join(parent_path, patient_folder, 'Output_2', 'Coronal_Labels')
    os.makedirs(coronal_images_path, exist_ok=True)
    os.makedirs(coronal_labels_path, exist_ok=True)
    for i in range(coronal_image_volume.GetSize()[2]):
        image_slice = sitk.GetArrayViewFromImage(coronal_image_volume)[..., i]
        label_slice = sitk.GetArrayViewFromImage(coronal_label_volume)[..., i]
        image_path = os.path.join(coronal_images_path, f"IMG{i+1:04}.dcm")
        label_path = os.path.join(coronal_labels_path, f"LBL{i+1:04}.dcm")
        sitk.WriteImage(sitk.GetImageFromArray(image_slice), image_path, True)
        sitk.WriteImage(sitk.GetImageFromArray(label_slice), label_path, True)
