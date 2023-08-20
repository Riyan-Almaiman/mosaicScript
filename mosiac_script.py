import os
import time
import arcpy



def mosiac_to_raster(folder_selected, destination_selection, number_of_bands, pixel_type_value):
  

    if not folder_selected:
        print("No folder selected. Exiting script.")
        exit()
    if not destination_selection:
        print("No destination folder selected. Exiting script.")    
        exit()
    if not number_of_bands:
        print("no band selected")
        exit()
    if not pixel_type_value:
        print("no pixel type selected")    
        exit()

    arcpy.env.workspace = folder_selected
    arcpy.env.parallelProcessingFactor = "80%"

    # Get all subfolders
    all_subfolders = arcpy.ListWorkspaces("*", "Folder")
    
    # Filter out the 'done' subfolders
    # subfolders = [folder for folder in all_subfolders if not os.path.exists(os.path.join(folder, 'done'))]


    numberofFolders = len(all_subfolders)

    print(f"Number of folders available to process (This checks for folders that are done and excludes them) = {numberofFolders}")




    DEM = ['dtm', 'dsm']


    for folder in all_subfolders:

        path = folder.rstrip('/')  
        last_part = os.path.basename(path)
        print(last_part)
        print(f"Starting processing for folder: {last_part}")


        for dem in DEM:
            start_time = time.time()
            data_folder = os.path.join(folder, 'vricon_raster_1over30asec', dem, 'data')

            if os.path.exists(data_folder):
                arcpy.env.workspace = data_folder
                tif_files = arcpy.ListRasters("*", "TIF")
                print(f"Number of TIF files found in {dem}/data = {len(tif_files)}")

                if tif_files:
                    tif_files_str = ";".join(tif_files)
                
                    
                    output_folder = os.path.join(destination_selection, f'{last_part}','mosaic', f'{dem}')

                    if not os.path.exists(output_folder):
                        os.makedirs(output_folder)
                        



                    arcpy.MosaicToNewRaster_management(
                        input_rasters=tif_files_str,
                        output_location=output_folder,
                        raster_dataset_name_with_extension=f'{last_part}.tif',
                        pixel_type=pixel_type_value,
                        number_of_bands=str(number_of_bands)
                    )
                    
                    

                    end_time = time.time()  
                    elapsed_time = end_time - start_time
                    print(f"Time taken to process {dem} data in folder {folder}: {elapsed_time:.2f} seconds")
                    
                else:
                    print(f"No TIF files found in {data_folder}.")
            else:
                print(f"Data folder {data_folder} does not exist.")

        
        print(f"Finished processing for folder: {folder}")

        

    print("All desired folders processed!")
