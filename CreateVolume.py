import SimpleITK as sitk

# Define the paths to the input DICOM directories and output MHA file
image_dir = "path/to/Image"
label_dir = "path/to/Label"
output_path = "path/to/output.mha"

# Load the image and label series as SimpleITK image objects
image_series = sitk.ImageSeriesReader().GetGDCMSeriesFileNames(image_dir)
label_series = sitk.ImageSeriesReader().GetGDCMSeriesFileNames(label_dir)

image = sitk.ReadImage(image_series)
label = sitk.ReadImage(label_series)

# Combine the images and labels into a single 3D volume
volume = sitk.JoinSeries([image, label])

# Resample the volume to have isotropic voxel spacing
original_spacing = volume.GetSpacing()
min_spacing = min(original_spacing)
new_spacing = [min_spacing]*3
new_size = [int(round(osz*ospc/nspc)) for osz, ospc, nspc in zip(volume.GetSize(), original_spacing, new_spacing)]
interpolator = sitk.sitkLinear
resampled_volume = sitk.Resample(volume, new_size, sitk.Transform(), interpolator, volume.GetOrigin(), new_spacing, volume.GetDirection(), 0.0, volume.GetPixelID())

# Set the voxel dimensions of the resampled volume to match the isotropic spacing
resampled_volume.SetSpacing(new_spacing)

# Save the resampled volume as an MHA file
sitk.WriteImage(resampled_volume, output_path)
