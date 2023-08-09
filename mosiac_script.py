import arcpy
import os
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# Display folder selection dialog
folder_selected = filedialog.askdirectory(title="Mosiac to new raster - select a folder - subfolder layout = ./vricon_raster_1over30asec/dtm-OR-dsm/data")

if not folder_selected:
    print("No folder selected. Exiting script.")
    exit()

arcpy.env.workspace = folder_selected

subfolders = arcpy.ListWorkspaces("*", "Folder")
numberofFolders = len(subfolders)

print(f"Number of folders found = {numberofFolders}")

DEM = ['dtm', 'dsm']

for index, folder in enumerate(subfolders):
    if os.path.exists(os.path.join(folder, 'done')):
        print(f"Folder {folder} already processed. Skipping...")
        continue

    print(f"Starting processing for folder: {folder}")

    for dem in DEM:
        print(f"Processing {dem} data in folder: {folder}")

        data_folder = os.path.join(folder, 'vricon_raster_1over30asec', dem, 'data')

        if os.path.exists(data_folder):
            arcpy.env.workspace = data_folder
            tif_files = arcpy.ListRasters("*", "TIF")

            print(f"Number of TIF files found in {data_folder} = {len(tif_files)}")

            if tif_files:
                tif_files_str = ";".join(tif_files)
                output_folder = os.path.join(folder, f'mosiac_{dem}')

                if not os.path.exists(output_folder):
                    os.mkdir(output_folder)

                arcpy.MosaicToNewRaster_management(tif_files_str, output_folder, 'Mosaic.tif', "32_BIT_FLOAT", "1")
                print(f"Finished processing {dem} data in folder: {folder}")

            else:
                print(f"No TIFF files found in {data_folder}.")
        else:
            print(f"Data folder {data_folder} does not exist.")

    os.mkdir(os.path.join(folder, 'done'))
    print(f"Finished processing for folder: {folder}")
    print(f"Number of folders remaining = {numberofFolders - index - 1}")

print("All folders processed!")
