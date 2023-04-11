import os
import shutil
import pandas as pd

# Set the path to the source directory (the Shared Google Drive Folder)
src_dir = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Shared Patients with Justin"

# Set the path to the destination directory where you want to copy the folders
dest_dir = "/Users/leobao/Library/CloudStorage/GoogleDrive-lkb44@case.edu/Shared drives/EBME 461 Project/Data"

# Set the prefix for the new folder names
prefix = "CA"

# Create a list of all the folders in the source directory
folders = [f for f in os.listdir(src_dir) if os.path.isdir(os.path.join(src_dir, f))]

# Create an empty list to store the old and new folder names
folder_names = []

# Loop through the folders and copy them to the destination directory with the new name
for i, folder in enumerate(folders):
    # Generate the new name for the folder
    new_name = f"{prefix}{str(i + 1).zfill(3)}"

    # Copy the folder and its contents to the destination directory with the new name
    shutil.copytree(os.path.join(src_dir, folder), os.path.join(dest_dir, new_name))

    # Append the old and new folder names to the list
    folder_names.append((folder, new_name))

    # Print a message to confirm the copy was successful
    print(f"Folder '{folder}' copied to '{new_name}'")

# Create a DataFrame from the list of old and new folder names
df = pd.DataFrame(folder_names, columns=["Old Name", "New Name"])

# Save the DataFrame as a CSV file
df.to_csv("/path/to/folder_names.csv", index=False)
