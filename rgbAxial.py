import pydicom
import numpy as np
import os
from skimage import exposure

# define the HU range to threshold to
HU_MIN = -135
HU_MAX = 215

# define the output directory
OUT_DIR = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Output"

# loop through the patient folders
for patient_folder in os.listdir("/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data"):
    
    # create a list to store the input slabs for this patient
    slabs = []
    
    # loop through the image files in the patient's Image folder
    for img_file in os.listdir(os.path.join("/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data", patient_folder, "Image")):
        
        # load the DICOM file and extract the pixel array
        dcm = pydicom.dcmread(os.path.join("/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data", patient_folder, "Image", img_file))
        pixel_array = dcm.pixel_array.astype(np.float32)
        
        # threshold the pixel array
        pixel_array[pixel_array < HU_MIN] = HU_MIN
        pixel_array[pixel_array > HU_MAX] = HU_MAX
        
        # rescale the pixel array to (0,1)
        pixel_array_rescaled = exposure.rescale_intensity(pixel_array, in_range=(HU_MIN, HU_MAX), out_range=(0, 1))
        
        # add the rescaled pixel array to the list of slabs
        slabs.append(pixel_array_rescaled)
        
        # if we have enough slabs, create a 2D RGB DICOM image and save it
        if len(slabs) >= 3:
            # combine the three most recent slabs into an RGB image
            r = slabs[-3]
            g = slabs[-2]
            b = slabs[-1]
            rgb_array = np.stack((r,g,b), axis=-1)
            
            # create a DICOM object and set the appropriate fields
            ds = pydicom.dataset.Dataset()
            ds.PixelData = rgb_array.tobytes()
            ds.Rows = rgb_array.shape[0]
            ds.Columns = rgb_array.shape[1]
            ds.BitsAllocated = 8
            ds.BitsStored = 8
            ds.HighBit = 7
            ds.SamplesPerPixel = 3
            ds.PhotometricInterpretation = "RGB"
            ds.PatientID = patient_folder
            ds.SeriesDescription = "Axial_Image"
            ds.SOPInstanceUID = pydicom.uid.generate_uid()
            slab_number = str(len(slabs) - 2).zfill(4)
            ds.SeriesNumber = int(slab_number)
            
            # save the DICOM file
            out_file = f"{patient_folder}_{slab_number}_Axial_Image.dcm"
            pydicom.filewriter.write_file(os.path.join(OUT_DIR, out_file), ds)
